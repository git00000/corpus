<template>
    <v-app>
        <v-sheet>
            <div>
                <translation-task-list/>
            </div>
        </v-sheet> 
    </v-app>
</template>

<script>

import TranslationTaskList from './TranslationTaskList.vue'

import {VApp, VSheet} from 'vuetify/lib'
export default {
    name: 'translation-task-app',
    components: {
        VApp,
        VSheet,
        TranslationTaskList,
    }
}
</script>