
import axios from 'axios'

export default {
    data: function () {
      return {
        _host: '',
        _protocol: '',

        modalbox_color: false,
        temp_css: '',
        //temp_css: 'add_modalbox',

        /*
        _payload: {
          topic: '',
          layout: temp_layout,
          led: temp_pos,
          msg: ''
        },

        _path: '',
        */
      }
    },

    methods: {
      initAxios: function() {
        let _host=window.location.host;
        _host = _host.slice(0, _host.lastIndexOf(":"));
        let _protocol=window.location.protocol;
        axios.defaults.baseURL = _protocol + "//"+ _host + ':5050';     //for backend server
        axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';   //確認request是否為XHR(XML Http Request)或者是正常的请求

        //axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
        //axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
        //axios.defaults.headers.post['Content-Type'] = 'text/plain';

        console.log("from mixin: axios baseURL: ", _protocol + "//"+ _host + ':5050');
      }
    }
}

