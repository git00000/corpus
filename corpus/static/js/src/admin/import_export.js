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


import ImportExportApp from './components/ImportExportApp.vue'


new Vue({
    vuetify,
    components: {
        ImportExportApp,
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
}).$mount('#import-export-app-container')

