export default {

    methods: {
        async getLanguages() {
            return await window.axios.get('/xhr/admin/languages/');
        },
        async getlanguages() {
            return await window.axios.get('/xhr/admin/languages/');
        },
        async addLanguage(language) {
            return await window.axios.post('/xhr/admin/languages/', language)
        },
        async updateLanguage(language) {
            return await window.axios.put(
            `/xhr/admin/languages/${language.id}/`,language)
        },
        async deletelanguage(language) {
            return await window.axios.delete(
            `/xhr/admin/languages/${language.id}/`)
        },

    }
}