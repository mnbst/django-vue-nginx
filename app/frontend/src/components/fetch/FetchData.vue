<template>
  <div id="FetchData">
    <v-container>
      <v-col cols="12">
        <h2>fetch data</h2>
        <VueTerminal
          :intro="intro"
          console-sign=">>"
          allow-arbitrary
          height="250px"
          full-screen
          @command="onCliCommand"
        ></VueTerminal>
      </v-col>
      <v-col cols="12">
        <v-card color="white align-center">
          <v-row>
            <v-col cols="12" style="padding-top: 0px;">
              <v-toolbar flat dark>
                <v-toolbar-title class="headline font-weight-bold">setting</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-card-actions>
                  <v-btn class="primary" v-on:click="modify(fetch_setting)">設定を保存</v-btn>
                  <v-btn color="orange font-weight-bold" @click="fetch(fetch_setting)">実行</v-btn>
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
                  v-model="fetch_setting.page_to_crawl"
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
                  v-model="fetch_setting.language_limit"
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
                  v-model="fetch_setting.minimum_sentence"
                  :min="10"
                  :max="1000"
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
                v-on:click="add_form(fetch_setting.video_to_delete)"
              >
                <v-icon dark>add_circle</v-icon>
              </v-btn>
              <v-btn
                icon
                top
                color="grey lighten-1"
                v-on:click="remove_form(fetch_setting.video_to_delete)"
                v-if="fetch_setting.video_to_delete && fetch_setting.video_to_delete.length>0"
              >
                <v-icon dark>remove_circle</v-icon>
              </v-btn>
              <v-col cols="2" v-for="(input, index) in fetch_setting.video_to_delete" :key="index">
                <v-text-field
                  class="my-n2 mb-n7 pa-0"
                  v-model="fetch_setting.video_to_delete[index]"
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
                v-on:click="add_form(fetch_setting.video_to_renewal)"
              >
                <v-icon dark>add_circle</v-icon>
              </v-btn>
              <v-btn
                icon
                top
                color="grey lighten-1"
                v-on:click="remove_form(fetch_setting.video_to_renewal)"
                v-if="fetch_setting.video_to_renewal && fetch_setting.video_to_renewal.length>0"
              >
                <v-icon dark>remove_circle</v-icon>
              </v-btn>
              <v-col cols="2" v-for="(_, index) in fetch_setting.video_to_renewal" :key="index">
                <v-text-field
                  class="my-n2 mb-n7 pa-0"
                  v-model="fetch_setting.video_to_renewal[index]"
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
                v-on:click="add_form(fetch_setting.excepted_href)"
              >
                <v-icon dark>add_circle</v-icon>
              </v-btn>
              <v-btn
                icon
                top
                color="grey lighten-1"
                v-on:click="remove_form(fetch_setting.excepted_href)"
                v-if="fetch_setting.excepted_href && fetch_setting.excepted_href.length>0"
              >
                <v-icon dark>remove_circle</v-icon>
              </v-btn>
              <v-col cols="2" v-for="(_,i) in fetch_setting.excepted_href" :key="i">
                <v-text-field class="my-n2 mb-n7 pa-0" v-model="fetch_setting.excepted_href[i]"></v-text-field>
              </v-col>
            </v-row>
          </v-col>
        </v-card>
      </v-col>
    </v-container>
  </div>
</template>
   
<script>
import { mapState } from "vuex";
import Vue from "vue";
import VueNumberInput from "@chenfengyuan/vue-number-input";
import VueTerminal from "vue-terminal-ui";
import axios from "axios";

Vue.use(VueNumberInput);

export default {
  name: "FetchData",
  components: {
    VueTerminal
  },
  data() {
    return {
      video_id: "video_id",
      intro: "terminal"
    };
  },
  mounted() {
    this.$store.dispatch("loadFetchSetting");
  },
  computed: {
    ...mapState(["fetch_setting"])
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
    },
    modify(setting) {
      const promise = new Promise(function(resolve) {
        resolve(
          Object.keys(setting).forEach(function(prop) {
            if (typeof setting[prop] == "object") {
              setting[prop] = setting[prop].filter(item => item != "");
            }
          })
        );
      });
      promise.then(function() {
        axios
          .patch(setting.url, setting)
          .then(response => {
            console.log(response);
          })
          .catch(e => {
            console.log(e);
          });
      });
    },
    fetch(settings) {
      console.log(settings);
    }
  }
};
</script>