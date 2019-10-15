<template>
    <user-detail :user="data"/>
</template>


<script>


import UserDetail from './UserDetail.vue'

export default {
    name: 'user-detail-dialog',
    components: {
        UserDetail,
    },
    props: {
        user: {
            type: Object,
            required: true
        },
    },
    data: function() {
        console.log(this)
        return {
            'data': this.user,
            dialog: false,
        }
    }
}
</script>