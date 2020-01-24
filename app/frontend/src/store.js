import Vue from 'vue'
import vuex from 'vuex'
import axios from 'axios';

Vue.use(vuex, axios)

export default new vuex.Store({
    state: {
        words: [],
        videos: [],
        captions: [],
        video_excepted: []
    },
    actions: {
        loadWords({
            commit
        }) {
            axios.get('/api/words').then(data => {
                let words = data.data
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
        loadVideosExcepted({
            commit
        }) {
            axios.get('/api/video_excepted').then(data => {
                let video_excepted=[]
                for (let d in data.data) {
                    video_excepted.push(data.data[d].video_href)
                }
                commit('SET_VIDEO_EXCEPTED', video_excepted)
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
        SET_VIDEO_EXCEPTED(
            state,
            video_excepted,
        ) {
            state.video_excepted = video_excepted;
        },
        SET_CAPTIONS(
            state,
            captions,
        ) {
            state.captions = captions;
        }
    }
})