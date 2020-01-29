<template>
  <div id="Caption">
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
                          <v-select v-model="screen_name" :items="tables" v-on:change="changeRoute"></v-select>
                        </v-row>
                      </v-col>
                    </v-toolbar-title>
                  </v-row>
                  <v-spacer></v-spacer>
                  <v-card-actions>
                    <v-btn color="orange font-weight-bold" @click="showCreateDialog">字幕追加</v-btn>
                    <v-dialog v-model="dialog" persistent max-width="600px">
                      <v-card>
                        <v-card-title>
                          <span class="headline">字幕情報</span>
                        </v-card-title>
                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12">
                                <v-text-field
                                  label="video_href*"
                                  required
                                  v-model="Caption.video_href"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="index*"
                                  min="0"
                                  step="1"
                                  type="number"
                                  required
                                  v-model="Caption.index"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="start_time*"
                                  min="0"
                                  step="1"
                                  type="number"
                                  required
                                  v-model="Caption.start_time"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="end_time*"
                                  min="0"
                                  step="1"
                                  type="number"
                                  required
                                  v-model="Caption.end_time"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-textarea label="text*" required v-model="Caption.text"></v-textarea>
                              </v-col>
                              <v-col cols="12">
                                <v-row>
                                  <v-col cols="2">
                                    <v-text-field label="word*" required v-model="Caption.word[0]"></v-text-field>
                                  </v-col>
                                  <v-col cols="2" v-for="(input, index) in form1" :key="index">
                                    <v-text-field label="word" v-model="Caption.word[index +1]"></v-text-field>
                                  </v-col>
                                  <v-btn
                                    icon
                                    bottom
                                    color="grey lighten-1"
                                    v-on:click="add_form(form1)"
                                  >
                                    <v-icon dark>add_circle</v-icon>
                                  </v-btn>
                                  <v-btn
                                    icon
                                    bottom
                                    color="grey lighten-1"
                                    v-on:click="remove_form(form1)"
                                    v-if="this.form1.length>0"
                                  >
                                    <v-icon dark>remove_circle</v-icon>
                                  </v-btn>
                                </v-row>
                              </v-col>
                              <v-col cols="12">
                                <v-row>
                                  <v-col cols="2">
                                    <v-text-field
                                      label="word_imi*"
                                      required
                                      v-model="Caption.word_imi[0]"
                                    ></v-text-field>
                                  </v-col>
                                  <v-col cols="2" v-for="(input, index) in form2" :key="index">
                                    <v-text-field
                                      label="word_imi"
                                      v-model="Caption.word_imi[index +1]"
                                    ></v-text-field>
                                  </v-col>
                                  <v-btn
                                    icon
                                    bottom
                                    color="grey lighten-1"
                                    v-on:click="add_form(form2)"
                                  >
                                    <v-icon dark>add_circle</v-icon>
                                  </v-btn>
                                  <v-btn
                                    icon
                                    bottom
                                    color="grey lighten-1"
                                    v-on:click="remove_form(form2)"
                                    v-if="this.form2.length>0"
                                  >
                                    <v-icon dark>remove_circle</v-icon>
                                  </v-btn>
                                </v-row>
                              </v-col>
                            </v-row>
                          </v-container>
                          <small>*indicates required field</small>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                          <v-btn color="blue darken-1" text @click="submit(Caption)">Save</v-btn>
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
            <v-col v-for="(item, i) in captions" :key="i">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="800">
                <v-card-title
                  class="headline font-weight-bold mx-auto"
                >{{item.video_href}}-{{item.index}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>video_href</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_href"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>index</h3>
                  <v-text-field
                    class="my-n2 mb-n7 pa-0"
                    min="0"
                    step="1"
                    type="number"
                    v-model="item.index"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>text</h3>
                  <v-textarea class="my-n2 mb-n7 pa-0" v-model="item.text"></v-textarea>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>start_time</h3>
                  <v-text-field
                    class="my-n2 mb-n7 pa-0"
                    min="0"
                    step="1"
                    type="number"
                    v-model="item.start_time"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>end_time</h3>
                  <v-text-field
                    class="my-n2 mb-n7 pa-0"
                    min="0"
                    step="1"
                    type="number"
                    v-model="item.end_time"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>text_tokenized</h3>
                  <v-layout row wrap>
                    <v-col cols="6">
                      <h4>word</h4>
                      <v-flex v-for="(_,word_index) in item.word" :key="word_index">
                        <v-text-field class="my-n2 mb-n7 pa-3" v-model="item.word[word_index]"></v-text-field>
                      </v-flex>
                      <v-btn icon bottom color="grey lighten-1" v-on:click="add_form(item.word)">
                        <v-icon dark>add_circle</v-icon>
                      </v-btn>
                      <v-btn
                        icon
                        bottom
                        color="grey lighten-1"
                        v-on:click="remove_form(item.word)"
                        v-if="item.word.length>1"
                      >
                        <v-icon dark>remove_circle</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col cols="6">
                      <h4>word_imi</h4>
                      <v-flex v-for="(_,word_imi_index) in item.word_imi" :key="word_imi_index">
                        <v-text-field
                          class="my-n2 mb-n7 pa-3"
                          v-model="item.word_imi[word_imi_index]"
                        ></v-text-field>
                      </v-flex>
                      <v-btn
                        icon
                        bottom
                        color="grey lighten-1"
                        v-on:click="add_form(item.word_imi)"
                      >
                        <v-icon dark>add_circle</v-icon>
                      </v-btn>
                      <v-btn
                        icon
                        bottom
                        color="grey lighten-1"
                        v-on:click="remove_form(item.word_imi)"
                        v-if="item.word_imi.length>0"
                      >
                        <v-icon dark>remove_circle</v-icon>
                      </v-btn>
                    </v-col>
                  </v-layout>
                </v-col>
                <v-row>
                  <v-btn class="ml-5 mb-4 primary" v-on:click="modify(item)">修正</v-btn>
                  <v-btn class="ml-4 mb-4" color="red" v-on:click="showConfirmationDialog(item)">削除</v-btn>
                </v-row>
              </v-card>
            </v-col>
            <v-dialog v-model="confirmationDialog" max-width="290">
              <v-card>
                <v-card-title class="headline">{{Caption.video_href}}を削除しますか？</v-card-title>
                <v-card-actions>
                  <v-btn color="green darken-1" text @click="confirmationDialog = false">Disagree</v-btn>
                  <v-btn color="green darken-1" text @click="deleteItem(Caption)">Agree</v-btn>
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
import { mapState } from "vuex";
import axios from "axios";

const re = /\S+/;
const promise = function(item) {
  return new Promise(function(resolve) {
    Object.keys(item).forEach(function(prop) {
      if (typeof item[prop] == typeof []) {
        try {
          item[prop] = item[prop].filter(item => item.match(re));
        } catch (_) {
          return;
        }
      }
    });
    resolve(item);
  });
};

export default {
  name: "Caption",
  data: () => ({
    screen_name: "caption",
    tables: ["word", "video", "caption"],
    dialog: false,
    confirmationDialog: false,
    Caption: {
      video_href: "",
      index: "",
      start_time: "",
      end_time: "",
      text: "",
      word: [],
      word_imi: []
    },
    form1: [],
    form2: []
  }),
  mounted() {
    this.$store.dispatch("loadCaptions");
  },
  computed: {
    ...mapState(["captions"])
  },
  methods: {
    changeRoute(a) {
      this.$router.push({ path: "/data/" + a });
    },
    add_form(form) {
      form.push("");
    },
    remove_form(form) {
      form.splice(-1, 1);
    },
    submit: function(caption) {
      const _this = this;
      promise(caption).then(function(caption) {
        axios
          .post("/api/captions/", caption)
          .then(response => {
            _this.$store.dispatch("loadCaptions");
            console.log(response);
            _this.dialog = false;
          })
          .catch(e => {
            console.log(e);
          });
      });
    },
    showCreateDialog: function() {
      this.Caption = {
        video_href: "",
        index: "",
        start_time: "",
        end_time: "",
        text: "",
        word: [],
        word_imi: []
      };
      this.dialog = true;
    },
    showConfirmationDialog: function(item) {
      this.Caption = item;
      this.confirmationDialog = true;
    },
    modify: function(caption) {
      const _this = this;
      promise(caption).then(function(caption) {
        axios
          .patch(caption.url, caption)
          .then(response => {
            console.log(response);
            _this.dialog = false;
          })
          .catch(e => {
            console.log(e);
          });
      });
    },
    deleteItem: function(item) {
      axios
        .delete(item.url, item)
        .then(response => {
          this.$store.dispatch("loadVideos");
          console.log(response);
          this.confirmationDialog = false;
        })
        .catch(e => {
          console.log(e);
        });
    }
  }
};
</script>