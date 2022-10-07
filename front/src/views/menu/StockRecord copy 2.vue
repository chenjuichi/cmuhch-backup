<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="80vw" class="pa-md-4 mx-lg-auto">  
        <v-data-table
          :headers="headers"
          :items="dessertsDisplay"
          item-key="name"
          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>庫存記錄查詢</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <!--<v-text-field v-model="search" label="Search (UPPER CASE ONLY)" class="mx-4"></v-text-field>-->
                <v-text-field v-model="search" label="查詢" class="mx-4"></v-text-field>
              </v-toolbar>
          </template>
          <template v-slot:body.append>
              <!--<tr style="height=60px important;">-->                                                
              <tr>                                                
                <td colspan="4">
                  <v-row>                
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
                          label="庫存查詢開始期間"
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
                          label="庫存查詢截止期間"
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

                    <v-select
                      ref="select"
                      :items="items"
                      label="供應商"
                      outlined
                      class="mt-1 ml-3 mx-auto" 
                      style="width:100px; height:30px;"
                      
                      v-model="selectSuppliers"

                      v-on:input="limiter"
                      @change="checkSelect($event)"
                      multiple
                    ></v-select>

                    <!--
                    <v-select
                      v-model="selectSuppliers"
                      :items="items"
                      label="供應商"
                      outlined
                      class="mt-1 ml-3 mx-auto" 
                      style="width:100px; height:30px;"
                      
                      multiple
                    ></v-select>
                    -->

                  </v-row>
                </td>

                <td>
                  <v-btn color="success" class="mt-n3 mr-15 mx-auto" @click="checkStockDays">
                    <v-icon left>mdi-file-search-outline</v-icon>
                    查詢
                  </v-btn>
                </td> 

                <td>
                  <v-text-field
                    @focus="compareStockDateStart='';compareStockDateEnd='';"
                    @blur="resetSafeStockDays"
                    v-on:keyup.enter="resetSafeStockDays"
                    v-model="comparePeriods"
                    :value="comparePeriods"
                    label="效期天數"                          
                    class="shrink"
                  ></v-text-field>
                </td>

                <td colspan="3">
                  <v-checkbox v-model="compareSafeStock" color="primary" hide-details label="庫存數量不足"></v-checkbox>                 
                </td>                

              </tr>
              <!--
              <tr style="height=60px important;">                                                
                <td colspan="4">
                  <v-row>                

                    <v-select
                      v-model="selectSuppliers"
                      :items="items"
                      label="供應商"
                      outlined
                      class="mt-1 ml-3 mx-auto" 
                      style="width:100px; height:30px;"
                      
                      multiple
                    ></v-select>

                  </v-row>
                </td>

                <td>
                  <v-btn color="success" class="mt-n3 mr-15 mx-auto" @click="checkStockDays">
                    <v-icon left>mdi-file-search-outline</v-icon>
                    查詢
                  </v-btn>
                </td>         
              </tr>
              -->
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
</template>

<script>
import axios from 'axios';
import Common from '../../mixin/common.js'

import '../../mixin/dateformate.js'

