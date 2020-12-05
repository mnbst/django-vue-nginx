import graphene

from .branches.caption import SaveCaption
from .branches.caption_word import SaveCaptionWord
from .branches.fetch_setting import CreateSettings
from .branches.video import ExceptVideo, ResetCaption, SelectVideo
from .branches.words import SearchForWords


class RootMutation(graphene.ObjectType):
    create_settings = CreateSettings.Field()
    except_video = ExceptVideo.Field()
    reset_caption = ResetCaption.Field()
    select_video = SelectVideo.Field()
    save_caption = SaveCaption.Field()
    search_for_words = SearchForWords.Field()
    save_caption_word = SaveCaptionWord.Field()
