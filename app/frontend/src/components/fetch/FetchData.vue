<template>
    <div id="FetchData" class="mt-5">
        <div class="container--fluid">
            <v-row justify="center">
                <v-icon class="mr-1">keyboard_arrow_left</v-icon>
                <h2 class="my-2">字幕作成</h2>
                <v-icon class="ml-1">keyboard_arrow_right</v-icon>
            </v-row>
            <v-row>
                <div class="col-lg-4 col-xs-12 pl-8">
                    <v-card color="white align-center">
                        <v-row>
                            <v-col cols="12" style="padding-top: 0;">
                                <v-toolbar flat dark>
                                    <v-toolbar-title class="headline font-weight-bold">setting</v-toolbar-title>
                                    <v-spacer></v-spacer>
                                    <v-card-actions>
                                        <v-btn class="primary" v-on:click="modify(settings)">
                                            設定を保存
                                        </v-btn>
                                        <v-btn
                                                v-if="activate===false"
                                                color="orange font-weight-bold"
                                                @click="fetch(settings,videoList)"
                                        >実行
                                        </v-btn>
                                        <v-btn
                                                v-else
                                                color="orange font-weight-bold"
                                                @click="stop_fetch(settings)"
                                        >中止
                                        </v-btn>
                                    </v-card-actions>
                                </v-toolbar>
                            </v-col>
                        </v-row>
                        <v-col>
                            <v-row>
                                <v-col cols="6">
                                    <div class="text-center col-12">最小字幕数</div>
                                </v-col>
                                <v-col cols="6">
                                    <number-input
                                            inline
                                            controls
                                            v-model="settings.minimumSentence"
                                            :min="10"
                                            :max="1000"
                                            :step="1"
                                    ></number-input>
                                </v-col>
                            </v-row>
                            <v-row>
                                <div class="list-view">
                                    <ul v-for="item in videoList" :key="item.id">
                                        <div v-if="item.want" class="row">
                                            <v-checkbox class="mx-1 left" v-model="item.want"></v-checkbox>
                                            <img class="col-4  mx-n5"
                                                 :src="item.videoImg"/>
                                            <div class="col-8">
                                                <div class="d-inline-block text-truncate"
                                                     style="max-width: 100%;">
                                                    {{item.videoTitle}}
                                                </div>
                                                <p class="grey--text">{{item.videoTime}}</p>
                                            </div>
                                        </div>
                                    </ul>
                                </div>
                            </v-row>
                        </v-col>
                    </v-card>
                </div>
                <div class="col-lg-8 col-xs-12 pr-8">
                    <div class="dark_terminal">
                        <virtual-list :size="30" :remain="22" :start="items.length">
                            <ul
                                    class="white--text font-weight-black"
                                    v-for="item in items"
                                    :key="item.id"
                            >-> {{item.text}}
                            </ul>
                        </virtual-list>
                    </div>
                </div>
            </v-row>
        </div>
    </div>
</template>

<script>
    import Vue from "vue";
    import VueNumberInput from "@chenfengyuan/vue-number-input";
    import virtualList from "vue-virtual-scroll-list";
    import {SETTING_OPTIMISTIC, VIDEO_SETTINGS} from '../../graphql/query/query.step1'
    import {CREATE_SETTINGS} from '../../graphql/mutation/mutation.step1'
    import {getCaption} from "../../endpoints";

    Vue.use(VueNumberInput);

    const re = /[a-zA-Z\s]/;
    export const promise = (setting) => new Promise((resolve) => {
        if (setting.authority) {
            Object.keys(setting).forEach(function (prop) {
                if (typeof setting[prop] === "object") {
                    try {
                        setting[prop] = setting[prop].filter(item => item.match(re));
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
        name: "FetchData",
        data: () => ({
            items: [{id: 0, text: "HELLO"}],
            activate: false,
            settings: {},
            videoList: [],
        }),
        components: {
            "virtual-list": virtualList
        },
        apollo: {
            settings: VIDEO_SETTINGS,
            videoList: VIDEO_SETTINGS
        },
        methods: {
            add_form(form) {
                form.push("");
            },
            remove_form(form) {
                form.splice(-1, 1);
            },
            modify(setting) {
                const items = this.$data.items;
                this.$apollo.mutate({
                    mutation: CREATE_SETTINGS,
                    variables: setting,
                    update: (store, {data: {createSettings}}) => {
                        const data = store.readQuery({query: VIDEO_SETTINGS});
                        data.settings = createSettings;
                        store.writeQuery({query: VIDEO_SETTINGS, data})
                    },
                    optimisticResponse: SETTING_OPTIMISTIC
                }).catch(e => {
                    console.log(e);
                    setting.authority = '';
                    items.push({id: items.length, text: 'ERROR while saving❗️'})
                });
                items.push({id: items.length, text: 'settings saved ✅'})
            },
            fetch(setting, videoList) {
                let items = this.items;
                let _this = this;
                socket = new WebSocket(getCaption);
                socket.onmessage = function (e) {
                    items.push({id: items.length, text: e.data});
                };
                socket.onopen = function () {
                    _this.$data.activate = true;
                    const sortedList = videoList.filter(video => video.want)
                    const data = {'videoList': sortedList, 'setting': setting}
                    socket.send(JSON.stringify(data));
                };
                socket.onerror = function () {
                    _this.$data.activate = false;
                };
                socket.onclose = function () {
                    items.push({id: items.length, text: 'connection closed 👋'});
                    _this.$data.activate = false;
                };
            },
            stop_fetch() {
                let items = this.items;
                if (socket && socket.readyState === 1) {
                    items.push({id: items.length, text: 'closing...'});
                    socket.close()
                }
            },
        }
    }
</script>

<style>
    .dark_terminal {
        background: black;
        border-radius: 10px;
    }

    .list-view {
        height: 480px;
        overflow-y: auto;
    }
</style>