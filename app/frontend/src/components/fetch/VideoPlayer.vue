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
                    <div class="row pl-4">
                        <v-card v-if="video" class="col-12 list mt-n3" color="white align-center">
                            <div cols="12" sm="12">
                                <div class="row">
                                    <v-dialog v-model="dialog" persistent max-width="290">
                                        <template v-slot:activator="{ on }">
                                            <v-btn class="ml-2 mt-n1" color="primary" v-on="on">保存</v-btn>
                                        </template>
                                        <v-card>
                                            <v-card-title class="headline">字幕{{index}}を保存しますか？
                                            </v-card-title>
                                            <v-card-actions>
                                                <v-spacer></v-spacer>
                                                <v-btn color="green darken-1" text @click="dialog = false">いいえ</v-btn>
                                                <v-btn color="green darken-1" text
                                                       @click="saveCaption(video.captionSet[index])">はい
                                                </v-btn>
                                            </v-card-actions>
                                        </v-card>
                                    </v-dialog>
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
                                <div v-for="(word,id) in video.captionSet[index].captionwordSet" :key="id">
                                    <div class="row">
                                        <div class="col-1">
                                            <div class="row">
                                                <v-dialog v-model="addDialog" persistent max-width="290">
                                                    <template v-slot:activator="{ on }">
                                                        <v-btn
                                                                class="mb-n12 mt-n3"
                                                                icon
                                                                top
                                                                color="grey lighten-1"
                                                                v-on="on"
                                                        >
                                                            <v-icon dark>add_circle</v-icon>
                                                        </v-btn>
                                                    </template>
                                                    <v-card>
                                                        <v-card-title class="headline">
                                                            単語を追加しますか？
                                                        </v-card-title>
                                                        <v-card-actions>
                                                            <v-spacer></v-spacer>
                                                            <v-btn color="green darken-1" text
                                                                   @click="addDialog = false">
                                                                いいえ
                                                            </v-btn>
                                                            <v-btn color="green darken-1" text
                                                                   v-on:click="addCaptionWord(video.captionSet[index].captionwordSet,id)">
                                                                はい
                                                            </v-btn>
                                                        </v-card-actions>
                                                    </v-card>
                                                </v-dialog>
                                                <v-dialog v-model="removeDialog" persistent max-width="290">
                                                    <template v-slot:activator="{ on }">
                                                        <v-btn
                                                                class="mb-n12 mt-n3"
                                                                icon
                                                                top
                                                                color="grey lighten-1"
                                                                v-on="on"
                                                        >
                                                            <v-icon dark>remove_circle</v-icon>
                                                        </v-btn>
                                                    </template>
                                                    <v-card>
                                                        <v-card-title class="headline">
                                                            単語を削除しますか？
                                                        </v-card-title>
                                                        <v-card-actions>
                                                            <v-spacer></v-spacer>
                                                            <v-btn color="green darken-1" text
                                                                   @click="removeDialog = false">
                                                                いいえ
                                                            </v-btn>
                                                            <v-btn color="green darken-1" text
                                                                   v-on:click="removeCaptionWord(id)">
                                                                はい
                                                            </v-btn>
                                                        </v-card-actions>
                                                    </v-card>
                                                </v-dialog>

                                            </div>
                                        </div>
                                        <div class="col-3">
                                            <div class="my-n2">
                                                <v-btn class="text-lowercase">{{word.fixedWord}}</v-btn>
                                            </div>
                                        </div>
                                        <div class="col-8 meaning">
                                            <div class="mb-n2">
                                                {{word.fixedMeaning}}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </v-card>
                    </div>
                </div>
                <div class="col-lg-4 col-xl-12">
                    <div :key="video.id" v-for="video in videoList">
                        <div v-if="video.hasCaption">
                            <div class="row">
                                <img class="col-4" :src="video.videoImg" v-on:click="chooseVideo(video)"/>
                                <div class="col-8">
                                    <a v-on:click="chooseVideo(video)">
                                        <div class="text-truncate" v-on:click="chooseVideo(video)">
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
                dialog: false,
                addDialog: false,
                removeDialog: false,
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
            addCaptionWord(captionWord, index) {
                captionWord.splice(index + 1, 0, captionWord[index]);
                this.addDialog = false;
            },
            removeCaptionWord(index) {
                const captionWord = this.video.captionSet[this.index].captionwordSet
                captionWord.splice(index, 1);
                this.removeDialog = false;
            },
            saveCaption(caption) {
                console.log(caption);
                this.dialog = false;
            },
            chooseVideo: function (video) {
                this.index = 0
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
</style>