<template>
    <div class="videoPlayer">
        <div class="container--fluid">
            <v-row justify="center">
                <v-icon class="mr-1">keyboard_arrow_left</v-icon>
                <h2 class="my-2">字幕編集</h2>
                <v-icon class="ml-1">keyboard_arrow_right</v-icon>
            </v-row>
            <h3 class="col-lg-8 col-xl-12 my-n8" v-if="video">{{video.videoTitle}} : {{video.videoHref}}</h3>
            <div class="row">
                <div class="col-lg-8">
                    <div v-if="loadingCaption===true" class="text-center">
                        <v-progress-circular
                                :size="50"
                                color="primary"
                                indeterminate
                        ></v-progress-circular>
                    </div>
                    <div v-else class="row">
                        <div class="col-lg-6 col-xl-12 px-4">
                            <div v-if="video" class="video-container">
                                <youtube class="video-player" :video-id="video.videoHref"
                                         width="100%"
                                         height="300"
                                         @playing="playing"
                                         @paused="paused"
                                         @ended="ended"
                                         ref="player"/>
                            </div>
                        </div>
                        <div class="col-lg-6 col-xl-12">
                            <virtual-list v-if="video" class="virtual-list pl-4 font-weight-black" :size="30"
                                          :remain="10"
                                          :start="index-3">
                                <div v-for="caption in video.captionSet" :key="caption.index">
                                    <a v-if="caption.index===index" class="blue--text"
                                       @click="jumpToIndex(caption.index)">
                                        {{caption.index}}: {{caption.text}}
                                    </a>
                                    <a v-else class="black--text" @click="jumpToIndex(caption.index)">{{caption.index}}:
                                        {{caption.text}}
                                    </a>
                                </div>
                            </virtual-list>
                        </div>
                    </div>
                    <div class="container">
                        <div class="row pl-2">
                            <v-card v-scroll v-if="video" class="col-12 list mt-n3" color="white align-center">
                                <div v-if="loadingCaptionWordSet===true" class="text-center">
                                    <v-progress-circular
                                            :size="50"
                                            color="primary"
                                            indeterminate
                                    ></v-progress-circular>
                                </div>
                                <div v-else>
                                    <div class="row">
                                        <h3 class="mt-2">text</h3>
                                        <v-text-field
                                                class="my-n2 mx-5 ml-12"
                                                type="text"
                                                v-model="video.captionSet[index].text"
                                        ></v-text-field>
                                    </div>
                                    <div class="row">
                                        <div class="col-6 my-n3">
                                            <div class="row">
                                                <h3>start time</h3>
                                                <v-text-field
                                                        class="my-n3 mx-5"
                                                        min="0"
                                                        step="1"
                                                        type="number"
                                                        v-model="video.captionSet[index].startTime"
                                                ></v-text-field>
                                            </div>
                                        </div>
                                        <div class="col-6 my-n3">
                                            <div class="row">
                                                <h3>end time</h3>
                                                <v-text-field
                                                        class="my-n3 mx-5"
                                                        min="0"
                                                        step="1"
                                                        type="number"
                                                        v-model="video.captionSet[index].endTime"
                                                ></v-text-field>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="video.captionSet[index].captionwordSet.length===0">
                                        <div class="col-1">
                                            <div class="row">
                                                <v-btn
                                                        class="mb-n12 mt-n3"
                                                        icon
                                                        top
                                                        color="grey lighten-1"
                                                        v-on:click="addCaptionWord(video.captionSet[index].captionwordSet,0)"
                                                >
                                                    <v-icon dark>add_circle</v-icon>
                                                </v-btn>
                                            </div>
                                        </div>
                                    </div>
                                    <draggable v-model="video.captionSet[index].captionwordSet" @update="onUpdate">
                                        <transition-group>
                                            <div v-for="(word,id) in video.captionSet[index].captionwordSet" :key="id">
                                                <div class="row">
                                                    <div class="col-1">
                                                        <div class="row">
                                                            <v-btn
                                                                    class="mb-n12 mt-n3"
                                                                    icon
                                                                    top
                                                                    color="grey lighten-1"
                                                                    v-on:click="addCaptionWord(video.captionSet[index].captionwordSet,id)"
                                                            >
                                                                <v-icon dark>add_circle</v-icon>
                                                            </v-btn>
                                                            <v-btn
                                                                    class="mb-n12 mt-n3"
                                                                    icon
                                                                    top
                                                                    color="grey lighten-1"
                                                                    v-on:click="removeCaptionWord(id)"
                                                            >
                                                                <v-icon dark>remove_circle</v-icon>
                                                            </v-btn>
                                                        </div>
                                                    </div>
                                                    <div class="col-3">
                                                        <v-btn class="px-2 mt-n3">{{word.rootWord.word}}
                                                        </v-btn>
                                                    </div>
                                                    <div class="col-2 my-n7">
                                                        <v-text-field
                                                                type="text"
                                                                v-model="word.fixedWord"
                                                        ></v-text-field>
                                                    </div>
                                                    <div class="col-6 my-n7">
                                                        <v-text-field
                                                                type="text"
                                                                v-model="word.fixedMeaning"
                                                        ></v-text-field>
                                                    </div>
                                                </div>
                                            </div>
                                        </transition-group>
                                    </draggable>
                                </div>
                                <v-row class="mx-n8 action-buttons">
                                    <v-col cols="12">
                                        <v-toolbar flat dense class="mb-n6">
                                            <v-spacer></v-spacer>
                                            <v-card-actions>
                                                <v-btn icon>
                                                    <v-icon size="50" @click="previousPage">
                                                        mdi-chevron-left-box
                                                    </v-icon>
                                                </v-btn>
                                                <v-btn icon>
                                                    <v-icon size="50" @click="forwardPage">mdi-chevron-right-box
                                                    </v-icon>
                                                </v-btn>
                                                <v-btn v-if="!playingVideo" icon>
                                                    <v-icon size="50" @click="playOneCaption">mdi-play</v-icon>
                                                </v-btn>
                                                <v-btn v-else icon>
                                                    <v-icon size="50" @click="pauseOneCaption">
                                                        mdi-pause
                                                    </v-icon>
                                                </v-btn>
                                                <span>index: {{index}}/{{video.captionSet.length-1}}</span>
                                                <v-btn class="ml-3" color="secondary"
                                                       @click="resetCaption">戻す
                                                </v-btn>
                                                <v-btn class="ml-3" color="primary" @click="saveCaption">保存</v-btn>

                                            </v-card-actions>
                                        </v-toolbar>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-xl-12">
                    <div :key="video.id" v-for="video in videoList">
                        <div v-if="video.hasCaption">
                            <div class="row">
                                <img class="col-4" :src="video.videoImg" v-on:click="selectVideo(video)"/>
                                <div class="col-8">
                                    <a v-on:click="selectVideo(video)">
                                        <div class="text-truncate" v-on:click="selectVideo(video)">
                                            {{video.videoTitle}}
                                        </div>
                                    </a>
                                    <p>{{video.videoTime}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import virtualList from "vue-virtual-scroll-list";
    import {VIDEO_SETTINGS} from "../../graphql/query/query.step1";
    import draggable from 'vuedraggable'
    import {RESET_CAPTION, SAVE_CAPTION, SELECT_VIDEO} from "../../graphql/mutation/mutation.step1";

    let timer;
    let oneLine = false;

    export default {
        name: 'VideoPlayer',
        data() {
            return {
                index: 0,
                loadingCaption: false,
                loadingCaptionWordSet: false,
                dialog: false,
                addDialog: false,
                removeDialog: false,
                playingVideo: false,
            }
        },
        computed: {
            player() {
                return this.$refs.player.player
            }
        },
        components: {
            "virtual-list": virtualList,
            draggable
        },
        apollo: {
            videoList: VIDEO_SETTINGS,
            video: VIDEO_SETTINGS,
        },
        methods: {
            previousPage() {
                const index = this.index;
                if (index > 0) {
                    this.index--;
                }
            },
            forwardPage() {
                const index = this.index;
                if (index <= this.video.captionSet.length) {
                    this.index++;
                }
            },
            playOneCaption() {
                if (!this.player) {
                    return;
                }
                const index = this.index
                const caption = this.video.captionSet[index]
                this.player.pauseVideo()
                this.player.seekTo(caption.startTime / 1000)
                oneLine = true
                this.playingVideo = true;
                this.player.playVideo()
            },
            pauseOneCaption() {
                this.player.pauseVideo();
                this.playingVideo = false;
            },
            addCaptionWord(captionWord, index) {
                const word = {rootWord: {word: '', meaning: ''}, fixedWord: '', fixedMeaning: ''}
                captionWord.splice(index + 1, 0, word);
            },
            removeCaptionWord(index) {
                const captionWord = this.video.captionSet[this.index].captionwordSet
                captionWord.splice(index, 1);
            },
            onUpdate() {
                const index = this.index;
                const caption = this.video.captionSet[index];
                for (let i = 0; i < caption.captionwordSet.length; ++i) {
                    caption.captionwordSet[i].order = i;
                }
            },
            saveCaption() {
                const index = this.index;
                const caption = this.video.captionSet[index];
                const _this = this;
                let rootWordList = [];
                let captionWordList = [];
                for (let i = 0; i < caption.captionwordSet.length; i++) {
                    const captionWord = caption.captionwordSet[i]
                    const rootWord = captionWord.rootWord
                    captionWordList.push({
                        id: captionWord.id,
                        fixedWord: captionWord.fixedWord,
                        fixedMeaning: captionWord.fixedMeaning,
                        order: captionWord.order
                    })
                    rootWordList.push({word: rootWord.word, meaning: rootWord.meaning})
                }
                if (confirm('保存しますか？')) {
                    _this.$apollo.mutate({
                            mutation: SAVE_CAPTION,
                            variables: {
                                captionInput: {
                                    id: caption.id,
                                    index: index,
                                    startTime: caption.startTime,
                                    endTime: caption.endTime,
                                    text: caption.text,
                                },
                                captionWordInputs: captionWordList,
                                wordInputs: rootWordList,
                            },
                            update: (store, {data: {saveCaption}}) => {
                                const data = store.readQuery({query: VIDEO_SETTINGS});
                                data.video.captionSet[index] = saveCaption.caption;
                                store.writeQuery({query: VIDEO_SETTINGS, data});
                            }
                        }
                    ).then(() => {
                        alert('saved');
                    })
                }
            },
            resetCaption() {
                const video = this.video;
                const index = this.index;
                const target = video.captionSet[index];
                this.$apollo.mutate(
                    {
                        mutation: RESET_CAPTION,
                        variables: {id: target.id},
                        update: (store, {data: {resetCaption}}) => {
                            const data = store.readQuery({query: VIDEO_SETTINGS});
                            const renderedCaption = data.video.captionSet[index];
                            const originalCaption = resetCaption.caption;
                            renderedCaption.index = originalCaption.index;
                            renderedCaption.id = originalCaption.id;
                            renderedCaption.startTime = originalCaption.startTime;
                            renderedCaption.end_time = originalCaption.end_time;
                            renderedCaption.text = originalCaption.text;
                            for (let i = 0; i < renderedCaption.captionwordSet.length; ++i) {
                                const wordSet = renderedCaption.captionwordSet[i];
                                const originalWordSet = originalCaption.captionwordSet[i];
                                wordSet.id = originalWordSet.id;
                                wordSet.order = originalWordSet.order;
                                wordSet.fixedWord = originalWordSet.fixedWord;
                                wordSet.fixedMeaning = originalWordSet.fixedMeaning;
                                wordSet.rootWord.word = originalWordSet.rootWord.word;
                                wordSet.rootWord.meaning = originalWordSet.rootWord.meaning;
                            }
                            store.writeQuery({query: VIDEO_SETTINGS, data})
                        }
                    })
            },
            selectVideo: function (video) {
                if (this.loadingCaption) {
                    return
                }
                this.index = 0;
                const _this = this;
                const videoHref = video.videoHref;
                this.loadingCaption = true
                this.$apollo.mutate(
                    {
                        mutation: SELECT_VIDEO,
                        variables: {videoHref: videoHref},
                        update: (store, {data: {selectVideo}}) => {
                            const data = store.readQuery({query: VIDEO_SETTINGS});
                            data.video = selectVideo.video
                            store.writeQuery({query: VIDEO_SETTINGS, data})
                        }
                    }).then(() => {
                    _this.loadingCaption = false
                })
            },
            jumpToIndex: function (index) {
                this.index = index
                const caption = this.video.captionSet.find(element => element.index === index)
                this.player.pauseVideo()
                this.player.seekTo(caption.startTime / 1000)
                oneLine = true
                this.player.playVideo()
            },
            playing: function (event) {
                clearTimeout(timer)
                let _this = this
                const sequenceSub = function (beforeEndTime, index) {
                    let endTime = _this.video.captionSet[index].endTime;
                    let timeout = endTime - beforeEndTime;
                    _this.index = index
                    timer = setTimeout(function () {
                        sequenceSub(endTime, index + 1);
                    }, timeout);
                };
                const whichSub = function (currentTime, captionList) {
                    let id = 0;
                    let time = captionList[id]["endTime"];
                    while (time < currentTime) {
                        id += 1;
                        time = captionList[id]["endTime"];
                    }
                    return id
                };
                const currentTime = event.getCurrentTime() * 1000;
                if (oneLine === false) {
                    const captionList = this.video.captionSet;
                    const index = whichSub(currentTime, captionList)
                    this.index = index
                    const stopTime = captionList[index].endTime;
                    const timeOut = stopTime - currentTime;
                    timer = setTimeout(function () {
                        sequenceSub(stopTime, index + 1);
                    }, timeOut);
                } else {
                    const stopTime = this.video.captionSet[this.index].endTime;
                    const timeOut = stopTime - currentTime;
                    timer = setTimeout(function () {
                        _this.player.pauseVideo();
                        _this.playingVideo = false;
                    }, timeOut);
                    oneLine = false
                }
            },
            paused: function () {
                clearTimeout(timer)
            },
            ended: () => {
                clearTimeout(timer)
            }
        }
    }
</script>

<style scoped>
    .video-player {
        width: 100%;
    }

    .virtual-list {
        border: 1px solid;
        border-radius: 4px
    }

    .thumbnail img {
        width: 168px;
    }

    .thumbnail h3 {
        font-size: 16px;
    }

    .video-player {
        display: flex;
        width: 100%;
        margin: auto;
    }

    .row {
        display: flex;
        justify-content: space-between;
    }

    .list {
        height: 370px;
        overflow-y: auto;
    }

    .videoPlayer {
        height: 760px;
    }

    .meaning {
        width: 100%;
        overflow-x: scroll;
        white-space: nowrap;
        border-bottom: solid 1px;
    }

    .meaning::-webkit-scrollbar {
        display: none;
    }

    .action-buttons {
        position: sticky;
        margin-top: 160px;
        bottom: 0;
    }
</style>