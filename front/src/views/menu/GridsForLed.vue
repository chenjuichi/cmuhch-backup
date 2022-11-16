<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm == 1 || currentUser.perm == 2">
      <v-card width="92vw" class="pa-md-4 mx-lg-auto">
        <v-toolbar flat>
          <v-toolbar-title>儲位Led資料設定</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>

        <v-tabs vertical>
          <v-tab>
            <v-icon left>mdi-account</v-icon>
            第1站料架
          </v-tab>
          <v-tab>
            <v-icon left>mdi-lock</v-icon>
            第2站料架
          </v-tab>
          <v-tab>
            <v-icon left>mdi-access-point</v-icon>
            第3站料架
          </v-tab>

          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_1" ref="card_text">
                <!--<div v-for="(k, index) in 5">-->

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
                    >
                    </div>
                  </div>

                  <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
                    <v-col class="px-4" cols="12" md="1"></v-col>
                    <v-col class="pl-6 pr-2" cols="12" md="8">
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
                            style="width: 60px"
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
                            style="width: 60px"
                            @focus="eraseErrMsg(0)"
                            @change="$set(ranges.range1, 1, $event)"
                          ></v-text-field>
                        </template>
                      </v-range-slider>
                      <small class="msgErr" v-text= "rangErrMsg"></small>
                    </v-col>
                    <v-col class="mt-1 pr-0 pl-0" cols="12" md="1">
                          <v-text-field
                            :value="segment_values[0]"
                            :max="max"
                            :min="min"

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
                        class="ml-0 mr-2 mt-2"
                        color="primary"
                        @click="toggleLed(0)">
                        <v-icon>mdi-gesture-tap</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col class="px-4" cols="12" md="1"></v-col>
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
                    >
                    </div>
                  </div>

                  <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
                    <v-col class="px-4" cols="12" md="1"></v-col>
                    <v-col class="pl-6 pr-2" cols="12" md="8">
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
                      <small class="msgErr" v-text= "rangErrMsg"></small>
                    </v-col>
                    <v-col class="mt-1 pr-0 pl-0" cols="12" md="1">
                          <v-text-field
                            :value="segment_values[1]"
                            :max="max"
                            :min="min"

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
                        class="ml-0 mr-2 mt-2"
                        color="primary"
                        @click="toggleLed(1)">
                        <v-icon>mdi-gesture-tap</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col class="px-4" cols="12" md="1"></v-col>
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
                    >
                    </div>
                  </div>

                  <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
                    <v-col class="px-4" cols="12" md="1"></v-col>
                    <v-col class="pl-6 pr-2" cols="12" md="8">
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
                      <small class="msgErr" v-text= "rangErrMsg"></small>
                    </v-col>
                    <v-col class="mt-1 pr-0 pl-0" cols="12" md="1">
                          <v-text-field
                            :value="segment_values[2]"
                            :max="max"
                            :min="min"

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
                        class="ml-0 mr-2 mt-2"
                        color="primary"
                        @click="toggleLed(2)">
                        <v-icon>mdi-gesture-tap</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col class="px-4" cols="12" md="1"></v-col>
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
                    >
                    </div>
                  </div>

                  <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
                    <v-col class="px-4" cols="12" md="1"></v-col>
                    <v-col class="pl-6 pr-2" cols="12" md="8">
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
                      <small class="msgErr" v-text= "rangErrMsg"></small>
                    </v-col>
                    <v-col class="mt-1 pr-0 pl-0" cols="12" md="1">
                          <v-text-field
                            :value="segment_values[3]"
                            :max="max"
                            :min="min"

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
                        class="ml-0 mr-2 mt-2"
                        color="primary"
                        @click="toggleLed(3)">
                        <v-icon>mdi-gesture-tap</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col class="px-4" cols="12" md="1"></v-col>
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
                    >
                    </div>
                  </div>

                  <v-row style="margin-bottom: 0px; height: 55px; max-height: 55px;">
                    <v-col class="px-4" cols="12" md="1"></v-col>
                    <v-col class="pl-6 pr-2" cols="12" md="8">
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
                      <small class="msgErr" v-text= "rangErrMsg"></small>
                    </v-col>
                    <v-col class="mt-1 pr-0 pl-0" cols="12" md="1">
                          <v-text-field
                            :value="segment_values[4]"
                            :max="max"
                            :min="min"

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
                        class="ml-0 mr-2 mt-2"
                        color="primary"
                        @click="toggleLed(4)">
                        <v-icon>mdi-gesture-tap</v-icon>
                      </v-btn>
                    </v-col>
                    <v-col class="px-4" cols="12" md="1"></v-col>
                  </v-row>

                <!--</div>-->
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_2">
                <p>
                  第2個料架建置中...
                </p>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_3">
                <p>
                  第3個料架建置中...
                </p>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>

      </v-card>
    </v-row>

    <v-row align="center" justify="space-around" v-else>
        <v-dialog
          v-model="permDialog"
          transition="dialog-bottom-transition"
          max-width="500"
        >
          <v-card>
            <v-toolbar
              color="primary"
              dark
            >錯誤訊息!</v-toolbar>
            <v-card-text>
              <div class="text-h4 pa-12">權限不足...</div>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-spacer></v-spacer>
              <v-btn text @click="permCloseFun"> 取消 </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-row>
  </v-container>
