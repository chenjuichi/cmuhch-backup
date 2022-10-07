<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="70vw" class="pa-md-4 mx-lg-auto">  
        <v-data-table
          :headers="headers"
          :items="desserts"
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
              <tr style="height=60px important;">
                                                
                <td colspan="4">
                  <v-row>                
                  <v-menu
                    v-model="fromDateMenu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="280px"
                    min-width="280px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        label="庫存查詢開始期間"
                        prepend-icon="event"
                        readonly
                        :value="fromDateDisp"
                        v-model="compareDate"
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
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    max-width="280px"
                    min-width="280px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        label="庫存查詢截止期間"
                        prepend-icon="event"
                        readonly
                        :value="fromDateDispEnd"
                        v-model="compareDateEnd"
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
                  </v-row>
                </td>
                
                <td>
                  <v-text-field
                    @focus="compareDate='';compareDateEnd='';"
                    @blur="resetSafeStockDays"
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
      compareDate: '',

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareDateEnd: '',

      comparePeriods: '',
      compareSafeStock: false,

      compareStart: false,      

      minDate: "2012-07-01",
      maxDate: "2042-06-30",
      
      search: '',      
      desserts: [
        {
          stkRecord_reagID: '123456789',
          stkRecord_reagName: 'ABC',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/06/30',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '2站2層4格',
          stkRecord_safe: true          
        },
        {
          stkRecord_reagID: '234567891',
          stkRecord_reagName: 'ABCD',
          stkRecord_Date: '111/05/01', 
          stkRecord_period: '111/06/30',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '3站2層6格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567892',
          stkRecord_reagName: 'A11',
          stkRecord_Date: '111/04/01', 
          stkRecord_period: '111/06/30',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '林成興',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '3站1層6格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567893',
          stkRecord_reagName: 'B11',
          stkRecord_Date: '111/04/01', 
          stkRecord_period: '111/05/31',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '3站2層2格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567894',
          stkRecord_reagName: 'C123',
          stkRecord_Date: '111/08/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '吳仲偉',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '2站3層5格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567897',
          stkRecord_reagName: 'AB112233',
          stkRecord_Date: '111/07/11', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_unit: '盒',
          stkRecord_cnt: 4,
          stkRecord_grid: '2站1層6格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567898',
          stkRecord_reagName: 'ABC12345',
          stkRecord_Date: '111/06/01', 
          stkRecord_period: '111/12/31',  //效期
          stkRecord_stock: 2,             //安全存量2盒          stkRecord_Employer: '陳健南',
          stkRecord_unit: '瓶',
          stkRecord_cnt: 4,
          stkRecord_grid: '1站4層4格',
          stkRecord_safe: false      
        },
        {
          stkRecord_reagID: '234567899',  //資材碼
          stkRecord_reagName: 'D100',     //品名
          stkRecord_Date: '111/02/01',    //入庫日期 

          stkRecord_In_unit: '盒',        //入庫單位
          stkRecord_Out_unit: '瓶',       //出庫單位
          stkRecord_Scale: 5,             //5瓶=1盒

          stkRecord_period: '111/12/31',  //效期
          stkRecord_stock: 2,             //安全存量2盒

          stkRecord_unit: '瓶',           //在庫存量單位
          stkRecord_cnt: 4,               //在庫存量數量 
          stkRecord_grid: '1站4層5格',
          stkRecord_safe: false      
        },
      ],

      //load_SingleTable_ok: false, //for get employer table data
      //load_2thTable_ok: false,    //for get department table data
      //load_3thTable_ok: false,    //for get permission table data
    }
  },
  
  watch: {
      /*
      comparePeriods(val) {
        //this.myIndexEnd=0;
        this.compareStart=false;
        for (let i = 0; i < this.desserts.length; i++) {    
          let cStart=this.strDateToNum(this.desserts[i].stkRecord_Date);
          let cEnd=this.strDateToNum(this.desserts[i].stkRecord_period);
          let diff =cEnd - cStart;

          let c1=parseInt(val);
          this.desserts[i].stkRecord_safe=false;
          if (diff <= c1)
            this.desserts[i].stkRecord_safe=true;
          console.log("safe days: ", i, cEnd, cStart, diff, c1, this.desserts[i].stkRecord_safe)
        }
        this.myIndex=0;
        this.myIndexEnd=this.desserts.length;
        this.compareStart=true;
      }
      */
  },


  computed: {
    headers () {
      return [
        { text: '資材碼', sortable: true, value: 'stkRecord_reagID', width: '10%', },
        { text: '品名', sortable: false, value: 'stkRecord_reagName', width: '20%',},
        { text: '入庫日期', sortable: false, value: 'stkRecord_Date', width: '13%', 
          filter: value => {
            this.myIndexEnd=this.desserts.length;
            if (this.compareDate=="" || this.compareDateEnd=="") {
              this.myIndex = 0;
              return true;
            }
            let kk=this.desserts[this.myIndex].stkRecord_Date
            let c1=this.strDateToNum(kk);
            let cStart=this.strDateToNum(this.compareDate);
            let cEnd=this.strDateToNum(this.compareDateEnd);
            console.log("date: ", c1, cStart, cEnd);
            this.myIndex++
            if (this.myIndex >= this.myIndexEnd) {
              this.myIndex=0;
            }

            return (c1 >= cStart && c1 <= cEnd);
          },      
        },

        { text: '效期', sortable: true, value: 'stkRecord_period', width: '8%',
        
          filter: value => {
            this.myIndexEnd=this.desserts.length;
            if (!this.compareStart) {
              console.log("safe days: none")
              this.myIndex = 0;
              return true;
            }

            let cStart=this.strDateToNum(this.desserts[this.myIndex].stkRecord_Date);
            let cEnd=this.strDateToNum(this.desserts[this.myIndex].stkRecord_period);
            let diff =cEnd - cStart;

            let c1=parseInt(this.comparePeriods);
          
          //if (diff <= c1)
            //this.desserts[i].stkRecord_safe=true;
            console.log("safe days: ", this.myIndex, this.myIndexEnd, cEnd, cStart, diff, c1)
            this.myIndex++
            //if (this.myIndex >= this.myIndexEnd) {
            //  this.myIndex=0;
            //  this.compareStart=false;
            //}
            if (this.myIndex < this.myIndexEnd) {

              return (diff <= c1);
            }
          },
        },
        { text: '安全存量', sortable: false, value: 'stkRecord_stock', width: '10%', align: 'center' },
        { text: '單位', sortable: false, value: 'stkRecord_unit', width: '10%', align: 'center' },
        { text: '數量', sortable: false, value: 'stkRecord_cnt', width: '10%', align: 'center' },
        { text: '儲位', sortable: false, value: 'stkRecord_grid', width: '20%', align: 'center' },
      ]
    },
    
    fromDateDisp() {
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.compareDate = yy_value + '/' + mmdd_value;
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
        this.compareDateEnd = yy_value + '/' + mmdd_value;
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

    //this.initialize()
  },

  methods: {
    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },

    strDateToNum(myVar) {
      var myVarParts = myVar.split('/');

      var arrOfNum = myVarParts.map(str => {
        return Number(str);
      });

      var tt=arrOfNum[0]*10000+arrOfNum[1]*100+arrOfNum[2];

      return tt;
    },

    computeSafeStockDays(i) {
      //for (let i = 0; i < this.desserts.length; i++) {
        let cStart=this.strDateToNum(this.desserts[i].stkRecord_Date);
        let cEnd=this.strDateToNum(this.desserts[i].stkRecord_period);
        let val =cEnd - cStart;

        let c1=parseInt(this.comparePeriods);
        console.log("safe days: ", i, cEnd, cStart, val, c1)
        this.desserts[i].stkRecord_safe=false;
        if (val <= c1)
          this.desserts[i].stkRecord_safe=true;
      //}
    },

    resetSafeStockDays() {
      this.compareStart=true;
      //for (let i = 0; i < this.desserts.length; i++) {
      //  this.desserts[i].stkRecord_safe=false;
      //}
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

::v-deep .v-label {
  font-size: 1.2em
}

::v-deep .v-label--active {
  font-size: 1.2em;
  font-weight: bold;
}

::v-deep .v-text-field{
      width: 200px;
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
</style>