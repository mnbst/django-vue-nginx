<template>
    <div id="Word">
        <v-container>
            <v-row dense>
                <v-col cols="12">
                    <v-card color="white align-center">
                        <v-row>
                            <v-col cols="12" style="padding-top: 0px;">
                                <v-toolbar flat dark>
                                    <v-col cols="2">
                                        <v-spacer></v-spacer>
                                    </v-col>
                                    <v-row>
                                        <v-toolbar-title class="headline font-weight-bold">
                                            <v-col cols="12">
                                                <v-row style="padding-top: 24px;">
                                                    <h3>table:</h3>
                                                    <v-select v-model="screen_name" :items="tables"
                                                              v-on:change="changeRoute"></v-select>
                                                </v-row>
                                            </v-col>
                                        </v-toolbar-title>
                                    </v-row>
                                    <v-spacer></v-spacer>
                                    <v-card-actions>
                                        <v-btn color="orange font-weight-bold" @click="showCreateDialog">単語追加</v-btn>
                                        <v-dialog v-model="dialog" persistent max-width="600">
                                            <v-card>
                                                <v-card-title>
                                                    <span class="headline">単語情報</span>
                                                </v-card-title>
                                                <v-card-text>
                                                    <v-container>
                                                        <v-row>
                                                            <v-col cols="12">
                                                                <v-text-field label="word_ini*" required
                                                                              v-model="Word.wordIni"></v-text-field>
                                                            </v-col>
                                                            <v-col cols="12">
                                                                <v-text-field label="word*" required
                                                                              v-model="Word.word"></v-text-field>
                                                            </v-col>
                                                            <v-col cols="12">
                                                                <v-text-field label="meaning*" required
                                                                              v-model="Word.meaning"></v-text-field>
                                                            </v-col>
                                                        </v-row>
                                                    </v-container>
                                                    <small>*indicates required field</small>
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn color="blue darken-1" text @click="dialog = false">Close
                                                    </v-btn>
                                                    <v-btn color="blue darken-1" text @click="add">Save</v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>
                                    </v-card-actions>
                                    <v-col cols="2">
                                        <v-spacer></v-spacer>
                                    </v-col>
                                </v-toolbar>
                            </v-col>
                        </v-row>
                        <virtual-list :size="100" :remain="50">
                            <v-col v-for="item in words" :key="item.id">
                                <v-card class="mx-auto d-flex flex-wrap align-center" max-width="400">
                                    <v-card-title class="headline font-weight-bold mx-auto">{{item.word}}</v-card-title>
                                    <v-col cols="12" sm="12">
                                        <h3>word_ini</h3>
                                        <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.wordIni"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="12">
                                        <h3>word</h3>
                                        <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.word"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="12">
                                        <h3>meaning</h3>
                                        <v-textarea class="my-n2 mb-n7 pa-0" v-model="item.meaning"></v-textarea>
                                    </v-col>
                                    <v-row>
                                        <v-btn class="ma-4 primary" @click="modify(item)">修正</v-btn>
                                        <v-btn
                                                class="ma-4 ml-n3"
                                                color="red"
                                                @click.stop="showConfirmationDialog(item)"
                                        >削除
                                        </v-btn>
                                    </v-row>
                                </v-card>
                            </v-col>
                        </virtual-list>
                        <v-dialog v-model="confirmationDialog" max-width="290">
                            <v-card>
                                <v-card-title class="headline">{{Word.word}}を削除しますか？</v-card-title>
                                <v-card-actions>
                                    <v-btn color="green darken-1" text @click="confirmationDialog = false">Disagree
                                    </v-btn>
                                    <v-btn color="green darken-1" text @click="deleteItem(Word)">Agree</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import VirtualList from "vue-virtual-scroll-list";

    export default {
        name: "Word",
        data: () => ({
            screen_name: "word",
            tables: ["word", "video", "caption"],
            dialog: false,
            confirmationDialog: false,
            Word: {
                wordIni: "",
                word: "",
                meaning: ""
            }
        }),
        components: {
            "virtual-list": VirtualList
        },
        mounted() {
            this.$store.dispatch("loadWords");
        },
        computed: {
            ...mapState(["words"])
        },
        methods: {
            changeRoute(a) {
                this.$router.push({path: "/data/" + a});
            },
            showCreateDialog: function () {
                this.Word = {
                    wordIni: "",
                    word: "",
                    meaning: ""
                };
                this.dialog = true;
            },
            showConfirmationDialog: function (item) {
                this.Word = item;
                this.confirmationDialog = true;
            },
            add: function () {
                // let word = this.Word;
                // axios
                //     .post("/graphql", {
                //         mutation: `mutation{
                //     createWord(input:{wordIni:` + word + `})
                //             {id,wordIni,word,meaning}}`
                //     })
                //     .then(response => {
                //         this.$store.dispatch("loadWords");
                //         console.log(response);
                //         this.dialog = false;
                //     })
                //     .catch(e => {
                //         console.log(e);
                //     });
            },
            modify: function (item) {
                console.log(item)
                // axios
                //     .post("/graphql", {
                //         mutation: `mutation{
                //             createWord(input:{id:` + item.id +
                //             `wordIni:` + item.wordIni +
                //             `, word:` + item.word +
                //             `, meaning:` + item.meaning + `})
                //             {id,wordIni,word,meaning}}`
                //     })
                //     .then(response => {
                //         this.$store.dispatch("loadWords");
                //         console.log(response);
                //         this.dialog = false;
                //     })
                //     .catch(e => {
                //         console.log(e);
                //     });
            },
            // deleteItem: function (item) {
            //     // axios
            //     //     .delete(item.url, item)
            //     //     .then(response => {
            //     //         this.$store.dispatch("loadWords");
            //     //         console.log(response);
            //     //         this.confirmationDialog = false;
            //     //     })
            //     //     .catch(e => {
            //     //         console.log(e);
            //     //     });
            // }
        }
    };
</script>

<style>
    .custom-placeholer-color input::placeholder {
        color: black !important;
        opacity: 1;
    }
</style>