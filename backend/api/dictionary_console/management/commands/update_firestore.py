from django.core.management.base import BaseCommand

from firebase_admin import firestore, initialize_app

from ...models import Word, Video

initialize_app()


class Command(BaseCommand):
    help = "update firestore"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        entire = options["--entire"]
        word = options["--word"]
        video = options["--video"]

        db = firestore.client()
        batch = db.batch()
        if entire or word:
            words = Word.objects.filter(ng=False).all()
            for index, word in enumerate(words):
                print(word.word)
                data = {
                    u"word": word.word,
                    u"initial": word.word_ini,
                    u"meaning": word.meaning,
                }
                word_ref = db.collection(u"dictionary").document(word.word)
                batch.set(word_ref, data, merge=True)
                if index % 499 == 0:
                    batch.commit()
            batch.commit()

        if entire or video:
            videos_list = Video.objects.filter(has_caption=True).all()
            for video in videos_list:
                captions = video.caption_set
                for caption in captions:
                    data = {}
            batch.commit()
