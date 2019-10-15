<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      

      <v-list dense>
        <slot name="navigation-items"></slot>
      </v-list>

    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title></v-toolbar-title>
    </v-app-bar>

    <v-content>
            <slot name="content"></slot>
    </v-content>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>

import {
  VApp,
  VAppBar,
  VAppBarNavIcon,
  VContainer, VContent,
  VFooter,
  VList, VListItem, VListItemAction, VListItemContent, VListItemTitle,
  VIcon,
  VToolbarTitle,

} from 'vuetify/lib';

export default {
    
    name: "app-layout", 
    props: {
      source: String,
    },
    components: {
        VApp,
        VAppBar,
        VAppBarNavIcon,
        VContainer, VContent,
        VFooter,
        VList, VListItem, VListItemAction, VListItemContent, VListItemTitle,
        VIcon,
        VToolbarTitle,
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>