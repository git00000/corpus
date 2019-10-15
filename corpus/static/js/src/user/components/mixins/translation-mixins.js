export default {
    methods: {
        async getTranslationTaskNextItem(task,next='current') {
            let fd = new FormData()
            fd.set('id', task)
            fd.set('next', next)

            return await window.axios.post(`/xhr/user/translation-task-next-item/`, fd, {
                'Content-type': 'application/json'
            })
        },

        async savePhrase(item, language_as, text, completed) {
            /*
             request data format:
                {
                    item: 23, # the translation task item id
                    language_as: "source" | "target", # phrase is source
                    text: "Hello world",
                    item_completed: true, # whetheir the task item is completed or not
                }
            */

            console.log(completed)
            let fd = new FormData()
            fd.set('item', item)
            fd.set('item_completed', completed)
            fd.set('language_as', language_as)
            fd.set('text', text)

            return await window.axios.post("/xhr/user/save-translation-task-item-phrase/", fd, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        }
    }
}