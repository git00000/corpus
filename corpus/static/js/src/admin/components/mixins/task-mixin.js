export default {

    methods: {

        async getTranslationTasks() {
            return await window.axios("/xhr/admin/translation-tasks/")
        },
        async createTranslationTask(requestData)
        {   
            console.log(requestData)

            /**
            request data form exmaple: {
                'source_language': 2,
                'target_language': 4,
                'user': 4,
                'end_at': "2019-03-15",

                'word_count': 123,
                'size_short': true,
                'size_medium': true,
                'size_long': false,
            }
             */
            let fd = new FormData()
            for(let prop in requestData)
            {
                if(requestData.hasOwnProperty(prop))
                {
                    fd.set(prop, requestData[prop])
                }
            }
        
            return await window
                            .axios
                            .post('/xhr/admin/translation-tasks/', fd, {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
            });
        },
        async getUntranslatedPhraseCount(requestData)
        {
            /**
                request format:
                {
                    source_language: 1, // source language id
                    target_language: 3, // target language id
                    size_short: true,
                    size_medium: false,
                    size_long: true
                }

                response format:
                {
                    source_language: {id: 1, name: 'french', code: 'fr'},
                    target_language: {id: 2, name: 'english', code: 'en'},
                    bilingual_users: [{id: 2, enamil: 'example@gmail.com'}, ...],
                    phrase_count: 1234,
                    total_word_count: 1234,
                } 
             */
            console.log(requestData)
            let fd = new FormData()
            for(let prop in requestData)
            {
                if(requestData.hasOwnProperty(prop))
                {
                    fd.set(prop, requestData[prop])
                }
            }

            return await window
                            .axios
                            .post('/xhr/admin/untranslated-phrases/', fd, {
                                headers: {
                                    'Content-Type': 'application/json'
                                }
                            });
        },
    }
}