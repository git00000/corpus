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

import  TranslationTaskApp from './components/TranslationTaskApp.vue'


new Vue({
    vuetify,
    components: {
        TranslationTaskApp,
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
}).$mount('#translation-task-app-container')

