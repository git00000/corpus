<template>
    <v-row class="d-flex justify-center">
        <v-col cols="12" md="4" sm="4" xs="12">
            <div class="mb-1"><strong>Format</strong></div>
            <div class="d-flex justify-center" >
                <v-select
                    v-model="export_as"
                    :items="['txt', 'json']"
                    label="Format"
                    solo
                ></v-select>
                <v-btn @click="on_export" x-large color="green">Exporter</v-btn>
            </div>
        </v-col>
    </v-row>
</template>

<script>
import ImportExportMixins from './mixins/import-export-mixins.js'
import {
    VApp,
    VSelect,
    VTextField,
    VBtn,
    VRow,
    VCol,
    VCheckbox,
    VContainer,
    VDatePicker
    } from 'vuetify/lib'

export default {
    name: 'export-form',
    components: {
        VApp,
        VSelect,
        VTextField,
        VBtn,
        VRow,
        VCol,
        VCheckbox,
        VContainer,
        VDatePicker
    },

    mixins: [ImportExportMixins],

    props: {
        source_language: {
             type: Number,
            required: true,
        },
        target_language: {
            type: Number,
            required: true
        },
        
    },

    data() { return { export_as: 'txt'} },
    
    methods: {
        on_export() {
            this.do_export(this.source_language, this.target_language, this.export_as)
                    .then((res => {
                        const url = window.URL.createObjectURL(new Blob([res.data]));
                        const filename= `traduction.${this.export_as}`
                                        
                        let link = document.createElement('a');
                        link.href = url;
                        link.setAttribute('download', filename);
                        document.body.appendChild(link);
                        link.click();
                        link.remove();

                    }).bind(this))
                    .catch(err => console.error(err))
        }
    }

}
</script>