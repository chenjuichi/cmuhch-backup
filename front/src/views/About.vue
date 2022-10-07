<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>
import axios from "axios";

export default {
  components: {},

  data() {
    return {};
  },

mounted () {

},

  created() {
    console.log("About, created()");

    let currentIP = window.location.host;
    currentIP = currentIP.slice(0, currentIP.lastIndexOf(":"));
    console.log("host: current ip:", currentIP);

    this.url_host = currentIP + ":8060";
    this.host = currentIP + ":5050";

    this.protocol = window.location.protocol;
    axios.defaults.baseURL = this.protocol + "//" + this.host;
    axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest"; //add, 確認request是否為XHR(XML Http Request)或者是正常的请求
    console.log("axios base data: ", this.protocol + "//" + this.host);

    this.getSelectData();
  },

  mounted() {
    console.log("About, mounted()");
  },

  computed: {},

  methods: {
    getSelectData() {
      const path = "/api/list-select";
      console.log("Axios get data test...", path);
      axios
        .get(path)
        .then((res) => {
          console.log("GET ok, Area table total records:", res.data.status);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

