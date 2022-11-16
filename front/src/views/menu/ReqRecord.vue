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
        ></Toaster>
      </v-col>
    </v-row>

    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="70vw" class="pa-md-4 mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          item-key="name"
          :options.sync="pagination"
          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title>領用記錄查詢</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <!--<v-text-field v-model="search" label="Search (UPPER CASE ONLY)" class="mx-4"></v-text-field>-->
                <!--<v-text-field v-model="search" label="查詢" class="mx-4"></v-text-field>-->
                <v-text-field v-model="search" placeholder="關鍵字查詢" class="style-1"></v-text-field>

                <v-btn color="primary" class="mt-n1 mr-15 mx-auto" @click="exportToExcel">
                  <v-icon left>mdi-microsoft-excel</v-icon>
                  Excel
                </v-btn>
              </v-toolbar>
          </template>
          <template v-slot:body.append>
              <tr style="height=60px important;">
                <td></td>
                <td colspan="6">
                  <!-- 查詢 -->
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
                          placeholder="領用開始日期查詢"
                          prepend-icon="event"
                          readonly
                          :value="fromDateDisp"
                          v-model="compareDate"
                          v-on="on"
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
                          placeholder="領用截止日期查詢"
                          prepend-icon="event"
                          readonly
                          :value="fromDateDispEnd"
                          v-model="compareDateEnd"
                          v-on="on"
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
                <!--<td colspan="2"></td>-->
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

export default {
  name: 'ReqRecord',

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
      tosterBody: '領用記錄excel轉檔完成!',
      tosterTimeout: '3',
      tosterOK: false,

      myIndex: 0,
      myIndexEnd: 0,

      fromDateMenu: false,
      fromDateVal: null,
      compareDate: '',

      fromDateMenuEnd: false,
      fromDateValEnd: null,
      compareDateEnd: '',

      minDate: "2012-07-01",
      maxDate: "2042-06-30",

      search: '',

      pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      },

      desserts: [
      /*
        {
          reqRecord_reagID: '123456789',
          reqRecord_reagName: 'ABC',
          reqRecord_Date: '111/06/01',
          reqRecord_Employer: '陳健南',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567891',
          reqRecord_reagName: 'ABCD',
          reqRecord_Date: '111/05/01',
          reqRecord_Employer: '林成興',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567892',
          reqRecord_reagName: 'A11',
          reqRecord_Date: '111/04/01',
          reqRecord_Employer: '林成興',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567893',
          reqRecord_reagName: 'B11',
          reqRecord_Date: '111/04/01',
          reqRecord_Employer: '吳仲偉',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567894',
          reqRecord_reagName: 'C123',
          reqRecord_Date: '111/08/01',
          reqRecord_Employer: '吳仲偉',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567897',
          reqRecord_reagName: 'AB112233',
          reqRecord_Date: '111/07/11',
          reqRecord_Employer: '陳健南',
          reag_Out_unit: '盒',
          reqRecord_cnt: 4 + ' 盒',
        },
        {
          reqRecord_reagID: '234567898',
          reqRecord_reagName: 'ABC12345',
          reqRecord_Date: '111/06/01',
          reqRecord_Employer: '陳健南',
          reag_Out_unit: '瓶',
          reqRecord_cnt: 4 + ' 瓶',
        },
        {
          reqRecord_reagID: '234567899',
          reqRecord_reagName: 'D100',
          reqRecord_Date: '111/02/01',
          reqRecord_Employer: '吳仲偉',
          reag_Out_unit: '瓶',
          reqRecord_cnt: 4 + ' 瓶',
        },
      */
      ],

      load_SingleTable_ok: false, //for get employer table data
      load_2thTable_ok: false,
    }
  },

  computed: {
    headers () {
      return [
        { text: '資材碼', sortable: true, value: 'reqRecord_reagID', width: '10%', },
        { text: '品名', sortable: false, value: 'reqRecord_reagName', width: '15%',},
        //{ text: '供應商', sortable: true, value: 'stkRecord_supplier', width: '15%',},
        { text: '供應商', sortable: true, value: 'reqRecord_supplier', width: '15%',},
        { text: '入庫日期', sortable: false, value: 'reqRecord_stockInDate', width: '15%', },
        { text: '領用日期', sortable: false, value: 'reqRecord_Date', width: '15%',
          filter: value => {
            //console.log("date: ", this.reqRecord_Date);
            this.myIndexEnd=this.desserts.length;
            if (this.compareDate=="" || this.compareDateEnd=="") {
              this.myIndex=0;
              //this.myIndexEnd=this.desserts.length;
              return true
            }
            let kk=this.desserts[this.myIndex].reqRecord_Date
            let c1=this.strDateToNum(kk);
            let cStart=this.strDateToNum(this.compareDate);
            let cEnd=this.strDateToNum(this.compareDateEnd);
            console.log("date: ", c1, cStart, cEnd);
            this.myIndex++
            if (this.myIndex >= this.myIndexEnd) {
              this.myIndex=0;
            }

            return c1 >= cStart && c1 <= cEnd
          },
        },
        { text: '領用人員', sortable: false, value: 'reqRecord_Employer', width: '15%',},
        //{ text: '領用單位', sortable: false, value: 'reag_Out_unit', width: '15%' },
        { text: '領用數量', sortable: false, value: 'reqRecord_cnt', width: '15%' },
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

  watch: {
    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok: ", val)

      if (val) {
        //this.tosterBody = es.data.outputs;
        //this.tosterOK = true;  //true: open toster訊息畫面
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

    this.listRequirements();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listRequirements();
    },

    listRequirements() {    //從後端讀取dataTable的資料
      const path = '/listRequirements';
      console.log("listRequirements, Axios get data...")
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
      console.log("ReqRecord, exportToExcel, Axios post data...")

      let obj= {
        reqRecord_reagID: '資材碼',
        reqRecord_reagName: '品名',
        reqRecord_supplier: '供應商',
        reqRecord_stockInDate: '入庫日期',
        reqRecord_Date: '領用日期',
        reqRecord_Employer: '領用人員',
        reqRecord_cnt: '領用數量',
      }
      let object_Desserts = Object.assign([], this.desserts);
      object_Desserts.unshift(obj);
      console.log("object_Desserts: ",object_Desserts);

      const path = '/exportToExcelForReq';
      var payload= {
        //blocks: this.desserts,
        blocks: object_Desserts,
        count: this.desserts.length+1,
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

    //onRemoveToaster(val) {
    //      this.tosterOK=false;
    //},

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

::v-deep .v-label {
  font-size: 1em
}
::v-deep .v-label--active {
  font-size: 1em;
  font-weight: bold;
}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 350px !important;
  width: 350px !important;

}

::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot {
  max-width: 350px !important;
  width: 350px !important;
}

::v-deep  .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child {
  background: #7DA79D;
}
</style>