<template>
    <div>
        <v-btn
        color="primary"
        dark
        @click.stop="dialog = true"
            >
        Nouveau
        </v-btn>
    <v-dialog v-model="dialog" fullscreen>
        <v-card>
            <v-card-title>
                <span class="headline">Nouvelle Tâche</span>
            </v-card-title>
            <v-card-text>
                <translation-task-form @save="close" @cancel="close"/>
            </v-card-text>
        </v-card>
    </v-dialog>
    </div>
</template>



<script>
import {
    VDialog,
    VApp,
    VCard, VCardActions, VCardText, VCardTitle
} from 'vuetify/lib'
import TranslationTaskForm from './TranslationTaskForm.vue'

export default {
    name: "translation-task-form-dialog",

    components: {
        VDialog,
        TranslationTaskForm,
        VCard, VCardActions, VCardText, VCardTitle
    },

    data: () => ({
        dialog: false
    }),

    methods: {
        close() {
            this.dialog = false
        }
    }
}
</script>