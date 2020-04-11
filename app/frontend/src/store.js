import Vue from 'vue'
import vuex from 'vuex'
import axios from 'axios';

Vue.use(vuex, axios);

function dynamicSort(property) {
    let sortOrder = 1;
    if (property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a, b) {
        /* next line works with strings and numbers,
         * and you may want to customize it to your needs
         */
        let result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

export default new vuex.Store({
    state: {
        words: [],
        videos: [],
        captions: [],
        fetch_setting: {}
    },
    actions: {
        loadWords({
                      commit
                  }) {
            axios.post('/graphql', {query: `query{word{id,wordIni,word,meaning}}`}).then(result => {
                let words = result.data.data.word;
                words.sort(dynamicSort('word'));
                commit('SET_WORDS', words)
            }).catch(e => {
                console.log(e);
            })
        },
        loadVideos({
                       commit
                   }) {
            axios.post('/graphql', {query: `query{video{id,videoHref,videoImg,videoTime,videoTitle,videoGenre,youtubeID}}`}).then(data => {
                let videos = data.data.data.video;
                for (let k in videos) {
                    videos[k].video_upload_date = new Date(videos[k].video_upload_date)
                }
                commit('SET_VIDEOS', videos)
            }).catch(e => {
                console.log(e);
            })
        },
        loadFetchSetting({
                             commit
                         }) {
            axios.post('/graphql', {
                query: `query{ settings(authority:"super") {
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
                         }`
            }).then(data => {
                let fetch_setting = data.data.data.settings;
                if (fetch_setting === null) {
                    fetch_setting = {
                        authority: "",
                        exceptedHref: [],
                        pageToCrawl: 1,
                        languageLimit: 1,
                        minimumSentence: 10,
                        videoPerPage: 1,
                        videoToDelete: [],
                        videoToRenewal: []
                    }
                }
                commit('SET_FETCH_SETTING', fetch_setting)
            }).catch(e => {
                console.log(e);
            })
        },
        loadCaptions({
                         commit
                     }) {
            axios.get('/api/captions', {params: {video_href: ''}}).then(data => {
                let captions = data.data;
                commit('SET_CAPTIONS', captions)
            }).catch(e => {
                console.log(e)
            })
        },
    },
    mutations: {
        SET_WORDS(
            state,
            words,
        ) {
            state.words = words;
        },
        SET_VIDEOS(
            state,
            videos,
        ) {
            state.videos = videos;
        },
        SET_FETCH_SETTING(
            state,
            fetch_setting,
        ) {
            state.fetch_setting = fetch_setting;
        },
        SET_CAPTIONS(
            state,
            captions,
        ) {
            state.captions = captions;
        }
    }
})