<template>
  <div>
    <v-btn class="ml-3" color="primary" @click="addCaption">保存</v-btn>
    <v-btn class="ml-3" color="primary" @click="removeCaption">保存</v-btn>
  </div>
</template>

<script>
export default {
  name: "CaptionAddRemoveButtons",
  props: ['captionSet', 'index'],
  methods: {
    addCaption() {
    },
    removeCaption() {
    }
  }
}
</script>

<style scoped>

</style>