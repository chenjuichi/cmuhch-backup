<template>
<v-app>
  <v-container fluid>
    <v-snackbar v-model="snackbar" :color="snackbar_color" :right='snackbar_right' :top='snackbar_top'>
      {{ snackbar_info }}
      <template v-slot:action="{ attrs }">
        <v-btn icon :color="snackbar_icon_color" @click="snackbar= false">
          <v-icon dark>mdi-close-circle</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="86vw" class="pa-md-4 mt-5 mx-lg-auto">
        <!--
          @click:row="getExpand"
          :expanded.sync="expanded"
          show-expand
          item-key="id"
         -->
        <v-data-table
          dense
          :headers="headers"
          :items="dessertsDisplay"
          :options.sync="pagination"
          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title style="height:40px;">庫存記錄查詢</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <!-- 查詢 -->
                <v-spacer></v-spacer>
                <v-text-field v-model="search" placeholder="關鍵字查詢" class="style-0"></v-text-field>
                <v-spacer></v-spacer>
                <!-- 入庫日期查詢 -->
                <v-menu
                  v-model="fromDateMenuStart"
                  :close-on-content-click="false"
                  :nudge-right="40"

                  transition="scale-transition"
                  offset-y

                  max-width="280px"
                  min-width="280px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="入庫開始日期查詢"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDispStart"
                      v-model="compareDateStart"
                      v-on="on"
                      class="shrink style-3"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateValStart"
                    no-title
                    @input="fromDateMenuStart = false"
                  ></v-date-picker>
                </v-menu>
                <v-menu
                  v-model="fromDateMenuEnd"
                  :close-on-content-click="false"
                  :nudge-right="40"

                  transition="scale-transition"
                  offset-y

                  max-width="280px"
                  min-width="280px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="入庫截止日期查詢"
                      prepend-icon="event"
                      readonly
                      :value="fromDateDispEnd"
                      v-model="compareDateEnd"
                      v-on="on"
                      class="shrink style-3"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateValEnd"
                    no-title
                    @input="fromDateMenuEnd = false"
                  ></v-date-picker>
                </v-menu>
                <v-spacer></v-spacer>
                <!-- 廠商查詢 -->
                <v-select
                  @change="checkSelect"
                  :items="itemsForSelect"
                  v-model="selectedItems"
                  label="供應商查詢"
                  class="style-4"
                  outlined
                  multiple
                  dense
                ></v-select>
                <v-spacer></v-spacer>
                <!-- 效期查詢 -->
                <v-menu
                  v-model="fromDateMenuPeriod"
                  :close-on-content-click="false"
                  :nudge-right="40"

                  transition="scale-transition"
                  offset-y

                  max-width="280px"
                  min-width="280px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      placeholder="效期查詢"
                      prepend-icon="event"
                      readonly
                      :value="displayPeriodDate"
                      v-model="compareDatePeriod"
                      v-on="on"
                      class="shrink style-2"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    locale="zh-TW"
                    :min="minDate"
                    :max="maxDate"
                    v-model="fromDateValP"
                    no-title
                    @input="fromDateMenuPeriod = false"
                  ></v-date-picker>
                </v-menu>
                <!-- 安全存量查詢 -->
                <v-checkbox class="myCheckbox"
                  v-model="compareSafeStock"
                  color="primary"
                  hide-details
                  label="安全存量查詢"
                ></v-checkbox>
                <!-- 按鍵指令 -->
                <v-btn color="primary" class="mt-n1 mr-15 mx-auto excel_wrapper" @click="exportToExcel">
                  <v-icon left>mdi-microsoft-excel</v-icon>
                  Excel
                </v-btn>
              </v-toolbar>
          </template>

          <template v-slot:item.stkRecord_sum="props" v-show="compareSafeStock">
            <v-edit-dialog
              :return-value.sync="props.item.stkRecord_sum"

              persistent
              @save="save"
              @cancel="cancel"
              @open="open"
              @close="close"
            >
              {{ props.item.stkRecord_sum }}  {{ props.item.stkRecord_unit }}
              <template v-slot:input>
                <v-text-field
                  v-model="props.item.stkRecord_sum"
                  label="Edit"
                  readonly
                  single-line
                ></v-text-field>
              </template>
            </v-edit-dialog>
          </template>

        </v-data-table>
      </v-card>
    </v-row>

    <v-row align="center" justify="space-around" v-else>
        <v-dialog
          v-model="permDialog"
          transition="dialog-bottom-transition"
          max-width="500"
        >
          <v-card>
            <v-toolbar color="primary" dark>錯誤訊息!</v-toolbar>
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
import Common from '../../mixin/common.js'

