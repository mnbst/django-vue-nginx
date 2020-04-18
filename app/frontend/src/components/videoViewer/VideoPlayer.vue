<template>
    <div class="videoPlayer">
        <div class="container">
            <div class="row">
                <div class="col-lg-7 col-xl-12">
                    <div class="video-container">
                        <h3>{{video.videoTitle}}</h3>
                        <iframe class="video-player" width="640" height="360"
                                :src="'https://www.youtube.com/embed/'+video.videoHref"
                                frameborder="0"
                                allow="autoplay; encrypted-media" allowfullscreen></iframe>
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
        components: {
            // "virtual-list": virtualList
        },
        apollo: {
            videoList: VIDEO_LIST,
            video: VIDEO,
            // captions: CAPTION,
        },
        methods: {
            chooseVideo: function (video) {
                this.$apollo.query({
                    query: VIDEO,
                    variables: {videoHref: video.videoHref},
                    update: (store, {data: {video}}) => {
                        const data = store.readQuery({query: VIDEO});
                        data.video = video;
                        store.writeQuery({query: VIDEO, data})
                    },
                })
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

    h3,
    p {
        margin: 0;
        padding: 0;
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