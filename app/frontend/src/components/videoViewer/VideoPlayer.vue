<template>
    <div class="videoPlayer">
        <div class="container">
            <h3 class="col-lg-8 col-xl-12">{{video.videoTitle}}</h3>
            <div class="row">
                <div class="col-lg-8">
                    <div class="row">
                        <div class="col-lg-6 col-xl-12">
                            <div class="video-container">
                                <youtube class="video-player" :video-id="video.videoHref"
                                         width="380"
                                         height="300"
                                         @playing="playing"
                                         @paused="paused"
                                         @ended="ended"/>
                            </div>
                        </div>
                        <div class="col-lg-6 col-xl-12">
                            <v-list class="overflow-y-auto font-weight-black">
                                <ul v-for="caption in captionList" :key="caption.index">
                                    {{caption.index}}: {{caption.text}}
                                </ul>
                            </v-list>
                        </div>
                    </div>
                    <div class="row">
                        <v-card class="col-12" color="white align-center">
                            <div style="padding-top: 0;">
                                <v-col cols="12" sm="12">
                                    <v-layout row wrap>
                                        <v-col cols="6">
                                            <h4>word</h4>
                                            <v-flex v-for="(word,word_index) in captionList[index].words"
                                                    :key="word_index">
                                                <v-text-field class="my-n6 ml-3"
                                                       v-model="captionList[index].words[word_index]"/>
                                            </v-flex>
                                            <v-btn icon bottom color="grey lighten-1"
                                                   v-on:click="add_form(captionList[index])">
                                                <v-icon dark>add_circle</v-icon>
                                            </v-btn>
                                            <v-btn
                                                    icon
                                                    bottom
                                                    color="grey lighten-1"
                                                    v-on:click="remove_form(captionList[index])"
                                                    v-if="captionList[index].meanings.length>1"
                                            >
                                                <v-icon dark>remove_circle</v-icon>
                                            </v-btn>
                                        </v-col>
                                        <v-col cols="6">
                                            <h4>meaning</h4>
                                            <v-flex v-for="(_,word_imi_index) in captionList[index].meanings"
                                                    :key="word_imi_index">
                                                <v-text-field
                                                        class="my-n6 ml-3"
                                                        v-model="captionList[index].meanings[word_imi_index]"/>
                                            </v-flex>
                                            <v-btn
                                                    icon
                                                    bottom
                                                    color="grey lighten-1"
                                                    v-on:click="add_form(captionList[index])"
                                            >
                                                <v-icon dark>add_circle</v-icon>
                                            </v-btn>
                                            <v-btn
                                                    icon
                                                    bottom
                                                    color="grey lighten-1"
                                                    v-on:click="remove_form(captionList[index])"
                                                    v-if="captionList[index].length>0"
                                            >
                                                <v-icon dark>remove_circle</v-icon>
                                            </v-btn>
                                        </v-col>
                                    </v-layout>
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
                                                    v-model="captionList[index].index">
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
                                                    v-model="captionList[index].startTime"
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
                                                    v-model="captionList[index].endTime"
                                            ></v-text-field>
                                        </v-col>
                                    </div>
                                </v-col>
                            </div>
                        </v-card>
                    </div>
                </div>
                <div class="col-lg-4 col-xl-12">
                    <div class="video-list">
                        <div :key="video.id" v-for="video in videoList" class="thumbnail">
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
</template>

<script>
    import {VIDEO_CAPTION_SET} from "../../graphql/query/query.video";

    export default {
        name: 'VideoPlayer',
        data() {
            return {
                video: {},
                videoList: [],
                captionList: [],
                index: 0
            }
        },
        apollo: {
            videoList: {
                query: VIDEO_CAPTION_SET,
                fetchPolicy: 'no-cache',
            },
            video: VIDEO_CAPTION_SET,
            captionList: VIDEO_CAPTION_SET,
        },
        components: {},
        methods: {
            chooseVideo: function (video) {
                this.$apollo.queries.video.refetch({
                    videoHref: video.videoHref
                })
                this.$apollo.queries.captionList.refetch({
                    videoHref: video.videoHref
                })
            },
            playing: (event) => {
                console.log(event.getCurrentTime());
            },
            paused: (event) => {
                console.log(event.getCurrentTime())
            },
            ended: (event) => {
                console.log(event.getCurrentTime())
            }
        }
    }
</script>

<style scoped>
    .video-player {
        width: 100%;
    }

    .overflow-y-auto {
        border: 1px solid;
        height: 100%;
        max-height: 300px;
        width: 100%;
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

</style>