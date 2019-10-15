<template>
        <v-sheet>
                <v-container fluid>
                <v-data-table
                    :headers="headers"
                    :items="tasks"
                    :items-per-page="5"
                    class="elevation-1"
                >

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

                    <template v-slot:item.progress="{ item }">
                        <div class="text-center">
                            {{ getPercentage(item.completed_item_count,item.item_count) }}%
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
                            <template v-if="item.finished_at"></tempalte>
                            {{ getFormatedDate(item.finished_at) }}
                            </template>
                            <v-icon v-else color="red">close</v-icon>
                        </div>
                    </template>

                    <template v-slot:item.action="{ item }">
                        <div class="text-center">
                            <v-btn small text color="primary" @click="gotoTranslationPage(item)">Traduire</v-btn>
                        </div>
                    </template>
                </v-data-table>
            </v-container>
        </v-sheet>
</template>

<script>

import {VContainer, VSheet, VDataTable, VIcon, VBtn} from 'vuetify/lib'
import UserMixin from './mixins/user-mixin.js'

export default {
    name:"user-detail",

    components: {
        VContainer,
        VSheet,
        VDataTable,
        VIcon,
        VBtn,
    },

    mixins: [UserMixin],
    props: {
        user: {
            type: Object,
            required: true,
        }
    },

    watch: {
        user() {
            this.initialize()
        }
    },

    data() {
        return {
            headers: [],
            tasks: [],

            enableTranslationPageLink: true,
        }
    },
    
    created() {
        this.initialize()
    },
    methods: {
        initialize() {
            this.getUserTranslationTasks(this.user.id)
                .then((res => {
                    this.initializeTranslationTaskDataTable(res.data)
                }).bind(this))
        },
        getPercentage(value, max_value){
            let percent = value*100 / max_value;
            return parseFloat(percent).toFixed(3)
        },
        getFormatedDate(dateString) {
            let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

            let date = new Date(dateString)
            return date.toLocaleDateString("fr-FR")

        },
        gotoTranslationPage(item) {
            // Django specific syntaxe
            let url = "{% url 'user:translation-task' 0 %}" // place holder 0
            url = url.replace('/0', `/${item.id}`)

            window.location.assign(url)
        },
        initializeTranslationTaskDataTable(data) {
            console.log('translationtask table initailizer')
            console.log(data)
            let headers = [
                {
                    'text': "Langue source",
                    'value': 'source_language',
                    'align': 'center',
                },
                {
                    'text': "Language cible",
                    'value': "target_language",
                    'align': 'center'
                },
                {
                    'text': 'NB Mots',
                    'value': 'word_count',
                    'align': 'center'
                },
                {
                    'text': "NB Phrases",
                    'value': 'item_count',
                    'align': 'center'
                },
                {
                    'text': 'NB Traduites',
                    'value': 'completed_item_count',
                    'align': 'center'
                },
                {
                    'text': "Progression",
                    'value': "progress",
                    'align': 'center'
                },
                {
                    'text': 'Création',
                    'value': 'created_at',
                    'align': 'center'
                },
                {
                    'text': "Echéance",
                    'value': 'end_at',
                    'align': 'center'
                },
                {
                    'text': 'Terminée',
                    'value': 'finished_at',
                    'align': 'center'
                }
            ]

            if(this.enableTranslationPageLink)
            {
                headers.push(
                    {
                        'text': 'Action',
                        'value': 'action',
                        'align': 'center'
                    })
            }

            this.headers = headers
            this.tasks = data;
            
        }
    }
}
</script>
