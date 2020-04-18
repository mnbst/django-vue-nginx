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

export const VIDEO = gql`query(
        $videoHref:String=""
    ){ video(
        videoHref:$videoHref
    ) {
        id
        videoHref
        videoImg
        videoTime
        videoTitle
        videoGenre
        youtubeID
    }
}`;

export const VIDEO_LIST = gql`query{ videoList{
        id
        videoHref
        videoImg
        videoTime
        videoTitle
        videoGenre
        youtubeID
    }
}`;