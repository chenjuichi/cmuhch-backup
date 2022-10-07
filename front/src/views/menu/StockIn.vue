<template>
  <v-app>
  <v-container fluid>  
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card class="overflow-hidden mx-auto mt-3" width="65vw">
        <v-toolbar flat color="#7DA79D" height="80" >
          <v-row dense style="margin-bottom: -36px; margin-top: -12x;">         
            <v-col cols="12" md="2" class="mr-1">                              
              <v-text-field                            
                v-model="stockInTag_reagID"
                label="資材碼"
                :value="stockInTag_reagID"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3" class="mr-2">                            
              <v-text-field                            
                v-model="stockInTag_reagName"
                label="品名"
                :value="stockInTag_reagName"
                readonly
              ></v-text-field> 
            </v-col>
            <v-col cols="12" md="2" align="right" style="display:table; margin-top:-29px">
              <!--<span class="text-decoration-underline">&nbsp;&nbsp;入庫數量</span>-->
              <span class="stockinStr" style="display:table-cell; vertical-align:middle; font-weight: bold; font-size: 1em;">入庫數量</span>
            </v-col>
            <v-col cols="12" md="2" align="left" class="pl-0 mx-1">
              <vue-numeric-input v-model="stockInTag_cnt" :min="1" :max="stockInTag_max_cnt" :step="1" size="small" align="center"></vue-numeric-input>
            </v-col>
            <v-col cols="12" md="1" align="right" class="pl-0 mx-1">            
              <!--<img v-show="stockInTag_reagID!=''" v-on:click="redirect_to_mqtt" :src="home_url" alt="Loading" style="height: 3vw;" v-bind:alt="pic">-->
              <img v-show="stockInTag_reagID!=''" @click="redirect_to_mqtt" :src="home_url" alt="Loading" style="height: 3vw;">
            </v-col>
              
            <v-col cols="12" md="1" align="center" class="pl-0 mx-1">           
                <v-btn v-show="isOK" @click="redirect_ok" color="success" rounded style="font-weight: bold; font-size: 0.9em;">
                  <!--<v-icon>mdi-domain</v-icon>-->完成
                </v-btn>
            </v-col>
          </v-row> 
        </v-toolbar>
        <v-sheet class="overflow-y-auto" max-height="600">
          <v-container>     
            <v-list three-line>
              <v-list-item-group v-model="model" mandatory color="indigo">
                <!--<template v-for="(item, index) in items">-->
                  <!--<v-list-item :key="item.stockInTag_reagName">-->
                <!--<template v-for="(item, index) in filteredItems">-->
                <template v-for="(item, index) in items">
                  <v-list-item>
                    <template v-slot:default="{ active }">
                      <v-list-item-content>
                        <!--<v-list-item-title class="font-weight-bold" v-text="`品名:${item.stockInTag_reagName}    入庫數量: ${item.stockInTag_cnt}`"></v-list-item-title>-->
                        <v-list-item-title class="font-weight-bold">
                          <span>品名:{{item.stockInTag_reagName}}</span>&nbsp;&nbsp;    
                          <span class="text-decoration-underline">入庫數量: {{item.stockInTag_cnt}}</span>
                        </v-list-item-title>
                        <v-list-item-subtitle class="mb-3" v-text="`效期:${item.stockInTag_reagPeriod}  保存溫度: ${item.stockInTag_reagTemp}  批號: ${item.stockInTag_batch}`"></v-list-item-subtitle>

                        <v-list-item-subtitle class="text--primary font-weight-bold" v-text="`入庫人員: ${item.stockInTag_Employer}  入庫日期: ${item.stockInTag_Date}`"
                        ></v-list-item-subtitle>
                      </v-list-item-content>

                      <v-list-item-action @click="listActionClick(index, active)">
                        <!--<v-list-item-action-text v-text="item.stockInTag_batch"></v-list-item-action-text>-->
                        <!--<img v-show="active" :src="home_url" alt="Loading" style="height: 2.5vw;">-->
                        
                        <v-icon v-if="!active" color="grey lighten-1">
                          mdi-star-outline
                        </v-icon>
                        <v-icon v-else color="yellow darken-3">
                          mdi-star
                        </v-icon>                      
                        <div v-show="active">{{item.grid_station}}站/{{item.grid_layout}}層/{{item.grid_pos}}格</div>
                      </v-list-item-action>
                    </template>
                  </v-list-item>

                  <v-divider v-if="index < items.length - 1" :key="index"></v-divider>
                </template>
              </v-list-item-group>
            </v-list>
          </v-container> 
        </v-sheet>
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
              <div class="text-h4 pa-12">使用這項功能, 請通知管理人員...</div>
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
</template>

