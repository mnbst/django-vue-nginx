<template>
  <div id="Caption">
    <v-container>
      <v-col cols="12">
        <v-card color="white align-center">
          <v-card-title class="headline font-weight-bold mx-auto">caption</v-card-title>
          <v-col v-for="item in caption" :key="item.href_index">
            <v-card class="mx-auto d-flex flex-wrap align-center" max-width="800">
              <v-card-title class="headline font-weight-bold mx-auto">{{item.href_index}}</v-card-title>
              <v-col cols="12" sm="12">
                <h3>text</h3>
                <v-textarea class="my-n2 mb-n7 pa-0" :placeholder="item.text"></v-textarea>
              </v-col>
              <v-col cols="12" sm="12">
                <h3>start_time</h3>
                <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.start_time"></v-text-field>
              </v-col>
              <v-col cols="12" sm="12">
                <h3>end_time</h3>
                <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.end_time"></v-text-field>
              </v-col>
              <v-col cols="12" sm="12">
                <h3>text_tokenized</h3>
                <v-layout row wrap>
                  <v-col cols="6">
                    <h4>word</h4>
                    <v-flex v-for="w in item.word" :key="w">
                      <v-text-field class="my-n2 mb-n7 pa-3" :placeholder="w"></v-text-field>
                    </v-flex>
                  </v-col>
                  <v-col cols="6">
                    <h4>word_imi</h4>
                    <v-flex v-for="wi in item.word_imi" :key="wi">
                      <v-text-field class="my-n2 mb-n7 pa-3" :placeholder="wi"></v-text-field>
                    </v-flex>
                  </v-col>
                </v-layout>
              </v-col>
              <v-row>
                <v-btn class="ma-4 primary">修正</v-btn>
                <v-btn class="ma-4 ml-n3" color="red">削除</v-btn>
              </v-row>
            </v-card>
          </v-col>
        </v-card>
      </v-col>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Caption",
  status: {
    type: String,
    required: true,
    validator: function(value) {
      return (
        ["syncing", "synced", "version-conflict", "error"].indexOf(value) !== -1
      );
    }
  },
  mounted() {
    this.$store.dispatch("loadCaptions");
  },
  computed: {
    ...mapState(["caption"])
  }
};
</script>