<template>
<v-app>
  <v-container fluid>
    <v-row v-show="tosterOK">
      <v-col class="d-flex justify-end">
        <Toaster 
          :Title="tosterTitlt" 
          :Type="tosterType" 
          :Body="tosterBody" 
          :Timeout="tosterTimeout"
          @removeToaster="tosterOK=false"
        >
        </Toaster>
      </v-col>
    </v-row>

    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="80vw" class="pa-md-4 mt-5 mx-lg-auto">  
        <v-data-table
          :headers="headers"
          :items="dessertsDisplay"
          item-key="name"
          :options.sync="pagination"
          class="elevation-1"

          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>庫存記錄查詢</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-text-field v-model="search" label="關鍵字查詢" class="style-1"></v-text-field>

                <v-btn color="primary" class="mt-n1 mr-15 mx-auto" @click="exportToExcel">
                  <v-icon left>mdi-microsoft-excel</v-icon>
                  Excel
                </v-btn>
              </v-toolbar>
          </template>
          <template v-slot:body.append>
              <tr>                                                
                <td colspan="7">
                  <v-row>
                    <!--查詢 1 -->                
                    <v-menu
                      v-model="fromDateMenu"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      
                      transition="scale-transition"
                      offset-y
                      
                      max-width="280px"
                      min-width="280px"
                    >
                      <template v-slot:activator="{ on }">
                        <v-text-field
                          label="入庫開始日期"
                          prepend-icon="event"
                          readonly
                          :value="fromDateDisp"
                          v-model="compareStockDateStart"
                          v-on="on"
                          class="shrink"                          
                        ></v-text-field>
                      </template>
                      <v-date-picker
                        locale="zh-TW"
                        :min="minDate"
                        :max="maxDate"
                        v-model="fromDateVal"
                        no-title
                        @input="fromDateMenu = false"
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
                          label="入庫截止日期"
                          prepend-icon="event"
                          readonly
                          :value="fromDateDispEnd"
                          v-model="compareStockDateEnd"
                          v-on="on"
                          class="shrink"
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

                    <!--查詢 2 -->               
                    <!--
                    <v-select
                      @input="limiter"
                    -->
                    <v-select
                      @change="checkSelect"                    
                      :items="items"
                      label="供應商"
                      outlined
                      multiple
                      class="mt-1 ml-3 mx-auto" 
                      style="width:100px; height:30px;"                      
                      v-model="selectSuppliers"
                    ></v-select>

                    <!--查詢 3 -->
                    <!--
                    <v-text-field
                      @focus="compareStockDateStart='';compareStockDateEnd='';"
                      @blur="resetSafeStockDays"
                      v-on:keyup.enter="resetSafeStockDays"
                    -->
                    <v-text-field
                      v-model="comparePeriods"
                      :value="comparePeriods"
                      :label="periodMessage"                          
                      class="shrink"
                    ></v-text-field>
                    <!--<small class="msgErr" v-text= "periodsErrMsg"></small>-->    

                    <!--查詢 4 -->
                    <v-checkbox class="myCheckbox"
                      v-model="compareSafeStock" 
                      color="primary" 
                      hide-details 
                      label="庫存數量不足"
                    ></v-checkbox>               
                  </v-row>
                </td>
                <!--查詢按鍵 -->
                <td>
                  <v-btn 
                    color="primary" 
                    class="mt-n1 mr-15 mx-auto" 
                    @click="myFilter"
                  >
                    <v-icon left>mdi-file-search-outline</v-icon>
                    查詢
                  </v-btn>
                </td>
              </tr>
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

import Toaster from '../../components/Toaster.vue';

import '../../mixin/dateformate.js'

