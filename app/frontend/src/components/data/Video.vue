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
                  <v-dialog v-model="dialog" persistent max-width="600px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="orange font-weight-bold" v-on="on">動画追加</v-btn>
                    </template>
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
                            <v-col cols="12">
                              <v-text-field
                                label="vieo_genre*"
                                required
                                v-model="Video.video_genre"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field label="youtubeID*" required v-model="Video.youtubeID"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-menu
                                ref="menu1"
                                v-model="menu1"
                                :close-on-content-click="false"
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                              >
                              <template v-slot:activator="{ on }">
                                <v-text-field
                                  v-model="dateFormatted"
                                  label="Date"
                                  hint="YYYY/MM/DD format"
                                  persistent-hint
                                  prepend-icon="event"
                                  @blur="date = parseDate(dateFormatted)"
                                  v-on="on"
                                ></v-text-field>
                                </template>
                                <v-date-picker v-model="date" no-title @input="menu1 = false"></v-date-picker>
                              </v-menu>
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
            <v-col v-for="(item, index) in videos" :key="index">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="800">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.video_title}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>video_href</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.video_href"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_img</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.video_img"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_time</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.video_time"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>youtubeID</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.youtubeID"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_update_time</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.video_update_time"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>video_genre</h3>
                  <v-textarea class="my-n2 mb-n7 pa-0" :placeholder="item.video_genre"></v-textarea>
                </v-col>
                <v-row>
                  <v-btn class="ma-4 primary">修正</v-btn>
                  <v-btn class="ma-4 ml-n3" color="red">削除</v-btn>
                </v-row>
              </v-card>
            </v-col>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "Video",
  data: () => ({
    dialog: false,
    Video: {
      video_href: "",
      video_title: "",
      video_img: "",
      video_time: "",
      video_genre: [],
      youtubeID: "",
      video_update_time: new Date()
        .toISOString()
        .split(" ")[0]
        .split("T")[0]
    }
  }),
  mounted() {
    this.$store.dispatch("loadVideos");
  },
  computed: {
    ...mapState(["videos"])
  },
  methods: {
    submit: function() {
      let newVideo = {
        video_href: this.Video.video_href,
        video_title: this.Video.video_title,
        video_img: this.Video.video_img,
        video_time: this.Video.video_time,
        video_genre: this.Video.video_genre,
        youtubeID: this.Video.youtubeID,
        video_update_time: this.Video.video_update_time
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
    }
  }
};
</script>