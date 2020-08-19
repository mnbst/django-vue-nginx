<template>
    <div class="row">
        <v-btn class="text-lowercase col-12"
               @click="openModal"
               color="grey lighten-1"
        >{{captionWord.rootWord.word}}
        </v-btn>
        <div id="overlay" v-show="showAddWordModal">
            <div id="content">
                <h3>原型を入力してください</h3>
                <p></p>
                <v-text-field
                        v-model="captionWord.rootWord.word"
                        @input="searchForWords"
                ></v-text-field>
                <v-card id="words-contents">
                    <div v-if="words">
                        <div v-for="(word,id) in words" :key="id">
                            <div class="row">
                                <a class="col-6 mb-n9" v-on:click="selectWord(word)">{{word.word}}</a>
                                <p class="col-6">{{word.meaning}}</p>
                            </div>
                        </div>
                    </div>
                </v-card>
            </div>
        </div>
    </div>
</template>

<script>
    import {START_UP} from "../../graphql/query/query.step1";
    import {SAVE_CAPTION_WORD, SEARCH_FOR_WORDS} from "../../graphql/mutation/mutation.step1";

    const __loading = "loading..."
    export default {
        name: "addWordButton",
        props: ['captionWord', 'order', 'captionIndex'],
        apollo: {
            words: START_UP
        },
        data() {
            return {
                showAddWordModal: false,
                selectedWord: {},
            }
        },
        methods: {
            openModal() {
                this.showAddWordModal = true;
                this.searchForWords()
            },
            searchForWords() {
                const inputWord = this.captionWord.rootWord.word
                this.$apollo.mutate(
                    {
                        mutation: SEARCH_FOR_WORDS,
                        variables: {word: inputWord},
                        update: (store, {data: {searchForWords}}) => {
                            let data = store.readQuery({query: START_UP});
                            data.words = []
                            for (let i = 0; i < searchForWords.words.length; i++) {
                                const word = searchForWords.words[i];
                                data.words.push({
                                    __typename: word.__typename,
                                    id: word.id,
                                    wordIni: word.wordIni,
                                    word: word.word,
                                    meaning: word.meaning
                                })
                            }
                            store.writeQuery({query: START_UP, data});
                        },
                        optimisticResponse: {
                            __typename: "Mutation",
                            searchForWords: {
                                __typename: "SearchForWords",
                                words: [{
                                    __typename: "WordType",
                                    id: -1,
                                    wordIni: "",
                                    word: __loading,
                                    meaning: "",
                                },]
                            }
                        },
                    })
            },
            selectWord(word) {
                if (word.word === __loading) {
                    return null;
                }
                const captionWordId = this.captionWord.id;
                const rootWordId = word.id;
                const captionIndex = this.captionIndex;
                const order = this.order;
                this.$apollo.mutate(
                    {
                        mutation: SAVE_CAPTION_WORD,
                        variables: {captionWordId: captionWordId, rootWordId: rootWordId},
                        update: (store, {data: {saveCaptionWord}}) => {
                            let data = store.readQuery({query: START_UP});
                            const targetRootWord = data.video.captionSet[captionIndex].captionwordSet[order].rootWord;
                            const modifiedRootWord = saveCaptionWord.captionWord.rootWord;
                            targetRootWord.id = modifiedRootWord.id;
                            targetRootWord.word = modifiedRootWord.word;
                            targetRootWord.meaning = modifiedRootWord.meaning;
                            data.words = [];
                            store.writeQuery({query: START_UP, data});
                        },
                    })
                this.showAddWordModal = false;
            },
        }
    }
</script>

<style>
    #overlay {
        z-index: 1;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #content {
        z-index: 2;
        width: 50%;
        height: 50%;
        padding: 1em;
        background: #fff;
        overflow: scroll;
    }

    #words-contents {
        height: 200px;
        overflow-y: auto;
    }
</style>