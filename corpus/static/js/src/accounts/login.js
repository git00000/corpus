import Vue from 'vue'
import vuetify from '../plugins/vuetify'


require('../boostrap');
require('./style.scss')
import {
    VApp,
    VSheet,
    VContainer,
    VBtn,
    VTextField,
    VCol,
    VRow
} from 'vuetify/lib'


new Vue({
    vuetify,
    components: {
        VApp,
        VSheet,
        VContainer,
        VBtn,
        VTextField,
        VCol,
        VRow
    },
    data() {
        return {
            show_password: false,
        }
    },

    delimiters: ["[[", "]]"]

}).$mount('#login-app-container')

