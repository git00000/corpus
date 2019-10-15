<template>
        <v-sheet>   
            <h4 class="text-center">LISTE DES TACHES</h4>
            <v-data-table
                :headers="headers"
                :items="translation_tasks"
                :items-per-page="5"
                class="elevation-1"
            >
            <template v-slot:top="{ item }">
                <div class="d-flex justify-end mr-1">
                    <translation-task-form-dialog/>  
                </div>
            </template>
            <template v-slot:item.user="{ item }">
                <div>
                    <v-btn @click="selected_task_user=item.user" text color="primary">{{ item.user.email }}</v-btn>
                </div>
            </template>
            <template v-slot:item.source_language="{ item }">
                <div class="text-center">
                    {{ item.source_language.name }} - (<span class="font-weight-bold">{{ item.source_language.code }}</span>)
                </div>
            </template>
            
            <template v-slot:item.target_language="{ item }">
                <div class="text-center">
                    {{ item.target_language.name }} - (<span class="font-weight-bold">{{ item.target_language.code }}</span>)
                </div>
            </template>

            <template v-slot:item.created_at="{ item }">
                <div class="text-center">
                    {{ getFormatedDate(item.created_at) }}
                </div>
            </template>

            <template v-slot:item.end_at="{ item }">
                <div class="text-center">
                    {{ getFormatedDate(item.end_at) }}
                </div>
            </template>

             <template v-slot:item.finished_at="{ item }">
                <div class="text-center">
                    <template v-if="item.finished_at">
                        {{ getFormatedDate(item.finished_at) }}
                    </template>
                    <v-icon v-else color="red">close</v-icon>
                </div>
            </template>
            </v-data-table>
            
            <v-divider
                class="mx-4"
                inset
                horizontal
            ></v-divider>
            
            <div class="mt-5 pt-2">
                <h4 class="text-center">DETAIL TACHE - {{ selected_task_user.email }}</h4>
                <user-detail v-if="selected_task_user" :user="selected_task_user"/>  
            </div>
        </v-sheet>
        
</template>


<script>
import TaskMixin from './mixins/task-mixin.js'
import TranslationTaskFormDialog from './TranslationTaskFormDialog.vue'

import { 
  VCard, VCardActions, VCardText, VCardTitle, 
  VCol,
  VContainer,
  VDivider,
  VBtn, 
  VSheet, VDataTable, 
  VIcon,
  VBadge,
  VSelect} from 'vuetify/lib'

import UserDetailDialog from './UserDetailDialog.vue'
import UserDetail from './UserDetail.vue'

export default {
    name: 'translation-task-list',
    mixins: [TaskMixin],

    components: {
        VCard, VCardActions, VCardText, VCardTitle, 
        VCol,
        VContainer,
        VDivider,
        VBtn, 
        VSheet, VDataTable, 
        VIcon,
        VBadge,
        VSelect,
        UserDetailDialog,
        UserDetail,
        TranslationTaskFormDialog 
    },
    data: () => ({
        headers: [],
        translation_tasks: [],
        selected_task_user:null
    }),

    created()
    {
        this.getTranslationTasks().then(
            (res => {
                this.initializeDataTable(res.data)
            }).bind(this)
        ).catch(err =>console.error(err.response))
    },
    
    methods: {

        getFormatedDate(dateString) {
            let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

            let date = new Date(dateString)
            return date.toLocaleDateString("fr-FR")

        },

        initializeDataTable(data) {
            
            this.headers = [
                {
                    text: "Utilisateur",
                    value: "user",
                    align: "center"

                },
                {
                    text: 'Language source',
                    value: 'source_language',
                    align: "center",
                },
                {
                    text: 'Language cible',
                    value: 'target_language',
                    align: "center",
                },
                {
                    text: "Date de création",
                    value: "created_at",
                    align: "center"
                },
                {
                    text: "Date d'echéance",
                    value:"end_at",
                    align: "center"
                },
                {
                    text: "Terminée le",
                    value: "finished_at",
                    align: "center",
                },
            ]

            this.translation_tasks = data

            this.selected_task_user = data[0].user
        }
    }
}
</script>