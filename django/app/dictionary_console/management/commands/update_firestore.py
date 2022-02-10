import firebase_admin
from django.core.management.base import BaseCommand
from django.db import transaction

from firebase_admin import firestore, initialize_app, credentials

from ...models import Word, Video, Caption

cred = credentials.Certificate(
    "/usr/src/app/app/dictionary_console/management/commands/firestore_sdk.json"
)
firebase_admin.initialize_app(cred)


class Command(BaseCommand):
    help = "update firestore"
    store_cli = None
    batch = None

    def add_arguments(self, parser):
        pass

    def update_dictionary(self):
        words = Word.objects.filter(ng=False, is_edited=True).all()
        with transaction.atomic():
            for index, word in enumerate(words):
                data = {
                    "word": word.word,
                    "initial": word.word_ini,
                    "meaning": word.meaning,
                }
                word_ref = self.store_cli.collection("dictionary").document(word.word)
                self.batch.set(word_ref, data, merge=True)
                word.is_edited = False
                word.save()
                if index % 499 == 0:
                    self.batch.commit()
            self.batch.commit()

    def update_videos(self):
        videos = Video.objects.filter(has_caption=True).all()
        with transaction.atomic():
            for index, video in enumerate(videos):
                data = {
                    "id": video.video_href,
                    "image": video.video_img,
                    "playtime": video.video_time,
                    "title": video.video_title,
                    "genre": video.video_genre,
                    "channelId": video.youtubeID,
                    "publishedAt": video.published_at,
                }
                videos_ref = self.store_cli.collection("videos").document(
                    video.video_href
                )
                self.batch.set(videos_ref, data, merge=True)
                if index % 499 == 0:
                    self.batch.commit()
                self.update_captions(video.caption_set.all())
            self.batch.commit()

    def update_captions(self, captions):
        for index, caption in enumerate(captions):
            data = {
                "index": caption.index,
                "startTime": caption.start_time,
                "endTime": caption.end_time,
                "text": caption.text,
                "videoId": caption.video.video_href,
            }
            caption_ref = self.store_cli.collection("captions").document()
            for caption_word in caption.captionword_set.all():
                caption_word_ref = caption_ref.collection("words").document(
                    caption_word.fixed_word
                )
                caption_word_ref.set(
                    {
                        "word": caption_word.fixed_word,
                        "meaning": caption_word.fixed_word,
                        "order": caption_word.order,
                        "rootReference": self.store_cli.document(
                            f"dictionary/{caption_word.root_word.word}"
                        ),
                    },
                    merge=True,
                )
            self.batch.set(caption_ref, data, merge=True)
            if index % 499 == 0:
                self.batch.commit()
        self.batch.commit()

    def handle(self, *args, **options):
        self.store_cli = firestore.client()
        self.batch = self.store_cli.batch()
        self.update_dictionary()
        self.update_videos()
