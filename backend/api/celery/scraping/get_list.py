from __future__ import absolute_import, unicode_literals

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ElementTree
from html import unescape

import isodate
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from googleapiclient.discovery import build
from googleapiclient.discovery_cache.base import Cache
from googleapiclient.errors import HttpError

from ... import settings as settings_py
from ...dictionary_console.serializers import VideoSerializer

from ...dictionary_console.models import *


time_out = (5.0, 30.0)


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


class GetVideoList:
    Y_KEY = os.environ.get("DEVELOPER_KEY")
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    EXCEPT_VIDEO = [
        "-3fl9HVCk3o",
        "vN_5MBIxjcs",
        "KLFjdzvTLWM",
        "CS9am2ctk1M",
        "r9QG3eFJUJk",
        "1jQdXHdJIQw",
        "FCeZqjTwO2M",
        "_lhS0oilP1Q",
        "auNX2WZLuXA",
        "AFD0nFg2s4M",
        "jvfAEtDlR2A",
        "C-vQZU1xAf4",
        "U8Fd0hqLApU",
        "OvMN_8ClEgA",
        "R2JhxW1rT8I",
        "pRpNiYI0g64",
        "xqJ-ag2VLbk",
        "SDD0r15AprU",
        "rEGmWKbHUAY",
        "UlFS0utBxB0",
        "APTRWJ8Q1UU",
        "lAeAO51aVKA",
        "Pl-RYkIXPnk",
        "e2RBRUFwmuw",
        "lIUYItKBbBc",
        "SJTzMHDaOlg",
        "fX6sg2xuvCw",
        "JT3Wc5alyfQ",
        "FlBdDhexQRc",
        "GePukn4vRV8",
        "-Xk5aUvZCc0",
        "5H-41WPSsHs",
        "bQ_WHZ_WS3s",
        "5M1_ufFxvlE",
        "1l_Y8X9HhUA",
        "d3yoDVp0hzc",
        "I7bVw0nGarQ",
        "XPzB_GSMABo",
        "_7SNK6m8okE",
        "sclwgAXiHhI",
        "jh8dEnVTvs8",
        "Xw5RBrqCoL8",
        "m37ByQITb9k",
        "BMmnrdlxdbg",
        "DCSC4OG4nEE",
        "n6hJXjka4Xk",
        "OCA9alkiptw",
        "ah0Vcf1X8r0",
        "EPgOhNeZYOc",
        "qGpvtvSzGQ8",
        "si16hSJF6v8",
        "A3LRdMUzI-4",
        "KaXx2z5rYIA",
        "MMIABcbEIGg",
        "9usVvl4q2Dc",
        "11I-WD-yBDU",
        "TRsf-OH9rM4",
    ]

    # 除外する記号
    REGEX_EXCEPT_HYPHEN = re.compile(r"[!-,.-/:-@[-`{-㿿]")
    REGEX = re.compile(r"[!-/:-@[-`{-㿿]")
    # アルファベット
    REGEX_ALPHABET = re.compile(r"[a-zA-Z\s]")
    REGEX_SPACE = re.compile(r"([-a-z0-9]+)\s([-a-z0-9]+)")
    REGEX_NUMBER = re.compile(r"[0-9０-９]+")

    def __init__(self, settings: dict):
        self.settings = settings
        self.channel_layer = get_channel_layer()

    def __send_to_websocket(self, group_name: str, *args, **kwargs):
        data = kwargs.get("data", None)
        message = kwargs.get("message", None)
        if data:
            video = json.dumps(VideoSerializer(data).data)
            async_to_sync(self.channel_layer.group_send)(
                group_name, {"type": "get.video.list.messages", "data": video}
            )
        else:

            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    "type": "get.video.list.messages",
                    "text": message,
                },
            )

    def get_video_list(self):
        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=self.Y_KEY,
            cache=MemoryCache(),
        )

        # Call worde search.list mewordod to retrieve results matching worde specified
        try:
            search_response = (
                youtube.search()
                .list(
                    q="indonesia",
                    part="id,snippet",
                    maxResults=self.settings["videoPerPage"],
                    regionCode="id",
                    relevanceLanguage="id",
                    safeSearch="moderate",
                    type="video",
                    videoCaption="closedCaption",
                    videoSyndicated="true",
                )
                .execute()
            )
        except HttpError as e:
            json_str_data = e.content.decode()
            json_data = json.loads(json_str_data)
            self.__send_to_websocket(
                message="ERROR❗... -> reason: "
                + json_data["error"]["errors"][0]["reason"],
                group_name="get_video_list",
            )
            return

        page_token = search_response.get("nextPageToken", str)
        self.__organize_list(response=search_response)

        for _ in range(0, self.settings["pageToCrawl"] - 1):
            search_response.update(
                youtube.search()
                .list(
                    q="indonesia",
                    pageToken=page_token,
                    part="id,snippet",
                    maxResults=self.settings["videoPerPage"],
                    regionCode="id",
                    relevanceLanguage="id",
                    safeSearch="moderate",
                    type="video",
                    videoCaption="closedCaption",
                    videoSyndicated="true",
                )
                .execute()
            )
            page_token = search_response.get("nextPageToken", str)
            self.__organize_list(response=search_response)
        self.__send_to_websocket(settings_py.END_MESSAGE, group_name="get_video_list")

    def __organize_list(self, response):
        for search_result in response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                href = search_result["id"]["videoId"]
                if href in self.EXCEPT_VIDEO + self.settings["exceptedHref"]:
                    continue
            else:
                continue
            video_exists = Video.objects.filter(video_href=href).exists()

            if video_exists and href not in self.settings["videoToRenewal"]:
                continue

            lang_codes = list()
            url = f"https://www.youtube.com/api/timedtext?type=list&v={href}"
            req = requests.get(url, timeout=time_out)
            if not req.ok:
                raise ValueError(f"Unexpected status code: {req.status_code}")
            try:
                root = ElementTree.fromstring(req.content)
            except ElementTree.ParseError:
                continue

            # 字幕言語取得
            r = dict()
            for r in root.iter():
                lang_code = r.attrib.get("lang_code")
                if lang_code is not None:
                    lang_codes.append(lang_code)

            # 字幕言語の数を指定してる
            if (
                len(lang_codes) < self.settings["languageLimit"] + 1
                and "id" in lang_codes
            ):
                name = r.attrib.get("name")
                title = search_result["snippet"]["title"]
                title = unescape(title)
                video = Video(
                    video_href=href,
                    video_img=search_result["snippet"]["thumbnails"]["medium"]["url"],
                    video_time=self.__get_duration(href),
                    video_title=title,
                    video_genre=[],
                    youtubeID=search_result["snippet"]["channelId"],
                    published_at=search_result["snippet"]["publishedAt"],
                    want=True,
                    has_caption=False,
                )
                video.save()
                self.__send_to_websocket(data=video, group_name="get_video_list")
        return

    def __get_duration(self, href):
        url = f"https://www.googleapis.com/youtube/v3/videos?id={href}&key={self.Y_KEY}&part=contentDetails"
        response = urllib.request.urlopen(url, timeout=3.0).read()
        if not response:
            raise ValueError(f"Unexpected status code: {response.status_code}")
        data = json.loads(response)
        duration = data["items"][0]["contentDetails"]["duration"]
        dur = isodate.parse_duration(duration).total_seconds()
        dur = int(dur)
        return "{0:1d}:{1:02d}".format(dur // 60, dur % 60)
