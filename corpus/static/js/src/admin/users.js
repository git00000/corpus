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

import UserList from './components/UserList.vue'

new Vue({
    vuetify,
    components: {
        UserList,
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
}).$mount('#user-list-container')

