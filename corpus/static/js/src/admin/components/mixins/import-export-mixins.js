export default {
    methods: {
        async do_export(source_language, target_language, export_as) {
            let fd = new FormData()
            fd.set('source_language', source_language)
            fd.set('target_language', target_language)
            fd.set('export_as', export_as)
            return await window.axios.post('/xhr/admin/import-export/export/', fd, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
        },

        async do_import(source_language, target_language, file)
        {
            let fd = new FormData()
            fd.set('source_language', source_language)
            fd.set('target_language', target_language)
            fd.set('file', file)

            return await window.axios.post('/xhr/admin/import-export/import/', fd, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
        },
    }
}