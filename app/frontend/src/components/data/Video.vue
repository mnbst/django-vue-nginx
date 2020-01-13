<template>
  <div id="Video">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-row>
              <v-col cols="12">
                <v-card-title class="justify-center">
                  <p class="headline font-weight-bold">video</p>
                </v-card-title>
                <v-card-actions class="justify-center">
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
                              <v-text-field label="video_href*" required v-model="Video.video_href"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field
                                label="video_title*"
                                required
                                v-model="Video.video_title"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field label="video_img*" required v-model="Video.video_img"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field label="vieo_time*" required v-model="Video.video_time"></v-text-field>
                            </v-col>
                            <v-col cols="2">
                              <v-text-field
                                label="vieo_genre*"
                                required
                                v-model="Video.video_genre[0]"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="2" v-for="(input, index) in form" :key="index">
                              <v-text-field
                                label="vieo_genre"
                                v-model="Video.video_genre[index +1]"
                              ></v-text-field>
                            </v-col>
                            <v-btn icon bottom color="grey lighten-1" v-on:click="add_form">
                              <v-icon dark>add_circle</v-icon>
                            </v-btn>
                            <v-btn
                              icon
                              bottom
                              color="grey lighten-1"
                              v-on:click="remove_form"
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
                                v-model="Video.video_upload_date"
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
                        <v-btn color="blue darken-1" text @click="submit">Save</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-card-actions>
              </v-col>
            </v-row>
            <v-col v-for="item in videos" :key="item.id">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="800">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.video_title}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>video_href</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_href"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_img</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_img"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_time</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_time"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>youtubeID</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.youtubeID"></v-text-field>
                </v-col>
                <v-col cols="12">
                  <h3>video_genre</h3>
                  <v-row>
                    <v-col cols="2" v-for="(_,i) in item.video_genre" :key="i">
                      <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_genre[i]"></v-text-field>
                    </v-col>
                    <v-btn icon bottom color="grey lighten-1" v-on:click="add_modify_form(item)">
                      <v-icon dark>add_circle</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      bottom
                      color="grey lighten-1"
                      v-on:click="remove_modify_form(item)"
                      v-if="item.video_genre.length>1"
                    >
                      <v-icon dark>remove_circle</v-icon>
                    </v-btn>
                  </v-row>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_upload_date</h3>
                  <v-datetime-picker
                    v-model="item.video_upload_date"
                    :text-field-props="{prependIcon:'event'}"
                  ></v-datetime-picker>
                </v-col>
                <v-col cols="12" sm="12">
                  <v-row>
                    <v-btn class="ml-4 primary" v-on:click="modify(item)">修正</v-btn>
                    <v-btn class="ml-4 error" v-on:click="showConfirmationDialog(item)">削除</v-btn>
                  </v-row>
                </v-col>
              </v-card>
            </v-col>
            <v-dialog v-model="confirmationDialog" max-width="290">
              <v-card>
                <v-card-title class="headline">{{Video.video_href}}を削除しますか？</v-card-title>
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

export default {
  name: "Video",
  data: () => ({
    dialog: false,
    confirmationDialog: false,
    Video: {
      video_href: "",
      video_title: "",
      video_img: "",
      video_time: "",
      video_genre: [],
      youtubeID: "",
      video_upload_date: new Date()
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
    add_form() {
      this.form.push({
        one: ""
      });
    },
    remove_form(index) {
      this.form.splice(index, 1);
    },
    submit: function() {
      let newVideo = {
        video_href: this.Video.video_href,
        video_title: this.Video.video_title,
        video_img: this.Video.video_img,
        video_time: this.Video.video_time,
        video_genre: this.Video.video_genre,
        youtubeID: this.Video.youtubeID,
        video_upload_date: this.Video.video_upload_date
      };
      console.log(newVideo);
      axios
        .post("/api/videos/", newVideo)
        .then(response => {
          this.$store.dispatch("loadVideos");
          console.log(response);
          this.dialog = false;
        })
        .catch(e => {
          console.log(e);
        });
    },
    add_modify_form: function(item) {
      item.video_genre.push("");
    },
    remove_modify_form: function(item) {
      item.video_genre.splice(-1, 1);
    },
    showCreateDialog: function() {
      this.Video = {
        video_href: "",
        video_title: "",
        video_img: "",
        video_time: "",
        video_genre: [],
        youtubeID: "",
        video_upload_date: new Date()
      };
      this.dialog = true;
    },
    showConfirmationDialog: function(item) {
      this.Video = item;
      this.confirmationDialog = true;
    },
    modify: function(item) {
      axios
        .patch(item.url, item)
        .then(response => {
          this.$store.dispatch("loadVideos");
          console.log(response);
          this.dialog = false;
        })
        .catch(e => {
          console.log(e);
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