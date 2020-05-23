import {gql} from 'apollo-boost';

export const VIDEO_OPTIMISTIC = {
    __typename: 'Mutation',
    createVideo: {
        id: 0,
        videoHref: 'loading...',
        videoImg: 'loading...',
        videoTime: 'loading...',
        videoTitle: 'loading...',
        videoGenre: ['loading...'],
        youtubeID: 'loading...',
    },
};
export const VIDEO_LIST = gql`query{
  videoList{
    id
    videoTitle
    videoImg
    videoTime
    videoHref
    videoGenre
    youtubeID
    publishedAt
    want
    hasCaption
  }
}`;

export const VIDEO_CAPTION_SET = gql`query(
        $videoHref:String=""
    ){
    video(
        videoHref:$videoHref
    ) {
        id
        videoHref
        videoTitle
        videoGenre
    }
    captionList(
        videoHref:$videoHref
    ) {
        index
        startTime
        endTime
        text
        words
        meanings
    }
    videoList{
        id
        videoHref
        videoImg
        videoTime
        videoTitle
    }
}`;
