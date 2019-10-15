import Vue from 'vue'
import vuetify from '../plugins/vuetify'
import AppLayout from '../AppLayout.vue'
import {
    VListItem,
    VListItemTitle,
    VListItemContent,
} from 'vuetify/lib'
require('../boostrap');
require('./style.scss')

import TranslationApp from './components/TranslationApp.vue'


new Vue({
    vuetify,
    components: {
        TranslationApp,
        AppLayout,
        VListItem,
        VListItemTitle,
        VListItemContent,
    },
    methods: {
        goTo(url) {
            window.location.assign(url)
        }
    }
}).$mount('#translation-app-container')

