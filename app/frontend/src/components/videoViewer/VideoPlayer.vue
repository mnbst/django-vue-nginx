<template>
    <div class="videoPlayer">
        <div class="container">
            <div class="row">
                <div class="col-lg-7 col-xl-12">
                    <div class="video-container">
                        <h3>{{video.videoTitle}}</h3>
                        <youtube class="video-player" :video-id="video.videoHref" @playing="playing" @paused="paused"
                                 @ended="ended"/>
                        <div id="subtitle_area" class="col-md-12">
                            <div class="panel panel-default">
                                <div id="subtitle_block"></div>
                            </div>
                        </div>
                        <div id="subtitle_detail_area"></div>
                    </div>
                    <div class="row">
                    </div>
                </div>
                <div class="col-lg-5 col-xl-12">
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
    // import virtualList from "vue-virtual-scroll-list";
    // import {CAPTION} from "../../graphql/query/query.caption";
    import {VIDEO, VIDEO_LIST} from "../../graphql/query/query.video";

    export default {
        name: 'VideoPlayer',
        data() {
            return {
                video: {},
                videoList: [],
                captions: [],
            }
        },
        apollo: {
            videoList: VIDEO_LIST,
            video: VIDEO,
            // captions: CAPTION,
        },
        components: {
            // "virtual-list": virtualList
        },
        methods: {
            chooseVideo: function (video) {
                this.$apollo.queries.video.refetch({
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

    button {
        background: #D0021B;
        color: white;
        border: none;
        padding: 10px 20px;
    }
</style>