import Vue from 'vue'
import vuex from 'vuex'
import axios from 'axios';

Vue.use(vuex, axios)

export default new vuex.Store({
    state: {
        word: [],
        video: [],
        caption: []
    },
    actions: {
        loadWords({
            commit
        }) {
            axios.get('/api/words').then(data => {
                let words = data.data
                commit('SET_WORDS', words)
            }).catch(e => {
                document.write(e);
            })
        },
        loadVideos({
            commit
        }) {
            axios.get('/api/videos').then(data => {
                let videos = data.data
                commit('SET_VIDEOS', videos)
            }).catch(e => {
                document.write(e);
            })
        },
        loadCaptions({
            commit
        }) {

            axios.get('/api/captions').then((raw) => {
                async function f(d) {
                    let captions = d.data
                    for (var i = 0; i < captions.length; i++) {
                        captions[i].word = captions[i].word.split(',')
                        captions[i].word_imi = captions[i].word_imi.split(',')
                        captions[i].start_time = captions[i].start_time.toString()
                        captions[i].end_time = captions[i].end_time.toString()
                    }
                    return captions;
                }
                f(raw).then((captions) => {
                    commit('SET_CAPTIONS', captions)
                })
            }).catch(e => {
                document.write(e)
            })
        },
    },
    mutations: {
        SET_WORDS(
            state,
            words,
        ) {
            state.word = words;
        },
        SET_VIDEOS(
            state,
            videos,
        ) {
            state.video = videos;
        },
        SET_CAPTIONS(
            state,
            captions,
        ) {
            state.caption = captions;
        }
    }
})