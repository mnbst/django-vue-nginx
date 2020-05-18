import graphene

from ...query.root import VideoType, FetchSettingsType
from ....dictionary_console.models import Video, FetchSetting


class VideoInput(graphene.InputObjectType):
    video_href = graphene.String()
    user_id = graphene.Int()


class ExceptVideo(graphene.Mutation):
    video_href = graphene.String()
    user_id = graphene.Int()

    class Arguments:
        video_input = VideoInput(required=True)

    video_list = graphene.List(VideoType)
    settings = graphene.Field(FetchSettingsType)

    @classmethod
    def mutate(cls, info, *args, **kwargs):
        video_input = kwargs['video_input']
        user_id = video_input['user_id']
        video_href = video_input.video_href
        Video.objects.filter(video_href=video_href).delete()
        settings = FetchSetting.objects.get(id=user_id)
        settings.excepted_href.append(video_href)
        settings.save()
        return cls(video_list=Video.objects.all(), settings=FetchSetting.objects.get(id=user_id))
