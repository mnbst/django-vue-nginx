import os.path
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import google.cloud.exceptions
import datetime
import urllib
import json
import isodate

dic = 'dictionary'
ng_dic = 'ng_dictionary'
video = 'video'
_caption = 'caption'

DEVELOPER_KEY = "AIzaSyArfj1GLTVUIyJ41bSm5I9gDLd5Frvn5Sk"

# connection firestore
file_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(file_path, 'CredentialKey.json')
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()
batch = db.batch()

# firestoreにデータ格納


class FireStore:
    @classmethod
    def dictionary_db(cls, w, word_ini, meaning):
        doc = db.collection(dic).document(w)
        doc.set({
            u'word': w,
            u'word_ini': word_ini,
            u'word_imi': meaning,
        })

    @classmethod
    def dictionary_db_ng(cls, w, word_ini):
        try:
            docng = db.collection(ng_dic).document(w)
            docng.set({
                u'word': w,
                u'word_ini': word_ini,
            })
            return
        except google.api_core.exceptions.InvalidArgument:
            return

    @classmethod
    def get_word(cls, w):
        return db.collection(dic).document(w).get()

    @classmethod
    def set_caption(cls, href, search_result, title, script, element):
        batch.set(
            db.collection(video).document(href), {
                u'video_href':
                href,
                u'youtubeID':
                search_result["snippet"]["channelId"],
                u'video_img':
                search_result["snippet"]["thumbnails"]["medium"]["url"],
                u'video_title':
                title,
                u'video_update_time':
                search_result["snippet"]["publishedAt"],
                u'video_time':
                getduration(href),
                u'get_caption_ymd':
                datetime.datetime.today(),
            })

        batch.set(
            db.collection(_caption).document(href), {
                u'caption_id': href,
                u'caption_title': title,
            })

        for i, s in enumerate(script):
            doc_name = str(i) + u'page'
            batch.set(
                db.collection(_caption).document(href).collection(
                    u'content').document(doc_name), {
                        u'index': s['index'],
                        u'start_time': s['start_time'],
                        u'end_time': s['end_time'],
                        u'text': s['text'],
                        u'text_tokenized': s['textTokenized'],
                })

        for j, t in enumerate(element):
            batch.set(db.collection(u'usecase').document(t),
                      {href + u'_exists': True},
                      merge=True)
            for e in element[t]:
                batch.set(
                    db.collection(u'usecase').document(t).collection(
                        u'case').document(href + '_' + str(e)), {
                            u'index': script[e]['index'],
                            u'video_href': href,
                            u'video_title': title,
                            u'video_time': getduration(href),
                            u'start_time': script[e]['start_time'],
                            u'end_time': script[e]['end_time'],
                            u'text': script[e]['text'],
                            u'text_tokenized': script[e]['textTokenized'],
                    })
            if len(batch._write_pbs) > 200:
                batch.commit()

        batch.commit()

    @classmethod
    def delete_href(cls, notwant_and_delete):

        for nd in notwant_and_delete:
            for k in db.collection(_caption).document(nd).collection(
                    u'content').stream():
                batch.delete(k.reference)
            k = None
            db.collection(video).document(nd).delete()
            db.collection(_caption).document(nd).delete()
            try:
                for k in db.collection('usecase').where(
                        nd + u'_exists', '==', True).stream():
                    batch.update(k.reference,
                                 {nd + u'_exists': firestore.DELETE_FIELD})
                    for k2 in k.reference.collection(u'cases').where(
                            u'href', '==', nd).stream():
                        batch.delete(k2.reference)
                        if len(batch._write_pbs) > 200:
                            batch.commit()
                k = None
                k2 = None
            except ValueError:
                continue

        batch.commit()

    @classmethod
    def video_data(cls, href):
        return db.collection(video).document(href).get()

    @classmethod
    def caption_data(cls, href):
        return db.collection(_caption).document(href).get()
