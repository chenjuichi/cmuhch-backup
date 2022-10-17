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
    //this.root = document.documentElement;
  },

  data() {
    return {
      timer: null,
      
      icon_color: 'primary',

      //content: [],
      content: {
        title: '',
        type: '',
        body: '',
        timeout: 3,
      },
      defaultContent: {
        title: 'Hello',
        type: '',
        body: '',
        timeout: 3,
      },
    };
  },

  watch: {
    'content.type': function () {
      console.log("tost type: ", this.content.type, (this.content.type=="info"))
      let bg = this.content.type=="info" ? "#008184" : "#f5c0d0";
      let txtColor = this.content.type=="info" ? "#ffffff" : "#000000";
      let iconColor = this.content.type=="info" ? "#ffffff" : "#adadad";

      document.documentElement.style.setProperty("--bg", bg);
      document.documentElement.style.setProperty("--txt", txtColor);
      this.icon_color = iconColor
      /*
      let th=this;
      console.log("toaster type: ", th.content.type);
      if (th.content.type=='info') {
        document.documentElement.style.setProperty("--bg", "#008184");
        document.documentElement.style.setProperty("--text", "#ffffff");
        th.icon_color="#ffffff"
      }
      if (th.content.type=='error') {
        document.documentElement.style.setProperty("--bg", "#f5c0d0");
        document.documentElement.style.setProperty("--text", "#000000");
        th.icon_color="#adadad"
      }
      */
    }  
  },

  created() {
    this.content.title=this.Title;

    this.content.type=this.Type;
    this.content.body=this.Body;
    
    this.content.timeout=parseInt(this.Timeout);    
  },

  beforeDestroy () {
    clearInterval(this.timer);  //取消setInterval所重複執行的動作
  },

  methods: {
    initTimer() { 
      this.timer=setInterval(this.countdown, 1000); //定期(每秒)去執行countdown
    },

    countdown() {
      this.content.timeout--;

      if (this.content.timeout == 0) {
        clearInterval(this.timer);
        this.remove();
      }
    },

    remove() {
      this.content = Object.assign({}, this.defaultContent);
      this.$emit('removeToaster', false);  
    },
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
  color: var(--text) !important;
  background-color: var(--bg) !important;
  margin: 0;
  top: 50%;
}
</style>