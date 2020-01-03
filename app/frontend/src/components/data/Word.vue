<template>
  <div id="Word">
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="white align-center">
            <v-row>
              <v-col cols="12">
                <v-card-title class="justify-center">
                  <p class="headline font-weight-bold">word</p>
                </v-card-title>
                <v-card-actions class="justify-center">
                  <v-dialog v-model="dialog" persistent max-width="600">
                    <template v-slot:activator="{ on }">
                      <v-btn color="orange font-weight-bold" v-on="on">単語追加</v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">単語情報</span>
                      </v-card-title>
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-text-field label="word_ini*" required v-model="Word.word_ini"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field label="word*" required v-model="Word.word"></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field label="word_imi*" required v-model="Word.word_imi"></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                        <small>*indicates required field</small>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                        <v-btn color="blue darken-1" text @click="add">Save</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-card-actions>
              </v-col>
            </v-row>
            <v-col v-for="(item) in words" :key="item.id">
              <v-card class="mx-auto d-flex flex-wrap align-center" max-width="400">
                <v-card-title class="headline font-weight-bold mx-auto">{{item.word}}</v-card-title>
                <v-col cols="12" sm="12">
                  <h3>word_ini</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.word_ini"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>word</h3>
                  <v-text-field class="my-n2 mb-n7 pa-0" v-model="item.word"></v-text-field>
                </v-col>
                <v-col cols="12" sm="12">
                  <h3>word_imi</h3>
                  <v-textarea class="my-n2 mb-n7 pa-0" v-model="item.word_imi"></v-textarea>
                </v-col>
                <v-row>
                  <v-btn class="ma-4 primary" @click="modify(item)">修正</v-btn>
                  <v-btn
                    class="ma-4 ml-n3"
                    color="red"
                    @click.stop="showConfirmationDialog(item)"
                  >削除</v-btn>
                </v-row>
              </v-card>
            </v-col>
            <v-dialog v-model="confirmationDialog" max-width="290">
              <v-card>
                <v-card-title class="headline">{{deleteWord.word}}を削除しますか？</v-card-title>
                <v-card-actions>
                  <v-btn color="green darken-1" text @click="confirmationDialog = false">Disagree</v-btn>
                  <v-btn color="green darken-1" text @click="deleteItem(deleteWord)">Agree</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script scoped>
import { mapState } from "vuex";
import axios from "axios";

export default {
  name: "Word",
  data: () => ({
    dialog: false,
    confirmationDialog: false,
    Word: {
      word_ini: "",
      word: "",
      word_imi: ""
    },
    deleteWord: {
      word_ini: "",
      word: "",
      word_imi: ""
    }
  }),
  mounted() {
    this.$store.dispatch("loadWords");
  },
  computed: {
    ...mapState(["words"])
  },
  methods: {
    showConfirmationDialog: function(item) {
      this.deleteWord = item;
      this.confirmationDialog = true;
    },
    add: function() {
      let newWord = {
        word_ini: this.Word.word_ini,
        word: this.Word.word,
        word_imi: this.Word.word_imi
      };
      axios
        .post("/api/words/", newWord)
        .then(response => {
          this.$store.dispatch("loadWords");
          console.log(response);
          this.dialog = false;
        })
        .catch(e => {
          console.log(e);
        });
    },
    modify: function(item) {
      axios
        .patch(item.url, item)
        .then(response => {
          this.$store.dispatch("loadWords");
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
          this.$store.dispatch("loadWords");
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

<style>
.custom-placeholer-color input::placeholder {
  color: black !important;
  opacity: 1;
}
</style>