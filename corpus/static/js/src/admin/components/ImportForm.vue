<template>
<form>
    <div v-if="!disabled" class="pb-0 d-flex align-center">
            <v-file-input accept=".txt" show-size label="Fichier" :disabled="disabled" class="mr-2" @change="onFileChange" ></v-file-input>
            <v-btn class="mr-4" color="primary" @click="submit">Importer</v-btn>
    </div>
    <div v-else class="text-center ma-12">
        <v-progress-circular
            indeterminate
            rotate
            size="100"
            width="10"
            color="light-blue"
        ></v-progress-circular>
        </div>
</form>

</template>

<script>
import {
    VBtn,
    VFileInput,
    VProgressCircular
} from 'vuetify/lib'

import ImportExportMixins from './mixins/import-export-mixins.js'

export default {
    name: 'import-form',
    props: {
        source_language: {
            type: Number,
            require: true,
        },
        target_language: {
            type: Number,
            required: true,
        }
    },
    components: {
        VBtn,
        VFileInput,
        VProgressCircular
    },

    mixins: [ImportExportMixins],

    data: () =>({
        file: '',
        disabled: false,

        languages: [],
    }),

    methods: {
        submit()
        {
            this.disabled = true
            this.do_import(
                this.$props.source_language, 
                this.$props.target_language, 
                this.file)
            .then(
                (res => {
                    this.disabled = false
                    console.log(res.data)
                }).bind(this)
            ).catch(err => console.error(err, err.response.data.error))
            
        },
        onFileChange(file) {
            this.file = file
        }        
    }
}
</script>