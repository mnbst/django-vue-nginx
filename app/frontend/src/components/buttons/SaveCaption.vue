<template>
    <v-btn class="ml-3" color="primary" @click="saveCaption">保存</v-btn>
</template>

<script>
    import {SAVE_CAPTION} from "../../graphql/mutation/mutation.step1";
    import {START_UP} from "../../graphql/query/query.step1";

    export default {
        name: "SaveCaptionButton",
        props: ["video", "index"],
        methods: {
            saveCaption() {
                const index = this.index;
                const caption = this.video.captionSet[index];
                const _this = this;
                let rootWordList = [];
                let captionWordList = [];
                for (let i = 0; i < caption.captionwordSet.length; i++) {
                    const captionWord = caption.captionwordSet[i]
                    const rootWord = captionWord.rootWord
                    captionWordList.push({
                        id: captionWord.id,
                        fixedWord: captionWord.fixedWord,
                        fixedMeaning: captionWord.fixedMeaning,
                        order: captionWord.order
                    })
                    rootWordList.push({word: rootWord.word, meaning: rootWord.meaning})
                }
                if (confirm('以下の内容で保存しますか？')) {
                    _this.$apollo.mutate({
                            mutation: SAVE_CAPTION,
                            variables: {
                                captionInput: {
                                    id: caption.id,
                                    index: index,
                                    startTime: caption.startTime,
                                    endTime: caption.endTime,
                                    text: caption.text,
                                },
                                captionWordInputs: captionWordList,
                                wordInputs: rootWordList,
                            },
                            update: (store, {data: {saveCaption}}) => {
                                const data = store.readQuery({query: START_UP});
                                const targetCaption = data.video.captionSet[index];
                                const updatedCaption = saveCaption.caption;
                                targetCaption.index = updatedCaption.index;
                                targetCaption.id = updatedCaption.id;
                                targetCaption.startTime = updatedCaption.startTime;
                                targetCaption.end_time = updatedCaption.end_time;
                                targetCaption.text = updatedCaption.text;
                                for (let i = 0; i < updatedCaption.captionwordSet.length; ++i) {
                                    let wordSet = targetCaption.captionwordSet[i];
                                    const originalWordSet = updatedCaption.captionwordSet[i];
                                    wordSet.id = originalWordSet.id;
                                    wordSet.order = originalWordSet.order;
                                    wordSet.fixedWord = originalWordSet.fixedWord;
                                    wordSet.fixedMeaning = originalWordSet.fixedMeaning;
                                    wordSet.rootWord.word = originalWordSet.rootWord.word;
                                    wordSet.rootWord.meaning = originalWordSet.rootWord.meaning;

                                }
                                store.writeQuery({query: START_UP, data});
                            }
                        }
                    ).then(() => {
                        alert('saved');
                    })
                }
            },
        }
    }
</script>

<style scoped>

</style>