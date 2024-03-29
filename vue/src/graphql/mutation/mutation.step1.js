import {gql} from "apollo-boost";

export const CREATE_SETTINGS = gql`
mutation ($settingInput: SettingsInput!) {
  createSettings(settingsInput: $settingInput) {
    id
    authority
    exceptedHref
    pageToCrawl
    languageLimit
    minimumSentence
    videoPerPage
    videoToDelete
    videoToRenewal
  }
}
`;

export const EXCEPT_VIDEO = gql`
mutation(
$videoHref:String!
$userId:Int!
){
exceptVideo(videoInput:{
videoHref:$videoHref
userId:$userId
}){
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
settings {
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
}
}
`;


export const RESET_CAPTION = gql`
mutation ($id: ID!) {
  resetCaption(id: $id) {
    caption {
      id
      index
      startTime
      endTime
      text
      captionwordSet {
        id
        rootWord {
          word
          meaning
        }
        order
        fixedWord
        fixedMeaning
      }
    }
  }
}
`;

export const SELECT_VIDEO = gql`
mutation ($videoHref: String!) {
  selectVideo(videoHref: $videoHref) {
    video {
      videoHref
      videoImg
      videoTime
      videoTitle
      videoGenre
      captionSet {
        id
        index
        startTime
        endTime
        text
        captionwordSet {
          id
          order
          rootWord {
            word
            meaning
          }
          fixedWord
          fixedMeaning
        }
      }
    }
  }
}
`;

export const SAVE_CAPTION = gql`
mutation ($captionInput: CaptionInput!, $captionWordInputs: [CaptionWordInput], $wordInputs: [WordInput]) {
  saveCaption(captionInput: $captionInput, captionWordInputs: $captionWordInputs, wordInputs: $wordInputs) {
    caption {
      id
      index
      startTime
      endTime
      text
      captionwordSet {
        id
        order
        rootWord {
          word
          meaning
        }
        fixedWord
        fixedMeaning
      }
    }
  }
}
`;

export const SEARCH_FOR_WORDS = gql`
mutation($word:String){
  searchForWords(word:$word){
    words{
      __typename
      id
      word
      wordIni
      meaning
    }
  }
}
`;

export const SAVE_CAPTION_WORD = gql`
mutation ($captionWordId: ID!, $rootWordId: ID!) {
  saveCaptionWord(captionWordId: $captionWordId, rootWordId: $rootWordId) {
    captionWord {
      id
      fixedWord
      fixedMeaning
      rootWord {
        id
        word
        meaning
      }
    }
  }
}
`;