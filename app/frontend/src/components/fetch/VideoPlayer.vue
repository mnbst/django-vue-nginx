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
                                    <div v-if="caption.index===index" class="blue--text"
                                         @click="jumpToIndex(caption.index)">
                                        {{caption.index}}: {{caption.text}}
                                    </div>
                                    <a v-else class="black--text" @click="jumpToIndex(caption.index)">{{caption.index}}:
                                        {{caption.text}}
                                    </a>
                                </div>
                            </virtual-list>
                        </div>
                    </div>
                    <div class="row pl-4">
                        <v-card v-if="video" class="col-12 list mt-n3" color="white align-center">
                            <v-col cols="12" sm="12">
                                <h3 class="mt-n5">word-meaning</h3>
                                <div class="row">
                                    <div class="col-3">
                                        <div v-for="(word,id) in video.captionSet[index].captionwordSet" :key="id">
                                            <v-text-field class="my-n7"
                                                          v-model="video.captionSet[index].captionwordSet[id].fixedWord"></v-text-field>
                                        </div>
                                    </div>
                                    <div class="col-9">
                                        <div v-for="(word,id) in video.captionSet[index].captionwordSet" :key="id">
                                            <v-text-field class="my-n7"
                                                          v-model="video.captionSet[index].captionwordSet[id].fixedMeaning"></v-text-field>
                                        </div>
                                    </div>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12">
                                <div class="row">
                                    <h3>index</h3>
                                    <v-col cols="3">
                                        <v-text-field
                                                class="my-n5 mb-n7 pa-0"
                                                min="0"
                                                step="1"
                                                type="number"
                                                v-model="video.captionSet[index].index">
                                        </v-text-field>
                                    </v-col>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12">
                                <div class="row">
                                    <h3>start_time</h3>
                                    <v-col cols="3">
                                        <v-text-field
                                                class="my-n5 mb-n7 pa-0"
                                                min="0"
                                                step="1"
                                                type="number"
                                                v-model="video.captionSet[index].startTime"
                                        ></v-text-field>
                                    </v-col>
                                </div>
                            </v-col>
                            <v-col cols="12" sm="12">
                                <div class="row">
                                    <h3>end_time</h3>
                                    <v-col cols="3">
                                        <v-text-field
                                                class="my-n5 mb-n7 pa-0"
                                                min="0"
                                                step="1"
                                                type="number"
                                                v-model="video.captionSet[index].endTime"
                                        ></v-text-field>
                                    </v-col>
                                </div>
                            </v-col>
                        </v-card>
                    </div>
                </div>
                <div class="col-lg-4 col-xl-12">
                    <div class="video-list">
                        <div :key="video.id" v-for="video in videoList" class="thumbnail">
                            <div v-if="video.hasCaption">
                                <a v-on:click="chooseVideo(video)" class="thumbnail-img">
                                    <img :src="video.videoImg"/>
                                </a>
                                <div class="thumbnail-info">
                                    <a v-on:click="chooseVideo(video)">
                                        <h3 v-on:click="chooseVideo(video)">{{video.videoTitle}}</h3>
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

    let timer;
    let oneLine = false;

    export default {
        name: 'VideoPlayer',
        data() {
            return {
                video: null,
                videoList: [],
                index: 0,
                loadingCaption: false,
            }
        },
        computed: {
            player() {
                return this.$refs.player.player
            }
        },
        components: {
            "virtual-list": virtualList
        },
        apollo: {
            videoList: VIDEO_SETTINGS,
            video: VIDEO_SETTINGS,
        },
        methods: {
            add_form(form) {
                form.push("");
            },
            remove_form(form) {
                form.splice(-1, 1);
            },
            chooseVideo: function (video) {
                const _this = this
                this.loadingCaption = true
                this.$apollo.queries.video.refetch({
                    videoHref: video.videoHref
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

    .thumbnail {
        display: flex;
    }

    .thumbnail img {
        width: 168px;
    }

    .thumbnail-info {
        margin-left: 20px;
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
        height: 340px;
        overflow-y: auto;
    }

    .videoPlayer {
        height: 730px;
    }

</style>