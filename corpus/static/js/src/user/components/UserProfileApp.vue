<template>
    <v-app>
        <v-sheet>
            <v-container>
                <div v-if="user">
                    <v-row class="d-flex justify-center">
                        <v-col cols="12">
                            <h4 class="text-center">INFORMATION DE PROFIL</h4>
                        </v-col>
                        <v-col cols="12" sm="5" xs="5">
                            <div><b>Email</b></div>
                            <div>{{ user.email }}</div>
                        </v-col>
                        <v-col cols="12" sm="5" xs="5">
                            <div><b>Langues</b></div>
                            <div>
                                <span  class="mx-1" v-for="language in user.languages" :key="language.id">{{ language.code }} </span>
                            </div>
                        </v-col>

                        <v-col cols="12">

                        </v-col>
                    </v-row>
                </div>
            </v-container>
            <v-container fluid>
                <v-col cols="12">
                            <h4 class="text-center">TACHE DE TRADUCTION</h4>
                </v-col>
                <div v-if="user">
                    <user-detail :user="user"/>
                </div>
            </v-container>
        </v-sheet>
    </v-app>

</template>
    

<script>
import UserMixin from '../../admin/components/mixins/user-mixin.js'
import UserDetail from '../../admin/components/UserDetail.vue'

import {
    VApp,
    VSheet,
    VContainer,
    VRow,
    VCol,
} from 'vuetify/lib'

export default {
    name: 'user-profile-app',
    props: {
        id: {
            type: String,
            required: true,
        }
    },
    
    components: {
        VApp,
        VSheet,
        VContainer,
        VRow,
        VCol,
        UserDetail,
    },

    mixins: [UserMixin],

    data() {
        return {
            user: null,
        }
    },

    created() {
        this.initialize()
    },

    methods: {
        initialize() {
            this.getUser(this.id).then((res => {
                this.user = res.data;
            }).bind(this))
            .catch(err => console.error(err))
        }
    }
}
</script>