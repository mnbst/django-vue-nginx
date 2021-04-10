<template>
  <div id="app">
    <v-app>
      <v-app-bar app color="red">
        <v-spacer></v-spacer>
        <div class="d-flex align-center font-weight-bold white--text">
          インドネシア語辞典
        </div>
        <v-spacer></v-spacer>
        <div>
          <a class="font-weight-bold white--text" href="/logout">ログアウト</a>
        </div>
      </v-app-bar>
      <v-content>
        <transition name="fade" mode="out-in">
          <router-view />
        </transition>
      </v-content>
    </v-app>
  </div>
</template>

<script>
import Home from "./components/Home";
import VideoPlayer from "./components/fetch/VideoPlayer";
import SelectableVideoList from "./components/fetch/CreateVideoList";
import FetchData from "./components/fetch/FetchData";
import Vue from "vue";
import VueRouter from "vue-router";
import VueYoutube from "vue-youtube";
// import {Carousel, Slide} from 'vue-carousel';

Vue.use(VueYoutube);
Vue.use(VueRouter);

const routes = [
  { path: "/data", component: Home },
  { path: "/videoPlayer", component: VideoPlayer },
  { path: "/fetchData", component: FetchData },
  { path: "/selectableVideoList", component: SelectableVideoList },
];

const router = new VueRouter({ routes });
router.replace("/selectableVideoList");

export default {
  name: "App",

  router,

  data: () => ({
    drawer: false,
  }),
  // components: {
  //     Carousel,
  //     Slide
  // }
};
</script>