<script>
import axios from 'axios';
import VueNumericInput from 'vue-numeric-input';

//import logo from '../../assets/image/icons8-light-on.gif'
import logo from '../../assets/image/icons8-light-on-unscreen.gif'
import logoR from '../../assets/image/icons8-R-light-on-50.png'
import logoY from '../../assets/image/icons8-Y-light-on-50.png'
import logoG from '../../assets/image/icons8-G-light-on-50.png'
import _ from 'lodash'

import Common from '../../mixin/common.js'

export default {
  name: 'StockIn',

  mixins: [Common],

  components: {
    VueNumericInput,
  },

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
    //
    this.stockInTag_cnt=this.items[this.model].stockInTag_cnt;
    this.stockInTag_max_cnt=this.items[this.model].stockInTag_cnt;

    this.stockInTag_min_cnt=1;
    this.stockInTag_reagID=this.items[this.model].stockInTag_reagID;
    this.stockInTag_reagName=this.items[this.model].stockInTag_reagName;
    this.items[this.model].active=true;
    //
  },

  data: () => ({
    currentUser: {
      	//empID: null,
        //name: null,
				//dep: null,
        //perm: 0,    //member: 2, admin: 1, none:0
    },
    permDialog: false,

    default_home_url: logo,
    home_url: logo,
    home_url_R: logoR,
    home_url_Y: logoY,
    home_url_G: logoG,

    stockInTag_reagID: '',
    stockInTag_reagName: '',
    stockInTag_cnt: 0,
    stockInTag_min_cnt: 0,
    stockInTag_max_cnt: 0,

    currentIndex: 0,
    currentLedStation: 1,
    currentLedLayout: 1,
    currentLedPos: 1,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },


    grids: [],

    isSort: true,   //textfield輸入資材碼
    isOK: false,    //是否顯示入庫完成的按鍵

    //selected: [2],
    model: 0,
    items: [
      {
        //id: 1,
        stockInTag_reagID: '123456789',
        stockInTag_reagName: 'ABC',
        stockInTag_reagPeriod: '111/10/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_Date: '111/06/01',
        stockInTag_EmpID: 'N12345',
        stockInTag_Employer: '陳健南',
        stockInTag_batch: '1110012345B123400066',
        stockInTag_cnt: 4,
        active: false,
      },
      {
        //id: 2,
        stockInTag_reagID: '234567891',
        stockInTag_reagName: 'ABCD1',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_Date: '111/06/01',
        stockInTag_EmpID: 'N12345',
        stockInTag_Employer: '陳健南',
        stockInTag_batch: '1110012345C123400055',
        stockInTag_cnt: 2,
        active: false,
      },
      {
        //id: 3,
        stockInTag_reagID: '234567892',
        stockInTag_reagName: 'A11',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_Date: '111/06/01',
        stockInTag_EmpID: 'N12345',
        stockInTag_Employer: '陳健南',
        stockInTag_batch: '1110012345B123400033',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 4,
        stockInTag_reagID: '234567893',
        stockInTag_reagName: 'A12',
        stockInTag_reagPeriod: '112/6/30',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_Date: '111/06/01',
        stockInTag_EmpID: 'N12345',
        stockInTag_Employer: '陳健南',
        stockInTag_batch: '1110012345B123400033',
        stockInTag_cnt: 1,
        active: false,
      },
      {
        //id: 5,
        stockInTag_reagID: '234567894',
        stockInTag_reagName: 'B2233',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_Date: '111/06/01',
        stockInTag_EmpID: 'N12345',
        stockInTag_Employer: '陳健南',
        stockInTag_batch: '1110012345B123400022',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 6,
        stockInTag_reagID: '234567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/03/10',
        stockInTag_EmpID: 'T12345',
        stockInTag_Employer: '林成興',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
        active: false,
      },
      {
        //id: 7,
        stockInTag_reagID: '234567898',
        stockInTag_reagName: 'B3341',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/03/10',
        stockInTag_EmpID: 'T12345',
        stockInTag_Employer: '林成興',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 8,
        stockInTag_reagID: '234567899',
        stockInTag_reagName: 'B3342',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/03/10',
        stockInTag_EmpID: 'T12345',
        stockInTag_Employer: '林成興',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 5,
        active: false,
      },
      {
        //id: 9,
        stockInTag_reagID: '214567897',
        stockInTag_reagName: 'B3343',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/03/10',
        stockInTag_EmpID: 'T12345',
        stockInTag_Employer: '林成興',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 10,
        stockInTag_reagID: '214567898',
        stockInTag_reagName: 'B3345',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/03/10',
        stockInTag_EmpID: 'T12345',
        stockInTag_Employer: '林成興',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 2,
        active: false,
      },
      {
        //id: 11,
        stockInTag_reagID: '214567899',
        stockInTag_reagName: 'B3346',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/06/25',
        stockInTag_EmpID: 'T87654',
        stockInTag_Employer: '吳仲偉',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 12,
        stockInTag_reagID: '224567897',
        stockInTag_reagName: 'B3347',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/06/25',
        stockInTag_EmpID: 'T87654',
        stockInTag_Employer: '吳仲偉',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 20,
        active: false,
      },
      {
        //id: 13,
        stockInTag_reagID: '224567898',
        stockInTag_reagName: 'B3348',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/06/25',
        stockInTag_EmpID: 'T87654',
        stockInTag_Employer: '吳仲偉',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 10,
        active: false,
      },
      {
        //id: 14,
        stockInTag_reagID: '224567899',
        stockInTag_reagName: 'B3349',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '常溫',
        stockInTag_Date: '111/06/25',
        stockInTag_EmpID: 'T87654',
        stockInTag_Employer: '吳仲偉',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 10,
        active: false,
      },
    ],
  }),

  computed: {
    filteredItems() {
    //透過filter()函式的第一參數, 進行callback函式所指定的過濾條件，並返回一個新陣列
    //透過includes(), 回傳是否包含該元素的Boolean值，true代表包含，false則代表不包含
      let temp_array=[];
      temp_array=
        _.orderBy(this.items.filter(item => {
        return item.stockInTag_reagID.toLowerCase().includes(this.stockInTag_reagID.toLowerCase());
      }), 'stockInTag_reagID');
      //console.log("filter: ", temp_array)
      return temp_array;
    },       
  },

  watch: {
    stockInTag_reagID (val) {
      this.fromReagIdDisp();
    },
  },

  //mounted() {
    //this.stockInTag_cnt=this.items[this.model].stockInTag_cnt;
    //this.stockInTag_max_cnt=this.items[this.model].stockInTag_cnt;
    //
    //this.stockInTag_min_cnt=1;
    //this.stockInTag_reagID=this.items[this.model].stockInTag_reagID;
    //this.stockInTag_reagName=this.items[this.model].stockInTag_reagName;
    //this.items[this.model].active=true;
  //},

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;

    this.initAxios();

    this.initialize();

    this.addGrids();  
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      /*
      const path='/xxx';
      axios.get(path)
      .then((res) => {

      this.load_SingleTable_ok=true;
      })
      .catch((error) => {

      });
      */
      this.grids = [
        {
          //id: 1,
          grid_reagID: '123456789',
          grid_reagName: 'ABC',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 4,         
        },
        {
          //id: 2,
          grid_reagID: '234567891',
          grid_reagName: 'ABCD',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 5,
        },
        {
          //id: 3,
          grid_reagID: '234567892',
          grid_reagName: 'A11',
          grid_station: 2,
          grid_layout: 1,
          grid_pos: 6,
        },
        {
          //id: 4,
          grid_reagID: '234567893',
          grid_reagName: 'A12',
          grid_station: 2,
          grid_layout: 3,
          grid_pos: 5,
        },
        {
          //id: 5,
          grid_reagID: '234567894',
          grid_reagName: 'B2233',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 2,
        },
        {
          //id: 6,
          grid_reagID: '234567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 1,
          grid_pos: 6,
        },
        {
          //id: 7,
          grid_reagID: '234567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 6,
        },
        {
          //id: 8,
          grid_reagID: '234567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 3,
          grid_pos: 6,
        },
        {
          //id: 9,
          grid_reagID: '214567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 4,
          grid_pos: 6,
        },
        {
          //id: 10,
          grid_reagID: '214567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 6,
        },
        {
          //id: 11,
          grid_reagID: '214567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 7,
        },
        {
          //id: 13,
          grid_reagID: '224567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 14,
          grid_reagID: '224567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 15,
          grid_reagID: '224567899',
          grid_reagName: 'B3344',
          grid_station: 1,
          grid_layout: 5,
          grid_pos: 8,
        },

      ];    
    },

    async mqttForStationA() {
        let path='/mqtt/stationA';
        let temp_layout=this.currentLedLayout.toString();
        let temp_pos=this.currentLedPos.toString();
        console.log(this.more + ' ' + this.currentIndex + " layout: " + temp_layout + " pos: " + temp_pos)
        let temp_sw= 'on';
        let payload= {
          //topic: temp_station,
          topic: 'Station1',
          layout: temp_layout,
          led: temp_pos,
          msg: temp_sw
        };

        try {
          let res = await axios.post(path, payload);
          console.log("mqtt ok", res.data.status);
        } catch (err) {
          console.error(err)
        }
    },

    listActionClick(index, active) {
      console.log("list action: ", index, active);
      
      this.currentIndex=index;
      this.currentLedStation=this.items[index].grid_station;
      this.currentLedLayout=this.items[index].grid_layout;
      this.currentLedPos=this.items[index].grid_pos;

      this.isSort=false;
      if (active) {
        this.stockInTag_cnt=0;
        this.stockInTag_max_cnt=0;
        this.stockInTag_min_cnt=0;

        this.stockInTag_reagID='';
        this.stockInTag_reagName='';
      } else {
        this.stockInTag_cnt=this.items[index].stockInTag_cnt;
        this.stockInTag_max_cnt=this.items[index].stockInTag_cnt;

        this.stockInTag_min_cnt=1;
        this.stockInTag_reagID=this.items[index].stockInTag_reagID;
        this.stockInTag_reagName=this.items[index].stockInTag_reagName;
      }

      //this.items[index].active=!this.items[index].active;
    },
    /*
    toggle(index) {
      const i = this.selected.indexOf(index)

      if (i > -1) {
          this.selected.splice(i, 1)
      } else {
          this.selected.push(index)
      }
    },
    */
    fromReagIdDisp() { 
      if (this.stockInTag_reagID != '' && this.isSort) {        
        //console.log("result 1-1...", this.items);
        const objIndex = this.items.findIndex((obj => obj['active'] == true));
        //console.log("result 1-1-1...", objIndex);
        if (objIndex != -1)
          this.items[objIndex].active = false;       
        const fromIndex = this.items.map(object => object.stockInTag_reagID).indexOf(this.stockInTag_reagID);
        const toIndex = 0;
        //console.log("result 1-2...", result);
        if (fromIndex != -1) {
          const element = this.items.splice(fromIndex, 1)[0];
          this.items.splice(toIndex, 0, element);
          //console.log("result 1-2...", this.items);
          this.model=0;
          this.items[0].active = true;
          
          this.stockInTag_cnt=this.items[0].stockInTag_cnt;
          this.stockInTag_max_cnt=this.items[0].stockInTag_cnt;
          this.stockInTag_min_cnt=1;
          
          this.stockInTag_reagName=this.items[0].stockInTag_reagName;

          this.currentIndex=0;
          this.currentLedStation=this.items[0].grid_station;
          this.currentLedLayout=this.items[0].grid_layout;
          this.currentLedPos=this.items[0].grid_pos;


          //return copyItems;
        }
        //if (index != -1) {
        //  console.log("result 2...", index); 
        //  this.model=index;
        //}      
      } else {
        this.isSort=true;
        if (this.stockInTag_reagID == '') {
          this.stockInTag_cnt=0;
          this.stockInTag_max_cnt=0;
          this.stockInTag_min_cnt=0;
          
          this.stockInTag_reagName='';
        }
      }
    },

    addGrids() {
      for (let i = 0; i < this.items.length; i++) {
        let obj = this.grids.find(o => o.grid_reagID === this.items[i].stockInTag_reagID)
        if (typeof(obj) !== 'undefined') {
          this.items[i].grid_station=obj.grid_station;
          this.items[i].grid_layout=obj.grid_layout;
          this.items[i].grid_pos=obj.grid_pos;
        }
      };
      //console.log("find: ", this.items);
    },

    redirect_to_mqtt() {
      console.log("hello click image button...", this.model);
      this.isOK=true;
      let temp_sw=this.items[this.model].grid_station;
      switch (temp_sw) {
        default:
          this.home_url=this.home_url_R;
          return;
        case 1:
          this.home_url=this.home_url_R;
          return;
        case 2:
          this.home_url=this.home_url_Y;
          return;
        case 2:
          this.home_url=this.home_url_G;
          return;
      }
    },

    redirect_ok() {
      this.isOK=false;
      this.home_url=this.default_home_url;
      if (this.stockInTag_cnt=this.items[this.model].stockInTag_cnt) {
        let removedEl = this.items.splice(this.model, 1); //remove object(index: this.model) from array(this.items)
        
        this.model=(this.model-1>= 0) ? this.model-1 : 0;
        this.stockInTag_cnt=this.items[this.model].stockInTag_cnt;
        this.stockInTag_max_cnt=this.items[this.model].stockInTag_cnt;
        this.stockInTag_min_cnt=1;
        this.stockInTag_reagID=this.items[this.model].stockInTag_reagID;
        this.stockInTag_reagName=this.items[this.model].stockInTag_reagName;
        this.items[this.model].active=true;        
      } else {
        this.items[this.model].stockInTag_cnt=this.items[this.model].stockInTag_cnt - this.stockInTag_cnt;
        this.stockInTag_cnt=this.items[this.model].stockInTag_cnt;
        this.stockInTag_max_cnt=this.items[this.model].stockInTag_cnt;
      }

      this.mqttForStationA();
    },
    
    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar'); 
    },    
  },
}
</script>

<style scoped>
/*
.v-text-field{
      width: 100px;
}
*/
</style>

<style lang="scss" scoped>
html {
  overflow: hidden !important;
}

span.text-decoration-underline {
  margin-top: 13px;
}

span.stockinStr {
  margin-top: 13px;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

.v-card.on-hover.theme--dark {
  background-color: rgba(255, 255, 255, 0.8);  
}

.v-card.on-hover.theme--dark > .v-card__text {
    color: #000;      
}
</style>