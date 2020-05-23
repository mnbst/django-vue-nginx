from __future__ import absolute_import, unicode_literals

import re
import socket
import time
import xml.etree.ElementTree as ElementTree
from html import unescape
from sqlite3 import Error
from typing import Optional

import OpenSSL
import nltk
import requests
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from channels.layers import get_channel_layer
from django.db import transaction

from ... import settings as settings_py

from ...dictionary_console.models import *

time_out = (5.0, 30.0)


class GetCaption:
    REGEX_EXCEPT_HYPHEN = re.compile(r"[!-,.-/:-@[-`{-㿿]")
    REGEX = re.compile(r"[!-/:-@[-`{-㿿]")
    REGEX_ALPHABET = re.compile(r"[a-zA-Z\s]")
    REGEX_SPACE = re.compile(r"([-a-z0-9]+)\s([-a-z0-9]+)")
    REGEX_NUMBER = re.compile(r"[0-9]+")

    def __init__(self, data: dict):
        self.settings = data["setting"]
        self.video_list = data["videoList"]
        self.channel_layer = get_channel_layer()

    def __send_to_websocket(self, *args, **kwargs):
        text = kwargs.get("text", None)
        message = kwargs.get("message", None)
        if text:
            print(text)
            async_to_sync(self.channel_layer.group_send)(
                "get_caption", {"type": "get.caption.messages", "text": text}
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                "get_caption", {"type": "get.caption.messages", "text": message,}
            )

    def get_caption(self):
        for video in self.video_list:
            captions, caption_words = self.__make_script(video=video)
            if captions is None:
                return True
            elif len(captions) < self.settings["minimumSentence"]:
                self.__send_to_websocket(f'"{video.title}" has short sentences❗️')
                continue
            with transaction.atomic():
                try:
                    video.save()
                    Caption.objects.bulk_create(captions)
                    CaptionWord.objects.bulk_create(caption_words)
                except Error as e:
                    self.__send_to_websocket(str(e))
        return True

    def __make_script(self, video):
        caption_words: Optional[list] = []
        captions: Optional[list] = []
        index: Optional[int] = 0
        root_word: Optional[str] = ""
        caption_word: CaptionWord

        url = "http://video.google.com/timedtext?lang=id&name=&v={}".format(
            video["videoHref"]
        )
        response = requests.get(url, timeout=time_out)
        if not response.ok:
            self.__send_to_websocket("error occurs")
            raise ValueError(f"Unexpected status code: {response.status_code}")
        soup = BeautifulSoup(response.text, "lxml")

        for element in soup.find_all("text"):
            text = element.text
            words = self.__text_tokenize(text)
            if not words:
                continue

            start_time, end_time = self.__get_start_end(element)
            caption = Caption(
                video_id=video["id"],
                index=index,
                start_time=start_time,
                end_time=end_time,
                text=text,
            )
            captions.append(caption)
            idiom_flag = False
            for j, fixed_word in enumerate(words):
                meaning = str()
                idiom = str()
                if idiom_flag or re.match(self.REGEX_EXCEPT_HYPHEN, fixed_word):
                    idiom_flag = False
                    try:
                        words.remove(fixed_word)
                        fixed_word = words[j]
                    except IndexError:
                        continue
                if fixed_word.startswith("-") or fixed_word.endswith("-"):
                    fixed_word = re.sub("-", "", fixed_word)
                if (
                    fixed_word != "di"
                    and j + 1 != len(words)
                    and words[j + 1] not in ["ini", "-"]
                ):
                    idiom = " ".join([fixed_word, words[j + 1]])
                    root_word, meaning = self.__get_imi(idiom)
                if meaning:
                    fixed_word = idiom
                    idiom_flag = True
                else:
                    root_word, meaning = self.__get_imi(fixed_word)
                try:
                    word_instance = Word.objects.get(word=root_word)
                except Word.DoesNotExist:
                    word_instance = None
                caption_word = CaptionWord(
                    root_word=word_instance,
                    fixed_word=fixed_word,
                    fixed_meaning=meaning,
                    order=j,
                    caption=caption,
                )
                caption_words.append(caption_word)

            index = index + 1

        return captions, caption_words

    def __text_tokenize(self, text):
        text = re.sub("\n", " ", text)
        text = unescape(text)
        self.__send_to_websocket(text=text)
        try:
            raw_list = nltk.tokenize.word_tokenize(text)
            raw_list = [re.sub(self.REGEX_EXCEPT_HYPHEN, "", item) for item in raw_list]
            words = [i.lower() for i in raw_list if i and i != "-"]
        except TypeError:
            return False
        return words

    @staticmethod
    def __get_start_end(element):
        start = element.attrs.get("start")
        try:
            start_time = int(float(start) * 1000)
        except TypeError:
            start_time = 0

        dur = element.attrs.get("dur")
        try:
            end_time = start_time + int(float(dur) * 1000)
        except TypeError:
            end_time = start_time

        return start_time, end_time

    def __get_imi(self, word: str, recursion: bool = False):
        root_word_option = ""
        word = word.strip()
        try:
            word = Word.objects.get(word=word)
            return word.word, word.meaning
        except Word.DoesNotExist:
            pass
        meaning = self.__get_imi_from_weblio(word)
        if not meaning and "-" in word and " " not in word:
            su_root_word = word.split("-")[1]
            root_word = word.split("-")[0]
            if su_root_word and root_word in su_root_word:
                root_word_option, meaning = self.__get_imi(su_root_word, recursion=True)
            if meaning:
                meaning = '{} ("-"=複数/動作の繰り返し)'.format(meaning)
        elif not meaning and word.endswith("nya"):
            root_word = word[: len(word) - 3]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+nya=特定の事柄・人を表す接尾辞)".format(meaning)
        elif not meaning and word.endswith("kah"):
            root_word = word[: len(word) - 3]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+kah=～ですか？)".format(meaning)
        elif not meaning and word.endswith("an") and not word.endswith("kan"):
            root_word = word[: len(word) - 2]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+an=単位/内容を特定する接尾辞)".format(meaning)
        elif not meaning and word.endswith("in") and "-" not in word:
            root_word = word[: len(word) - 2]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+in=ジャカルタ方言・他動詞の語幹をつくる接尾辞)".format(meaning)
        elif not meaning and word.endswith("i"):
            root_word = word[: len(word) - 1]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+i=前置詞を代替する接尾辞/動作の反復・集中)".format(meaning)
        elif not meaning and word.endswith("kan"):
            root_word = word[: len(word) - 3]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+kan=他動詞の語幹をつくる接尾辞)".format(meaning)
        elif not meaning and word.startswith("mu"):
            root_word = word[2:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning and "=" not in meaning:
                meaning = "{} (+mu=君)".format(meaning)
        elif not meaning and word.startswith("ku"):
            root_word = word[2:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning and "=" not in meaning:
                meaning = "{} (+ku=僕)".format(meaning)
        elif not meaning and word.endswith("lah"):
            root_word = word[: len(word) - 3]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+lah=強調)".format(meaning)
        elif not meaning and word.endswith("pun"):
            root_word = word[: len(word) - 3]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+pun=～でさえ/～でも)".format(meaning)
        elif not meaning and word.endswith("mu"):
            root_word = word[: len(word) - 2]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+mu=君)".format(meaning)
        elif not meaning and word.endswith("ku"):
            root_word = word[: len(word) - 2]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+ku=僕)".format(meaning)
        if not meaning and word.startswith("di"):
            root_word = word[2:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)

            if not meaning:
                if root_word.startswith(("l", "r", "m", "n", "w", "y")):
                    root_word = "me{}".format(root_word)
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                elif root_word.startswith("t"):
                    root_word = "men{}".format(root_word[1:])
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                elif root_word.startswith("p"):
                    root_word = "mem{}".format(root_word[1:])
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                elif root_word.startswith(("c", "j", "z", "sy", "d")):
                    root_word = "men{}".format(root_word)
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                elif root_word.startswith("b"):
                    root_word = "mem{}".format(root_word)
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                elif root_word.startswith("s"):
                    root_word = "meny{}".format(root_word[1:])
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )
                else:
                    root_word = "meng{}".format(root_word)
                    root_word_option, meaning = self.__get_imi(
                        root_word, recursion=True
                    )

            if meaning:
                meaning = "{} (+di=受け身を表す接頭辞/～で、～に)".format(meaning)
        elif not meaning and word.startswith("ber"):
            root_word = word[3:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+ber=～を持っている／身につけている／伴っている)".format(meaning)
        elif not meaning and word.startswith("ter"):
            root_word = word[3:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+ter=最も～/～してしまう，～してしまっている)".format(meaning)
        elif not meaning and word.startswith("se"):
            root_word = word[2:]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+se=1つの/1回の/同じ/全体)".format(meaning)
        elif not meaning and word.startswith("ke") and word.endswith("an"):
            root_words_count = len(word) - 2
            root_word = word[2:root_words_count]
            root_word_option, meaning = self.__get_imi(root_word, recursion=True)
            if meaning:
                meaning = "{} (+ke~an=ke--an派生語を作る共接辞)".format(meaning)

        root_word = root_word_option if meaning and root_word_option else word
        if root_word.startswith("-") or root_word.endswith("-"):
            root_word = re.sub("-", "", root_word)
        word_ini = root_word[0:1]

        if re.match(self.REGEX_SPACE, root_word) and not meaning:
            return root_word, meaning
        elif not recursion and root_word == word:
            with transaction.atomic():
                meaning = meaning.strip()
                word_instance = Word(
                    word=root_word,
                    word_ini=word_ini,
                    meaning=meaning,
                    ng=False if meaning else True,
                )
                word_instance.save()
        return root_word, meaning

    def __get_imi_from_weblio(self, word):
        meaning = ""
        url = "https://njjn.weblio.jp/content/{}".format(word)
        time.sleep(0) if settings_py.DEBUG_CELERY else time.sleep(0.3)
        while True:
            try:
                response = requests.get(url, timeout=time_out)
                break
            except OpenSSL.SSL.WantReadError:
                time.sleep(0.1)
            except socket.timeout:
                time.sleep(0.1)
        soup = BeautifulSoup(response.text, "lxml")

        elements_crosslink = soup.find_all(class_="crosslink")
        elements_igngj = soup.find_all(class_="Igngj")
        elements_midashigo = soup.find_all(class_="midashigo")
        if elements_crosslink or elements_igngj:
            for element in elements_midashigo:
                if word == element.text.lower().strip():
                    meaning = self.__format_text(elements_crosslink + elements_igngj)
                    break
        response.close()
        return meaning

    def __format_text(self, elements):
        contents = list()
        key1 = str()
        description = False
        key = ""
        for tag in elements:
            contents = contents + tag.text.strip().split(",")
        c_unique = list(set(contents))
        for c in c_unique:
            if "【説明】" in c:
                description = True
                key = c
                key1 = key.split(" / ")[1]
                break
        if description:
            c_unique.remove("説明")
            c_unique.remove(key)
            for c in c_unique:
                c = c.strip()
                if c in key and c != key:
                    c_unique.remove(c)
                elif self.REGEX_ALPHABET.match(c):
                    c_unique.remove(c)
            c_unique.append(key1)
        return "、".join(c_unique)
