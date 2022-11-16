<template>
<!--<v-app>-->
  <!--<v-card outlined width="75vw" class="mt-1 mx-auto">-->
    <v-card-text id="app_tab_1" style="padding-top: 8px;">
      <!-- seg1 -->
      <div class="container_tab1" style="width: 885px; padding: 0px 5px 0px 5px; border-radius: 10px; height:55px;">
        <div style="color: white; font-size: 14px; text-align: center;">
          <p
            v-for="field in selectedLeds.led1"
            style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;"
            v-model="field.value">
            {{ field.value }}
          </p>
        </div>
        <div
          class="dot"
          :id="`light_${index}`"
          style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
          v-for="(n, index) in 30"
        ></div>
      </div>

      <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
        <v-col class="px-1" cols="12" md="1"
          style="text-align: right; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位寬度</v-col>

        <v-col class="px-2" cols="12" md="8">
          <v-range-slider
            v-model="ranges.range1"
            @click="eraseErrMsg(0)"
            :max="max"
            :min="min"
            hide-details
            class="align-center"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.range1[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(0)"
                class="mt-0 pt-0"
                v-model="ranges.range1[0]"
                hide-details
                single-line
                type="number"
                style="width: 40px"
                @change="$set(ranges.range1, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.range1[1]"
                :max="max"
                :min="min"
                class="mt-0 pt-0"
                v-model="ranges.range1[1]"
                hide-details
                single-line
                type="number"
                style="width: 40px"
                @focus="eraseErrMsg(0)"
                @change="$set(ranges.range1, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
          <small class="msgErr" v-text= "errorMessages.message1"></small>
        </v-col>

        <v-col class="px-0" cols="12" md="1"
          style="text-align: center; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位編號</v-col>

        <v-col class="mt-1 px-0" cols="12" md="1">
              <v-text-field
                :value="segment_values[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(0)"
                class="mt-0 pt-0 centered-input"
                v-model="segment_values[0]"
                hide-details
                single-line
                type="number"
                style="width: 50px; border-radius: 5px; border: 1px solid #000000;"
              ></v-text-field>
        </v-col>
        <v-col class="mt-1 pr-2 pl-0" cols="12" md="1">
          <v-btn
            small
            class="ml-0 mr-2 mt-1"
            color="primary"
            @click="toggleLed(0)">
            <v-icon>mdi-gesture-tap</v-icon>
            設定
          </v-btn>
        </v-col>
        <!--<v-col class="px-4" cols="12" md="1"></v-col>-->
      </v-row>

      <!-- seg2 -->

      <div class="container_tab1" style="width: 885px; padding: 0px 5px 0px 5px; border-radius: 10px; height:55px;">
        <div style="color: white; font-size: 14px; text-align: center;">
          <p
            v-for="field in selectedLeds.led2"
            style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;"
            v-model="field.value">
            {{ field.value }}
          </p>
        </div>
        <div
          class="dot"
          :id="`light_${index}`"
          style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
          v-for="(n, index) in 30"
        ></div>
      </div>

      <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
        <v-col class="px-1" cols="12" md="1"
          style="text-align: right; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位寬度</v-col>

        <v-col class="px-2" cols="12" md="8">
          <v-range-slider
            v-model="ranges.range2"
            @click="eraseErrMsg(1)"
            :max="max"
            :min="min"
            hide-details
            class="align-center"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.range2[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(1)"
                class="mt-0 pt-0"
                v-model="ranges.range2[0]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.range2, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.range2[1]"
                :max="max"
                :min="min"
                class="mt-0 pt-0"
                v-model="ranges.range2[1]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @focus="eraseErrMsg(1)"
                @change="$set(ranges.range2, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
          <small class="msgErr" v-text= "errorMessages.message2"></small>
        </v-col>

        <v-col class="px-0" cols="12" md="1"
          style="text-align: center; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位編號</v-col>

        <v-col class="mt-1 px-0" cols="12" md="1">
              <v-text-field
                :value="segment_values[1]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(1)"
                class="mt-0 pt-0 centered-input"
                v-model="segment_values[1]"
                hide-details
                single-line
                type="number"
                style="width: 50px; border-radius: 5px; border: 1px solid #000000;"
              ></v-text-field>
        </v-col>
        <v-col class="mt-1 pr-2 pl-0" cols="12" md="1">
          <v-btn
            small
            class="ml-0 mr-2 mt-1"
            color="primary"
            @click="toggleLed(1)">
            <v-icon>mdi-gesture-tap</v-icon>
            設定
          </v-btn>
        </v-col>
        <!--<v-col class="px-4" cols="12" md="1"></v-col>-->
      </v-row>

      <!-- seg3 -->

      <div class="container_tab1" style="width: 885px; padding: 0px 5px 0px 5px; border-radius: 10px; height:55px;">
        <div style="color: white; font-size: 14px; text-align: center;">
          <p
            v-for="field in selectedLeds.led3"
            style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;"
            v-model="field.value">
            {{ field.value }}
          </p>
        </div>
        <div
          class="dot"
          :id="`light_${index}`"
          style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
          v-for="(n, index) in 30"
        ></div>
      </div>

      <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
        <v-col class="px-1" cols="12" md="1"
          style="text-align: right; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位寬度</v-col>

        <v-col class="px-2" cols="12" md="8">
          <v-range-slider
            v-model="ranges.range3"
            @click="eraseErrMsg(2)"
            :max="max"
            :min="min"
            hide-details
            class="align-center"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.range3[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(2)"
                class="mt-0 pt-0"
                v-model="ranges.range3[0]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.range3, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.range3[1]"
                :max="max"
                :min="min"
                class="mt-0 pt-0"
                v-model="ranges.range3[1]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @focus="eraseErrMsg(2)"
                @change="$set(ranges.range3, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
          <small class="msgErr" v-text= "errorMessages.message3"></small>
        </v-col>

        <v-col class="px-0" cols="12" md="1"
          style="text-align: center; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位編號</v-col>

        <v-col class="mt-1 px-0" cols="12" md="1">
              <v-text-field
                :value="segment_values[2]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(0)"
                class="mt-0 pt-0 centered-input"
                v-model="segment_values[2]"
                hide-details
                single-line
                type="number"
                style="width: 50px; border-radius: 5px; border: 1px solid #000000;"
              ></v-text-field>
        </v-col>
        <v-col class="mt-1 pr-2 pl-0" cols="12" md="1">
          <v-btn
            small
            class="ml-0 mr-2 mt-1"
            color="primary"
            @click="toggleLed(2)">
            <v-icon>mdi-gesture-tap</v-icon>
            設定
          </v-btn>
        </v-col>
        <!--<v-col class="px-4" cols="12" md="1"></v-col>-->
      </v-row>

      <!-- seg4 -->

      <div class="container_tab1" style="width: 885px; padding: 0px 5px 0px 5px; border-radius: 10px; height:55px;">
        <div style="color: white; font-size: 14px; text-align: center;">
          <p
            v-for="field in selectedLeds.led4"
            style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;"
            v-model="field.value">
            {{ field.value }}
          </p>
        </div>
        <div
          class="dot"
          :id="`light_${index}`"
          style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
          v-for="(n, index) in 30"
        ></div>
      </div>

      <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
        <v-col class="px-1" cols="12" md="1"
          style="text-align: right; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位寬度</v-col>
        <v-col class="px-2" cols="12" md="8">
          <v-range-slider
            v-model="ranges.range4"
            @click="eraseErrMsg(3)"
            :max="max"
            :min="min"
            hide-details
            class="align-center"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.range4[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(3)"
                class="mt-0 pt-0"
                v-model="ranges.range4[0]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.range4, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.range4[1]"
                :max="max"
                :min="min"
                class="mt-0 pt-0"
                v-model="ranges.range4[1]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @focus="eraseErrMsg(3)"
                @change="$set(ranges.range4, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
          <small class="msgErr" v-text= "errorMessages.message4"></small>
        </v-col>

        <v-col class="px-0" cols="12" md="1"
          style="text-align: center; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位編號</v-col>

        <v-col class="mt-1 px-0" cols="12" md="1">
              <v-text-field
                :value="segment_values[3]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(0)"
                class="mt-0 pt-0 centered-input"
                v-model="segment_values[3]"
                hide-details
                single-line
                type="number"
                style="width: 50px; border-radius: 5px; border: 1px solid #000000;"
              ></v-text-field>
        </v-col>
        <v-col class="mt-1 pr-2 pl-0" cols="12" md="1">
          <v-btn
            small
            class="ml-0 mr-2 mt-1"
            color="primary"
            @click="toggleLed(3)">
            <v-icon>mdi-gesture-tap</v-icon>
            設定
          </v-btn>
        </v-col>
        <!--<v-col class="px-4" cols="12" md="1"></v-col>-->
      </v-row>

      <!-- seg5 -->

      <div class="container_tab1" style="width: 885px; padding: 0px 5px 0px 5px; border-radius: 10px; height:55px;">
        <div style="color: white; font-size: 14px; text-align: center;">
          <p
            v-for="field in selectedLeds.led5"
            style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;"
            v-model="field.value">
            {{ field.value }}
          </p>
        </div>
        <div
          class="dot"
          :id="`light_${index}`"
          style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
          v-for="(n, index) in 30"
        ></div>
      </div>

      <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
        <v-col class="px-1" cols="12" md="1"
          style="text-align: right; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位寬度</v-col>
        <v-col class="px-2" cols="12" md="8">
          <v-range-slider
            v-model="ranges.range5"
            @click="eraseErrMsg(4)"
            :max="max"
            :min="min"
            hide-details
            class="align-center"
          >
            <template v-slot:prepend>
              <v-text-field
                :value="ranges.range5[0]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(4)"
                class="mt-0 pt-0"
                v-model="ranges.range5[0]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(ranges.range5, 0, $event)"
              ></v-text-field>
            </template>
            <template v-slot:append>
              <v-text-field
                :value="ranges.range5[1]"
                :max="max"
                :min="min"
                class="mt-0 pt-0"
                v-model="ranges.range5[1]"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @focus="eraseErrMsg(4)"
                @change="$set(ranges.range5, 1, $event)"
              ></v-text-field>
            </template>
          </v-range-slider>
          <small class="msgErr" v-text= "errorMessages.message5"></small>
        </v-col>

        <v-col class="px-0" cols="12" md="1"
          style="text-align: center; line-height: 42px; font-size: 14px; font-weight: 600;"
        >格位編號</v-col>

        <v-col class="mt-1 px-0" cols="12" md="1">
              <v-text-field
                :value="segment_values[4]"
                :max="max"
                :min="min"
                @focus="eraseErrMsg(0)"
                class="mt-0 pt-0 centered-input"
                v-model="segment_values[4]"
                hide-details
                single-line
                type="number"
                style="width: 50px; border-radius: 5px; border: 1px solid #000000;"
              ></v-text-field>
        </v-col>
        <v-col class="mt-1 pr-2 pl-0" cols="12" md="1">
          <v-btn
            small
            class="ml-0 mr-2 mt-1"
            color="primary"
            @click="toggleLed(4)">
            <v-icon>mdi-gesture-tap</v-icon>
            設定
          </v-btn>
        </v-col>
        <!--<v-col class="px-4" cols="12" md="1"></v-col>-->
      </v-row>
    </v-card-text>
  <!--</v-card>-->
<!--</v-app>-->
</template>

<script>
export default {
  name: 'LedStrip',

  props: {
    my_object: {
      type: Object,
      default: () => ({
        segs: {
          segments1: [],
          segments2: [],
          segments3: [],
          segments4: [],
          segments5: [],
        },
        rans: {
          range1: [],
          range2: [],
          range3: [],
          range4: [],
          range5: [],
        },
      }),
      required: true,
    },
    my_key:{
      type: Number,
    }
  },

  mounted() {
    //this.$emit('closeLedStrip', this.my_key, this.temp_segments);
  },

  data() {
    return {
      //time: 99,

      min: 1,
      max: 30,

      errorMessages: {  //for 錯誤訊息
        message1: '',
        message2: '',
        message3: '',
        message4: '',
        message5: '',
      },
      ranges: {     //for slider輸入範圍
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab1_rans: {
        //range1: [],
        //range2: [],
        //range3: [],
        //range4: [],
        //range5: [],
      },
      segment_values: [], //for輸入segment代號
      selectedLeds: {   //for顯示數字或'.' , 共30組
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },
      selectedLamps: {  //for顯示Led燈號
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },
      segments: {     //for在各segment內的值
        segment1: [
      //  seg_id:,
      //  range0:,
      //  range1:,
        ],
        segment2: [],
        segment3: [],
        segment4: [],
        segment5: [],
      },
      tab1_segs: {
        //segments1: [],
        //segments2: [],
        //segments3: [],
        //segments4: [],
        //segments5: [],
      },

      temp_segments: {     //for在各segment內的值
        segment1: [],
        segment2: [],
        segment3: [],
        segment4: [],
        segment5: [],
      },

      load_SingleTable_ok: false, //for get grids table data
      slider_data_ok: false,      //for update slider area data
      slider_led_dig_ok: false,   //for update slider led number
      slider_led_lamp_ok: false,  //for update slider led lamp

      new_lamp_seg: 0,
    }
  },

  computed: {
  },

  watch: {
    my_object: {
      handler: function (newVal, oldVal) {
          if (newVal) {
            this.tab1_segs=newVal.segs;
            this.tab1_rans=newVal.rans;
            console.log("LedStrip, watch(), newVal: ", newVal, this.tab1_segs);
            //console.log("LedStrip, watch(), tab1_rans and segments1: ", this.tab1_rans, this.tab1_rans.range1);
            this.slider_data_ok = true;
            //return newVal;
          }
          //return oldVal;
      },
      deep: true,
      //immediate: true,
    },

    slider_data_ok(val) {
      if (val) {
        console.log("LedStrip, watch, slider_data_ok() ...");

        this.slider_data_ok=false;

        this.ranges.range1 = Object.assign([], this.tab1_rans.range1);
        this.ranges.range2 = Object.assign([], this.tab1_rans.range2);
        this.ranges.range3 = Object.assign([], this.tab1_rans.range3);
        this.ranges.range4 = Object.assign([], this.tab1_rans.range4);
        this.ranges.range5 = Object.assign([], this.tab1_rans.range5);

        //init '在各segment內的值'
        let seg_len =this.tab1_segs.segments1.length;   //seg1
        //console.log("LedStrip, segment1: ", this.my_key, seg_len, this.tab1_segs.segments1);

        this.segments.segment1 = [];
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments1[i][key] :", i, this.tab1_segs.segments1[i]);
          let obj= {
            grid_station: this.tab1_segs.segments1[i].grid_station,
            grid_layout: this.tab1_segs.segments1[i].grid_layout,
            seg_id: parseInt(this.tab1_segs.segments1[i].seg_id),
            range0: this.tab1_segs.segments1[i].range0,
            range1: this.tab1_segs.segments1[i].range1,
          }
          this.segments.segment1.push(obj);
        }

        seg_len =this.tab1_segs.segments2.length;    //seg2
        //console.log("LedStrip, segment2: ", this.my_key, seg_len);

        this.segments.segment2 = [];
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments2[i][key] :", i, this.tab1_segs.segments2[i]);
          let obj= {
            grid_station: this.tab1_segs.segments2[i].grid_station,
            grid_layout: this.tab1_segs.segments2[i].grid_layout,
            seg_id: parseInt(this.tab1_segs.segments2[i].seg_id),
            range0: this.tab1_segs.segments2[i].range0,
            range1: this.tab1_segs.segments2[i].range1,
          }
          this.segments.segment2.push(obj);
        }
        //console.log("LedStrip, segment2: ", this.segments.segment2);

        seg_len =this.tab1_segs.segments3.length;    //seg3
        //console.log("LedStrip, segment3: ", this.my_key, seg_len);
        this.segments.segment3 = [];
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments3[i][key] :", i, this.tab1_segs.segments3[i]);
          let obj= {
            grid_station: this.tab1_segs.segments3[i].grid_station,
            grid_layout: this.tab1_segs.segments3[i].grid_layout,
            seg_id: parseInt(this.tab1_segs.segments3[i].seg_id),
            range0: this.tab1_segs.segments3[i].range0,
            range1: this.tab1_segs.segments3[i].range1,
          }
          this.segments.segment3.push(obj);
        }
        //console.log("LedStrip, segment3: ", this.segments.segment3);

        seg_len =this.tab1_segs.segments4.length;    //seg4
        //console.log("LedStrip, segment4: ", this.my_key, seg_len);
        this.segments.segment4 = [];
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments4[i][key] :", i, this.tab1_segs.segments4[i]);
          let obj= {
            grid_station: this.tab1_segs.segments4[i].grid_station,
            grid_layout: this.tab1_segs.segments4[i].grid_layout,
            seg_id: parseInt(this.tab1_segs.segments4[i].seg_id),
            range0: this.tab1_segs.segments4[i].range0,
            range1: this.tab1_segs.segments4[i].range1,
          }
          this.segments.segment4.push(obj);
        }
        //console.log("LedStrip, segment4: ", this.segments.segment4);

        seg_len =this.tab1_segs.segments5.length; //seg5
        //console.log("LedStrip, segment5: ", this.my_key, seg_len);
        this.segments.segment5 = [];
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments5[i][key] :", i, this.tab1_segs.segments5[i]);
          let obj= {
            grid_station: this.tab1_segs.segments5[i].grid_station,
            grid_layout: this.tab1_segs.segments5[i].grid_layout,
            seg_id: parseInt(this.tab1_segs.segments5[i].seg_id),
            range0: this.tab1_segs.segments5[i].range0,
            range1: this.tab1_segs.segments5[i].range1,
          }
          this.segments.segment5.push(obj);
        }
        //console.log("LedStrip, segment5: ", this.segments.segment5);

        // init '輸入segment代號'的值
        this.segment_values[0]=!this.segments.segment1.length?"1":this.segments.segment1[0].seg_id;
        this.segment_values[1]=!this.segments.segment2.length?"1":this.segments.segment2[0].seg_id;
        this.segment_values[2]=!this.segments.segment3.length?"1":this.segments.segment3[0].seg_id;
        this.segment_values[3]=!this.segments.segment4.length?"1":this.segments.segment4[0].seg_id;
        this.segment_values[4]=!this.segments.segment5.length?"1":this.segments.segment5[0].seg_id;

        console.log("LedStrip, watch, slider_data_ok(), ", this.segments);

        this.slider_led_dig_ok=true;
      } //end if condition
    },  //slider_data_ok()

    slider_led_dig_ok(val) {
      if (val) {
        this.slider_led_dig_ok=false;

        for (let index=0; index<5; index++) {
          let seg_len =this.segments[Object.keys(this.segments)[index]].length;
          //reset 燈條所有數字
          for (let i=0; i<this.max; i++) {
            this.selectedLeds[Object.keys(this.selectedLeds)[index]][i].value = '.';
          }
          //有區段
          if (seg_len) {
            //console.log("segments, index, len: ", this.my_key, index, seg_len)
            for (let i=0; i<seg_len; i++) {
              let start_p=this.segments[Object.keys(this.segments)[index]][i].range0-1
              //console.log("segments dig(start_p, old, new): ", this.my_key, start_p, this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value, this.segments[Object.keys(this.segments)[index]][i].seg_id)
              this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = this.segments[Object.keys(this.segments)[index]][i].seg_id.toString();
            }
          }
        }

        this.slider_led_lamp_ok = true;
      } //end if condition
    },  //end slider_led_dig_ok()

    slider_led_lamp_ok(val) {
      if (val) {
        this.slider_led_lamp_ok = false;

        let els = document.getElementsByClassName('container_tab1');

        for (let index=0; index<5; index++) {
          let seg_len = this.segments[Object.keys(this.segments)[index]].length;
          //console.log("lamp data: ", this.my_key, index , seg_len);

          //熄滅燈條
          for (let j=0; j<this.max; j++) {
            let dot = els[index].childNodes[j+1];
            //console.log("dot data: ", dot);
            this.selectedLamps[Object.keys(this.selectedLamps)[index]][j].value = false;
            let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j].value ? (dot.className += " on") : (dot.className = "dot");
          }

          let current_segs = 0;
          if (seg_len) {
            do {
              let begin_p = parseInt(this.segments[Object.keys(this.segments)[index]][current_segs].range0)
              let end_p = parseInt(this.segments[Object.keys(this.segments)[index]][current_segs].range1)

              for (let j=begin_p; j<=end_p; j++) {
                let dot = els[index].childNodes[j];
                //console.log("dot data: ", dot);
                this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = true;
                let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
              }

              current_segs++;
            } while (current_segs < seg_len);
          }
        }
      }
    },  //end slider_led_lamp_ok()
  },

  created () {
    // init燈號數字資料
    let obj= {value: '.',}
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led1.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led2.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led3.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led4.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led5.push(obj);
    }

    // init燈號led資料
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led1.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led2.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led3.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led4.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led5.push(obj);
    }
    console.log("LedStrip, created() end...", this.my_key);
  },

  methods: {
    //input: errorMessages, segments, ranges, selectedLamps, segment_values, selectedLeds
    //output: errorMessages, segments, selectedLamps, selectedLeds
    toggleLed(index) {
      //init 常數的值
      this.errorMessages[Object.keys(this.errorMessages)[index]] = '';
      let temp_seg_size=this.segments[Object.keys(this.segments)[index]].length;
      let r0=this.ranges[Object.keys(this.ranges)[index]][0];   //新的range slider min值
      let r1=this.ranges[Object.keys(this.ranges)[index]][1];   //新的range slider min值
      let new_seg_val = parseInt(this.segment_values[index]);   //新的segment value值
      //console.log("hello, r0, r1, new_seg_val and temp_seg_size : ", r0, r1, new_seg_val, temp_seg_size);

      //檢查資料的正確性
      if (r0 > r1) {
        this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
        return;
      }

      for (let i=0; i<temp_seg_size; i++) {
        //console.log("hello, this.segments[Object.keys(this.segments)[index]][i].range0 : ", this.segments[Object.keys(this.segments)[index]][i].range0)
        //console.log("hello, this.segments[Object.keys(this.segments)[index]][i].range1 : ", this.segments[Object.keys(this.segments)[index]][i].range1)
        let old_seg_val = parseInt(this.segments[Object.keys(this.segments)[index]][i].seg_id);
        if ( (new_seg_val != old_seg_val) && (
          (r0 > this.segments[Object.keys(this.segments)[index]][i].range0 && r0 < this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r1 > this.segments[Object.keys(this.segments)[index]][i].range0 && r1 < this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r0 == this.segments[Object.keys(this.segments)[index]][i].range0 && r1 > this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r1 == this.segments[Object.keys(this.segments)[index]][i].range1 && r0 < this.segments[Object.keys(this.segments)[index]][i].range0))) {
          this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
          return;
        }

        //if ((new_seg_val == old_seg_val) &&
        //  ((r0 > this.segments[Object.keys(this.segments)[index]][i].range0 && r1 > this.segments[Object.keys(this.segments)[index]][i].range1))) {
        //  this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
        //  return;
        //}

      }

      let ch1=this.checkSegmentRange(index);
      let ch2=this.checkSegmentID(index);

      if (!ch1 && ch2) {  //更改range slider的值, segment value編號不變
        console.log("hello !ch1 && ch2..., 更改range slider, 但segment value不變")
        let obj = this.segments[Object.keys(this.segments)[index]].find(o => (parseInt(o.seg_id) == new_seg_val));
        //console.log("obj..., ", obj)

        let old_els = document.getElementsByClassName('container_tab1');
        for (let j=parseInt(obj.range0); j<parseInt(obj.range1)+1; j++) {
          //console.log("obj lamp point... ", j)

          let dot = old_els[index].childNodes[j];
          this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = false;
          let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");

          this.selectedLeds[Object.keys(this.selectedLeds)[index]][j-1].value = '.';
        }

        let new_els = document.getElementsByClassName('container_tab1');
        for (let j=r0; j<r1+1; j++) {
          let dot = new_els[index].childNodes[j];
          this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = true;
          let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
        }

        for (let i=0; i<this.segments[Object.keys(this.segments)[index]].length; i++) {
          let new_start_p = r0-1
          let old_start_p = parseInt(this.segments[Object.keys(this.segments)[index]][i].range0)-1
          //console.log("obj point, new, old..., ", new_start_p, old_start_p)

          //this.selectedLeds[Object.keys(this.selectedLeds)[index]][old_start_p].value = '.';
          this.selectedLeds[Object.keys(this.selectedLeds)[index]][new_start_p].value = new_seg_val;
        }

        obj.range0 = r0;
        obj.range1 = r1;

        this.temp_segments=Object.assign({}, this.segments);

        console.log("$emit object..., ", this.temp_segments)

        this.$emit('closeLedStrip', this.my_key, index, this.temp_segments);
        return;
      }

      if (ch1 && ch2) {  //range slider的值不變, segment value編號不變, 或該燈條都熄滅
        console.log("hello ch1 && ch2..., range slider, 及segment value不變");

        if (this.segments[Object.keys(this.segments)[index]].length == 0) {
          console.log("step1...");
          let obj= {
            seg_id: parseInt(this.segment_values[index]),
            range0: r0,
            range1: r1,
          }
          this.segments[Object.keys(this.segments)[index]].push(obj);
          this.temp_segments=Object.assign({}, this.segments);
        } else {
          console.log("step2...");
          let temp_Obj=Object.assign({}, this.segments);

          this.segments[Object.keys(this.segments)[index]] = this.segments[Object.keys(this.segments)[index]].filter(function( obj ) {
            return (obj.range0 != r0  && obj.range1 != r1);
          });
          this.temp_segments=Object.assign({}, this.segments);

          //找出目標區段
          this.segments[Object.keys(this.segments)[index]] = temp_Obj[Object.keys(temp_Obj)[index]].filter(function( obj ) {
            return (obj.range0 == r0  && obj.range1 == r1);
          });

          //this.temp_segments=Object.assign({}, this.segments);

          //this.segments[Object.keys(this.segments)[index]] = this.segments[Object.keys(this.segments)[index]].filter(function( obj ) {
          //  return (obj.range0 != r0  && obj.range1 != r1);
          //});
          //this.temp_segments=Object.assign({}, this.segments);

          console.log("step2...", r0, r1, this.temp_segments, this.segments[Object.keys(this.segments)[index]]);
        }
      } //end

      if (ch1 && !ch2) {  //range slider的值不變, 更改segment value的編號
        console.log("hello ch1 && !ch2..., range slider不變, 更改segment value")

        let obj = this.segments[Object.keys(this.segments)[index]].find(o => (o.range0 == r0 && o.range1 == r1));
        obj.seg_id = parseInt(this.segment_values[index]);

        this.temp_segments=Object.assign({}, this.segments);
      } //end

      if (!ch1 && !ch2) {  //新增range slider及segment value
        console.log("hello !ch1 && !ch2..., 新增range slider及segment value, 或刪除")

        let obj= {
          seg_id: parseInt(this.segment_values[index]),
          range0: r0,
          range1: r1,
        }
        this.segments[Object.keys(this.segments)[index]].push(obj);

        this.temp_segments=Object.assign({}, this.segments);

        //找出目標區段
        this.segments[Object.keys(this.segments)[index]] = this.segments[Object.keys(this.segments)[index]].filter(function( obj ) {
          return (obj.range0 == r0  && obj.range1 == r1);
        });
      } //end

      let els = document.getElementsByClassName('container_tab1');
      let begin_p = parseInt(this.segments[Object.keys(this.segments)[index]][0].range0)
      let end_p = parseInt(this.segments[Object.keys(this.segments)[index]][0].range1)
      console.log("begin_p, end_p...", begin_p, end_p);

      for (let j=begin_p; j<=end_p; j++) {
        let dot = els[index].childNodes[j];
        //console.log("dot...", dot);
        //console.log("before, lamp...", this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value);
        this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = !this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value;
        //console.log("after, lamp...", this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value);
        let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
        //console.log("dot...", temp_togg);
      }

      let start_p = r0-1;

      if (isNaN(this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value)) {
        let obj = this.segments[Object.keys(this.segments)[index]].find(o => (parseInt(o.range0)==r0 && parseInt(o.range1)==r1));
        this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = obj.seg_id.toString();
      } else {
        this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = '.';
      }

      console.log("$emit object..., ", this.temp_segments)

      this.$emit('closeLedStrip', this.my_key, index, this.temp_segments);
    },

    //input: errorMessages
    //output: errorMessages
    eraseErrMsg(index) {
      console.log("range data error..., index", index)
      this.errorMessages[Object.keys(this.errorMessages)[index]] = '';
    },

    //input: segments, ranges
    //output: true/false
    checkSegmentRange(index) {
      if (this.segments[Object.keys(this.segments)[index]].length == 0)
        return true;

      let r0=this.ranges[Object.keys(this.ranges)[index]][0];
      let r1=this.ranges[Object.keys(this.ranges)[index]][1];

      let obj = this.segments[Object.keys(this.segments)[index]].find(o => (o.range0 == r0 && o.range1 == r1));
      if (typeof obj !== 'undefined')
        return true;
      else
        return false;
    },

    //input: segments
    //output: true/false
    checkSegmentID(index) {
      if (this.segments[Object.keys(this.segments)[index]].length == 0)
        return true;

      let obj = this.segments[Object.keys(this.segments)[index]].find(o => parseInt(o.seg_id) == parseInt(this.segment_values[index]));
      if (typeof obj !== 'undefined')
        return true;
      else
        return false;
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

::v-deep .centered-input input {
  text-align: center !important;
}
.container_tab1  {
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
  font-size: 85%;
  color: red;
  margin-top: -10px;
  position: relative;
  right: -120px;
  top: -17px;
}
</style>