<template>
    <v-app>
        <v-sheet>
        <v-container v-if="item">
            <form>
                <v-row>
                    <v-col cols="12" sm="12" md="12">
                            <v-row>
                                <v-col cols="12" xs="12" sm="6" md="6">
                                    <div><b>Phrase ({{ item.translation_task.source_language.code }})</b></div>
                                    <v-textarea readonly :value="item.source_phrase.text"/>
                                </v-col>  

                                <v-col cols="12" xs="12" sm="6" md="6">
                                    <div><b>Traduction ({{ item.translation_task.target_language.code }})</b></div>
                                    <v-textarea v-model="text"/>
                                </v-col> 
                            </v-row> 
                    </v-col> 
                    <v-col cols="12" class="align-center">
                        <p>Phrase {{ item.position }}/{{ item.translation_task.item_count }}</p>
                    </v-col>
                    
                    <v-col cols="12" class="align-center" sm="12" md="12">
                        <div class="d-flex justify-center">
                            <v-checkbox v-model="completed" label="Terminée"/>
                        </div>
                        
                        <div class="d-flex justify-center">
                            <v-btn color="primary" rounded small @click="prev" >
                                <v-icon>chevron_left</v-icon>
                            </v-btn>

                            
                            <v-btn color="primary"  class="text-white" rounded small @click="next">
                                <v-icon>chevron_right</v-icon>
                            </v-btn>
                        </div>
                    </v-col>     
                </v-row>
            </form>
        </v-container>
        </v-sheet>
    </v-app>
</template>

<script>

import TanslationMixins from './mixins/translation-mixins.js'
import {
    VApp,
    VContainer,
    VRow,
    VCol,
    VBtn,
    VIcon,
    VCheckbox,
    VTextarea,
    VSheet,
} from 'vuetify/lib'


// for only test
window.sleep = function (ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export default {
    name: 'translation-app',

    props: {
        translationTaskId: {
            type: Number,
            required: true
        }
    },
    components: {
        VApp,
        VContainer,
        VRow,
        VCol,
        VBtn,
        VIcon,
        VCheckbox,
        VTextarea,
        VSheet,
    },
    mixins: [TanslationMixins],
    data() {
        return {
            item: null,
            text: "",
            completed: false,
        }
    },
    watch: {
        item(new_value, old_value) {
            
            let text_save = this.text
            let completed_save = this.completed
            
            this.text = new_value.target_phrase.text
            this.completed = new_value.completed
            

            if(
                !old_value || 
                (old_value.target_phrase.text == text_save 
                && completed_save == old_value.completed
                && old_value.completed != undefined)) {
                return
            } 

            let data = {
                'item': old_value.id,
                'language_as': 'target',
                'text': text_save || '',
                'item_completed': completed_save,
            }
            
            this.savePhrase(
                data['item'],
                data['language_as'],
                data['text'],
                data['item_completed']).then((res => {
                    console.log(res)
                }).bind(this))
                .catch(err => console.error(err))
        }
    },


    created() {
        this.getCurrentItem().then((res => {
            this.item = res.data
        }).bind(this))
    },

    methods: {
        prev() {
            this.getPrevItem()
                    .then((res => {
                        this.item = res.data
                    }).bind(this))
                    .catch(err => console.error(err))
        },
        next() {
            this.getNextItem().then((res => this.item = res.data).bind(this)).catch(err => console.error(err))
        },

        async getCurrentItem() {
            return await this.getTranslationTaskNextItem(this.translationTaskId, "current")
        },
        async getNextItem() {
            return await this.getTranslationTaskNextItem(this.translationTaskId, "next")
        },

        async getPrevItem() {
            return await this.getTranslationTaskNextItem(this.translationTaskId, 'previous')
        }
    }
}
</script>