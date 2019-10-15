export default {

    methods: {
        async getUsers() {
            return await window.axios.get('/xhr/admin/users/');
        },
        async getUser(user) {
            return await window.axios.get(`/xhr/admin/users/${user}/`)
        },
        async addUser(user) {
            return await window.axios.post('/xhr/admin/users/', user)
        },
        async updateUser(user) {
            user = Object.assign({}, user)
            user.languages = user.languages.map(l => l)

            return await window.axios.put(
                `/xhr/admin/users/${user.id}/`,user)
        },
        async deleteUser(user) {
            return await window.axios.delete(
                `/xhr/admin/users/${user.id}/`)
        },

        async getUserTranslationTasks(user) {
            return await window.axios.get(
                `/xhr/admin/users/${user}/translation-tasks/`)
        }
    }
}