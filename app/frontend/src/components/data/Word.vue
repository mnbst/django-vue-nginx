<template>
  <div id="Word">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-card-title class="headline font-weight-bold mx-auto">word</v-card-title>
            <v-col v-for="item in word" :key="item.id">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="400">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.word}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>word_ini</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.word_ini"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>word</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" :placeholder="item.word"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>word_imi</h3>
                  <v-textarea class="my-n2 mb-n7 pa-0" :placeholder="item.word_imi"></v-textarea>
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

<script scoped>
import { mapState } from "vuex";

export default {
  name: "Word",
  mounted() {
    this.$store.dispatch("loadWords");
  },
  computed: {
    ...mapState(["word"])
  }
};
</script>

<style>
.custom-placeholer-color input::placeholder {
  color: black !important;
  opacity: 1;
}
</style>