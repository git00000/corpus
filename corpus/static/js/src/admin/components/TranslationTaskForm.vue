<template>
    <v-app>
        <v-container>

        <form>
            <v-row>
                <v-col class="d-flex" cols="12" sm="6">
                    <v-select
                    v-model="source_language"
                    :items="languages"
                    label="Langue source"
                    item-text="name"
                    item-value="id"
                    solo
                    return-object
                    single-line
                    ></v-select>
                </v-col>
                <v-col class="d-flex" cols="12" sm="6">
                    <v-select
                    v-model="target_language"
                    :items="languages"
                    label="Language cible"
                    item-text="name"
                    item-value="id"
                    solo
                    return-object
                    single-line
                    ></v-select>
                </v-col>
            </v-row>
            
            <!-- word count-->
            <v-row>
                <v-col cols="12">
                    <div><strong>Longueur phrases:</strong></div>
                    <v-row class="d-flex ">
                        <v-col cols="12" sm="4">
                            <v-checkbox
                                v-model="size_short"
                                label="Courte"
                                color="green"
                                class="mt-1"
                            ></v-checkbox>
                        </v-col>
                        <v-col cols="12" sm="4">                                    
                            <v-checkbox
                                v-model="size_medium"
                                label="Moyenne"
                                color="orange"
                                class="mt-0 mb-1"
                            ></v-checkbox>
                        </v-col>
                        <v-col cols="12" sm="4">
                            <v-checkbox
                                v-model="size_long"
                                label="Longue"
                                color="red"
                                class="mt-0"
                            ></v-checkbox>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            
            <v-row>
                <v-col cols="12"  md="12" sm="12" xs="12">
                    <v-slider
                        v-model="word_count"
                        min="0"
                        :max="max_word_count"
                        thumb-label="always"
                        :label="`NB Mots (max: ${max_word_count})`"
                    >
                        <template v-slot:append>
                            <v-text-field
                                v-model="word_count"
                                class="mt-0 pt-0"
                                hide-details
                                single-line
                                type="number"
                                min="0"
                                :max="max_word_count"
                                style="width: 60px"
                            ></v-text-field>
                        </template>
                    </v-slider>
                </v-col>
                
                <v-col cols="12"  md="12" sm="12">
                    <div><strong>Traducteur</strong></div>
                    <v-select
                        v-model="selected_user"
                        :items="users"
                        label="Traducteurs"
                        item-text="email"
                        item-value="id"
                        solo
                        return-object
                        single-line
                        class="mt-1"
                    ></v-select>

                    <div class="mb-4"><strong>Date d'échéance</strong></div>
                        <v-date-picker
                        v-model="end_at"
                        full-width
                        landscape
                        reactive
                        show-current
                        :first-day-of-week="0"
                        locale="fr-fr"
                        required
                        ></v-date-picker>
                </v-col>
            </v-row>
            <div class="d-flex justify-center mt-4">
                <v-btn class="mr-4" color="primary" large @click="submit">Créer</v-btn>
                <v-btn class="mr-4" color="red" large @click="cancel">Annuler</v-btn>
            </div>
        </form>
        </v-container>
    </v-app>
</template>

<script>
import TaskMixin from './mixins/task-mixin.js'
import LanguageMixin from './mixins/language-mixin.js'
import UserMixin from './mixins/user-mixin.js'

import {
    VApp,
    VSelect,
    VTextField,
    VBtn,
    VRow,
    VCol,
    VCheckbox,
    VContainer,
    VDatePicker,
    VSlider,
    } from 'vuetify/lib'

export default {
    name: 'translation-task-form',
    components: {
        VApp,
        VSelect,
        VTextField,
        VBtn,
        VRow,
        VCol,
        VCheckbox,
        VContainer,
        VDatePicker,
        VSlider
    },
    
    mixins: [TaskMixin,LanguageMixin, UserMixin],

    data: () => ({
        languages: [],
        users: [],

        // API related request_data fields
        source_language: {id: '', name: '', code: ''},
        target_language: {id: '', name: '', code: ''},
        size_short: true,
        size_medium: false,
        size_long: false,
        
        phrase_count: 0,
        word_count: 0,
        max_word_count: 0,

        selected_user: [],
        end_at: '',
    }),

    created() {
        this.getLanguages().then((res => this.languages = res.data).bind(this))
        //this.getUsers().then((res=>this.users= res.data).bind(this))
    },
    
    watch: {
        source_language() {
            this.onLanguageChange()
        },
        target_language() {
            this.onLanguageChange()
        },
        word_count(old_value, new_value) {
            new_value = +new_value

            if(isNaN(new_value))
            {
                this.word_count = old_value
            }
            else if(new_value > this.max_word_count)
            {
                this.word_count = this.max_word_count
            }
            else if(new_value < 0) {
                this.word_count = 0
            }
        },

        size_short() {
            this._updateForm()
        },

        size_long() {
            this._updateForm()
        },

        size_medium()
        {
            this._updateForm()
        }
    },

    methods: {
        onLanguageChange()
        {
            let source_language = Object.assign({}, this.source_language)
            let target_language = Object.assign({}, this.target_language)

           if(!source_language.id || !target_language.id)
           {
               return;
           }

            this._updateForm()
        },

        _updateForm() {
            let requestData = {
                'source_language': this.source_language.id,
                'target_language': this.target_language.id,
                'size_short': this.size_short,
                'size_medium': this.size_medium,
                'size_long': this.size_long,
            }

            // valdiate requestData before send else cancel request
            for(let prop in requestData) {
                if(requestData.hasOwnProperty(prop) && requestData[prop] == null)
                {
                    console.log(`Form update canceled: ${prop} is required`)
                    return;   
                }
            }


            this.getUntranslatedPhraseCount(requestData)
                .then((res => {
                    // console.log(res.data)
                    this.users = res.data.bilingual_users
                    this.max_word_count = res.data.total_word_count
                    this.phrase_count = res.data.phrase_count
                }).bind(this))
                .catch(err => console.error(err.response))
        },
        cancel() {
            this.$emit("cancel")
        },
        submit() {

            let requestData = {
                'source_language': this.source_language.id,
                'target_language': this.target_language.id,
                'word_count': this.word_count,
                'size_short': !!this.size_short,
                'size_medium': !!this.size_medium,
                'size_long': !!this.size_long,
                'user': this.selected_user.id,
                'end_at': this.end_at
            }

            let requiredFields = [
                    'source_language',
                    'target_language',
                    'word_count',
                    'user',
                    'end_at']

            // cancel the request if requestData is not value
            for(let prop in requestData) 
            {
                if(requestData.hasOwnProperty(prop) && 
                    !!requestData[prop] == false &&
                    requiredFields.indexOf(prop) != -1
                )
                {
                    throw new Error(`${prop} is required`)
                }
            }

            this.createTranslationTask(requestData)
                .then((res =>{
                    this.$emit('save', res.data)
                }).bind(this))
                .catch((err) => console.error(err.response))
        }
    } 
}
</script>