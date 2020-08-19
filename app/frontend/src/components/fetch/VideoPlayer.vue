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
                            <v-card v-scroll v-if="video" class="col-12 list mt-n4" height="360"
                                    color="white align-center">
                                <div v-if="loadingCaptionWordSet===true" class="text-center">
                                    <v-progress-circular
                                            :size="50"
                                            color="primary"
                                            indeterminate
                                    ></v-progress-circular>
                                </div>
                                <div v-else>
                                    <div class="row">
                                        <h3 class="">text</h3>
                                        <v-text-field
                                                class="mt-n4 mx-5 ml-12"
                                                type="text"
                                                v-model="video.captionSet[index].text"
                                        ></v-text-field>
                                    </div>
                                    <div class="row">
                                        <div class="col-6 my-n4">
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
                                        <div class="col-6 my-n4">
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
                                                <add-word-button class="mt-n3"></add-word-button>
                                            </div>
                                        </div>
                                    </div>
                                    <draggable v-model="video.captionSet[index].captionwordSet" @update="onUpdate">
                                        <transition-group>
                                            <div v-for="(captionWord,id) in video.captionSet[index].captionwordSet"
                                                 :key="id">
                                                <div class="row">
                                                    <div class="col-1">
                                                        <v-btn
                                                                class="mb-n12 mt-n12"
                                                                icon
                                                                top
                                                                color="grey lighten-1"
                                                                v-on:click="removeCaptionWord(id)"
                                                        >
                                                            <v-icon dark>remove_circle</v-icon>
                                                        </v-btn>
                                                    </div>
                                                    <div class="col-2">
                                                        <add-word-button :caption-word="captionWord" :order="id"
                                                                         :caption-index="index"></add-word-button>
                                                    </div>
                                                    <div class="col-2 ml-12 my-n4">
                                                        <v-text-field
                                                                type="text"
                                                                v-model="captionWord.fixedWord"
                                                        ></v-text-field>
                                                    </div>
                                                    <div class="col-6 my-n4">
                                                        <v-text-field
                                                                type="text"
                                                                v-model="captionWord.fixedMeaning"
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
                                                <reset-caption-button :video="video"
                                                                      :index="index"></reset-caption-button>
                                                <save-caption-button :video="video"
                                                                     :index="index"></save-caption-button>
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
    import {START_UP} from "../../graphql/query/query.step1";
    import draggable from 'vuedraggable'
    import {SELECT_VIDEO} from "../../graphql/mutation/mutation.step1";
    import AddWordButton from "../buttons/AddWord";
    import SaveCaptionButton from "../buttons/SaveCaption";
    import ResetCaptionButton from "../buttons/ResetCaption";

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
            ResetCaptionButton,
            SaveCaptionButton,
            AddWordButton,
            "virtual-list": virtualList,
            draggable
        },
        apollo: {
            videoList: START_UP,
            video: START_UP,
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
                this.playingVideo = false
                this.player.seekTo(caption.startTime / 1000)
                oneLine = true
                this.player.playVideo()
                this.playingVideo = true;
            },
            pauseOneCaption() {
                if (!this.player) {
                    return;
                }
                this.player.pauseVideo();
                this.playingVideo = false;
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
                            const data = store.readQuery({query: START_UP});
                            data.video = selectVideo.video
                            store.writeQuery({query: START_UP, data})
                        }
                    }).then(() => {
                    _this.loadingCaption = false
                })
            },
            jumpToIndex: function (index) {
                this.index = index
                const caption = this.video.captionSet.find(element => element.index === index)
                this.player.pauseVideo()
                this.playingVideo = false
                this.player.seekTo(caption.startTime / 1000)
                oneLine = true
                this.player.playVideo()
                this.playingVideo = true
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

    .action-buttons {
        position: sticky;
        margin-top: 160px;
        bottom: 0;
    }
</style>