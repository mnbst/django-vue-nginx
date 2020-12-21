<template>
  <div class="caption-add-remove-buttons">
    <button class="ml-3 button" @click="addCaption">
      <v-icon class="icon" dark>add</v-icon>
    </button>
    <button class="ml-3 button" @click="removeCaption">
      <v-icon class="icon" dark>remove</v-icon>
    </button>
  </div>
</template>

<script>
export default {
  name: "CaptionAddRemoveButtons",
  props: ['captionSet', 'index'],
  methods: {
    addCaption() {
      const caption = this.captionSet[this.index]
      const startIndex = caption.index + 1

      let copyCaption = Object.assign({}, caption)
      copyCaption.id = ''
      copyCaption.index = startIndex
      copyCaption.startTime = 0
      copyCaption.endTime = 0
      copyCaption.text = ""
      copyCaption.captionwordSet = []
      this.captionSet.splice(startIndex, 0, copyCaption)
      for (let i = startIndex; i < this.captionSet.length; i++) {
        this.captionSet[i].index = i;
      }
    },
    removeCaption() {
      this.captionSet.splice(this.index, 1)
      for (let i = this.index; i < this.captionSet.length; i++) {
        this.captionSet[i].index = i;
      }
    }
  }
}
</script>

<style scoped>
.caption-add-remove-buttons {
  display: flex;
  margin-left: -12px
}

.caption-add-remove-buttons > .button {
  background: rgb(244, 67, 54);
  width: 30px;
  height: 30px;
  border-radius: 5px;
}

.caption-add-remove-buttons > .button > .icon {
  width: 10px;
}
</style>