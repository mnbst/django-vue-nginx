<template>
    <div class="selectableVideoList">
        <div class="container--fluid">
            <v-row justify="center">
                <v-icon class="mr-1">keyboard_arrow_left</v-icon>
                <h2 class="my-2">動画リスト作成</h2>
                <v-icon class="ml-1">keyboard_arrow_right</v-icon>
            </v-row>
            <div class="row">
                <div class="col-lg-4 col-xl-12 px-4">
                    <div class="video-container">
                        <youtube class="video-player" :video-id="videoHref"
                                 width="100%"
                                 height="380"

                                 ref="player"/>
                    </div>
                    <div v-if="video">
                        <div>
                            <h3>TITLE: {{video.videoTitle}}</h3>
                            <h4 class="pt-5">ID: {{video.videoHref}}</h4>
                            <h4 class="pt-5">PLAY TIME: {{video.videoTime}}</h4>
                            <div class="row pl-3">
                                <h4 class="pt-5 mr-5">SELECT: </h4>
                                <v-checkbox v-model="video.want"></v-checkbox>
                                <v-spacer></v-spacer>
                                <v-dialog v-model="dialog" persistent max-width="290">
                                    <template v-slot:activator="{ on }">
                                        <v-btn class="mt-5 mr-5" color="error" v-on="on">ADD THIS VIDEO TO NG</v-btn>
                                    </template>
                                    <v-card>
                                        <v-card-title class="headline">{{video.videoHref}}を除外動画idリストに追加しますか?
                                        </v-card-title>
                                        <v-card-actions>
                                            <v-spacer></v-spacer>
                                            <v-btn color="green darken-1" text @click="dialog = false">いいえ</v-btn>
                                            <v-btn color="green darken-1" text @click="addExceptedList(video)">はい
                                            </v-btn>
                                        </v-card-actions>
                                    </v-card>
                                </v-dialog>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 col-xl-12 ml-n7">
                    <v-row>
                        <v-checkbox class="ml-7 my-n3" v-model="checkbox" :label="`全選択`"
                                    @change="checkAll($event)"></v-checkbox>
                    </v-row>
                    <virtual-list v-if="videoList" :size="26" :remain="24">
                        <ul v-for="item in videoList" :key="item.id">
                            <div v-if="!item.hasCaption" class="row">
                                <v-checkbox class="mx-1 left" v-model="item.want"></v-checkbox>
                                <img class="col-4  mx-n5" @click="setVideoId(item)"
                                     :src="item.videoImg"/>
                                <div class="col-8">
                                    <a @click="setVideoId(item)" class="d-inline-block text-truncate"
                                       style="max-width: 100%;">
                                        {{item.videoTitle}}
                                    </a>
                                    <p class="grey--text">{{item.videoTime}}</p>
                                </div>
                            </div>

                        </ul>
                    </virtual-list>
                </div>
                <div class=" col-lg-4 col-xl-12 px-4">
                    <v-card class="col-12" color="white align-center">

                        <v-row>
                            <div class="col-6">
                                <p class="text-center col-10">クロールするページ数</p>
                            </div>
                            <v-col cols="6">
                                <number-input
                                        inline
                                        controls
                                        v-model="settings.pageToCrawl"
                                        :min="1"
                                        :max="10"
                                        :step="1"
                                ></number-input>
                            </v-col>
                        </v-row>
                        <v-row>
                            <div class="col-6">
                                <p class="text-center col-10">字幕言語数</p>
                            </div>
                            <div class="col-6">
                                <number-input
                                        inline
                                        controls
                                        v-model="settings.languageLimit"
                                        :min="1"
                                        :max="10"
                                        :step="1"
                                ></number-input>
                            </div>
                        </v-row>
                        <v-row>
                            <div class="col-6">
                                <p class="text-center col-10">ページ毎の取得動画数</p>
                            </div>
                            <div class="col-6">
                                <number-input
                                        inline
                                        controls
                                        v-model="settings.videoPerPage"
                                        :min="1"
                                        :max="50"
                                        :step="1"
                                ></number-input>
                            </div>
                        </v-row>
                        <v-row>
                            <div class="col-6">
                                <p class="text-center col-10">再取得動画id</p>
                            </div>
                            <div class="col-6">
                                <div class="list-view mb-n5 pa-0">
                                    <v-text-field class="mb-n4"
                                                  v-for="(_, renewal_index) in settings.videoToRenewal"
                                                  :key="renewal_index+1"
                                                  v-model="settings.videoToRenewal[renewal_index]">
                                    </v-text-field>
                                    <v-text-field class="mb-n4"
                                                  v-if="settings.videoToRenewal && settings.videoToRenewal.length===0"
                                                  v-model="settings.videoToRenewal[0]">
                                    </v-text-field>
                                </div>
                                <v-btn
                                        class="pt-6"
                                        icon
                                        color="grey lighten-1"
                                        v-on:click="add_form(settings.videoToRenewal)"
                                >
                                    <v-icon dark>add_circle</v-icon>
                                </v-btn>
                                <v-btn
                                        class="pt-6"
                                        icon
                                        color="grey lighten-1"
                                        v-on:click="remove_form(settings.videoToRenewal)"
                                >
                                    <v-icon dark>remove_circle</v-icon>
                                </v-btn>
                            </div>
                        </v-row>
                        <v-row>
                            <div class="col-6">
                                <p class="text-center col-10">NG動画id</p>
                            </div>
                            <div class="col-6">
                                <div class="list-view mb-n5 pa-0">
                                    <v-text-field class="mb-n4"
                                                  v-for="(_,delete_index) in settings.exceptedHref"
                                                  :key="delete_index+1"
                                                  v-model="settings.exceptedHref[delete_index]">
                                    </v-text-field>
                                    <v-text-field class="mb-n4"
                                                  v-if="settings.exceptedHref && settings.exceptedHref.length===0"
                                                  v-model="settings.exceptedHref[0]">
                                    </v-text-field>
                                </div>
                                <v-btn
                                        class="pt-6"
                                        icon
                                        top
                                        color="grey lighten-1"
                                        v-on:click="add_form(settings.exceptedHref)"
                                >
                                    <v-icon dark>add_circle</v-icon>
                                </v-btn>
                                <v-btn
                                        class="pt-6"
                                        icon
                                        top
                                        color="grey lighten-1"
                                        v-on:click="remove_form(settings.exceptedHref)"
                                >
                                    <v-icon dark>remove_circle</v-icon>
                                </v-btn>
                            </div>
                        </v-row>
                        <v-row>
                            <v-spacer></v-spacer>
                            <v-btn v-if="saving===false" class="mr-5" color="orange font-weight-bold"
                                   v-on:click="modify(settings)">save settings
                            </v-btn>
                            <v-btn v-if="activate===false" class="primary" @click="getList(settings)">
                                get video
                                list
                            </v-btn>
                            <v-btn v-else class="primary" @click="stopGetList(settings)">stop</v-btn>
                            <v-spacer></v-spacer>
                        </v-row>
                    </v-card>
                </div>
            </div>
        </div>
        <FetchData></FetchData>
        <VideoPlayer></VideoPlayer>
    </div>
