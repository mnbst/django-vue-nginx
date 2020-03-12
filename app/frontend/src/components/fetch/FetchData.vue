<template>
    <div id="FetchData">
        <v-container>
            <v-col cols="12">
                <h2>fetch data</h2>
                <div class="dark_terminal">
                    <virtual-list :size="30" :remain="10" :start="items.length">
                        <ul
                                class="white--text font-weight-black"
                                v-for="item in items"
                                :key="item.id"
                        >-> {{item}}
                        </ul>
                    </virtual-list>
                </div>
            </v-col>
            <v-col cols="12">
                <v-card color="white align-center">
                    <v-row>
                        <v-col cols="12" style="padding-top: 0;">
                            <v-toolbar flat dark>
                                <v-toolbar-title class="headline font-weight-bold">setting</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-card-actions>
                                    <v-btn v-if="activate===false" class="primary" v-on:click="modify(fetch_setting)">
                                        設定を保存
                                    </v-btn>
                                    <v-btn
                                            v-if="activate===false"
                                            color="orange font-weight-bold"
                                            @click="fetch(fetch_setting)"
                                    >実行
                                    </v-btn>
                                    <v-btn
                                            v-else
                                            color="orange font-weight-bold"
                                            @click="stop_fetch(fetch_setting)"
                                    >中止
                                    </v-btn>
                                </v-card-actions>
                            </v-toolbar>
                        </v-col>
                    </v-row>
                    <v-col>
                        <v-row>
                            <v-col cols="2">
                                <p class="text-center">クロールするページ数</p>
                            </v-col>
                            <v-col cols="2">
                                <number-input
                                        inline
                                        controls
                                        v-model="fetch_setting.page_to_crawl"
                                        :min="1"
                                        :max="10"
                                        :step="1"
                                ></number-input>
                            </v-col>
                            <v-col cols="2">
                                <p class="text-center">字幕言語数</p>
                            </v-col>
                            <v-col cols="2">
                                <number-input
                                        inline
                                        controls
                                        v-model="fetch_setting.language_limit"
                                        :min="1"
                                        :max="5"
                                        :step="1"
                                ></number-input>
                            </v-col>
                            <v-col cols="2">
                                <p class="text-center">最小字幕数</p>
                            </v-col>
                            <v-col cols="2">
                                <number-input
                                        inline
                                        controls
                                        v-model="fetch_setting.minimum_sentence"
                                        :min="10"
                                        :max="1000"
                                        :step="1"
                                ></number-input>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <p class="text-center">ページ毎の取得動画数</p>
                            </v-col>
                            <v-col cols="2">
                                <number-input
                                        inline
                                        controls
                                        v-model="fetch_setting.video_per_page"
                                        :min="1"
                                        :max="50"
                                        :step="1"
                                ></number-input>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <p class="text-center">削除動画id</p>
                            </v-col>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="add_form(fetch_setting.video_to_delete)"
                            >
                                <v-icon dark>add_circle</v-icon>
                            </v-btn>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="remove_form(fetch_setting.video_to_delete)"
                                    v-if="fetch_setting.video_to_delete && fetch_setting.video_to_delete.length>0"
                            >
                                <v-icon dark>remove_circle</v-icon>
                            </v-btn>
                            <v-col cols="2" v-for="(_,index_of_delete) in fetch_setting.video_to_delete"
                                   :key="index_of_delete">
                                <v-text-field
                                        class="my-n2 mb-n7 pa-0"
                                        v-model="fetch_setting.video_to_delete[index_of_delete]"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <p class="text-center">再取得動画id</p>
                            </v-col>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="add_form(fetch_setting.video_to_renewal)"
                            >
                                <v-icon dark>add_circle</v-icon>
                            </v-btn>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="remove_form(fetch_setting.video_to_renewal)"
                                    v-if="fetch_setting.video_to_renewal && fetch_setting.video_to_renewal.length>0"
                            >
                                <v-icon dark>remove_circle</v-icon>
                            </v-btn>
                            <v-col cols="2" v-for="(_,index_of_renewal) in fetch_setting.video_to_renewal"
                                   :key="index_of_renewal">
                                <v-text-field
                                        class="my-n2 mb-n7 pa-0"
                                        v-model="fetch_setting.video_to_renewal[index_of_renewal]"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <p class="text-center">除外動画id</p>
                            </v-col>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="add_form(fetch_setting.excepted_href)"
                            >
                                <v-icon dark>add_circle</v-icon>
                            </v-btn>
                            <v-btn
                                    icon
                                    top
                                    color="grey lighten-1"
                                    v-on:click="remove_form(fetch_setting.excepted_href)"
                                    v-if="fetch_setting.excepted_href && fetch_setting.excepted_href.length>0"
                            >
                                <v-icon dark>remove_circle</v-icon>
                            </v-btn>
                            <v-col cols="2" v-for="(_,index_of_excepted) in fetch_setting.excepted_href"
                                   :key="index_of_excepted">
                                <v-text-field class="my-n2 mb-n7 pa-0"
                                              v-model="fetch_setting.excepted_href[index_of_excepted]"></v-text-field>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-card>
            </v-col>
        </v-container>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import Vue from "vue";
    import VueNumberInput from "@chenfengyuan/vue-number-input";
    import axios from "axios";
    import virtualList from "vue-virtual-scroll-list";

    Vue.use(VueNumberInput);
    const re = /[a-zA-Z\s]/;
    const promise = (settings) => new Promise((resolve) => {
        Object.keys(settings).forEach(function (prop) {
            if (typeof settings[prop] === "object") {
                try {
                    settings[prop] = settings[prop].filter(item => item.match(re));
                } catch (_) {
                    return null;
                }
            }
        });
        resolve(settings);
    });
    const loc = window.location;
    let wsStart = "ws://";
    if (loc.protocol === "https:") {
        wsStart = "wss://";
    }
    const endpoint = wsStart + loc.host + loc.pathname + "realtime";
    let socket = null;

    export default {
        name: "FetchData",
        data: () => ({
            items: ["HELLO"],
            activate: false,
        }),
        components: {
            "virtual-list": virtualList
        },
        mounted() {
            this.$store.dispatch("loadFetchSetting");
        },
        computed: {
            ...mapState(["fetch_setting"])
        },
        methods: {
            add_form(form) {
                form.push("");
            },
            remove_form(form) {
                form.splice(-1, 1);
            },
            modify(setting) {
                promise(setting).then((setting) => {
                    axios
                        .patch(setting.url, setting)
                        .then(response => {
                            console.log(response);
                            this.$data.items.push('settings saved ✅')
                        })
                        .catch(e => {
                            console.log(e);
                            this.$data.items.push('ERROR while saving')
                        });
                });
            },
            fetch(setting) {
                let _this = this;
                socket = new WebSocket(endpoint);
                socket.onmessage = function (e) {
                    _this.$data.items.push(e.data);
                };
                socket.onopen = function () {
                    _this.$data.activate = true;
                    socket.send(JSON.stringify(setting));
                };
                socket.onerror = function () {
                    _this.$data.activate = false;
                };
                socket.onclose = function () {
                    _this.$data.items.push('connection closed 👋');
                    _this.$data.activate = false;
                };
            },
            stop_fetch() {
                let _this = this;
                if (socket && socket.readyState === 1) {
                    _this.$data.items.push('closing...');
                    socket.close()
                }
            },
        }
    };
</script>

<style>
    .dark_terminal {
        background: black;
        border-radius: 10px;
    }
</style>