import Vue from 'vue'
import vuex from 'vuex'
import axios from 'axios';

Vue.use(vuex, axios)

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
            axios.get('/api/words').then(data => {
                let words = data.data
                words.sort(dynamicSort('word'))
                commit('SET_WORDS', words)
            }).catch(e => {
                console.log(e);
            })
        },
        loadVideos({
                       commit
                   }) {
            axios.get('/api/videos').then(data => {
                let videos = data.data
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
            axios.get('/api/fetch_setting').then(data => {
                let fetch_setting = data.data[0]
                commit('SET_FETCH_SETTING', fetch_setting)
            }).catch(e => {
                console.log(e);
            })
        },
        loadCaptions({
                         commit
                     }) {
            axios.get('/api/captions').then(data => {
                let captions = data.data
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