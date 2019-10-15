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

import UserProfileApp from './components/UserProfileApp.vue'

new Vue({
    vuetify,
    components: {
        UserProfileApp,
        AppLayout,
        VListItem,
        VListItemTitle,
        VListItemContent,    }
}).$mount('#user-profile-app-container')