import '../../mixin/dateformate.js'

export default {
  name: 'StockRecord',

  mixins: [Common],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data () {
    return {
      currentUser: {},
      permDialog: false,

      snackbar: false,
      snackbar_color: 'success',
      snackbar_right: true,
      snackbar_top: true,
      snackbar_info: '',
      snackbar_icon_color: '#adadad',

      fromDateMenuStart: false,
      fromDateValStart: null,
      compareDateStart: '',  //查詢開始日期

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareDateEnd: '',    //查詢截止日期

      fromDateMenuPeriod: false,
      fromDateValP: null,
      compareDatePeriod: '',      //查詢效期

      comparePeriods: '',
      compareSafeStock: false,

      //compareStart: false,

      minDate: "2012-07-01",
      maxDate: "2042-06-30",

      search: '',

      periodMessage: '效期天數',
      /*
      headers:
      [
        { text: 'ID', sortable: false, value: 'id', align: 'start' },
        { text: '資材碼', sortable: true, value: 'stkRecord_reagID', width: '11%', },
        { text: '品名', sortable: false, value: 'stkRecord_reagName', width: '14%',},
        { text: '供應商', sortable: true, value: 'stkRecord_supplier', width: '12%',},
        { text: '入庫日期', sortable: true, value: 'stkRecord_Date', width: '13%',},
        { text: '效期', sortable: true, value: 'stkRecord_period', width: '8%',},
        { text: '安全存量', sortable: false, value: 'stkRecord_saftStockUnit', width: '12%', align: 'center' },
        { text: '數量', sortable: false, value: 'stkRecord_cntUnit', width: '8%', align: 'center' },
        { text: '儲位', sortable: false, value: 'stkRecord_grid', width: '14%', align: 'center' },
        { text: '', value: 'data-table-expand' },
      ],
      */
      pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      },

      itemsForSelect:[],
      selectedItems: [],
      isAllSelected: false,

      singleExpand: false,
      expanded: [],

      dessertsDisplayForCheckbox: [],
      dessertsDisplayForSelect: [],
      dessertsDisplay: [],
      desserts: [ ],
      temp_desserts: [],

      load_SingleTable_ok: false, //for get employer table data
    }
  },

  computed: {
    headers() {
      const headers =
      [
        { text: 'ID', sortable: false, value: 'id', width: '4%', align: 'start' },
        { text: '資材碼', sortable: true, value: 'stkRecord_reagID', width: '8%', },
        { text: '品名', sortable: true, value: 'stkRecord_reagName', width: '14%',},
        { text: '供應商', sortable: true, value: 'stkRecord_supplier', width: '12%',},
        { text: '入庫日期', sortable: true, value: 'stkRecord_Date', width: '8%',},
        { text: '效期', sortable: true, value: 'stkRecord_period', width: '8%',},
        { text: '安全存量', sortable: false, value: 'stkRecord_saftStockUnit', width: '12%', align: 'center' },
        { text: '數量', sortable: false, value: 'stkRecord_cntUnit', width: '8%', align: 'center' },
        { text: '儲位', sortable: false, value: 'stkRecord_grid', width: '15%', align: 'center' },
        //{ text: '', value: 'data-table-expand' },
      ]

      if (this.compareSafeStock) {
        headers.push({ text: '在庫總數', sortable: false, value: 'stkRecord_sum', width: '12%', class: 'sum_class' });
      }

      return headers;
    },

    //input: fromDateValP,
    //output: fromDateValP, compareDatePeriod
    displayPeriodDate() {
      if (this.fromDateValP != null) {
        let yy_value=this.fromDateValP.substring(0, 4);
        let mmdd_value=this.fromDateValP.substring(5, this.fromDateValP.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDatePeriod = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValP;
    },

    //input: fromDateValStart,
    //output: fromDateValStart, compareDateStart
    fromDateDispStart() {
      if (this.fromDateValStart != null) {
        let yy_value=this.fromDateValStart.substring(0, 4);
        let mmdd_value=this.fromDateValStart.substring(5, this.fromDateValStart.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDateStart = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValStart;
    },

    //input: fromDateValEnd,
    //output: fromDateValEnd, compareDateEnd
    fromDateDispEnd() {
      if (this.fromDateValEnd != null) {
        let yy_value=this.fromDateValEnd.substring(0, 4);
        let mmdd_value=this.fromDateValEnd.substring(5, this.fromDateValEnd.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDateEnd = yy_value + '/' + mmdd_value;
      }
      return this.fromDateValEnd;
    },
  },

  watch: {
    //input: dessertsDisplay,
    //       compareSafeStock
    //output: dessertsDisplay, dessertsDisplayForSelect
    //        itemsForSelect, selectedItems
    //        isAllSelected
    compareSafeStock(val) {
      if (val) {
        let safeStockEl=[];
        this.dessertsDisplayForCheckbox =  JSON.parse(JSON.stringify(this.dessertsDisplay))
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          let cStart=parseInt(this.dessertsDisplay[i].stkRecord_saftStock);     //安全庫存數量
          //let cEnd=this.dessertsDisplay[i].stkRecord_inStock_count;   //目前在庫存量
          let cEnd=this.dessertsDisplay[i].stkRecord_sum;             //目前在庫總數量
          console.log("start, end", cStart, cEnd)
          if (cEnd < cStart)
            safeStockEl.push(this.dessertsDisplay[i]);
        }
        this.dessertsDisplay =  Object.assign([], safeStockEl);
        //this.dessertsDisplayForCheckbox =  Object.assign([], this.dessertsDisplay);

        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();

        //if (removedEl.length !=0)
        //  this.initialize(removedEl);
        //else
        //  this.initialize(this.desserts);
      } else {
        this.dessertsDisplay =  Object.assign([], this.dessertsDisplayForCheckbox);
        this.dessertsDisplayForCheckbox=[];
      //  this.initialize(this.desserts);
      }
    },

    //input: desserts, dessertsDisplay,
    //       compareDatePeriod
    //output: dessertsDisplay, dessertsDisplayForSelect
    //        itemsForSelect, selectedItems
    //        isAllSelected
    compareDatePeriod(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stkRecord_period.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            console.log("效期, date: ", c1, c2)
            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },

    //input: desserts, dessertsDisplay,
    //       compareDate
    //output: dessertsDisplay, dessertsDisplayForSelect
    //        itemsForSelect, selectedItems
    //        isAllSelected
    compareDateStart(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar1 = obj.stkRecord_Date.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            let myVar2 = val.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },

    //input: desserts, dessertsDisplay,
    //       compareDateEnd
    //output: dessertsDisplay, dessertsDisplayForSelect
    //        itemsForSelect, selectedItems
    //        isAllSelected
    compareDateEnd(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stkRecord_Date.split('/');
            let c2 = myVar2.map(str => {
              return Number(str);
            });

            let myVar1 = val.split('/');
            let c1 = myVar1.map(str => {
              return Number(str);
            });

            if (c1[0] > c2[0])
                return obj;
            if (c1[0] == c2[0] && c1[1] > c2[1])
                return obj;
            if (c1[0] == c2[0] && c1[1] == c2[1] && c1[2] >= c2[2])
                return obj;
          });
        }
        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.getSumForDisplay();
      }
    },

    //input: temp_desserts,
    //       load_SingleTable_ok
    //output: dessertsy , dessertsDisplay, dessertsDisplayForSelect
    //        itemsForSelect, selectedItems
    //        isAllSelected
    //        load_SingleTable_ok
    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        //this.desserts = Object.assign([], this.temp_desserts);
        this.desserts =  JSON.parse(JSON.stringify(this.temp_desserts))
        this.desserts = this.desserts.map(v => ({...v, stkRecord_sum: '--'}))   //新增 在庫總數, 初始值為0
        this.desserts = this.desserts.map(v => ({...v, stkRecord_sumDisp: 0}))   //新增 在庫總數, 初始值為0

        //let unique = [...new Set(this.desserts.map(a => a['stkRecord_reagID']))];
        //console.log("duplicateIds: ", unique);

        var result = [this.desserts.reduce(function(agg, item) {
          agg[item.stkRecord_reagID] = (agg[item.stkRecord_reagID] || 0) + parseInt(item.stkRecord_inStock_count)
          return agg;
        }, {})]
        const temp_l=Object.keys(result[0]).length;
        //console.log("1. duplicateIds: ", result, temp_l);
        for (let j = 0; j < temp_l; j++) {
          let kk = this.desserts.find(element => {
            let temp=result.map(item => Object.keys(item)[j]);
            return element.stkRecord_reagID==temp[0];
          });
          //console.log("2-1. duplicateIds: ", kk.id);
          let idx = this.desserts.indexOf(kk);
          let temp_val=result.map(item => Object.values(item)[j]);
          this.desserts[idx].stkRecord_sum=temp_val[0];
          this.desserts[idx].stkRecord_sumDisp=temp_val[0];
          //this.desserts[idx].stkRecord_sum=this.desserts[idx].stkRecord_sum + ' [' + this.desserts[idx].stkRecord_sumDisp + ']';
        }

        this.dessertsDisplay = Object.assign([], this.desserts);

        this.dessertsDisplay = Object.assign([], this.desserts);

        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stkRecord_supplier)
        }
        this.itemsForSelect = [...new Set(removedEl)];
        this.selectedItems = Object.assign([], this.itemsForSelect);
        this.isAllSelected=true;

        this.load_SingleTable_ok=false;
      }
    },
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockRecords();
    //this.initialize(this.desserts);
  },

  methods: {
    initialize() {
        this.load_SingleTable_ok=false;
        this.listStockRecords();
    },

    listStockRecords() {    //從後端讀取dataTable的資料
      const path = '/listStockRecords';
      console.log("listStockRecords, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;    //true: dataTable的資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    exportToExcel() {
      console.log("StockRecord, exportToExcel, Axios post data...")

      let obj= {
        stkRecord_reagID: '資材碼',
        stkRecord_reagName: '品名',
        stkRecord_supplier: '供應商',
        stkRecord_Date: '入庫日期',
        stkRecord_period: '效期',
        stkRecord_saftStockUnit: '安全存量',
        stkRecord_cntUnit: '數量',
        stkRecord_grid: '儲位',
      }

      let object_Desserts = Object.assign([], this.dessertsDisplay);
      object_Desserts.unshift(obj);

      const path = '/exportToExcelForStock';
      var payload= {
        blocks: object_Desserts,
        //count: this.dessertsDisplay.length+1,
        count: this.object_Desserts.length,
        name: this.currentUser.name,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("export into excel status: ", res.data.status, res.data.outputs)
        if (res.data.status) {
          this.snackbar_color='#008184';
          this.snackbar=true;
          this.snackbar_info= '庫存記錄('+ res.data.outputs + ')轉檔完成!';
          this.snackbar_icon_color= "#ffffff";
        } else {
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          this.snackbar_info= '存檔錯誤!';
          this.snackbar_icon_color= '#adadad';
        }
      })
      .catch((error) => {
        console.error("axios error, code: ",error);
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '存檔錯誤!';
        this.snackbar_icon_color= '#adadad';
      });
    },

    checkSelect(e) {
      let ck=e.includes('全部');
      console.log('Select... ', e, ck, this.isAllSelected);
      if (ck) {  //press全部, 且不是全部的狀態
        if (this.isAllSelected) {
          this.isAllSelected = false;
          this.selectedItems = [];
          for (let i=1; i<e.length; i++) {
            this.selectedItems.push(e[i])
          }
        } else {
          console.log('Select all...');
          this.selectedItems = [];
          for (let i=0; i<this.itemsForSelect.length; i++) {
            this.selectedItems.push(this.itemsForSelect[i])
          }
          this.isAllSelected = true;
        }
      } else if (this.isAllSelected) {  //取消全部, 且不是全部的狀態
        console.log('Remove all...');
        this.selectedItems = [];
        this.isAllSelected = false;
      } else {  //取消全部, 且不是全部的狀態
        console.log('Click some item...');
        this.selectedItems = [];
        for (let i=0; i<e.length; i++) {
          let jj=this.itemsForSelect.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectedItems.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        console.log('length...', e.length, this.itemsForSelect.length);
        if (e.length==this.itemsForSelect.length-1) {
            this.selectedItems.unshift('全部')
            this.isAllSelected = true;
        }
      } //end else if

      console.log('item3...');

      if (this.selectedItems != []) {
        console.log('item4...');
        //this.dessertsDisplay = this.desserts.filter(val => this.selectedEmployers.includes(val.stockInTag_Employer));
        this.dessertsDisplay = this.dessertsDisplayForSelect.filter(val => this.selectedItems.includes(val.stkRecord_supplier));
      }
    },

    getExpand(value) {
      console.log("expand: ", value)
    },


    //查詢全部資料(不限制比較條件)
    //input: value, search, item
    //output: value
    filterOnlyCapsText(value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
        //value.toString().indexOf(search) !== -1
    },

    getSumForDisplay() {
        let result = [this.dessertsDisplay.reduce(function(agg, item) {
          agg[item.stkRecord_reagID] = (agg[item.stkRecord_reagID] || 0) + parseInt(item.stkRecord_inStock_count)
          return agg;
        }, {})]
        const temp_l=Object.keys(result[0]).length;
        //console.log("1. duplicateIds: ", result, temp_l);
        for (let j = 0; j < temp_l; j++) {
          let kk = this.dessertsDisplay.find(element => {
            let temp=result.map(item => Object.keys(item)[j]);
            return element.stkRecord_reagID==temp[0];
          });
          //console.log("2-1. duplicateIds: ", kk.id);
          let idx = this.dessertsDisplay.indexOf(kk);
          let temp_val=result.map(item => Object.values(item)[j]);
          //this.desserts[idx].stkRecord_sum=temp_val[0];

          //this.dessertsDisplay[idx].stkRecord_sumDisp=temp_val[0];
          this.dessertsDisplay[idx].stkRecord_sum=temp_val[0];
          //this.dessertsDisplay[idx].stkRecord_sum = '[' + temp_val[0] + '] ' + this.desserts[idx].stkRecord_sumDisp;
          //console.log("2-1. fun, duplicateIds: ", this.dessertsDisplay[idx].stkRecord_sum, this.desserts[idx].stkRecord_sum, this.dessertsDisplay[idx].stkRecord_sumDisp);

        }
        //this.dessertsDisplay[idx].stkRecord_sum=this.dessertsDisplay[idx].stkRecord_sum + ' [' + this.dessertsDisplay[idx].stkRecord_sumDisp + ']';
    },


    save () {
      //this.snack = true
      //this.snackColor = 'success'
      //this.snackText = 'Data saved'
      console.log('Dialog click save')
    },
    cancel () {
      //this.snack = true
      //this.snackColor = 'error'
      //this.snackText = 'Canceled'
      console.log('Dialog click cancel')
    },
    open () {
      //this.snack = true
      //this.snackColor = 'info'
      //this.snackText = 'Dialog opened'
      console.log('Dialog open')
    },
    close () {
      console.log('Dialog closed')
    },

    myFilter() {
      //this.checkStockDays();
      //this.checkSuppliers();
      //this.checkPeriodDays();
      this.checkSafeStock();
    /*
      let search=this.search;

      let j=0;
      let dessertsSearch=[];
      for (const item of this.dessertsDisplay) {
        var len = Object.keys(item).length;
        let nameList=[];
        for (let i = 0; i<len; i++) {
          nameList.push(Object.values(item)[i]);
        }

        if (nameList.toString().indexOf(search) != -1) {
          console.log("myFilter: ", j+1, nameList.toString());
          dessertsSearch.push(item);
        }
        j++;
      }
      //console.log("myFilter return: ", dessertsSearch);
      this.dessertsDisplay = Object.assign([], dessertsSearch);
    */
    },

    //查詢 1(針對入庫日期)
    /*
    checkStockDays() {
      let removedEl=[];
      let orangeEl= Object.assign([], this.dessertsDisplay);

      let c3 = (this.compareDateStart!='' || this.compareDateEnd!='');  //check start/end date does not blank
      for (let i = 0; i< orangeEl.length && c3; i++) {
        let myVarParts_end = orangeEl[i].stkRecord_Date.split('/');
        let arrOfNum_end = myVarParts_end.map(str => {
          return Number(str);
        });
        let cStockIn = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2])

        let cStart = new Date();
        if (this.compareDateStart!='') {
          myVarParts_end = this.compareDateStart.split('/');
          arrOfNum_end = myVarParts_end.map(str => {
            return Number(str);
          });
          cStart = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2]);
        }

        let cEnd = new Date();
        if (this.compareDateEnd!='') {
          myVarParts_end = this.compareDateEnd.split('/');
          arrOfNum_end = myVarParts_end.map(str => {
            return Number(str);
          });
          cEnd = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2]);
        }

        // 查詢開始日 < 入庫日 < 查詢結束日//
        //將入庫日與查詢開始日作日期比較
        //let diff1 = (cStockIn - cStart) / (1000 * 60 * 60 * 24);
        let diff1 = cStockIn - cStart;
        //將入庫日與查詢結束日作日期比較
        //let diff2 = (cEnd - cStockIn) / (1000 * 60 * 60 * 24);
        let diff2 = cEnd - cStockIn;
        //console.log("diff....",i, diff1, diff2, cStockIn, cStart, cEnd)

        if (diff1>=0 && diff2>=0) //Check if a Date is between Two Dates
          removedEl.push(orangeEl[i]);
      }

      if (removedEl.length!=0 && c3)
        this.initialize(removedEl);
      else
        this.initialize(orangeEl);
    },
    */
    //查詢 2(針對供應商)
    /*
    checkSuppliers() {
      let removedEl= Object.assign([], this.dessertsDisplay); //dtaaTable 顯示內容
      let orangeEl= Object.assign([], this.selectedItems);  //搜尋供應商條件內容
      orangeEl = orangeEl.filter(function( obj ) {
        return obj !== '全部';    //把'全部'選項刪除
      });

      let c3 = (this.selectedItems!='');  //check suppliers does not blank
      for (let i = 0; i< orangeEl.length && c3; i++) {
        removedEl = removedEl.filter(function( obj ) {
          return obj.stkRecord_supplier == orangeEl[i];
        });
      }

      if (removedEl.length!=0 && c3)
        this.initialize(removedEl);
    },
    */
    //查詢 3(針對效期)
    /*
    checkPeriodDays() {
      let removedEl=[];
      let orangeEl= Object.assign([], this.dessertsDisplay);

      let c1=parseInt(this.comparePeriods); //blank: isNaN(c1)=true
      for (let i = 0; i<orangeEl.length && !isNaN(c1); i++) {
        //console.log("diff1....")

        //將效期的國曆日期轉為西元年,並轉為Date Object
        let myVarParts_end = orangeEl[i].stkRecord_period.split('/');
        let arrOfNum_end = myVarParts_end.map(str => {
          return Number(str);
        });
        let cEnd = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2]) //月為index 0~11

        //當天+效期天數(西元年),並轉為Date Object
        let cToday=new Date();
        let cToday_add=cToday.addDays(c1);

        //將cToday_add(資料形式為Date Object)與cEnd(資料形式為Date Object)作日期比較
        //let diff2 = (cToday_add - cEnd) / (1000 * 60 * 60 * 24);
        let diff2 = (cToday_add - cEnd)
        //將cToday(資料形式為Date Object)與cEnd(資料形式為Date Object)作日期比較
        //let diff1 = (cToday - cEnd) / (1000 * 60 * 60 * 24);
        let diff1 = (cToday - cEnd)
        console.log("diff2, diff1....",i, diff2,diff1, c1)

        //console.log("diff1 : diff2: ",diff1, diff2)

        if ((diff2 >=0 && diff1 <0 && c1!=0) || (diff1 >=0 && c1==0))
          removedEl.push(orangeEl[i]);
      }

      //if (removedEl.length!=0 && c1!=0)
      if (removedEl.length!=0)
        this.initialize(removedEl);
      else
        this.initialize(orangeEl);
    },
    */
    //查詢 4(針對安全存量)
    checkSafeStock() {
      let removedEl=[];
      let orangeEl= Object.assign([], this.dessertsDisplay);

      let c1=this.compareSafeStock; //blank: isNaN(c1)=true
      for (let i = 0; i< orangeEl.length && c1; i++) {
        let s_unit = orangeEl[i].stkRecord_s_unit;        //入庫單位
        let c_unit = orangeEl[i].stkRecord_c_unit;        //在庫單位
        let s_cnt = orangeEl[i].stkRecord_saftStock;      //安全存量
        let c_cnt = orangeEl[i].stkRecord_cnt;            //在庫數量
        let scale = c_cnt / orangeEl[i].stkRecord_scale;  //入出庫單位比例
        let result=s_unit.localeCompare(c_unit);
        //顯示庫存不足資料
        let c2=((result==0) && (c_cnt < s_cnt))?true:false;
        let c3=((result!=0) && (c_cnt < scale))?true:false;
        //console.log("stock: ", i, result, c2, c3, c_cnt, s_cnt, scale, orangeEl[i].stkRecord_reagID)
        if (c2 || c3)
          removedEl.push(orangeEl[i]);
      }

      if (removedEl.length!=0 && c1)
        this.initialize(removedEl);
      else
        this.initialize(orangeEl);
    },

    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
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

::v-deep .v-data-table-header {
  background-color: #7DA79D;
}

::v-deep .v-data-table-header th {
  font-size: 0.9em !important;
}

::v-deep .v-data-table td {
  font-size: 12px !important;
}

::v-deep .v-label {
  /*font-size: 1em*/
  font-size: 14px;
}

::v-deep .v-label--active {
  /*font-size: 1em*/
  font-size: 14px;
  font-weight: bold;
}

::v-deep input::placeholder {
  font-size: 14px;
}
/*
::v-deep .v-text-field {
  width: 160px;
}
*/
::v-deep .v-input--selection-controls__input {
  margin-top: -8px;
}

::v-deep .v-input--checkbox {
  margin-top: 8px;
}
/*
::v-deep .v-text-field--box .v-input__slot, .v-text-field--outline .v-input__slot{
  min-height:36px !important;
  min-height: 36px !important;
  margin-top: 10px;
}
*/
::v-deep div.v-input__slot {
  min-height: 36px !important;
  margin-top: 14px;
  max-width: 140px !important;
}

::v-deep .v-input__prepend-outer {
  margin-right: 9px;
  margin-top: 14px;
}
/* for data table的header間距 start*/
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > tbody > tr > td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}
/* */
/* for data table的header, 最後一個row的color start*/
::v-deep .sum_class span {
  color: #1f4788 !important;
}
/* */

/*
::v-deep div.v-input__control > div.v-input__slot > fieldset {
  width: 170px;
}
*/
//::v-deep div.v-input__control {
//  max-width: 140px !important;
//}
/* for excel按鍵 start*/
.excel_wrapper {
  position: relative;
  top: -4px !important;
  right: -72px !important;
  width: 90px !important;
}
/* */

/* for 關鍵字查詢 start*/
::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 100px !important;
  width: 100px !important;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot {
  max-width: 100px !important;
  width: 100px !important;
}
/* */
/*
::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  min-width: 350px !important;
  width: 350px !important;
}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot {
  min-width: 350px !important;
  width: 350px !important;
}
*/
/* for 安全存量 start*/
::v-deep .myCheckbox {
  position: relative;
  top: -8px !important;
  right: -62px !important;
}
::v-deep .myCheckbox > .v-input__control > .v-input__slot > .v-text-field__slot > label{
  max-width: 120px !important;
  width: 120px !important;
}
::v-deep .myCheckbox > .v-input__control > .v-input__slot{
  max-width: 120px !important;
  width: 120px !important;
}
/* */
/* for 效期查詢 start*/
::v-deep .style-2 {
  position: relative;
  right: -46px !important;
}
::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 70px !important;
  width: 70px !important;
}
::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot {
  max-width: 70px !important;
  width: 70px !important;
}
/* */
/* for 入庫日期查詢 start*/
::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 120px !important;
  width: 120px !important;
}
::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}
/* */
/*-- for v-select begin--*/
::v-deep .style-4 {
  position: relative;
  right: -28px !important;
  top: -8px !important;
}
::v-deep div.v-input.style-4 > .v-input__control >.v-input__slot > .v-select__slot > .v-select__selections > input {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;

  //text-overflow: ellipsis;
  //white-space: nowrap;

  overflow-y: hidden !important;
}
::v-deep div.v-input.style-4 > .v-input__control >.v-input__slot > .v-select__slot > .v-label {
  margin-top: 4px;
  top: 12px;
  font-size: 14px;;
}
::v-deep .v-list--dense .v-list-item, .v-list-item--dense {
    min-height: 30px !important;
    height: 30px !important;
}
::v-deep .v-select.v-input--dense .v-select__selection--comma {
  font-size: 14px !important;
  margin: 5px 4px 3px 0 !important;
}
::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;
  top: 10px !important;
  overflow-y: hidden !important;
}
::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot > .v-select__slot > .v-select__selections {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;

  //text-overflow: ellipsis;
  //white-space: nowrap;

  overflow-y: hidden !important;
  margin-top: 12px !important;
}
/* */
::v-deep .v-data-table__expand-icon {
  color: red;
}


/*-- 以顏色識別最後一筆資料 begin--*/
//::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child {
//  background: #7DA79D;
//}
/* */
/*
::v-deep .v-select__selections {
  overflow-y: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-height: 50px;
}
*/
/*
small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}
*/
</style>