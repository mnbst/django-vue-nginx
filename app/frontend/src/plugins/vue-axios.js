const VueAxiosPlugin = {};

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie) {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

export default VueAxiosPlugin.install = function (Vue, {axios}) {
    const csrf_token = getCSRFToken();
    axios.defaults.headers.common = {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRF-Token": csrf_token
    };
    Vue.axios = axios;
    Object.defineProperties(Vue.prototype, {
        axios: {
            get() {
                return axios
            }
        }
    })
}
