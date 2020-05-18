import {gql} from "apollo-boost";

export const CREATE_SETTINGS = gql`
   mutation(
    $id: Int!
    $authority: String!
    $exceptedHref: [String!]
    $pageToCrawl: Int!
    $languageLimit: Int!
    $minimumSentence: Int!
    $videoPerPage: Int!
    $videoToDelete: [String!]
    $videoToRenewal: [String!]
   ){
  createSettings(settingsInput:{
    id:$id
    authority:$authority
    exceptedHref: $exceptedHref
    pageToCrawl:  $pageToCrawl
    languageLimit:  $languageLimit
    minimumSentence:  $minimumSentence
    videoPerPage: $videoPerPage
    videoToDelete: $videoToDelete
    videoToRenewal: $videoToRenewal
  })
  {
    id
    authority
    exceptedHref
    pageToCrawl
    languageLimit
    minimumSentence
    videoPerPage
    videoToDelete
    videoToRenewal}
  }`;

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
    excepted
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
}`;