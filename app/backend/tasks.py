from __future__ import absolute_import, unicode_literals

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ElementTree
from html import unescape
from urllib.error import HTTPError, URLError

import isodate
import nltk
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from celery import shared_task
from channels.layers import get_channel_layer
# from django.apps import apps
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from googleapiclient.errors import HttpError

from .dictionary_console.models import *


@shared_task
def scraping(settings: dict, group_name: str):
    youtube_scraping = YoutubeScraping(settings=settings, group_name=group_name)
    youtube_scraping.youtube_search()


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

    def __init__(self, settings: dict, group_name: str):
        self.settings = settings
        self.group_name = group_name
        self.channel_layer = get_channel_layer()

    def send_to_websocket(self, message: str):
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            "type": "fetch.data.message",
            "text": message,
        })

    def youtube_search(self):
        self.send_to_websocket('connecting...')
        Video.objects.filter(
            video_href__in=self.settings['video_to_delete'] + self.settings[
                'excepted_href'] + self.EXCEPT_VIDEO).delete()

        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey=self.Y_KEY, cache=MemoryCache())

        # Call worde search.list mewordod to retrieve results matching worde specified
        try:
            search_response = youtube.search().list(
                q='indonesia',
                part="id,snippet",
                maxResults=self.settings['video_per_page'],
                regionCode="id",
                relevanceLanguage="id",
                safeSearch="moderate",
                type="video",
                videoCaption="closedCaption",
                videoSyndicated="true").execute()
        except HttpError as e:
            json_str_data = e.content.decode()
            json_data = json.loads(json_str_data)
            self.send_to_websocket('ERROR❗... -> reason: ' + json_data['error']['errors'][0]['reason'])
            return

        page_token = search_response.get("nextPageToken", str)
        flag_disconnect = self.fill_in_db(response=search_response)
        if flag_disconnect:
            return

        for _ in range(0, self.settings['page_to_crawl'] - 1):
            search_response.update(youtube.search().list(
                q='indonesia',
                pageToken=page_token,
                part="id,snippet",
                maxResults=self.settings['video_per_page'],
                regionCode="id",
                relevanceLanguage="id",
                safeSearch="moderate",
                type="video",
                videoCaption="closedCaption",
                videoSyndicated="true").execute())
            page_token = search_response.get("nextPageToken", str)
            flag_disconnect = self.fill_in_db(response=search_response)
            if flag_disconnect:
                return

    def fill_in_db(self, response):
        # video_model = apps.get_model(app_label='dictionary_console', model_name='Video')
        # WordAppearance = apps.get_model(app_label='dictionary_console', model_name='WordAppearance')
        # word_model = apps.get_model(app_label='dictionary_console', model_name='Word')
        # caption_model = apps.get_model(app_label='dictionary_console', model_name='Caption')
        video_data = dict()
        for search_result in response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                href = search_result["id"]["videoId"]
                if href in self.EXCEPT_VIDEO + self.settings['excepted_href']:
                    continue
            else:
                continue

            try:
                video_data = Video.objects.get(video_href=href)
            except Video.DoesNotExist:
                self.send_to_websocket(f'getting video id: {href}')

            if video_data and href not in self.settings['video_to_renewal']:
                continue

            lang_codes = list()
            url = f'https://www.youtube.com/api/timedtext?type=list&v={href}'
            req = requests.get(url)
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
            if len(lang_codes) < self.settings['language_limit'] + 1 and 'id' in lang_codes:
                name = r.attrib.get('name')
                self.send_to_websocket('VIDEO TITLE: ' + search_result['snippet']['title'])
                title = search_result["snippet"]["title"]
                title = unescape(title)
                video = Video(video_href=href, video_img=search_result["snippet"]["thumbnails"]["medium"]["url"],
                              video_time=self.get_duration(href), video_title=title, video_genre=[],
                              youtubeID=search_result["snippet"]["channelId"],
                              video_upload_date=search_result["snippet"]["publishedAt"])

                script, element = self.make_script(name, video_instance=video)
                if script is None and element is None:
                    return True
                elif len(script) < self.settings['minimum_sentence']:
                    self.send_to_websocket(f'"{title}" has short sentences')
                    continue
                word_appearances = list()
                for el in element:
                    try:
                        db_data = WordAppearance.objects.filter(word=el)
                        print(db_data['el'])
                    except WordAppearance.DoesNotExist:
                        print(f'{el} not in db')
                    word_instance = Word.objects.filter(word=el)
                    word_appearance = WordAppearance(word=word_instance,
                                                     appearance=json.dumps({href: element[el]}))
                    word_appearances.append(word_appearance)
                while True:
                    if not script and not element:
                        break
                    Caption.objects.bulk_create(script, batch_size=50)
                    WordAppearance.objects.bulk_create(element, batch_size=50)
                video.save()

        return False

    def make_script(self, name: str, video_instance):
        # caption_model = apps.get_model(app_label='dictionary_console', model_name='Caption')
        url = f"http://video.google.com/timedtext?lang=id&name={name}&v={video_instance.video_href}"
        req = requests.get(url)
        root = ElementTree.fromstring(req.content)

        # 字幕つくる。構成単語も
        element = dict()
        script = list()
        index = int()

        for r in root.iter():

            imi = list()
            try:
                text = re.sub("\n", " ", r.text)
                text = unescape(text)
                self.send_to_websocket(text)
            except TypeError:
                text = r.text
            except AttributeError:
                text = r.text

            try:
                row = nltk.tokenize.word_tokenize(text)
                row = [re.sub(self.REGEX_EXCEPT_HYPHEN, '', item) for item in row]
                word = [i for i in row if i and not i == '-']
            except TypeError:
                continue

            if not word:
                continue

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

            # DBから意味を取得。なければinsert
            idiom_flag = False
            for j, w in enumerate(word):
                if idiom_flag:
                    word.remove(w)
                    idiom_flag = False
                    w = word[j]

                if re.match(self.REGEX, w):
                    word.remove(w)
                    w = word[j]

                meaning = str()
                idiom = str()
                w = w.lower()
                if w.startswith('-') or w.endswith('-'):
                    w = re.sub('-', '', w)

                if w != 'di' and j + 1 != len(word) and word[
                    j + 1] != 'ini' and w and word[j + 1] and word[
                    j + 1] != '-' and not self.REGEX.match(w) \
                        and not self.REGEX_EXCEPT_HYPHEN.match(word[j + 1]):
                    idiom = w + ' ' + word[j + 1]
                    idiom = idiom.lower()
                    meaning = self.get_imi(idiom)

                if meaning and idiom_flag:
                    w = idiom
                    idiom_flag = True
                elif not meaning:
                    meaning = self.get_imi(w)

                if meaning and w in element:
                    element[w].append(index)
                elif meaning and w not in element:
                    element[w] = [index]
                    if idiom_flag:
                        self.send_to_websocket('idiom found')

                if word[j]:
                    imi.append(meaning)
                    word[j] = w

            word = [i for i in word if i]
            sentence = Caption(video_href=video_instance, index=index, start_time=start_time,
                               end_time=end_time, text=text,
                               word=word, word_imi=imi)
            script.append(sentence)
            index = index + 1

        return script, element

    def get_imi(self, w):
        # WordAppearance = apps.get_model(app_label='dictionary_console', model_name='WordAppearance')
        # word_model = apps.get_model(app_label='dictionary_console', model_name='Word')
        meaning = self.get_meaning_from_db(w)
        if meaning:
            return meaning

        url = f'https://njjn.weblio.jp/content/{w}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        try:
            elements_crosslink = soup.find_all(class_="crosslink")
            elements_igngj = soup.find_all(class_="Igngj")
            elements_midashigo = soup.find_all(class_='midashigo')
            if elements_crosslink != [] or elements_igngj != []:
                if w == elements_midashigo[0].text.lower().strip():
                    meaning = self.format_text(elements_crosslink + elements_igngj)
        except HTTPError:
            meaning = ""
        except URLError:
            meaning = ""

        # 接頭語・接尾語とか。登録したくない奴はリターンする。
        if not meaning and '-' in w and ' ' not in w:
            w2 = w.split('-')[1]
            w1 = w.split('-')[0]
            if w2 and w1 in w2:
                meaning = self.get_imi(w2)
            if meaning:
                meaning = meaning + " (\"-\"=複数/動作の繰り返し)"
                return meaning
        elif not meaning and w.endswith('nya'):
            w1 = w[:len(w) - 3]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+nya=特定の事柄・人を表す接尾辞)"
                return meaning
        elif not meaning and w.endswith('kah'):
            w1 = w[:len(w) - 3]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+kah=～ですか？)"
                return meaning
        elif not meaning and w.endswith('an') and not w.endswith('kan'):
            w1 = w[:len(w) - 2]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+an=単位/内容を特定する接尾辞)"
                return meaning
        elif not meaning and w.endswith('in') and '-' not in w:
            w1 = w[:len(w) - 2]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+in=ジャカルタ方言・他動詞の語幹をつくる接尾辞)"
                return meaning
        elif not meaning and w.endswith('i'):
            w1 = w[:len(w) - 1]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+i=前置詞を代替する接尾辞/動作の反復・集中)"
                return meaning
        elif not meaning and w.endswith('kan'):
            w1 = w[:len(w) - 3]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+kan=他動詞の語幹をつくる接尾辞)"
                return meaning
        elif not meaning and w.startswith('mu'):
            w1 = w[2:]
            meaning = self.get_imi(w1)
            if meaning and '=' not in meaning:
                meaning = meaning + " (+mu=君)"
                return meaning
        elif not meaning and w.startswith('ku'):
            w1 = w[2:]
            meaning = self.get_imi(w1)
            if meaning and '=' not in meaning:
                meaning = meaning + " (+ku=僕)"
                return meaning
        elif not meaning and w.endswith('lah'):
            w1 = w[:len(w) - 3]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+lah=強調)"
                return meaning
        elif not meaning and w.endswith('pun'):
            w1 = w[:len(w) - 3]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+pun=～でさえ/～でも)"
                return meaning
        elif not meaning and w.endswith('mu'):
            w1 = w[:len(w) - 2]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+mu=君)"
                return meaning
        elif not meaning and w.endswith('ku'):
            w1 = w[:len(w) - 2]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+ku=僕)"
                return meaning

        if not meaning and w.startswith('di'):
            w1 = w[2:]
            meaning = self.get_imi(w1)

            if meaning == '':
                if w1.startswith(('l', 'r', 'm', 'n', 'w', 'y')):
                    w2 = 'me' + w1
                    meaning = self.get_imi(w2)
                elif w1.startswith('t'):
                    w2 = 'men' + w1[1:]
                    meaning = self.get_imi(w2)
                elif w1.startswith('p'):
                    w2 = 'mem' + w1[1:]
                    meaning = self.get_imi(w2)
                elif w1.startswith(('c', 'j', 'z', 'sy', 'd')):
                    w2 = 'men' + w1
                    meaning = self.get_imi(w2)
                elif w1.startswith('b'):
                    w2 = 'mem' + w1
                    meaning = self.get_imi(w2)
                elif w1.startswith('s'):
                    w2 = 'meny' + w1[1:]
                    meaning = self.get_imi(w2)
                else:
                    w2 = 'meng' + w1
                    meaning = self.get_imi(w2)

            if meaning:
                meaning = meaning + " (+di=受け身を表す接頭辞/～で、～に)"
                return meaning
        elif not meaning and w.startswith('ber'):
            w1 = w[3:]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+ber=～を持っている／身につけている／伴っている)"
                return meaning
        elif not meaning and w.startswith('ter'):
            w1 = w[3:]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+ter=最も～/～してしまう，～してしまっている)"
                return meaning
        elif not meaning and w.startswith('se'):
            w1 = w[2:]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+se=1つの/1回の/同じ/全体)"
                return meaning
        elif not meaning and w.startswith('ke') and w.endswith('an'):
            w1 = w[2:len(w) - 2]
            meaning = self.get_imi(w1)
            if meaning:
                meaning = meaning + " (+ke~an=ke--an派生語を作る共接辞)"
                return meaning

        if w.startswith('-') or w.endswith('-'):
            w = re.sub('-', '', w)
        word_ini = w[0:1]

        if meaning:
            meaning = meaning.strip()
            # set word
            word_instance = Word(word=w, word_ini=word_ini, word_imi=meaning)
            word_instance.save()
            WordAppearance(word=word_instance).save()
        return meaning

    @staticmethod
    def get_meaning_from_db(w):
        # word_model = apps.get_model(app_label='dictionary_console', model_name='Word')
        try:
            doc = Word.objects.get(word=w)
        except Word.DoesNotExist:
            meaning = ""
            return meaning

        if doc:
            meaning = doc.word_imi
            return meaning
        else:
            meaning = ''
        return meaning

    def format_text(self, elements):
        contents = list()
        key1 = str()
        setsumei = False
        key = ''
        for tag in elements:
            contents = contents + tag.text.strip().split(',')
        c_unique = list(set(contents))
        for c in c_unique:
            if u'【説明】' in c:
                setsumei = True
                key = c
                key1 = key.split(' / ')[1]
                break
        if setsumei:
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

    def get_duration(self, href):
        url = f"https://www.googleapis.com/youtube/v3/videos?id={href}&key={self.Y_KEY}&part=contentDetails"
        response = urllib.request.urlopen(url).read()
        data = json.loads(response)
        duration = data['items'][0]['contentDetails']['duration']
        dur = isodate.parse_duration(duration).total_seconds()
        dur = int(dur)
        return '{:2}:{:02}'.format(dur // 60, dur % 60)
