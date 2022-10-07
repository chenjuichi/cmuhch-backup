<template>
  <v-app id="toster">
    <div class="wrap">
        <div class="block"> 
          {{ content.body }}
          <v-btn icon :color="icon_color" @click="remove">
            <v-icon dark>mdi-close-circle</v-icon>
          </v-btn>                 
        </div>
    </div>  
  </v-app>
</template>

<script>

export default {
  name: 'Toaster',

  props: [
    'Title', 'Type', 'Body', 'Timeout' 
  ],

  mounted() {
    //this.initTimer();
    this.root = document.documentElement;
  },

  data() {
    return {
      timer: null,
      time: 2,
      show: true,
      icon_color: 'primary',

      defaults: {
        title: 'undefined title',
        body: 'undefined body',
        timeout: 5 
      },

      //content: [],
      content: {
        title: '',
        type: '',
        body: '',
        timeout: 0,
      },
    };
  },

  watch: {
    'content.type': function () {
      if (this.content.type=='info') {
        this.root.style.setProperty("--bg", "#008184");
        this.root.style.setProperty("--text", "#ffffff");
        this.icon_color="#ffffff"
      }
      if (this.content.type=='error') {
        this.root.style.setProperty("--bg", "#f5c0d0");
        this.root.style.setProperty("--text", "#000000");
        this.icon_color="#adadad"
      }
    }  
  },

  created() {
    //console.log("1 toster:", this.Body)
    this.content.title=this.Title;
    this.content.type=this.Type;
    this.content.body=this.Body;
    //console.log("2 toster:", this.content.body)
    this.content.timeout=parseInt(this.Timeout);    
    //this.add({ title: this.Title, type: this.Type, body: this.Body, timeout: parseInt(this.Timeout) })
  },

  beforeDestroy () {
    //clearInterval(this.timer);
  },

  methods: {
    initTimer() {
      //this.time=3;
      this.timer=setInterval(this.countdown, 1000);
    },

    countdown() {
      //this.time--;
      this.timeout--;
      //if (this.time==0) {
      if (this.timeout==0) {
        clearInterval(this.timer);
        //this.show=false;
        this.remove(0);
      }
    },

    add(params) {
      params.created = Date.now();
      //params.id = Math.random();
      params.id = 0;

      //console.log("toaster params: ", params);
      
      //params.expire = setTimeout(() => {this.remove(params.id);}, params.timeout * 1000);
      //params.expire = setTimeout(() => {this.countdown();}, params.timeout * 1000);

      console.log("params: ", params)
      this.content = Object.assign({}, params);
    },

    remove() {
      //this.content = {};
      this.$emit('removeToaster', false);  
    },

    //index(id) {
    //  for (let key in this.content) {
    //    if (id === this.content.id) {
    //      return key;
    //    }
    //  }
    //},
    /*
    type(type) {
      switch (type) {
        case 'error':
          return 'error';
        case 'success':
          return 'success';
        case 'info':
          return 'info';
      }
    },
    */
  },
};
</script>

<style scoped>

:root {
  --bg: #ffc1b0;
  --text: #000000
}

#toster {
  position: relative;
  display: block;
  font-size: 1rem; 
  height: 42px;
}

.wrap {
  width: 300px;
  overflow: hidden;
  float: left;
  border-radius: 0 5px 0 5px;
}

.block {
  text-align: center;
  font-weight: 600;
  color: var(--text);
  background-color: var(--bg);
  margin: 0;
  top: 50%;
}
</style>