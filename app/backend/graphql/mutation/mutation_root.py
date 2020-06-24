import graphene

from .branches.caption import SaveCaption
from .branches.fetch_setting import CreateSettings
from .branches.video import ExceptVideo, ResetCaption, SelectVideo
from .branches.word import CreateWord


class RootMutation(graphene.ObjectType):
    create_word = CreateWord.Field()
    create_settings = CreateSettings.Field()
    except_video = ExceptVideo.Field()
    reset_caption = ResetCaption.Field()
    select_video = SelectVideo.Field()
    save_caption = SaveCaption.Field()
