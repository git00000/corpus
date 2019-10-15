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

import LanguageList from './components/LanguageList.vue'


new Vue({
    vuetify,
    components: {
        LanguageList,
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
}).$mount('#language-list-container')



