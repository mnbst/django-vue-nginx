import {gql} from 'apollo-boost';

export const SETTINGS = gql`
   query{ settings(authority:"super") {
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
`;

export const CREATE_SETTINGS = gql`
   mutation{
  createSettings(settingsInput:{
  
  })}
`;