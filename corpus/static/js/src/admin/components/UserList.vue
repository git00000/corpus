<template>
  <div class="text-center">
    <v-app>
        <v-sheet color="orange lighten-2" class="text-center">            
            <v-data-table
                :headers="headers"
                :items="users"
                :items-per-page="5"
                class="elevation-1"
            >

            <template v-slot:top>
                  <v-toolbar flat color="white">
                    <v-toolbar-title>Utilisateurs</v-toolbar-title>
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
                                <v-text-field v-model="editedItem.email" label="Email"></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <div><strong>Langues</strong></div>
                                <v-select
                                    v-model="editedItem.languages"
                                    :items="languages"
                                    label="Languages"
                                    item-text="code"
                                    item-value="id"
                                    solo
                                    single-line
                                    multiple
                                    class="mt-1"
                                ></v-select>
                              </v-col>
                              <v-col cols="12">
                                <p>Status</p>
                                <v-switch
                                  v-model="editedItem.admin"
                                  :label="`Administrateur`"
                                  color="blue"
                                  class="ma-0"
                                ></v-switch>
                                <v-switch
                                  v-model="editedItem.active"
                                  :label="`Active`"
                                  color="blue"
                                  class="ma-0"
                                ></v-switch>
                              </v-col>
                              
                                <v-col cols="12">
                                  <v-checkbox v-if="!itemAdd" color="red" v-model="password_edit" label="Changer de mot de passe"/>
                                  <v-text-field
                                    v-model="editedItem.password"
                                    :append-icon="show_password ? 'visibility' : 'visibility_off'"
                                    :type=" show_password ? 'text' : 'password'"
                                    :disabled="!password_edit  && !itemAdd"
                                    name="password"
                                    label="Mot de passe"
                                    hint="Au moins 8 caractères"
                                    counter
                                    @click:append="show_password = !show_password"
                                  ></v-text-field>
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
                
                <template v-slot:item.admin="{ item }">
                  <v-badge
                    :color="item.admin ? 'teal':'red'"
                    bottom
                    
                  >
                    <template v-slot:badge>
                      <v-icon dark v-if="item.admin">
                          check
                      </v-icon>
                      <v-icon dark v-else>
                          close
                      </v-icon>
                    </template>
                  </v-badge>
                </template>
                

                <template v-slot:item.languages="{ item }">
                  <template v-for="l in item.languages">
                    <span class="font-weight-bold mx-1" :key="l.id">{{ l.code }}</span>
                  </template>

                </template>

                <template v-slot:item.active="{ item }">
                  <v-badge
                    :color="item.active ? 'teal':'red'"
                    bottom
                    
                  >
                    <template v-slot:badge>
                      <v-icon dark v-if="item.active">
                          check
                      </v-icon>
                      <v-icon dark v-else>
                          close
                      </v-icon>
                    </template>
                  </v-badge>
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
import UserMixin from './mixins/user-mixin.js'

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
  VSelect,
  VCheckbox, VSwitch} from 'vuetify/lib'

export default {
    
    name: "user-list",
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
      VSelect,
      VCheckbox, VCheckbox
    },
    mixins: [LanguageMixin, UserMixin],

    data: () =>({
        dialog: false,
        headers: [],
        users: [],
        editedIndex: -1,
        
        password_edit: false,
        show_password: false,

        languages: [],

        editedItem: {
          email: '',
          admin: false,
          active: false,
          languages: [],
          password: '',
        },
        defaultItem: {
          email: '',
          admin: null,
          active: false,
          languages: [],
          password: '',
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
        this.getUsers().then(
          res => this.initializeDataTable(res.data)
        ).catch(err => console.error(err));

        this.getLanguages()
              .then((res => this.languages = res.data).bind(this))
              .catch(err => console.log(err))
    },


    methods: {
      editItem (item) {
        this.editedIndex = this.users.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.users.indexOf(item)
        confirm('Vous êtes sûr de vouloir supprimer cet utilisateur ?') 
        && this.deleteUser(item)
                .then((_ =>this.users.splice(index, 1)).bind(this))
                .catch(err => console.error(err))
      },
      
      close () {
        this.dialog = false
        this.password_edit = false
        this.show_password = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      
      save () {
        if (this.editedIndex > -1) {
          this.updateUser(this.editedItem).then(
            (res => {Object.assign(this.users[this.editedIndex], res.data)}).bind(this)
          ).catch(err => console.error(err.response.data))

        } else {

          this.addUser(this.editedItem).then(
            (res => { this.users.push(res.data)}).bind(this)
          ).catch(err => console.error(err))
        }
        this.close()
      },
      initializeDataTable(users) {
          this.headers = [  
            {
              text: 'email',
              align: 'left',
              sortable: false,
              value: 'email',
            },
            {
              text: 'Languages',
              sortable: false,
              value: 'languages',
            },
            { text: 'Admin', value: 'admin' },
            { text: 'Active', value: 'active' },
            { text: "Action", value:"action", sortable: false }
          ]
          this.users = users
        }
    },
}

</script>



