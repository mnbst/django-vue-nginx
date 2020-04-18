import {gql} from 'apollo-boost';

export const CAPTION_OPTIMISTIC = {
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

export const CAPTION = gql`query{ settings(authority:"super") {
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