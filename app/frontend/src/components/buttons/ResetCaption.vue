<template>
    <v-btn class="ml-3" color="secondary"
           @click="resetCaption">元に戻す
    </v-btn>
</template>

<script>
    import {RESET_CAPTION} from "../../graphql/mutation/mutation.step1";
    import {START_UP} from "../../graphql/query/query.step1";

    export default {
        name: "ResetCaptionButton",
        props: ["video", "index"],
        methods: {
            resetCaption() {
                const video = this.video;
                const index = this.index;
                const target = video.captionSet[index];
                this.$apollo.mutate(
                    {
                        mutation: RESET_CAPTION,
                        variables: {id: target.id},
                        update: (store, {data: {resetCaption}}) => {
                            let data = store.readQuery({query: START_UP});
                            const renderedCaption = data.video.captionSet[index];
                            const originalCaption = resetCaption.caption;
                            renderedCaption.index = originalCaption.index;
                            renderedCaption.id = originalCaption.id;
                            renderedCaption.startTime = originalCaption.startTime;
                            renderedCaption.end_time = originalCaption.end_time;
                            renderedCaption.text = originalCaption.text;

                            for (let i = 0; i < originalCaption.captionwordSet.length; ++i) {
                                let wordSet = renderedCaption.captionwordSet[i];
                                const originalWordSet = originalCaption.captionwordSet[i];
                                try {
                                    wordSet.id = originalWordSet.id;
                                    wordSet.order = originalWordSet.order;
                                    wordSet.fixedWord = originalWordSet.fixedWord;
                                    wordSet.fixedMeaning = originalWordSet.fixedMeaning;
                                    wordSet.rootWord.word = originalWordSet.rootWord.word;
                                    wordSet.rootWord.meaning = originalWordSet.rootWord.meaning;
                                } catch (e) {
                                    renderedCaption.captionwordSet.push({
                                        id: originalWordSet.id,
                                        order: originalWordSet.order,
                                        fixedWord: originalWordSet.fixedWord,
                                        fixedMeaning: originalWordSet.fixedMeaning,
                                        rootWord: {
                                            word: originalWordSet.rootWord.word,
                                            meaning: originalWordSet.rootWord.meaning,
                                            __typename: originalWordSet.rootWord.__typename
                                        },
                                        __typename: originalWordSet.__typename
                                    })
                                }
                            }
                            store.writeQuery({query: START_UP, data})
                        }
                    })
            },
        }
    }
</script>

<style scoped>

</style>