<template>
  <div class="text-xs-center" id="Home">
    <v-container>
      <main class="App__main">
        <transition name="fade" >
          <router-view />
        </transition>
      </main>
    </v-container>
  </div>
</template>

<script>
import Word from "./data/Word";
import Video from "./data/Video";
import Caption from "./data/Caption";
import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  { path: "/data", component: Word },
  { path: "/data/word", component: Word },
  { path: "/data/video", component: Video },
  { path: "/data/caption", component: Caption }
];

const router = new VueRouter({ routes, history: true });

export default {
  name: "Home",
  router,
  computed: {
    data() {
      return this.$store.state.data;
    }
  }
};
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.3s;
  transition-property: opacity;
  transition-timing-function: ease;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}
</style>