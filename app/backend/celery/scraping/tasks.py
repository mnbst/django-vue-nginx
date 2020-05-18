from __future__ import absolute_import, unicode_literals

import json
import os
import re
import socket
import time
import urllib.request
import xml.etree.ElementTree as ElementTree
from html import unescape
from typing import Optional

import OpenSSL
import django
import isodate
import nltk
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from celery import shared_task
from channels.layers import get_channel_layer
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from googleapiclient.errors import HttpError

from ... import settings as settings_py
from ...dictionary_console.serializer import VideoSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from ...dictionary_console.models import *

time_out = (5.0, 30.0)


@shared_task
def get_list(settings: dict):
    youtube_scraping = YoutubeScraping(settings=settings)
    youtube_scraping.get_video_list()


@shared_task
def scraping(settings: dict):
    youtube_scraping = YoutubeScraping(settings=settings)
    # youtube_scraping.youtube_search()


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


class YoutubeScraping:
    Y_KEY = os.environ.get('DEVELOPER_KEY')
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    EXCEPT_VIDEO = [
        '-3fl9HVCk3o', 'vN_5MBIxjcs', 'KLFjdzvTLWM', 'CS9am2ctk1M',
        'r9QG3eFJUJk', '1jQdXHdJIQw', 'FCeZqjTwO2M', '_lhS0oilP1Q',
        'auNX2WZLuXA', 'AFD0nFg2s4M', 'jvfAEtDlR2A', 'C-vQZU1xAf4',
        'U8Fd0hqLApU', 'OvMN_8ClEgA', 'R2JhxW1rT8I', 'pRpNiYI0g64',
        'xqJ-ag2VLbk', 'SDD0r15AprU', 'rEGmWKbHUAY', 'UlFS0utBxB0',
        'APTRWJ8Q1UU', 'lAeAO51aVKA', 'Pl-RYkIXPnk', 'e2RBRUFwmuw',
        'lIUYItKBbBc', 'SJTzMHDaOlg', 'fX6sg2xuvCw', 'JT3Wc5alyfQ',
        'FlBdDhexQRc', 'GePukn4vRV8', '-Xk5aUvZCc0', '5H-41WPSsHs',
        'bQ_WHZ_WS3s', '5M1_ufFxvlE', '1l_Y8X9HhUA', 'd3yoDVp0hzc',
        'I7bVw0nGarQ', 'XPzB_GSMABo', '_7SNK6m8okE', 'sclwgAXiHhI',
        'jh8dEnVTvs8', 'Xw5RBrqCoL8', 'm37ByQITb9k', 'BMmnrdlxdbg',
        'DCSC4OG4nEE', 'n6hJXjka4Xk', 'OCA9alkiptw', 'ah0Vcf1X8r0',
        'EPgOhNeZYOc', 'qGpvtvSzGQ8', 'si16hSJF6v8', 'A3LRdMUzI-4',
        'KaXx2z5rYIA', 'MMIABcbEIGg', '9usVvl4q2Dc', '11I-WD-yBDU',
        'TRsf-OH9rM4'
    ]

    # 除外する記号
    REGEX_EXCEPT_HYPHEN = re.compile(r"[!-,.-/:-@[-`{-㿿]")
    REGEX = re.compile(r"[!-/:-@[-`{-㿿]")
    # アルファベット
    REGEX_ALPHABET = re.compile(r'[a-zA-Z\s]')
    REGEX_SPACE = re.compile(r'([-a-z0-9]+)\s([-a-z0-9]+)')
    REGEX_NUMBER = re.compile(r'[0-9０-９]+')

    def __init__(self, settings: dict):
        self.settings = settings
        self.channel_layer = get_channel_layer()

    def __send_to_websocket(self, group_name: str, **kwargs):
        data = kwargs.get('data', None)
        message = kwargs.get('message', None)
        if data:
            video = json.dumps(VideoSerializer(data).data)
            async_to_sync(self.channel_layer.group_send)(group_name, {
                "type": "get.video.list.messages",
                "data": video})
        else:
            async_to_sync(self.channel_layer.group_send)(group_name, {
                "type": "get.video.list.messages",
                "text": message,
            })

    def get_video_list(self):
        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey=self.Y_KEY, cache=MemoryCache())

        # Call worde search.list mewordod to retrieve results matching worde specified
        try:
            search_response = youtube.search().list(
                q='indonesia',
                part="id,snippet",
                maxResults=self.settings['videoPerPage'],
                regionCode="id",
                relevanceLanguage="id",
                safeSearch="moderate",
                type="video",
                videoCaption="closedCaption",
                videoSyndicated="true").execute()
        except HttpError as e:
            json_str_data = e.content.decode()
            json_data = json.loads(json_str_data)
            self.__send_to_websocket(message='ERROR❗... -> reason: ' + json_data['error']['errors'][0]['reason'],
                                     group_name='get_video_list')
            return

        page_token = search_response.get("nextPageToken", str)
        self.__organize_list(response=search_response)

        for _ in range(0, self.settings['pageToCrawl'] - 1):
            search_response.update(youtube.search().list(
                q='indonesia',
                pageToken=page_token,
                part="id,snippet",
                maxResults=self.settings['videoPerPage'],
                regionCode="id",
                relevanceLanguage="id",
                safeSearch="moderate",
                type="video",
                videoCaption="closedCaption",
                videoSyndicated="true").execute())
            page_token = search_response.get("nextPageToken", str)
            self.__organize_list(response=search_response)
        # self.__send_to_websocket(settings_py.END_MESSAGE, group_name="get_video_list")

    def __organize_list(self, response):
        for search_result in response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                href = search_result["id"]["videoId"]
                if href in self.EXCEPT_VIDEO + self.settings['exceptedHref']:
                    continue
            else:
                continue
            video_exists = Video.objects.filter(video_href=href).exists()

            if video_exists and href not in self.settings['videoToRenewal']:
                continue

            lang_codes = list()
            url = f'https://www.youtube.com/api/timedtext?type=list&v={href}'
            req = requests.get(url, timeout=time_out)
            if not req.ok:
                raise ValueError(f'Unexpected status code: {req.status_code}')
            try:
                root = ElementTree.fromstring(req.content)
            except ElementTree.ParseError:
                continue

            # 字幕言語取得
            r = dict()
            for r in root.iter():
                lang_code = r.attrib.get('lang_code')
                if lang_code is not None:
                    lang_codes.append(lang_code)

            # 字幕言語の数を指定してる
            if len(lang_codes) < self.settings['languageLimit'] + 1 and 'id' in lang_codes:
                name = r.attrib.get('name')
                title = search_result["snippet"]["title"]
                title = unescape(title)
                video = Video(video_href=href, video_img=search_result["snippet"]["thumbnails"]["medium"]["url"],
                              video_time=self.__get_duration(href), video_title=title, video_genre=[],
                              youtubeID=search_result["snippet"]["channelId"],
                              published_at=search_result["snippet"]["publishedAt"],
                              want=True, excepted=False)
                video.save()
                self.__send_to_websocket(data=video, group_name='get_video_list')
        return
        # script, elements = self.__make_script(name, video_instance=video)
        # if script is None:
        #     return True
        # elif len(script) < self.settings['minimumSentence']:
        #     self.__send_to_websocket(f'"{title}" has short sentences❗️')
        #     continue
        # word_appearances = []
        # for element in elements:
        #     word_instance = Word.objects.get(word=element)
        #     word_appearances.append(
        #         WordAppearance(word=word_instance, video_href=video, appearance=elements[element]))
        # with transaction.atomic():
        #     try:
        #         video.save()
        #         WordAppearance.objects.bulk_create(word_appearances)
        #         Caption.objects.bulk_create(script)
        #     except Error as e:
        #         self.__send_to_websocket(str(e))

    def __make_script(self, name: str, video_instance: Video):
        url = f"http://video.google.com/timedtext?lang=id&name={name}&v={video_instance.video_href}"
        req = requests.get(url, timeout=time_out)
        if not req.ok:
            self.__send_to_websocket('error occurs')
            raise ValueError(f'Unexpected status code: {req.status_code}')
        root = ElementTree.fromstring(req.content)

        # 字幕つくる。構成単語も
        word_appearances: Optional[dict] = {}
        script: Optional[list] = []
        index: Optional[int] = 0

        for r in root.iter():
            imi = list()
            try:
                text = re.sub("\n", " ", r.text)
                text = unescape(text)
                self.__send_to_websocket(text)
            except TypeError:
                text = r.text
            except AttributeError:
                text = r.text

            try:
                raw_list = nltk.tokenize.word_tokenize(text)
                raw_list = [re.sub(self.REGEX_EXCEPT_HYPHEN, '', item) for item in raw_list]
                words = [i.lower() for i in raw_list if i and i != '-']
            except TypeError:
                continue

            if not words:
                continue

            # DBから意味を取得。なければinsert
            idiom_flag = False
            for j, w in enumerate(words):
                meaning = str()
                idiom = str()
                if idiom_flag or re.match(self.REGEX_EXCEPT_HYPHEN, w):
                    idiom_flag = False
                    try:
                        words.remove(w)
                        w = words[j]
                    except IndexError:
                        continue

                if w.startswith('-') or w.endswith('-'):
                    w = re.sub('-', '', w)

                if w != 'di' and j + 1 != len(words) and words[j + 1] not in ['ini', '-']:
                    idiom = ' '.join([w, words[j + 1]])
                    meaning = self.__get_imi(idiom)
                if meaning:
                    w = idiom
                    idiom_flag = True
                else:
                    meaning = self.__get_imi(w)

                if meaning and w in word_appearances:
                    word_appearances[w].append(index)
                elif meaning and Word.objects.filter(word=w).exists():
                    word_appearances[w] = [index]

                if words[j]:
                    imi.append(meaning)
                    words[j] = w

            words = [i for i in words if i]
            start_time, end_time = self.__get_start_end(r)
            caption = Caption(video_href=video_instance, index=index, start_time=start_time,
                              end_time=end_time, text=text,
                              words=words, meanings=imi)
            script.append(caption)
            index = index + 1

        return script, word_appearances

    @staticmethod
    def __get_start_end(r):
        start = r.attrib.get('start')
        try:
            start_time = int(float(start) * 1000)
        except TypeError:
            start_time = 0

        dur = r.attrib.get('dur')
        try:
            end_time = start_time + int(float(dur) * 1000)
        except TypeError:
            end_time = start_time

        return start_time, end_time

    def __get_imi(self, w, recursion: bool = False) -> (str, bool):
        meaning = str()
        word = self.__get_word_from_db(w)
        if word:
            return word.meaning
        url = f'https://njjn.weblio.jp/content/{w}'

        time.sleep(0) if settings_py.DEBUG_CELERY else time.sleep(0.3)
        while True:
            try:
                r = requests.get(url, timeout=time_out)
                break
            except OpenSSL.SSL.WantReadError:
                time.sleep(0.1)
            except socket.timeout:
                time.sleep(0.1)
        soup = BeautifulSoup(r.text, 'lxml')

        elements_crosslink = soup.find_all(class_="crosslink")
        elements_igngj = soup.find_all(class_="Igngj")
        elements_midashigo = soup.find_all(class_='midashigo')
        if elements_crosslink or elements_igngj:
            for element in elements_midashigo:
                if w == element.text.lower().strip():
                    meaning = self.__format_text(elements_crosslink + elements_igngj)
                    break
        r.close()
        # 接頭語・接尾語とか。登録したくない奴はリターンする。
        if not meaning and '-' in w and ' ' not in w:
            w2 = w.split('-')[1]
            w1 = w.split('-')[0]
            if w2 and w1 in w2:
                meaning = self.__get_imi(w2, recursion=True)
            if meaning:
                meaning = meaning + " (\"-\"=複数/動作の繰り返し)"
                return meaning
        elif not meaning and w.endswith('nya'):
            w1 = w[:len(w) - 3]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+nya=特定の事柄・人を表す接尾辞)"
                return meaning
        elif not meaning and w.endswith('kah'):
            w1 = w[:len(w) - 3]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+kah=～ですか？)"
                return meaning
        elif not meaning and w.endswith('an') and not w.endswith('kan'):
            w1 = w[:len(w) - 2]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+an=単位/内容を特定する接尾辞)"
                return meaning
        elif not meaning and w.endswith('in') and '-' not in w:
            w1 = w[:len(w) - 2]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+in=ジャカルタ方言・他動詞の語幹をつくる接尾辞)"
                return meaning
        elif not meaning and w.endswith('i'):
            w1 = w[:len(w) - 1]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+i=前置詞を代替する接尾辞/動作の反復・集中)"
                return meaning
        elif not meaning and w.endswith('kan'):
            w1 = w[:len(w) - 3]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+kan=他動詞の語幹をつくる接尾辞)"
                return meaning
        elif not meaning and w.startswith('mu'):
            w1 = w[2:]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning and '=' not in meaning:
                meaning = meaning + " (+mu=君)"
                return meaning
        elif not meaning and w.startswith('ku'):
            w1 = w[2:]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning and '=' not in meaning:
                meaning = meaning + " (+ku=僕)"
                return meaning
        elif not meaning and w.endswith('lah'):
            w1 = w[:len(w) - 3]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+lah=強調)"
                return meaning
        elif not meaning and w.endswith('pun'):
            w1 = w[:len(w) - 3]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+pun=～でさえ/～でも)"
                return meaning
        elif not meaning and w.endswith('mu'):
            w1 = w[:len(w) - 2]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+mu=君)"
                return meaning
        elif not meaning and w.endswith('ku'):
            w1 = w[:len(w) - 2]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+ku=僕)"
                return meaning

        if not meaning and w.startswith('di'):
            w1 = w[2:]
            meaning = self.__get_imi(w1, recursion=True)

            if meaning == '':
                if w1.startswith(('l', 'r', 'm', 'n', 'w', 'y')):
                    w2 = 'me' + w1
                    meaning = self.__get_imi(w2, recursion=True)
                elif w1.startswith('t'):
                    w2 = 'men' + w1[1:]
                    meaning = self.__get_imi(w2, recursion=True)
                elif w1.startswith('p'):
                    w2 = 'mem' + w1[1:]
                    meaning = self.__get_imi(w2, recursion=True)
                elif w1.startswith(('c', 'j', 'z', 'sy', 'd')):
                    w2 = 'men' + w1
                    meaning = self.__get_imi(w2, recursion=True)
                elif w1.startswith('b'):
                    w2 = 'mem' + w1
                    meaning = self.__get_imi(w2, recursion=True)
                elif w1.startswith('s'):
                    w2 = 'meny' + w1[1:]
                    meaning = self.__get_imi(w2, recursion=True)
                else:
                    w2 = 'meng' + w1
                    meaning = self.__get_imi(w2, recursion=True)

            if meaning:
                meaning = meaning + " (+di=受け身を表す接頭辞/～で、～に)"
                return meaning
        elif not meaning and w.startswith('ber'):
            w1 = w[3:]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+ber=～を持っている／身につけている／伴っている)"
                return meaning
        elif not meaning and w.startswith('ter'):
            w1 = w[3:]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+ter=最も～/～してしまう，～してしまっている)"
                return meaning
        elif not meaning and w.startswith('se'):
            w1 = w[2:]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+se=1つの/1回の/同じ/全体)"
                return meaning
        elif not meaning and w.startswith('ke') and w.endswith('an'):
            w1 = w[2:len(w) - 2]
            meaning = self.__get_imi(w1, recursion=True)
            if meaning:
                meaning = meaning + " (+ke~an=ke--an派生語を作る共接辞)"
                return meaning

        if w.startswith('-') or w.endswith('-'):
            w = re.sub('-', '', w)
        word_ini = w[0:1]

        if re.match(self.REGEX_SPACE, w) and not meaning:
            return meaning
        elif not recursion and not re.match(self.REGEX_NUMBER, w):
            meaning = meaning.strip()
            word_instance = Word(word=w, word_ini=word_ini, meaning=meaning)
            word_instance.save()
        return meaning

    @staticmethod
    def __get_word_from_db(w):
        try:
            word = Word.objects.get(word=w)
        except Word.DoesNotExist:
            word = None
        return word

    def __format_text(self, elements):
        contents = list()
        key1 = str()
        description = False
        key = ''
        for tag in elements:
            contents = contents + tag.text.strip().split(',')
        c_unique = list(set(contents))
        for c in c_unique:
            if u'【説明】' in c:
                description = True
                key = c
                key1 = key.split(' / ')[1]
                break
        if description:
            c_unique.remove(u'説明')
            c_unique.remove(key)
            for c in c_unique:
                c = c.strip()
                if c in key and c != key:
                    c_unique.remove(c)
                elif self.REGEX_ALPHABET.match(c):
                    c_unique.remove(c)
            c_unique.append(key1)
        return '、'.join(c_unique)

    def __get_duration(self, href):
        url = f"https://www.googleapis.com/youtube/v3/videos?id={href}&key={self.Y_KEY}&part=contentDetails"
        response = urllib.request.urlopen(url, timeout=3.0).read()
        if not response:
            raise ValueError(f'Unexpected status code: {response.status_code}')
        data = json.loads(response)
        duration = data['items'][0]['contentDetails']['duration']
        dur = isodate.parse_duration(duration).total_seconds()
        dur = int(dur)
        return '{0:1d}:{1:02d}'.format(dur // 60, dur % 60)
