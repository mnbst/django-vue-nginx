import {gql} from 'apollo-boost';

export const SETTING_OPTIMISTIC = {
    __typename: 'Mutation',
    createSettings: {
        __typename: "setting",
        id: 1,
        authority: "super",
        exceptedHref: [],
        pageToCrawl: 0,
        languageLimit: 0,
        minimumSentence: 0,
        videoPerPage: 0,
        videoToDelete: [],
        videoToRenewal: [],
    },
};

export const SETTINGS = gql`query{ settings(authority:"super") {
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
                         }`;
