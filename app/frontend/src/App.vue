<template>
    <div id="app">
        <v-app>
            <v-app-bar app color="red">
                <v-spacer></v-spacer>
                <div class="d-flex align-center font-weight-bold white--text">インドネシア語辞典</div>
                <v-spacer></v-spacer>
            </v-app-bar>
            <v-content>
                <selectable-video-list/>
            </v-content>
        </v-app>
    </div>
</template>

<script>
    import Vue from "vue";
    import VueYoutube from 'vue-youtube'
    import SelectableVideoList from "@/components/fetch/CreateVideoList";

    Vue.use(VueYoutube)

    export default {
        name: "App",
      components: {SelectableVideoList},

        data: () => ({
            drawer: false
        }),
    };
</script>
