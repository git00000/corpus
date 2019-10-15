<template>
  <div class="text-center">
    <v-app>
        <v-sheet color="orange lighten-2" class="text-center">            
            <v-data-table
                :headers="headers"
                :items="languages"
                :items-per-page="5"
                class="elevation-1"
            >

            <template v-slot:top>
                  <v-toolbar flat color="white">
                    <v-toolbar-title>Languages</v-toolbar-title>
                    <v-divider
                      class="mx-4"
                      inset
                      vertical
                    ></v-divider>
                    <div class="flex-grow-1"></div>
                    <v-dialog v-model="dialog" max-width="500px">
                      <template v-slot:activator="{ on }">
                        <v-btn color="primary" dark class="mb-2" v-on="on">Nouveau</v-btn>
                      </template>
                      <v-card>
                        <v-card-title>
                          <span class="headline">{{ formTitle }}</span>
                        </v-card-title>

                        <v-card-text>
                          <v-container>
                            <v-row>
                              <v-col cols="12">
                                <v-text-field v-model="editedItem.name" label="Non"></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field v-model="editedItem.code" label="Code"></v-text-field>
                              </v-col>
                            </v-row>
                          </v-container>
                        </v-card-text>

                        <v-card-actions>
                          <div class="flex-grow-1"></div>
                          <v-btn color="blue darken-1" text @click="close">Annuler</v-btn>
                          <v-btn color="blue darken-1" text @click="save">Sauver</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-toolbar>
                </template>


                <template v-slot:item.action="{ item }">
                    <v-icon small class="mr-2" @click="editItem(item)">edit</v-icon>
                    <v-icon small @click="deleteItem(item)">delete</v-icon>
                </template>

            </v-data-table>
        </v-sheet>
    </v-app>
  </div>
</template>



<script>
import LanguageMixin from './mixins/language-mixin.js'

import { 
  VApp, 
  VCard, VCardActions, VCardText, VCardTitle, 
  VToolbar, VToolbarTitle,
  VDialog,
  VCol,
  VContainer,
  VDivider,
  VBtn, 
  VSheet, VDataTable, 
  VIcon,
  VBadge,
  VCheckbox, VSwitch} from 'vuetify/lib'

export default {
    
    name: "language-list",
    components: {
      VApp, 
      VCard, VCardActions, VCardText, VCardTitle, 
      VToolbar, VToolbarTitle,
      VDialog,
      VCol,
      VContainer,
      VDivider,
      VBtn, 
      VSheet, VDataTable,
      VIcon,
      VBadge,
      VCheckbox, VCheckbox
    },

    mixins: [LanguageMixin],

    data: () =>({
        dialog: false,
        headers: [],
        languages: [],
        editedIndex: -1,

        editedItem: {
          name: '',
          code: ''
        },
        defaultItem: {
          name: '',
          code: ''
        },
      }),
  computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'Nouveau' : 'Editer'
      },
      itemAdd() {
        return this.editedIndex === -1
      }
    },

    watch: {
      dialog (val) {
        val || this.close()
      }
    },

    created() {
        this.getlanguages().then(
          res => this.initialize(res.data)
        ).catch(err => console.error(err));
    },

    methods: {
      editItem (item) {
        this.editedIndex = this.languages.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.languages.indexOf(item)
        confirm('Vous êtes sûr de vouloir supprimer cette language ?') 
        && this.deletelanguage(item)
                .then((_ =>this.languages.splice(index, 1)).bind(this))
                .catch(err => console.error(err))
      },
      
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      
      save () {
        if (this.editedIndex > -1) {
          this.updateLanguage(this.editedItem).then(
            (res => {Object.assign(this.languages[this.editedIndex], res.data)}).bind(this)
          ).catch(err => console.error(err))

        } else {

          this.addLanguage(this.editedItem).then(
            (res => { this.languages.push(res.data)}).bind(this)
          ).catch(err => console.error(err))
        }
        this.close()
      },
      initialize(languages) {
          this.headers = [  
            {
              text: 'Nom',
              align: 'left',
              sortable: false,
              value: 'name',
            },
            { text: 'Code', value: 'code' },
            { text: "Action", value:"action", sortable: false }
          ]
          this.languages = languages
        }
    },
}

</script>



