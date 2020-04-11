<template>
  <div id="Video">
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
                    <v-btn color="orange font-weight-bold" @click="showCreateDialog">動画追加</v-btn>
                    <v-dialog v-model="dialog" persistent max-width="600px">
                      <v-card>
                        <v-card-title>
                          <span class="headline">動画情報</span>
                        </v-card-title>
                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12">
                                <v-text-field
                                  label="video_href*"
                                  required
                                  v-model="Video.videoHref"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="video_title*"
                                  required
                                  v-model="Video.videoTitle"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field label="video_img*" required v-model="Video.videoImg"></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="vieo_time*"
                                  required
                                  v-model="Video.videoTime"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="2">
                                <v-text-field
                                  label="vieo_genre*"
                                  required
                                  v-model="Video.videoGenre[0]"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="2" v-for="(input, index) in form" :key="index">
                                <v-text-field
                                  label="vieo_genre"
                                  v-model="Video.videoGenre[index +1]"
                                ></v-text-field>
                              </v-col>
                              <v-btn icon bottom color="grey lighten-1" v-on:click="add_form(form)">
                                <v-icon dark>add_circle</v-icon>
                              </v-btn>
                              <v-btn
                                icon
                                bottom
                                color="grey lighten-1"
                                v-on:click="remove_form(form)"
                                v-if="this.form.length>0"
                              >
                                <v-icon dark>remove_circle</v-icon>
                              </v-btn>
                              <v-col cols="12">
                                <v-text-field label="youtubeID*" required v-model="Video.youtubeID"></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-datetime-picker
                                  label="vieo_upload_date*"
                                  v-model="Video.videoUploadDate"
                                  :text-field-props="{prependIcon: 'event'}"
                                ></v-datetime-picker>
                              </v-col>
                            </v-row>
                          </v-container>
                          <small>*indicates required field</small>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                          <v-btn color="blue darken-1" text @click="submit(Video)">Save</v-btn>
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
            <v-col v-for="item in videos" :key="item.id">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="800">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.videoTitle}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>video_href</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.videoHref"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_img</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.videoImg"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_time</h3>
                  <v-text-field
                    class="my-n2 mb-n7 pa-0"
                    v-model="item.videoTime"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>youtubeID</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.youtubeID"></v-text-field>
                </v-col>
                <v-col cols="12">
                  <h3>video_genre</h3>
                  <v-row>
                    <v-col cols="2" v-for="(_,i) in item.videoGenre" :key="i">
                      <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.videoGenre[i]"></v-text-field>
                    </v-col>
                    <v-btn
                      icon
                      bottom
                      color="grey lighten-1"
                      v-on:click="add_form(item.videoGenre)"
                    >
                      <v-icon dark>add_circle</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      bottom
                      color="grey lighten-1"
                      v-on:click="remove_form(item.videoGenre)"
                      v-if="item.videoGenre.length>1"
                    >
                      <v-icon dark>remove_circle</v-icon>
                    </v-btn>
                  </v-row>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_upload_date</h3>
                  <v-datetime-picker
                    v-model="item.videoUploadDate"
                    :text-field-props="{prependIcon:'event'}"
                  ></v-datetime-picker>
                </v-col>
                <v-col cols="12" sm="12">
                  <v-row>
                    <v-btn class="ml-3 primary" v-on:click="modify(item)">修正</v-btn>
                    <v-btn class="ml-4" color="red" v-on:click="showConfirmationDialog(item)">削除</v-btn>
                  </v-row>
                </v-col>
              </v-card>
            </v-col>
            <v-dialog v-model="confirmationDialog" max-width="290">
              <v-card>
                <v-card-title class="headline">{{Video.videoHref}}を削除しますか？</v-card-title>
                <v-card-actions>
                  <v-btn color="green darken-1" text @click="confirmationDialog = false">Disagree</v-btn>
                  <v-btn color="green darken-1" text @click="deleteItem(Video)">Agree</v-btn>
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
import Vue from "vue";
import DatetimePicker from "vuetify-datetime-picker";

Vue.use(DatetimePicker);

const re = /\S+/;
const promise = function(item) {
  return new Promise(function(resolve) {
    Object.keys(item).forEach(function(prop) {
      if (typeof item[prop] === typeof []) {
        try {
          item[prop] = item[prop].filter(item => item.match(re));
        } catch (_) {
          return null;
        }
      }
    });
    resolve(item);
  });
};

export default {
  name: "Video",
  data: () => ({
    screen_name: "video",
    tables: ["word", "video", "caption"],
    dialog: false,
    confirmationDialog: false,
    Video: {
      videoHref: "",
      videoTitle: "",
      videoImg: "",
      videoTime: 0,
      videoGenre: [],
      youtubeID: "",
      videoUploadDate: new Date()
    },
    form: []
  }),
  mounted() {
    this.$store.dispatch("loadVideos");
  },
  computed: {
    ...mapState(["videos"])
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
    submit: function(video) {
      const _this = this;
      promise(video).then(function(video) {
        axios
          .post("/api/videos/", video)
          .then(response => {
            console.log(response);
            _this.$store.dispatch("loadVideos");
            _this.dialog = false;
          })
          .catch(e => {
            console.log(e);
          });
      });
    },
    showCreateDialog: function() {
      this.Video = {
      videoHref: "",
      videoTitle: "",
      videoImg: "",
      videoTime: 0,
      videoGenre: [],
      youtubeID: "",
      videoUploadDate: new Date()
      };
      this.dialog = true;
    },
    showConfirmationDialog: function(item) {
      this.Video = item;
      this.confirmationDialog = true;
    },
    modify: function(video) {
      const _this = this;
      promise(video).then(function(video) {
        axios
          .patch(video.url, video)
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