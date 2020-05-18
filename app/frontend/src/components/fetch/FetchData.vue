<template>
    <div id="FetchData" class="mt-5">
        <div class="container--fluid">
            <v-row justify="center">
                <v-icon class="mr-1">keyboard_arrow_left</v-icon>
                <h2 class="my-2">字幕生成</h2>
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
                                                @click="fetch(settings)"
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
                                <v-col cols="2">
                                    <p class="text-center">クロールするページ数</p>
                                </v-col>
                                <v-col cols="2">
                                    <number-input
                                            inline
                                            controls
                                            v-model="settings.pageToCrawl"
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
                                            v-model="settings.languageLimit"
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
                                            v-model="settings.minimumSentence"
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
                                            v-model="settings.videoPerPage"
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
                                        v-on:click="add_form(settings.videoToDelete)"
                                >
                                    <v-icon dark>add_circle</v-icon>
                                </v-btn>
                                <v-btn
                                        icon
                                        top
                                        color="grey lighten-1"
                                        v-on:click="remove_form(settings.videoToDelete)"
                                        v-if="settings.videoToDelete && settings.videoToDelete.length>0"
                                >
                                    <v-icon dark>remove_circle</v-icon>
                                </v-btn>
                                <v-col cols="2" v-for="(_,index_of_delete) in settings.videoToDelete"
                                       :key="index_of_delete">
                                    <v-text-field
                                            class="my-n2 mb-n7 pa-0"
                                            v-model="settings.videoToDelete[index_of_delete]"
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
                                        v-on:click="add_form(settings.videoToRenewal)"
                                >
                                    <v-icon dark>add_circle</v-icon>
                                </v-btn>
                                <v-btn
                                        icon
                                        top
                                        color="grey lighten-1"
                                        v-on:click="remove_form(settings.videoToRenewal)"
                                        v-if="settings.videoToRenewal && settings.videoToRenewal.length>0"
                                >
                                    <v-icon dark>remove_circle</v-icon>
                                </v-btn>
                                <v-col cols="2" v-for="(_,index_of_renewal) in settings.videoToRenewal"
                                       :key="index_of_renewal">
                                    <v-text-field
                                            class="my-n2 mb-n7 pa-0"
                                            v-model="settings.videoToRenewal[index_of_renewal]"
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
                                        v-on:click="add_form(settings.exceptedHref)"
                                >
                                    <v-icon dark>add_circle</v-icon>
                                </v-btn>
                                <v-btn
                                        icon
                                        top
                                        color="grey lighten-1"
                                        v-on:click="remove_form(settings.exceptedHref)"
                                        v-if="settings.exceptedHref && settings.exceptedHref.length>0"
                                >
                                    <v-icon dark>remove_circle</v-icon>
                                </v-btn>
                                <v-col cols="2" v-for="(href,index_of_excepted) in settings.exceptedHref"
                                       :key="index_of_excepted">
                                    <v-text-field class="my-n2 mb-n7 pa-0"
                                                  v-model="settings.exceptedHref[index_of_excepted]"></v-text-field>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-card>
                </div>
                <div class="col-lg-8 col-xs-12 pr-8">
                    <div class="dark_terminal">
                        <virtual-list :size="30" :remain="20" :start="items.length">
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
    import {SETTING_OPTIMISTIC, SETTINGS} from '../../graphql/query/query.step1'
    import {CREATE_SETTINGS} from '../../graphql/mutation/mutation.step1'

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
            items: [{id: 0, text: "HELLO"}],
            activate: false,
            settings: {},
        }),
        components: {
            "virtual-list": virtualList
        },
        apollo: {
            settings: SETTINGS
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
                promise(setting)
                    .then(setting => {
                        this.$apollo.mutate({
                            mutation: CREATE_SETTINGS,
                            variables: setting,
                            update: (store, {data: {createSettings}}) => {
                                const data = store.readQuery({query: SETTINGS});
                                data.settings = createSettings;
                                store.writeQuery({query: SETTINGS, data})
                            },
                            optimisticResponse: SETTING_OPTIMISTIC
                        });
                        items.push({id: items.length, text: 'settings saved ✅'})
                    })
                    .catch(e => {
                        console.log(e);
                        setting.authority = '';
                        items.push({id: items.length, text: 'ERROR while saving❗️'})
                    });
            },
            fetch(setting) {
                let items = this.items;
                let _this = this;
                socket = new WebSocket(endpoint);
                socket.onmessage = function (e) {
                    items.push({id: items.length, text: e.data});
                };
                socket.onopen = function () {
                    _this.$data.activate = true;
                    socket.send(JSON.stringify(setting));
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
    };
</script>

<style>
    .dark_terminal {
        background: black;
        border-radius: 10px;
    }
</style>