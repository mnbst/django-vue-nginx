<template>
  <div id="Video">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-card-title class="headline font-weight-bold mx-auto">video</v-card-title>
            <v-col v-for="(item, index) in video" :key="index">
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

export default {
  name: "Video",
  mounted() {
    this.$store.dispatch("loadVideos");
  },
  computed: {
    ...mapState(["video"])
  }
};
</script>