export default {
  name: 'StockRecord',

  mixins: [Common],

  components: {
    Toaster,
  },

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

      tosterTitlt: 'Hello',
      tosterType: 'info',
      tosterBody: '庫存記錄excel存檔完成!',
      tosterTimeout: '3',
      tosterOK: false,

      //myIndex: 0,
      //myIndexEnd: 0,
      
      fromDateMenu: false,
      fromDateVal: null,
      compareStockDateStart: '',  //庫存查詢開始日期

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareStockDateEnd: '',    //庫存查詢結束日期

      comparePeriods: '',
      compareSafeStock: false,

      //compareStart: false,      

      minDate: "2012-07-01",
      maxDate: "2042-06-30",
      
      search: '', 
      
      periodMessage: '效期天數',

      headers: 
      [
        { text: '資材碼', sortable: true, value: 'stkRecord_reagID', width: '11%', },
        { text: '品名', sortable: false, value: 'stkRecord_reagName', width: '14%',},
        { text: '供應商', sortable: true, value: 'stkRecord_supplier', width: '12%',},
        { text: '入庫日期', sortable: true, value: 'stkRecord_Date', width: '13%',},
        { text: '效期', sortable: true, value: 'stkRecord_period', width: '8%',},
        { text: '安全存量', sortable: false, value: 'stkRecord_saftStockUnit', width: '12%', align: 'center' },
        { text: '數量', sortable: false, value: 'stkRecord_cntUnit', width: '8%', align: 'center' },
        { text: '儲位', sortable: false, value: 'stkRecord_grid', width: '14%', align: 'center' },
      ],
      /*
      filters: {
        comparePeriods: [],
        compareSafe: [],
      },
      */
      items:[],
      selectSuppliers: [],
      isAllSelected: false,

      pagination: { 
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      },

      dessertsDisplay: [],
      temp_desserts: [],
      desserts: [
        /*
        {
          stkRecord_reagID: '123456789',
          stkRecord_reagName: 'ABC',
          stkRecord_supplier: 'pmcA',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/06/30',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_s_unit: '盒',             //入庫單位
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',             //在庫單位
          stkRecord_grid: '2站2層4格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567891',
          stkRecord_reagName: 'ABCD',
          stkRecord_supplier: 'pmcB',
          stkRecord_Date: '111/05/01', 
          stkRecord_period: '111/07/20',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '3站2層6格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567892',
          stkRecord_reagName: 'A11',
          stkRecord_Date: '111/04/01', 
          stkRecord_supplier: 'pmcC',
          stkRecord_period: '111/09/30',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_saftStockUnit: 2 + ' 盒',        //id:234567892, 1盒=10瓶
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 0.4,
          stkRecord_cntUnit: 0.4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '3站1層6格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567893',
          stkRecord_reagName: 'B11',
          stkRecord_supplier: 'pmcD',
          stkRecord_Date: '111/04/01', 
          stkRecord_period: '111/05/31',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '3站2層2格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567894',
          stkRecord_reagName: 'C123',
          stkRecord_supplier: 'pmcE',
          stkRecord_Date: '111/08/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '2站3層5格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567897',
          stkRecord_reagName: 'AB112233',
          stkRecord_supplier: 'pmcLL',
          stkRecord_Date: '111/07/11', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_saftStock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 4 ,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '2站1層6格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567898',
          stkRecord_reagName: 'ABC12345',
          stkRecord_supplier: 'pmcB',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_saftStock: 6,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 6 + ' 盒',
          stkRecord_s_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '1站4層4格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        {
          stkRecord_reagID: '234567899',  //資材碼
          stkRecord_reagName: 'D100',     //品名
          stkRecord_supplier: 'pmcA123456789012345',
          stkRecord_Date: '111/02/01',    //入庫日期 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_saftStock: 2 ,             //安全存量2盒
          stkRecord_saftStockUnit: 2 +' 瓶',           //在庫存量單位
          stkRecord_s_unit: '瓶',
          stkRecord_cnt: 4,               //在庫存量數量 
          stkRecord_cntUnit: 4 +' 瓶',
          stkRecord_c_unit: '盒',
          stkRecord_grid: '1站4層5格',
          stkRecord_scale:  4,                        //入/出庫單位轉換比例
        },
        */
      ],
      /*
      dessertsReag: [
        {
          _R_ID: '123456789',  //資材瑪
          _R_Supplier: 'pmcA',     //供應商
          _R_Period: '111/06/30',  //效期
          _R_SaftStock: 2,         //安全存量
          _R_In_unit: '盒',         //入庫單位
          _R_Out_unit: '盒',         //出庫單位
          _R_In_Out_scale:  4,            //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567891',
          _R_Supplier: 'pmcB',
          _R_Period: '111/07/20',      //效期
          _R_SaftStock: 2,             //安全存量2盒          stkRecord_R_Employer: '林成興',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567892',
          _R_Supplier: 'pmcC',
          _R_Period: '111/09/30',      //效期
          _R_SaftStock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567893',
          _R_Supplier: 'pmcD',
          _R_Period: '111/05/31',      //效期
          _R_SaftStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567894',
          _R_Supplier: 'pmcE',
          _R_Period: '111/12/31',      //效期
          _R_SaftStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567897',
          _R_Supplier: 'pmcLL',
          _R_Period: '111/12/31',      //效期
          _R_SaftStock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567898',
          _R_Supplier: 'pmcB',
          _R_Period: '111/12/31',      //效期
          _R_SaftStock: 6,             //安全存量2盒          stkRecord_Employer: '陳健南',
          _R_In_unit: '盒',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                //入/出庫單位轉換比例
        },
        {
          _R_ID: '234567899',              //資材碼
          _R_Supplier: 'pmcA123456789012345',
          _R_Period: '111/12/31',              //效期
          _R_SaftStock: 2 ,                    //安全存量2盒
          _R_In_unit: '瓶',
          _R_Out_unit: '盒',
          _R_In_Out_scale:  4,                        //入/出庫單位轉換比例
        },
      ],      
      */
      load_SingleTable_ok: false, //for get employer table data
      load_2thTable_ok: false,    //for get department table data
      //load_3thTable_ok: false,    //for get permission table data
    }
  },
  
  watch: {
    comparePeriods(val) {
      let result = /\D/.test(val);
      this.periodMessage = '效期天數';
      if (result) {
        this.periodMessage = this.periodMessage + '請輸入數字!';        
      }    
    },

    /*
    compareSafeStock(val) {
        if (val) {
          let removedEl=[];
          for (let i = 0; i < this.desserts.length; i++) {        
            let cStart=this.desserts[i].stkRecord_saftStock;  //安全存量
            let cEnd=this.desserts[i].stkRecord_cnt;          //目前庫存量
            
            if (cEnd < cStart)
              removedEl.push(this.desserts[i]);
          }

          if (removedEl.length !=0)
            this.initialize(removedEl);
          else
            this.initialize(this.desserts);
        } else {
          this.initialize(this.desserts);
        }
    },
    */
    //關鍵字查詢
    search(val) {
      let search=val;
      
      //*let j=0;
      let dessertsSearch=[];
      
      //for (const item of this.desserts) {
      for (const item of this.dessertsDisplay) {
        var len = Object.keys(item).length;
        let nameList=[];
        for (let i=0; i<len; i++) {
          nameList.push(Object.values(item)[i]);
        }
        
        if (nameList.toString().indexOf(search) != -1) {
          //console.log("myFilter: ", j+1, nameList.toString());
          dessertsSearch.push(item);
        }
        //*j++;
      }
      //console.log("myFilter return: ", dessertsSearch);      
      this.dessertsDisplay = Object.assign([], dessertsSearch);      
    },

    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);
        this.dessertsDisplay = Object.assign([], this.desserts);
        //在v-select的供應商資料
        let removedEl=['全部'];
        for (let i = 0; i < this.desserts.length; i++) {
          removedEl.push(this.desserts[i].stkRecord_supplier)
        } 
        //console.log("suppliers: ", removedEl);
        this.items = [...new Set(removedEl)];

        this.load_SingleTable_ok=false;
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok: ", val)

      //if (val) {
        //this.tosterBody = es.data.outputs;
        //this.tosterOK = true;  //true: open toster訊息畫面
      //}  
    },
  },

  computed: {
    /*
    filteredDesserts() {
      return this.desserts.filter(d => {
        return Object.keys(this.filters).every(f => {
          return this.filters[f].length < 1 || this.filters[f].includes(d[f])
        })
      })
    },
    */
    fromDateDisp() {
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareStockDateStart = yy_value + '/' + mmdd_value;
      }      
      return this.fromDateVal;
    },

    fromDateDispEnd() {
      if (this.fromDateValEnd != null) {
        let yy_value=this.fromDateValEnd.substring(0, 4);
        let mmdd_value=this.fromDateValEnd.substring(5, this.fromDateValEnd.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareStockDateEnd = yy_value + '/' + mmdd_value;
      }      
      return this.fromDateValEnd;
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
    //initialize(buffer) {        
        //let cToday=new Date(); 
        /*
        for (let i = 0; i < buffer.length; i++) {      
          //let cEnd   = new Date(buffer[i].stkRecord_period);

          let myVarParts = buffer[i].stkRecord_period.split('/');
          let arrOfNum = myVarParts.map(str => {
            return Number(str);
          });
          let cEnd = new Date(arrOfNum[0]+1911, arrOfNum[1]-1, arrOfNum[2])

          //console.log("diff2-1: ",cToday,  cEnd)
          let diff2 = (cToday - cEnd) / (1000 * 60 * 60 * 24);
          console.log("diff2: ", cEnd, diff2)
          if (diff2 >= 0)
            buffer[i].stkRecord_reagID = '* ' + buffer[i].stkRecord_reagID
        }
        */

        //this.dessertsDisplay = Object.assign([], buffer);

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
      //console.log("object_Desserts: ",object_Desserts);

      const path = '/exportToExcelForStock';
      var payload= {
        blocks: object_Desserts,
        count: this.dessertsDisplay.length+1,
        name: this.currentUser.name,
      };      
      axios.post(path, payload)
      .then((res) => {
        console.log("export into excel status: ", res.data.status, res.data.outputs)
        if (res.data.status) {
          this.tosterBody = res.data.outputs;
          this.tosterOK = true;  //true: open toster訊息畫面
        } else {
          this.tosterOK = false;
        }
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
        this.tosterOK = false;
      });
    },
   
    //setWidth() {
    //  return 'style-1';
    //},    

    //*limiter(e) {
    //*  if(e.length > 2) {
    //*    console.log('you can only select two', e)
    //*    //e.pop()   //取出 array 最後item
    //*  }
    //*},

    //allFiltersBtn() {
    //  
    //}, 

    checkSelect(e) {
      let ck=e.includes('全部');
      console.log('Select... ', e, ck, this.isAllSelected);
      if (ck) {  //press全部, 且不是全部的狀態
        if (this.isAllSelected) {
          this.isAllSelected = false;
          this.selectSuppliers = [];
          for (let i=1; i<e.length; i++) {
            this.selectSuppliers.push(e[i])          
          }
        } else {
          console.log('Select all...');
          this.selectSuppliers = [];
          for (let i=0; i<this.items.length; i++) {
            this.selectSuppliers.push(this.items[i])
          }
          this.isAllSelected = true;
        }
      } else if (this.isAllSelected) {  //取消全部, 且不是全部的狀態
        console.log('Remove all...');
        this.selectSuppliers = [];
        this.isAllSelected = false;
      } else {  //取消全部, 且不是全部的狀態
        console.log('Click some item...');
        this.selectSuppliers = [];
        for (let i=0; i<e.length; i++) {
          let jj=this.items.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectSuppliers.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        console.log('length...', e.length, this.items.length);
        if (e.length==this.items.length-1) {
            this.selectSuppliers.push('全部')
            this.isAllSelected = true;
        }
      } //end else if

      this.checkSuppliers();
      
    },
    
    /*
    //查詢全部資料(不限制比較條件)
    filterOnlyCapsText(value, search, item) {     
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().indexOf(search) !== -1
        //value.toString().toLocaleUpperCase().indexOf(search) !== -1 
    },
    */

    myFilter() {
      this.checkStockDays();
      this.checkSuppliers();
      this.checkPeriodDays();
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
    checkStockDays() {
      let removedEl=[];
      let orangeEl= Object.assign([], this.dessertsDisplay);

      let c3 = (this.compareStockDateStart!='' || this.compareStockDateEnd!='');  //check start/end date does not blank
      for (let i = 0; i< orangeEl.length && c3; i++) {
        let myVarParts_end = orangeEl[i].stkRecord_Date.split('/');
        let arrOfNum_end = myVarParts_end.map(str => {
          return Number(str);
        });
        let cStockIn = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2])

        let cStart = new Date();
        if (this.compareStockDateStart!='') {
          myVarParts_end = this.compareStockDateStart.split('/');
          arrOfNum_end = myVarParts_end.map(str => {
            return Number(str);
          });
          cStart = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2]);
        }

        let cEnd = new Date();
        if (this.compareStockDateEnd!='') {
          myVarParts_end = this.compareStockDateEnd.split('/');
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

    //查詢 2(針對供應商)
    checkSuppliers() {
      let removedEl= Object.assign([], this.dessertsDisplay); //dtaaTable 顯示內容
      let orangeEl= Object.assign([], this.selectSuppliers);  //搜尋供應商條件內容
      orangeEl = orangeEl.filter(function( obj ) {
        return obj !== '全部';    //把'全部'選項刪除
      });

      let c3 = (this.selectSuppliers!='');  //check suppliers does not blank
      for (let i = 0; i< orangeEl.length && c3; i++) {
        removedEl = removedEl.filter(function( obj ) {
          return obj.stkRecord_supplier == orangeEl[i];
        });
      }
      
      if (removedEl.length!=0 && c3)
        this.initialize(removedEl);  
    },
    
    //查詢 3(針對效期)
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

::v-deep div.v-input.myCheckbox {
  margin-top: 13px;
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
  font-size: 1em
}

::v-deep .v-label--active {
  font-size: 1em;
  font-weight: bold;
}

::v-deep .v-text-field{
      width: 160px;
}

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

/*
::v-deep div.v-input__control > div.v-input__slot > fieldset {
  width: 170px;
}
*/
::v-deep div.v-input__control {
  max-width: 140px !important;
}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  min-width: 350px !important;
  width: 350px !important;
}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot {
  min-width: 350px !important;
  width: 350px !important;
}

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child { 
  background: #7DA79D; 
}

::v-deep .v-select__selections {
  overflow-y: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap;
  max-height: 50px;  
}
/*
small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}
*/
</style>