</v-app>
</div>
</template>

<script>
import axios from 'axios';
import Common from '../../mixin/common.js'
//import TempText from '../../components/TempText.vue'

export default {
  name: 'GridsForLed',

  //components: {
  //  TempText: TempText,
  //},

  mixins: [Common],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      //const userData = JSON.parse(localStorage.getItem('loginedUser'));
      //userData.setting_items_per_page = this.pagination.itemsPerPage;
      //localStorage.setItem('loginedUser', JSON.stringify(userData));
    };

    //this.getTabsData();
  },

  data() {
    return {
      currentUser: {},
      permDialog: false,

      //pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      //},


      tab: null,
      items: ['  料架1  ', '  料架2  ', '  料架3  '],
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',

      rangErrMsg: '',
      errorMessages: {  //for 錯誤訊息
        message1: '',
        message2: '',
        message3: '',
        message4: '',
        message5: '',
      },
      min: 1,
      max: 30,
      range: [1, 3],
      ranges: {     //for slider輸入範圍
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab1_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab2_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab3_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      Leds: [],
      //segment_value: 1,
      segment_values: [], //for輸入segment代號
      //selectedChips: [],
      selectedLeds: {   //for數字或'.' , 共30組
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },
      selectedLamps: {  //for燈號
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },

      tabs: [],
      layouts: [],

      segment: [
      //  seg_id:,
      //  range0:,
      //  range1:,
      ],
      segments: {     //for segment內的值
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
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },
      tab2_segs: {
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },
      tab3_segs: {
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },
      //segment_width: 44,
      //light_width: 29,
      init_id: 1,

      //styleObject: {
      //  marginRight: 56 + 'px', //init margin-right value
      //  marginLeft: 56 + 'px',  //init margin-left value
      //},
      temp_desserts: [],

      load_SingleTable_ok: false, //for get grids table data
      slider_data_ok: false,      //for update slider area data
      slider_led_dig_ok: false,   //for update slider led number
      slider_led_lamp_ok: false,  //for update slider led lamp
    }
  },

  computed: {

  },

  watch: {
    load_SingleTable_ok(val) {
      if (val) {
        this.load_SingleTable_ok=false;
        this.getTabsData();
      }
    },

    slider_data_ok(val) {
      if (val) {
        this.slider_data_ok=false;

        this.ranges.range1 = Object.assign([], this.tab1_rans.range1);
        this.ranges.range2 = Object.assign([], this.tab1_rans.range2);
        this.ranges.range3 = Object.assign([], this.tab1_rans.range3);
        this.ranges.range4 = Object.assign([], this.tab1_rans.range4);
        this.ranges.range5 = Object.assign([], this.tab1_rans.range5);

        let seg_len =this.tab1_segs.segments1.length;   //seg1
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments1[i][key] :", i, this.tab1_segs.segments1[i]);
          let obj= {
            seg_id: this.tab1_segs.segments1[i].seg_id,
            range0: this.tab1_segs.segments1[i].range0,
            range1: this.tab1_segs.segments1[i].range1,
          }
          this.segments.segment1.push(obj);
        }

        seg_len =this.tab1_segs.segments2.length;    //seg2
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments2[i][key] :", i, this.tab1_segs.segments2[i]);
          let obj= {
            seg_id: this.tab1_segs.segments2[i].seg_id,
            range0: this.tab1_segs.segments2[i].range0,
            range1: this.tab1_segs.segments2[i].range1,
          }
          this.segments.segment2.push(obj);
        }

        seg_len =this.tab1_segs.segments3.length;    //seg3
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments3[i][key] :", i, this.tab1_segs.segments3[i]);
          let obj= {
            seg_id: this.tab1_segs.segments3[i].seg_id,
            range0: this.tab1_segs.segments3[i].range0,
            range1: this.tab1_segs.segments3[i].range1,
          }
          this.segments.segment3.push(obj);
        }

        seg_len =this.tab1_segs.segments4.length;    //seg4
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments4[i][key] :", i, this.tab1_segs.segments4[i]);
          let obj= {
            seg_id: this.tab1_segs.segments4[i].seg_id,
            range0: this.tab1_segs.segments4[i].range0,
            range1: this.tab1_segs.segments4[i].range1,
          }
          this.segments.segment4.push(obj);
        }

        seg_len =this.tab1_segs.segments5.length; //seg5
        for (let i=0; i<seg_len; i++) {
          //console.log("this.tab1_segs.segments5[i][key] :", i, this.tab1_segs.segments5[i]);
          let obj= {
            seg_id: this.tab1_segs.segments5[i].seg_id,
            range0: this.tab1_segs.segments5[i].range0,
            range1: this.tab1_segs.segments5[i].range1,
          }
          this.segments.segment5.push(obj);
        }

        this.segment_values[0]=this.ranges.range1[0];
        this.segment_values[1]=this.ranges.range2[0];
        this.segment_values[2]=this.ranges.range3[0];
        this.segment_values[3]=this.ranges.range4[0];
        this.segment_values[4]=this.ranges.range5[0];

        this.slider_led_dig_ok=true;
      }
    },

    slider_led_dig_ok(val) {
      if (val) {
        this.slider_led_dig_ok=false;

        for (let index=0; index<5; index++) {
          let seg_len =this.segments[Object.keys(this.segments)[index]].length;   //seg1
          for (let i=0; i<seg_len; i++) {
            let start_p=this.segments[Object.keys(this.segments)[index]][i].range0-1
            this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = this.segments[Object.keys(this.segments)[index]][i].seg_id;
          }
        }

        this.slider_led_lamp_ok=true;
      }
    },

    slider_led_lamp_ok(val) {
      if (val) {
        this.slider_led_lamp_ok=false;

        let els = document.getElementsByClassName('container_tab1');
        for (let i=0; i<5; i++) {
          for (let j=this.ranges[Object.keys(this.ranges)[i]][0]; j<this.ranges[Object.keys(this.ranges)[i]][1]+1; j++) {
            let dot = els[i].childNodes[j];
            //console.log("node name: ", dot);

            this.selectedLamps[Object.keys(this.selectedLamps)[i]][j-1].value = !this.selectedLamps[Object.keys(this.selectedLamps)[i]][j-1].value;
            let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[i]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
          }
        }
      }
    },

  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0 || this.currentUser.perm >1) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    //this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    // init燈號led資料
    this.Leds=[];
    for (let i=0; i<this.max; i++) {
      this.Leds.push(false)
    }

    // init燈號數字資料
    let obj= {value: '.',}
    //this.selectedChips=[];
    //for (let i=0; i<this.max; i++) {
    //  this.selectedChips.push(obj)
    //}

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

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listGrids();
  },

  methods: {
    listGrids() {
      const path = '/listGrids';
      console.log("listGrids, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    getTabsData() {
      let max_stations=3;
      let max_layouts=5;
      let grid_count=this.temp_desserts.length;

      for (let i=0; i<grid_count; i++) {
        let sw = parseInt(this.temp_desserts[i].grid_station);
        switch (sw) {
          case 1:
            for (let i=0; i<max_layouts; i++) {
              this.tab1_segs[Object.keys(this.tab1_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 1  && parseInt(obj.grid_layout) == i+1);
              });
            }

            break;
          case 2:
            for (let i=0; i<max_layouts; i++) {
              this.tab2_segs[Object.keys(this.tab2_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 2  && parseInt(obj.grid_layout) == i+1);
              });
            }

            break;
          default:
            for (let i=0; i<max_layouts; i++) {
              this.tab3_segs[Object.keys(this.tab3_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 3  && parseInt(obj.grid_layout) == i+1);
              });
            }

            break;
        } //end switch loop
      } //end for loop

      for (let i=0; i<max_layouts; i++) {
        //console.log("key 1...")
        //console.log("object key: ", i, this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range0, this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range1);
        //console.log("object key: ", i, this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range0, this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range1);
        //console.log("object key: ", i, this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range0, this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range1);
        //console.log("key 1...")
        if (this.tab1_segs[Object.keys(this.tab1_segs)[i]].length!=0) {
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][0]=parseInt(this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range0);
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][1]=parseInt(this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range1);
        } else {
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][0]=1;
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][1]=3;
        }

        //console.log("key 2...")
        if (this.tab2_segs[Object.keys(this.tab2_segs)[i]].length!=0) {
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][0]=parseInt(this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range0);
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][1]=parseInt(this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range1);
        } else {
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][0]=1;
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][1]=3;
        }

        //console.log("key 3...")
        if (this.tab3_segs[Object.keys(this.tab3_segs)[i]].length!=0) {
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][0]=parseInt(this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range0);
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][1]=parseInt(this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range1);
        } else {
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][0]=1;
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][1]=3;
        }
      }

      console.log("tab1_rans.range1: ", this.tab1_rans.range1)
      this.slider_data_ok=true;

    },

    /*
    getComp() {
      let el = document.getElementsByClassName('temp_text').length;

      for (let i=0; i< el; i++) {
        document.getElementsByClassName('temp_text')[i].style['margin-left'] = (this.light_width * this.segment[i].size - this.segment_width) / 2  + 'px';
        document.getElementsByClassName('temp_text')[i].style['margin-right'] = (this.light_width * this.segment[i].size - this.segment_width) / 2  + 'px';
        document.getElementsByClassName('temp_text')[i].style['left'] = (10+29) - 20 * (this.segment[i].id - 1)+ 'px';
        document.getElementsByClassName('temp_text')[i]
        .getElementsByClassName('v22')[0].childNodes[1].style['left']= (29 * this.segment[i].range0 -39) / 2 + 'px';
        //.getElementsByClassName('v22')[0].childNodes[1].style['left']= (29 * this.segment[i].size -39) / 2 + 'px';
      }
    },
    */
    toggleLed(index) {
      //init 常數的值
      //this.segments[Object.keys(this.segments)[index]];
      this.errorMessages[Object.keys(this.errorMessages)[index]] = '';
      let temp_seg_size=this.segments[Object.keys(this.segments)[index]].length;
      let r0=this.ranges[Object.keys(this.ranges)[index]][0];
      let r1=this.ranges[Object.keys(this.ranges)[index]][1];

      //檢查資料的正確性
      if (r0 > r1) {
        //this.rangErrMsg='格位資料設定錯誤!'
        this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
        return;
      }

      for (let i=0; i<temp_seg_size; i++) {
        if ((r0 > this.segments[Object.keys(this.segments)[index]][i].range0 && r0 < this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r1 > this.segments[Object.keys(this.segments)[index]][i].range0 && r1 < this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r0 == this.segments[Object.keys(this.segments)[index]][i].range0 && r1 > this.segments[Object.keys(this.segments)[index]][i].range1) ||
          (r1 == this.segments[Object.keys(this.segments)[index]][i].range1 && r0 < this.segments[Object.keys(this.segments)[index]][i].range0)) {
          this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
          return;
        }
      }

      let ch1=this.checkSegmentRange(index);
      let ch2=this.checkSegmentID(index);

      if (!ch1 && ch2) {
        console.log("hello !ch1 && ch2...")
        this.errorMessages[Object.keys(this.errorMessages)[index]] = '格位資料設定錯誤!';
        return;
      }

      if (ch1 && ch2) {
        console.log("hello ch1 && ch2...");
        let l1 = this.segments[Object.keys(this.segments)[index]].length;
        this.segments[Object.keys(this.segments)[index]] = this.segments[Object.keys(this.segments)[index]].filter(function( obj ) {
          return (obj.range0 != r0  && obj.range1 != r1);
        });
        let l2 = this.segments[Object.keys(this.segments)[index]].length;
        if (l2 == l1) {
          let obj= {
            seg_id: this.segment_values[index],
            range0: r0,
            range1: r1,
          }
          this.segments[Object.keys(this.segments)[index]].push(obj);
        }
      }

      if (ch1 && !ch2) {
        console.log("hello ch1 && !ch2...")

        let obj = this.segments[Object.keys(this.segments)[index]].find(o => (o.range0 == r0 && o.range1 == r1));
        obj.seg_id = this.segment_values[index];

        let els = document.getElementsByClassName('container_tab1');
        for (let j=this.ranges[Object.keys(this.ranges)[index]][0]; j<this.ranges[Object.keys(this.ranges)[index]][1]+1; j++) {
          let dot = els[index].childNodes[j];
          //this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = !this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value;
          this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = true;
          let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
        }

        for (let i=0; i<this.segments[Object.keys(this.segments)[index]].length; i++) {
          let start_p=this.segments[Object.keys(this.segments)[index]][i].range0-1
          console.log("1. point: ", i, start_p, this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value, isNaN(this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value))
          console.log("2. point: ", index, this.segments[Object.keys(this.segments)[index]][i].seg_id, this.segment_values[index])
          if (!isNaN(this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value))
            //this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = this.segments[Object.keys(this.segments)[index]][i].seg_id;
            this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = parseInt(this.segment_values[index]);
          else
            this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = '.';
        }
        return;
      }

      if (!ch1 && !ch2) {
        console.log("hello !ch1 && !ch2...")
        //檢查是否power off Led
        let l1 = this.segments[Object.keys(this.segments)[index]].length
        //console.log("seg point: ", this.segment.length, l1)
        this.segments[Object.keys(this.segments)[index]] = this.segments[Object.keys(this.segments)[index]].filter(function( obj ) {
          return (obj.range0 != r0  && obj.range1 != r1);
        });

        let obj= {
          seg_id: this.segment_values[index],
          range0: r0,
          range1: r1,
        }
        this.segments[Object.keys(this.segments)[index]].push(obj);
      }

      let els = document.getElementsByClassName('container_tab1');
      for (let j=this.ranges[Object.keys(this.ranges)[index]][0]; j<this.ranges[Object.keys(this.ranges)[index]][1]+1; j++) {
        let dot = els[index].childNodes[j];
        this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value = !this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value;
        let temp_togg = this.selectedLamps[Object.keys(this.selectedLamps)[index]][j-1].value ? (dot.className += " on") : (dot.className = "dot");
      }

      let start_p = r0-1;
      //let start_p=this.segment[i].range0-1;
      console.log("point: ", start_p, this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value);

      if (isNaN(this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value)) {
        let obj = this.segments[Object.keys(this.segments)[index]].find(o => (o.range0 == r0 && o.range1 == r1));
        this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = obj.seg_id;
      } else {
        this.selectedLeds[Object.keys(this.selectedLeds)[index]][start_p].value = '.';
      }
    },

    eraseErrMsg(index) {
      console.log("range data error...")
      this.errorMessages[Object.keys(this.errorMessages)[index]] = '';
    },

    //input: fromDateValStart,
    //output: fromDateValStart, compareDateStart
    checkSegmentRange(index) {
      if (this.segments[Object.keys(this.segments)[index]].length == 0)
        return true;

      let r0=this.ranges[Object.keys(this.ranges)[index]][0];
      let r1=this.ranges[Object.keys(this.ranges)[index]][1];


      //console.log("type check...", typeof(r0))
      let obj = this.segments[Object.keys(this.segments)[index]].find(o => (o.range0 == r0 && o.range1 == r1));
      if (typeof obj !== 'undefined')
        return true;
      else
        return false;
    },

    checkSegmentID(index) {
      if (this.segments[Object.keys(this.segments)[index]].length == 0)
        return true;

      let obj = this.segments[Object.keys(this.segments)[index]].find(o => o.seg_id == this.segment_values[index]);
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
  font-size: 80%;
  color: red;
  margin-top: -10px;
}
</style>