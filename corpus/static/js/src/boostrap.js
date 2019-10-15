

window.Vue = require('vue').default

/**
 * We'll load the axios HTTP library which allows us to easily issue requests
 * to our Laravel back-end. This library automatically handles sending the
 * CSRF token as a header based on the value of the "XSRF" token cookie.
 */

window.axios = require('axios');
window.axios.defaults.xsrfCookieName = 'csrftoken'
window.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

/**
 * Next we will register the CSRF Token as a common header with Axios so that
 * all outgoing HTTP requests automatically have it attached. This is just
 * a simple convenience so we don't have to attach every token manually.
 */

let token = document.head.querySelector('meta[name="csrf-token"]');

if (token) {
    window.axios.defaults.headers.common['X-CSRFTOKEN'] = token.content;
} else {
    console.error('CSRF token not found: https://laravel.com/docs/csrf#csrf-x-csrf-token');
}

// Helper for url reversing
window.corpus  = {} 
window.corpus.urlPathReverse = async (path) => {
    // replace the : with _ for endpoint compatibility
    path = path.replace(':', '_')
    try {
        const response = await window.axios.get('/xhr/url-service/path-reverse/' + path + '/')
        return response.data.url
      } catch (error) {
        console.error(error);
      }
} 