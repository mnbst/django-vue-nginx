<template>
    <div id="app">
        <v-app>
            <v-app-bar app color="red">
                <v-app-bar-nav-icon color="white" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
                <v-spacer></v-spacer>
                <div class="d-flex align-center font-weight-bold white--text">インドネシア語辞典</div>
                <v-spacer></v-spacer>
            </v-app-bar>

            <v-navigation-drawer v-model="drawer" absolute temporary>
                <v-list nav dense>
                    <v-list-item-group active-class="deep-purple--text text--accent-4">
                        <v-list-item @click="drawer = false" to="/fetch_data">
                            <v-list-item-title>
                                <h4>fetch data</h4>
                            </v-list-item-title>
                        </v-list-item>

                        <v-list-item @click="drawer = false" to="/video_player">
                            <v-list-item-title>
                                <h4>video</h4>
                            </v-list-item-title>
                        </v-list-item>

                        <v-list-item @click="drawer = false" to="/data">
                            <v-list-item-title>
                                <h4>data</h4>
                            </v-list-item-title>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-navigation-drawer>

            <v-content>
                <transition name="fade" mode="out-in">
                    <router-view/>
                </transition>
            </v-content>
        </v-app>
    </div>
</template>

<script>
    import Home from "./components/Home";
    import VideoPlayer from "./components/videoViewer/VideoPlayer";
    import FetchData from "./components/fetch/FetchData";
    import Vue from "vue";
    import VueRouter from "vue-router";

    Vue.use(VueRouter);

    const routes = [
        {path: "/data", component: Home},
        {path: "/video_player", component: VideoPlayer},
        {path: "/fetch_data", component: FetchData}
    ];

    const router = new VueRouter({routes});
    router.replace("/fetch_data");

    export default {
        name: "App",

        router,

        data: () => ({
            drawer: false
        })
    };
</script>
