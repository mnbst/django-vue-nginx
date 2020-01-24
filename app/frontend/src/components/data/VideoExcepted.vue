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
                                  v-model="VideoExcepted.video_href"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="video_title"
                                  required
                                  v-model="VideoExcepted.video_title"
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="video_img"
                                  required
                                  v-model="VideoExcepted.video_img"
                                ></v-text-field>
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
                  <v-col cols="2">
                    <v-spacer></v-spacer>
                  </v-col>
                </v-toolbar>
              </v-col>
            </v-row>
            <v-col v-for="item in video_excepted" :key="item.id">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="400">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.video_href}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>video_href</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_href"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_title</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_title"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_img</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.video_img"></v-text-field>
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
                <v-card-title class="headline">{{VideoExcepted.video_href}}を削除しますか？</v-card-title>
                <v-card-actions>
                  <v-btn color="green darken-1" text @click="confirmationDialog = false">Disagree</v-btn>
                  <v-btn color="green darken-1" text @click="deleteItem(VideoExcepted)">Agree</v-btn>
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
  name: "VideoExcepted",
  data: () => ({
    screen_name: "video_excepted",
    tables: ["word", "video", "caption", "video_excepted"],
    dialog: false,
    confirmationDialog: false,
    VideoExcepted: {
      video_href: "",
      video_title: "",
      video_img: ""
    },
    form: []
  }),
  mounted() {
    this.$store.dispatch("loadVideosExcepted");
  },
  computed: {
    ...mapState(["video_excepted"])
  },
  methods: {
    changeRoute(a) {
      this.$router.push({ path: "/data/" + a });
    },
    add_form() {
      this.form.push({
        one: ""
      });
    },
    remove_form(index) {
      this.form.splice(index, 1);
    },
    submit: function() {
      let newVideoExcepted = {
        video_href: this.VideoExcepted.video_href,
        video_title: this.VideoExcepted.video_title,
        video_img: this.VideoExcepted.video_img
      };
      console.log(newVideoExcepted);
      axios
        .post("/api/video_excepted/", newVideoExcepted)
        .then(response => {
          this.$store.dispatch("loadVideosExcepted");
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
      this.VideoExcepted = {
        video_href: "",
        video_title: "",
        video_img: ""
      };
      this.dialog = true;
    },
    showConfirmationDialog: function(item) {
      this.VideoExcepted = item;
      this.confirmationDialog = true;
    },
    modify: function(item) {
      axios
        .patch(item.url, item)
        .then(response => {
          this.$store.dispatch("loadVideosExcepted");
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
          this.$store.dispatch("loadVideosExcepted");
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