</template>

<script>
    import virtualList from "vue-virtual-scroll-list";
    import {SETTING_OPTIMISTIC, VIDEO_SETTINGS,VIDEO_OPTIMISTIC} from "../../graphql/query/query.step1";
    import {CREATE_SETTINGS, EXCEPT_VIDEO} from "../../graphql/mutation/mutation.step1";
    import FetchData from "./FetchData";
    import VideoPlayer from "./VideoPlayer";
    import {getVideoList} from "../../endpoints";

    const reg = new RegExp(/[!-/:-@[-`{-㿿]/g);
    const promise = (setting) => new Promise((resolve) => {
        if (setting.authority) {
            Object.keys(setting).forEach(function (prop) {
                if (Array.isArray(setting[prop])) {
                    let property = setting[prop]
                    property = property.map(Function.prototype.call, String.prototype.trim)
                    try {
                        setting[prop] = property.filter(item => reg.test(item) === false && item !== '');
                    } catch (_) {
                        return null;
                    }
                }
            });
            resolve(setting)
        } else {
            setting.authority = 'super';
            resolve(setting)
        }
    });
    let socket = null;
    export default {
        name: "SelectableVideoList",
        data: () => ({
            videoList: [],
            settings: {},
            video: null,
            videoHref: '',
            saving: false,
            activate: false,
            dialog: false,
            checkbox: 1
        }),
        computed: {
            player() {
                return this.$refs.player.player
            }
        },
        components: {
            VideoPlayer,
            FetchData,
            virtualList
        },
        apollo: {
            settings: VIDEO_SETTINGS,
            videoList: VIDEO_SETTINGS,
        },
        methods: {
            add_form(form) {
                form.push("");
            },
            remove_form(form) {
                form.splice(-1, 1);
            },
            setVideoId(video) {
                if (video !== null) {
                    this.video = video
                    this.videoHref = video.videoHref
                }
            },
            modify(settings) {
                let _this = this
                this.saving = true
                promise(settings)
                    .then(settings => {
                        this.$apollo.mutate({
                            mutation: CREATE_SETTINGS,
                            variables: settings,
                            update: (store, {data: {createSettings}}) => {
                                const data = store.readQuery({query: VIDEO_SETTINGS});
                                data.settings = createSettings;
                                store.writeQuery({query: VIDEO_SETTINGS, data})
                            },
                            optimisticResponse: SETTING_OPTIMISTIC
                        });
                        _this.saving = false;
                    })
                    .catch(e => {
                        console.log(e);
                        settings.authority = '';
                        _this.saving = false;
                    });
            },
            getList(setting) {
                let _this = this;
                socket = new WebSocket(getVideoList);
                socket.onmessage = function (message) {
                    _this.setVideoList(message);
                };
                socket.onopen = function () {
                    _this.$data.activate = true;
                    socket.send(JSON.stringify(setting));
                };
                socket.onerror = function () {
                    _this.$data.activate = false;
                };
                socket.onclose = function () {
                    _this.$data.activate = false;
                };
            },
            stopGetList() {
                if (socket && socket.readyState === 1) {
                    socket.close()
                }
            },
            setVideoList(message) {
                try {
                    const json = JSON.parse(message.data)
                    const videoExist = this.videoList.filter(video => video.videoTitle === json.videoTitle)
                    if (videoExist.length > 0) {
                        return null;
                    } else {
                        this.videoList.push(json);
                    }
                } catch (_) {
                    this.videoList.push({id: this.videoList.length, text: message.data});
                }
            },
            addExceptedList(video) {
                const _this = this
                this.dialog = false;
                video.userId = Number(this.settings.id)
                this.$apollo.mutate({
                    mutation: EXCEPT_VIDEO,
                    variables: video,
                    update: (store, {data: {exceptVideo}}) => {
                        const data = store.readQuery({query: VIDEO_SETTINGS});
                        for (let prop in data) {
                            if (Object.prototype.hasOwnProperty.call(exceptVideo, prop)) {
                                data[prop] = exceptVideo[prop];
                            }
                        }
                        store.writeQuery({query: VIDEO_SETTINGS, data});
                    },
                    optimisticResponse: VIDEO_OPTIMISTIC
                }).then(() => {
                    _this.video = null
                    _this.videoHref = null
                }).catch((error) => {
                    console.error(error)
                });
            },
            checkAll(event) {
                const videoList = this.videoList
                const iterator = videoList.values()
                for (const video of iterator) {
                    video.want = event
                }
            },
        }
    }
</script>

<style scoped>
    .list-view {
        border: 1px solid lightgray;
        border-radius: 4px;
        height: 100px;
        overflow-y: auto;
    }
</style>