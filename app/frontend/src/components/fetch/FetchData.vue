<template>
  <div id="FetchData">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <VueTerminal
            :intro="intro"
            console-sign=">>"
            allow-arbitrary
            height="300px"
            @command="onCliCommand"
          ></VueTerminal>
        </v-col>
      </v-row>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-row>
              <v-col cols="12" style="padding-top: 0px;">
                <v-toolbar flat dark>
                  <v-toolbar-title class="headline font-weight-bold">setting</v-toolbar-title>
                </v-toolbar>
              </v-col>
            </v-row>
            <v-col>
              <v-row>
                <v-col cols="2">
                  <p class="text-center">クロールするページ数</p>
                </v-col>
                <v-col cols="2">
                  <number-input inline controls v-model="pages" :min="1" :max="10" :step="1"></number-input>
                </v-col>
                <v-col cols="2">
                  <p class="text-center">字幕言語数</p>
                </v-col>
                <v-col cols="2">
                  <number-input inline controls v-model="languages" :min="1" :max="5" :step="1"></number-input>
                </v-col>
                <v-col cols="2">
                  <p class="text-center">最小字幕数</p>
                </v-col>
                <v-col cols="2">
                  <number-input inline controls v-model="captions" :min="10" :max="1000" :step="1"></number-input>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="2">
                  <p class="text-center">削除動画id</p>
                </v-col>
                <v-col cols="2">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-col cols="2" v-for="(input, index) in delete_list" :key="index">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-btn icon top color="grey lighten-1" v-on:click="add_form(delete_list)">
                  <v-icon dark>add_circle</v-icon>
                </v-btn>
                <v-btn
                  icon
                  top
                  color="grey lighten-1"
                  v-on:click="remove_form(delete_list)"
                  v-if="this.delete_list.length>0"
                >
                  <v-icon dark>remove_circle</v-icon>
                </v-btn>
              </v-row>
              <v-row>
                <v-col cols="2">
                  <p class="text-center">再取得動画id</p>
                </v-col>
                <v-col cols="2">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-col cols="2" v-for="(_, index) in renewal" :key="index">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-btn icon top color="grey lighten-1" v-on:click="add_form(renewal)">
                  <v-icon dark>add_circle</v-icon>
                </v-btn>
                <v-btn
                  icon
                  top
                  color="grey lighten-1"
                  v-on:click="remove_form(renewal)"
                  v-if="this.renewal.length>0"
                >
                  <v-icon dark>remove_circle</v-icon>
                </v-btn>
              </v-row>
              <v-row>
                <v-col cols="2">
                  <p class="text-center">除外動画id</p>
                </v-col>
                <v-col cols="2" v-for="(_,i) in video_excepted" :key="i">
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="video_excepted[i]"></v-text-field>
                </v-col>
                <v-btn icon top color="grey lighten-1" v-on:click="add_form(video_excepted)">
                  <v-icon dark>add_circle</v-icon>
                </v-btn>
                <v-btn
                  icon
                  top
                  color="grey lighten-1"
                  v-on:click="remove_form(video_excepted)"
                  v-if="this.video_excepted.length>0"
                >
                  <v-icon dark>remove_circle</v-icon>
                </v-btn>
              </v-row>
            </v-col>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
   
<script>
import { mapState } from "vuex";
import Vue from "vue";
import VueNumberInput from "@chenfengyuan/vue-number-input";
import VueTerminal from "vue-terminal-ui";

Vue.use(VueNumberInput);

export default {
  name: "FetchData",
  components: {
    VueTerminal
  },
  data() {
    return {
      pages: 1,
      languages: 1,
      captions: 10,
      video_id: "video_id",
      delete_list: [],
      renewal: [],
      VideoExcepted: {
        video_href: "",
        video_title: "",
        video_img: ""
      },
      intro: "terminal"
    };
  },
  mounted() {
    this.$store.dispatch("loadVideosExcepted");
  },
  computed: {
    ...mapState(["video_excepted"])
  },
  methods: {
    onCliCommand(data, resolve) {
      setTimeout(() => {
        resolve("");
      }, 300);
    },
    add_form(form) {
      form.push("");
    },
    remove_form(form) {
      form.splice(-1, 1);
    }
  }
};
</script>