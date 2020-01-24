<template>
  <div id="FetchData">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-card-title class="headline font-weight-bold mx-auto">setting</v-card-title>
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
                <v-col cols="2" v-for="(input, index) in form" :key="index">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-btn icon top color="grey lighten-1" v-on:click="add_form">
                  <v-icon dark>add_circle</v-icon>
                </v-btn>
                <v-btn
                  icon
                  top
                  color="grey lighten-1"
                  v-on:click="remove_form"
                  v-if="this.form.length>0"
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
                <v-col cols="2" v-for="(input, index) in renewal" :key="index">
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="video_id"></v-text-field>
                </v-col>
                <v-btn icon top color="grey lighten-1" v-on:click="add_renewal">
                  <v-icon dark>add_circle</v-icon>
                </v-btn>
                <v-btn
                  icon
                  top
                  color="grey lighten-1"
                  v-on:click="remove_renewal"
                  v-if="this.renewal.length>0"
                >
                  <v-icon dark>remove_circle</v-icon>
                </v-btn>
              </v-row>
              <v-row>
                <v-col cols="2">
                  <p class="text-center">除外動画id</p>
                </v-col>
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
Vue.use(VueNumberInput);

export default {
  name: "FetchData",
  data() {
    return {
      pages: 1,
      languages: 1,
      captions: 10,
      video_id: "video_id",
      form: [],
      renewal: [],
      VideoExcepted: {
        video_href: "",
        video_title: "",
        video_img: ""
      }
    };
  },
  mounted() {
    this.$store.dispatch("loadVideoExcepted");
  },
  computed: {
    ...mapState(["video_excepted"])
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
    add_renewal() {
      this.renewal.push({
        one: ""
      });
    },
    remove_renewal(index) {
      this.renewal.splice(index, 1);
    }
  }
};
</script>