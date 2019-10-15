import Vue from 'vue'
import vuetify from '../plugins/vuetify'
import {
    VApp,
    VContainer,
    VSheet,
    VBtn
} from 'vuetify/lib'
require('../boostrap');
require('./style.scss')

new Vue({
    vuetify,
    components: {
        VApp,
        VContainer,
        VSheet,
        VBtn
    },
    methods: {    
        goTo(url) {
            window.location.assign(url)
        }
    }
}).$mount('#app')