<template>
<v-app>
  <div class="container_tab" style="width: 900px; padding: 10px; border-radius: 10px;">
    <div
      class="dot"
      :id="`light_${index}`"
      style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
      v-for="(n, index) in 30"
    ></div>
  </div>
  <div v-show="isShow"
    class="temp_text"
    v-for="field in segments" :key="field.id"
    :style="styleObject"
    @mouseover="hover = true"
    @mouseleave="hover = false">
    <span v-show="hover">
      LED{{ field.range0 }} 至 LED{{ field.range1 }}
    </span>
    <div class="v22">
      <TempText :myText="field" @closeTempText="getComp"></TempText>
      <div class="vl" :style="styleLeft"></div>
    </div>
  </div>
  <v-row>
    <v-col class="px-4" cols="12" md="1"></v-col>
    <v-col class="pl-6 pr-2" cols="12" md="10">
      <v-range-slider
        v-model="range"
        @click="eraseErrMsg"
        :max="max"
        :min="min"
        hide-details
        class="align-center">
        <template v-slot:prepend>
          <v-text-field
            :value="range[0]"
            :max="max"
            :min="min"
            @focus="eraseErrMsg"
            class="mt-0 pt-0"
            v-model="range[0]"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            @change="$set(range, 0, $event)"
          ></v-text-field>
        </template>
        <template v-slot:append>
          <v-text-field
            :value="range[1]"
            :max="max"
            :min="min"
            class="mt-0 pt-0"
            v-model="range[1]"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            @focus="eraseErrMsg"
            @change="$set(range, 1, $event)"
          ></v-text-field>
        </template>
      </v-range-slider>
      <small class="msgErr" v-text= "rangErrMsg"></small>
    </v-col>
    <v-col class="pr-4 pl-0" cols="12" md="1">
      <v-btn
        small
        class="ml-0 mr-2 mt-2"
        color="primary"
        @click="toggleLed()">
        <v-icon>mdi-gesture-tap</v-icon>
      </v-btn>
    </v-col>
  </v-row>
</v-app>
</div>
</template>

<script>
import TempText from './TempText.vue'

export default {
  name: 'LedStrip',
  /* 說明
  temp_text: seg_text_s1_l1, seg_text_s1_l2,....
  light_:    seg_light_s1_l1_, seg_light_s1_l2_,...
  type:
  */
  components: {
    TempText: TempText,
  },

  props: ['ledStrip'],

  mounted() {
  },

  data() {
    return {
      rangErrMsg: '',
      min: 1,
      max: 30,
      range: [1, 3],
      Leds: [],

      isShow: false,
      segments: [],
      segment_width: 56,
      light_width: 29,
      init_id: 1,
      hover: false,

      styleObject: {
        marginRight: 56 + 'px', //init margin-right value
        marginLeft: 56 + 'px',  //init margin-left value
      },

      styleLeft: {
        left: 29 + 'px',        //init left value
      },
    };
  },

  computed: {
  },

  watch: {
  },

  created () {
    this.Leds=[];
    for (let i=0; i<this.max; i++) {
      this.Leds.push(false)
    }
  },

  methods: {
    getComp() {
      let el = document.getElementsByClassName('temp_text').length;
      for (let i=0; i< el; i++) {
        let el = document.getElementsByClassName('temp_text')[i]
        el.style['margin-left'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
        el.style['margin-right'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
        el.getElementsByClassName('v22')[0].childNodes[1].style['left']= (29 * this.segments[i].size -39) / 2 + 'px';
      }
    },

    toggleLed() {
      this.rangErrMsg='';
      let temp_seg_size=this.segments.length;
      let r0=this.range[0];
      let r1=this.range[1];
//檢查資料的正確性
      if (this.range[0] > this.range[1]) {
        this.rangErrMsg='格位資料設定錯誤!'
        return;
      }
      for (let i=0; i<temp_seg_size; i++) {
        if ((r0 > this.segments[i].range0 && r0 < this.segments[i].range1) ||
            (r1 > this.segments[i].range0 && r1 < this.segments[i].range1) ||
            (r0 == this.segments[i].range0 && r1 > this.segments[i].range1) ||
            (r1 == this.segments[i].range1 && r0 < this.segments[i].range0)) {
          this.rangErrMsg='格位資料設定錯誤!'
          return;
        }
      }
//檢查是否power off Led
      for (let i=0; i<temp_seg_size; i++) {
        if (this.range[0] == this.segments[i].range0 && this.range[1] == this.segments[i].range1) {
          poweroffLed(this.range[0], this.range[1]);
          return
        }
      }

      let temp_size=this.range[1] - this.range[0]+1;
      let obj= {
        id: this.init_id,
        text:this.init_id.toString(),
        size: temp_size,
        type: 'station1',
        range0: this.range[0],
        range1: this.range[1],
      }
      this.segments.push(obj);

      this.init_id++;

      this.isShow = true;

      for (let i=this.range[0]-1; i<this.range[1]; i++) {
        let dot = document.getElementById("light_" + i);
        this.Leds[i]= !this.Leds[i];
        let temp_togg= this.Leds[i] ? (dot.className += " on") : (dot.className = "dot");
      }
    },

    poweroffLed(r0, r1) {
      for (let i=r0-1; i<r1; i++) {
        let dot = document.getElementById("light_" + i);
        this.Leds[i]= !this.Leds[i];
        let temp_togg= this.Leds[i] ? (dot.className += " on") : (dot.className = "dot");
      }

      this.segments = this.segments.filter(function( obj ) {
        return !(obj.range0==r0 && obj.range1==r1);
      });
      let temp_id=1;
      for (const obj of this.segments) {
        obj.id = temp_id;
        obj.text=temp_id.toString(),
        temp_id++;
      }
      this.init_id=temp_id;
      this.isShow = (this.segments.length !=0) ? true:false;
    },

    eraseErrMsg() {
      console.log("range data error...")
      this.rangErrMsg='';
    },
  },
}
</script>

<style lang="scss" scoped>

@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

div.v-toolbar__title {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

.v22 {
  display: flex;
  height: 22px;
}

.vl {
  border-left: 2px solid green;
  height: 22px;
  position: relative;
  left: 12px
}

.temp_text {
  position: relative;
  left: 50px;
  top: 5px;
  display: inline-block;
  font-size: 10px;
  border-radius: 20px;
  background: red;

  padding: 0 10px 0 10px;
  //margin: 0 15px 0 15px;
  margin-top: 0;
  margin-bottom: 0;
}

.led_segment {
  display: inline-block;
}

.container_tab  {
  background: #666;
  overflow: hidden;
  margin: auto;
  font-size: 0;
}

.dot {
  display: inline-block;
  font-size: 0px;
  line-height: 0;
  border-radius: 50%;
  background: #444;
  box-shadow: inset 0px 0px 10px 5px #303030;
  position:relative;
}
.dot::after{
  content:' ';
  position:absolute;
  background-color:rgba(255,255,255,1);
  border-radius:50%;
  width:15px;
  height:15px;
  right:4px;
  bottom:4px;
  background-image: radial-gradient(center, circle closest-side, #777, #333);
  background-image: -o-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -ms-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -moz-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -webkit-radial-gradient(center, circle closest-side, #777, #333);
}
.on {
  background: #fff;
  box-shadow: 0px 0px 20px 3px #fcfcaa, inset 0px 0px 13px #777;
}
.on::after{
  display:none;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}
</style>