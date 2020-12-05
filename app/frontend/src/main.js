import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import ApolloClient from 'apollo-boost'
import VueApollo from 'vue-apollo'
import {InMemoryCache} from 'apollo-cache-inmemory';

const cache = new InMemoryCache();

Vue.config.productionTip = false;

const apolloProvider = new VueApollo({
    defaultClient: new ApolloClient({
        cache: cache,
        uri: '/graphql'
    })
});

Vue.use(VueApollo);
new Vue({
    el: '#app',
    vuetify,
    apolloProvider,
    render: h => h(App)
});