export default {
  name: 'StockRecord',
  mixins: [Common],

  data () {
    return {
      currentUser: {},      
      permDialog: false,

      myIndex: 0,
      myIndexEnd: 0,
      
      fromDateMenu: false,
      fromDateVal: null,
      compareStockDateStart: '',  //庫存查詢開始日期

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareStockDateEnd: '',    //庫存查詢結束日期

      comparePeriods: '',
      compareSafeStock: false,

      compareStart: false,      

      minDate: "2012-07-01",
      maxDate: "2042-06-30",
      
      search: '', 
      
      headers: 
      [
        { text: '資材碼', sortable: true, value: 'stkRecord_reagID', width: '11%', },
        { text: '品名', sortable: false, value: 'stkRecord_reagName', width: '14%',},
        { text: '供應商', sortable: true, value: 'stkRecord_supplier', width: '12%',},
        { text: '入庫日期', sortable: true, value: 'stkRecord_Date', width: '13%',},
        { text: '效期', sortable: true, value: 'stkRecord_period', width: '8%',},
        { text: '安全存量', sortable: false, value: 'stkRecord_saftStockUnit', width: '12%', align: 'center' },
        //{ text: '單位', sortable: false, value: 'stkRecord_saftStockUnit', width: '8%', align: 'center' },
        { text: '數量', sortable: false, value: 'stkRecord_cntUnit', width: '8%', align: 'center' },
        { text: '儲位', sortable: false, value: 'stkRecord_grid', width: '14%', align: 'center' },
      ],

      filters: {
        comparePeriods: [],
        compareSafe: [],
      },

      items:[],
      selectSuppliers: [],
      isAllSelected: false,
      dessertsDisplay: [],
      desserts: [
        {
          stkRecord_reagID: '123456789',
          stkRecord_reagName: 'ABC',
          stkRecord_supplier: 'pmcA',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/06/30',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '2站2層4格',
        },
        {
          stkRecord_reagID: '234567891',
          stkRecord_reagName: 'ABCD',
          stkRecord_supplier: 'pmcB',
          stkRecord_Date: '111/05/01', 
          stkRecord_period: '111/07/20',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '3站2層6格',
        },
        {
          stkRecord_reagID: '234567892',
          stkRecord_reagName: 'A11',
          stkRecord_Date: '111/04/01', 
          stkRecord_supplier: 'pmcC',
          stkRecord_period: '111/09/30',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_saftStockUnit: 2 + ' 盒',        //id:234567892, 1盒=10瓶
          stkRecord_cnt: 0.4,
          stkRecord_cntUnit: 0.4 + ' 盒',
          stkRecord_grid: '3站1層6格',
        },
        {
          stkRecord_reagID: '234567893',
          stkRecord_reagName: 'B11',
          stkRecord_supplier: 'pmcD',
          stkRecord_Date: '111/04/01', 
          stkRecord_period: '111/05/31',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '3站2層2格',
        },
        {
          stkRecord_reagID: '234567894',
          stkRecord_reagName: 'C123',
          stkRecord_supplier: 'pmcE',
          stkRecord_Date: '111/08/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '2站3層5格',
        },
        {
          stkRecord_reagID: '234567897',
          stkRecord_reagName: 'AB112233',
          stkRecord_supplier: 'pmcLL',
          stkRecord_Date: '111/07/11', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_sfteStock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 2 + ' 盒',
          stkRecord_cnt: 4 ,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '2站1層6格',
        },
        {
          stkRecord_reagID: '234567898',
          stkRecord_reagName: 'ABC12345',
          stkRecord_supplier: 'pmcB',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_sfteStock: 6,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_saftStockUnit: 6 + ' 盒',
          stkRecord_cnt: 4,
          stkRecord_cntUnit: 4 + ' 盒',
          stkRecord_grid: '1站4層4格',
        },
        {
          stkRecord_reagID: '234567899',  //資材碼
          stkRecord_reagName: 'D100',     //品名
          stkRecord_supplier: 'pmcA',
          stkRecord_Date: '111/02/01',    //入庫日期 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_sfteStock: 2 ,             //安全存量2盒
          stkRecord_saftStockUnit: 2 +' 瓶',           //在庫存量單位
          stkRecord_cnt: 4,               //在庫存量數量 
          stkRecord_cntUnit: 4 +' 瓶',
          stkRecord_grid: '1站4層5格',
        },
      ],

      //load_SingleTable_ok: false, //for get employer table data
      //load_2thTable_ok: false,    //for get department table data
      //load_3thTable_ok: false,    //for get permission table data
    }
  },
  
  watch: {
    compareSafeStock(val) {
        if (val) {
          let removedEl=[];
          //let c1=parseInt(this.comparePeriods);
          for (let i = 0; i < this.desserts.length; i++) {        
            let cStart=this.desserts[i].stkRecord_sfteStock;  //安全存量
            let cEnd=this.desserts[i].stkRecord_cnt;          //目前庫存量
            
            //let diff =cEnd - cStart;
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
  },

  computed: {
    filteredDesserts() {
      return this.desserts.filter(d => {
        return Object.keys(this.filters).every(f => {
          return this.filters[f].length < 1 || this.filters[f].includes(d[f])
        })
      })
    },
    
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
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
    }

    //this.load_SingleTable_ok = false;
    this.initAxios();

    this.initialize(this.desserts);
  },

  mounted() {
    //this.$refs.select.lastItem = 2;
    let removedEl=['全部'];
    for (let i = 0; i < this.desserts.length; i++) {
      removedEl.push(this.desserts[i].stkRecord_supplier)
    }
    
    this.items = [...new Set(removedEl)];
    console.log("mounted... ", this.items, removedEl)
  },

  methods: {
    initialize(buffer) {
        
        let cToday=new Date(); 
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
        this.dessertsDisplay = Object.assign([], buffer);
    },

    limiter(e) {
      if(e.length > 2) {
        console.log(' you can only select two', e, typeof(e))
        //e.pop()
      }
    },

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
      }
      
    },

    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },

    checkStockDays() {
      console.log("hello checkStockDays....")
      let removedEl=[];
      let c3=(this.compareStockDateStart!='' || this.compareStockDateEnd!='');
      for (let i = 0; i<this.desserts.length && c3; i++) {
        //this.myIndexEnd=this.desserts.length;
            
        let myVarParts_end = this.desserts[i].stkRecord_Date.split('/');
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
        console.log("diff....",i, diff1, diff2, cStockIn, cStart, cEnd)
        
        if (diff1>=0 && diff2>=0) //Check if a Date is between Two Dates
          removedEl.push(this.desserts[i]);
      }

      if (removedEl.length!=0 && c3)
        this.initialize(removedEl);
      else
        this.initialize(this.desserts);
    },

    resetSafeStockDays() {
      let removedEl=[];
      let c1=parseInt(this.comparePeriods); //blank: isNaN(c1)=true
      for (let i = 0; i<this.desserts.length && !isNaN(c1); i++) {
        //將效期的國曆日期轉為西元年,並轉為Date Object
        let myVarParts_end = this.desserts[i].stkRecord_period.split('/');
        let arrOfNum_end = myVarParts_end.map(str => {
          return Number(str);
        });
        let cEnd = new Date(arrOfNum_end[0]+1911, arrOfNum_end[1]-1, arrOfNum_end[2])
        
        //當天+效期天數(西元年),並轉為Date Object
        let cToday=new Date();
        let cToday_add=cToday.addDays(c1);

        //將cToday_add(資料形式為Date Object)與cEnd(資料形式為Date Object)作日期比較
        let diff2 = (cToday_add - cEnd) / (1000 * 60 * 60 * 24);
        //將cToday(資料形式為Date Object)與cEnd(資料形式為Date Object)作日期比較
        let diff1 = (cToday - cEnd) / (1000 * 60 * 60 * 24);

        console.log("diff1 : diff2: ",diff1, diff2)

        if (diff2 >=0 || diff1 >=0)
          removedEl.push(this.desserts[i]);
      }

      if (removedEl.length!=0 && c1!=0)
        this.initialize(removedEl);
      else
        this.initialize(this.desserts);
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

::v-deep  .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child { 
  background: #7DA79D; 
}

::v-deep .v-select__selections {
  overflow-y: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap;
  max-height: 50px;  
}
</style>