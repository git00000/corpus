<template>
    <v-app>
        <v-container>
         <v-row>
                <v-col cols="12" md="5" sm="5">
                    <div class="mb-1"><strong>Langue source</strong></div>
                    <v-select
                    v-model="source_language"
                    :items="languages"
                    label="Langue source"
                    item-text="name"
                    item-value="id"
                    solo
                    single-line
                    ></v-select>
                </v-col>
                <v-col cols="12" md="5" sm="5">
                    <div class="mb-1"><strong>Langue cible</strong></div>
                    <v-select
                    v-model="target_language"
                    :items="languages"
                    label="Language cible"
                    item-text="name"
                    item-value="id"
                    solo
                    single-line
                    ></v-select>
                </v-col>
                <v-col cols="12" md="2" sm="2">
                    <div class="mb-1"><strong>Import ou Export</strong></div>
                    <v-select
                    v-model="operation"
                    :items="['import', 'export']"
                    
                    label="Language cible"
                    item-text="name"
                    item-value="id"
                    solo
                    single-line
                    ></v-select>
                </v-col>
                <template v-if="!!source_language && !! target_language">
                    
                    <v-col cols="12" sm="12" v-if="operation == 'import'">
                        <div><strong>Choisir un fichier</strong></div>
                        <import-form
                            :source_language="source_language"
                            :target_language="target_language"
                        />
                    </v-col>
                    <v-col cols="12" sm="12" v-else-if="operation == 'export'" >
                        <export-form
                            :source_language="source_language"
                            :target_language="target_language"
                        />
                    </v-col>
                </template>
            </v-row>
            </v-container>
    </v-app>
</template>

<script>
import {
    VApp,
    VSelect,
    VRow,
    VCol,
    VContainer,
    VDivider
    } from 'vuetify/lib'

import ImportForm from './ImportForm.vue'
import ExportForm from './ExportForm.vue'
import languageMixins from './mixins/language-mixin.js'

export default {
    name: 'import-export-app',
    components: {
        VApp,
        VContainer,
        ImportForm,
        VSelect,
        VRow,
        VCol,
        VDivider,
        ExportForm
    },
    mixins: [
        languageMixins
    ],

    data: () => ({
            languages: [],
            source_language: null,
            target_language: null,

            operation: 'export', // default
            operationOptions: ['import', 'export']
    }),

    created() {
        this.getLanguages()
            .then((res => this.languages = res.data).bind(this))
            .catch(err => console.error(err))
    },

    methods: {
    }
}
</script>