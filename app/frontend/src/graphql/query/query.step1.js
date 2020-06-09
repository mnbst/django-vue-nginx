import {gql} from 'apollo-boost';

export const SETTING_OPTIMISTIC = {
    __typename: 'Mutation',
    createSettings: {
        __typename: "setting",
        id: 1,
        authority: "super",
        exceptedHref: ['saving...'],
        pageToCrawl: 0,
        languageLimit: 0,
        minimumSentence: 0,
        videoPerPage: 0,
        videoToDelete: ['saving...'],
        videoToRenewal: ['saving...'],
    },
};

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
        hasCaption:true,
        captionSet: [{
            index: 0,
            startTime: 0,
            endTime: 0,
            text: "loading",
            captionwordSet: [
                {
                    rootWord: {
                        word: "",
                        meaning: ""
                    },
                    fixedWord: "",
                    fixedMeaning: ""
                },
                {
                    rootWord: {
                        word: "",
                        meaning: ""
                    },
                    fixedWord: "",
                    fixedMeaning: ""
                },
            ],

        }]
    }
}

export const VIDEO_SETTINGS = gql`query ($videoHref: String=""){ 
settings(authority:"super") {
    id
    authority
    exceptedHref
    pageToCrawl
    videoPerPage
    videoToDelete
    videoToRenewal
    minimumSentence
    languageLimit
    }
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
  video(videoHref: $videoHref) {
    videoHref
    videoImg
    videoTime
    videoTitle
    videoGenre
    captionSet {
      index
      startTime
      endTime
      text
      captionwordSet {
        rootWord {
          word
          meaning
        }
        fixedWord
        fixedMeaning
      }
    }
  }
}`;
