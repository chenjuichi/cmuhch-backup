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
      <v-card width="90vw" class="pa-md-4 mt-5 mx-lg-auto">
        <v-data-table            
          dense
          :headers="headers"
          :items="desserts"        
          class="elevation-1"
          :options.sync="pagination"
          :item-class="setRowStyle"        
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"          
        >
        <template v-slot:top>
          <v-toolbar flat>              
            <v-toolbar-title style="height: 40px;">盤點作業</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-spacer></v-spacer>
            <v-text-field label="請輸入關鍵字" class="style-0"></v-text-field>
            <v-spacer></v-spacer>
            <!--<v-text-field label="效期" class="style-2"></v-text-field>-->
            <v-menu
              v-model="fromDateMenuP"
              :close-on-content-click="false"
              :nudge-right="40"
              
              transition="scale-transition"
              offset-y
              
              max-width="280px"
              min-width="280px"
            >
              <template v-slot:activator="{ on }">
                <v-text-field
                  label="效期"
                  prepend-icon="event"
                  readonly
                  :value="fromDateDispP"
                  v-model="PeriodDate"
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
                @input="fromDateMenuP = false"
              ></v-date-picker>
            </v-menu>            
            <v-spacer></v-spacer>
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
                  label="入庫日期"
                  prepend-icon="event"
                  readonly
                  :value="fromDateDisp"
                  v-model="StockDate"
                  v-on="on"
                  class="shrink style-3"
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
            <v-spacer></v-spacer>
            <!--<v-text-field label="入庫人員" class="style-4"></v-text-field>-->
            <v-select
              :items="['陳瑞琪', '林政仰', '陳健南', '周明慶', '顏榮俊', '林成興', '吳仲偉']"
              label="入庫人員"
              prepend-icon="mdi-account-group"   
              v-model="Employer"
              class="style-4" 
            ></v-select>

            <v-btn color="primary" class="mt-n1 mr-15 mx-auto" @click="exportToExcel">
              <v-icon left>mdi-microsoft-excel</v-icon>
              Excel
            </v-btn>

          </v-toolbar>    
        </template>
        <!-- text field 1 -->
            <!--
            @open="editName = props.item.stockInTag_grid" 
            -->
        <template v-slot:item.stockInTag_grid="props">          
          <v-edit-dialog
            
            @save="saveName(props.item)"
            @open="openName(props.item.stockInTag_grid)"          
            @close="props.item.stockInTag_grid = editName"            
            :return-value.sync="props.item.stockInTag_grid"
            save-text="確定"
            cancel-text="取消"
            large
          > {{ props.item.stockInTag_grid }}
            <template v-slot:input>
              <v-row>
                <v-col cols="12" md="4">
                  <div style="color: #007bff; font-weight: 400; font-size: 14px;">站別</div>
                  <vue-numeric-input  
                    v-model="num1" 
                    :min="1" 
                    :max="3" 
                    :step="1"
                    align="center"
                    size="small"
                  ></vue-numeric-input>
                </v-col>
                <v-col cols="12" md="4">
                  <div style="color: #007bff; font-weight: 400; font-size: 14px;">層別</div>
                  <vue-numeric-input  
                    v-model="num2" 
                    :min="1" 
                    :max="5" 
                    :step="1"
                    align="center"
                    size="small"
                  ></vue-numeric-input>
                </v-col>              
                <v-col cols="12" md="4">
                  <div style="color: #007bff; font-weight: 400; font-size: 14px;">格位別</div>
                  <vue-numeric-input  
                    v-model="num3" 
                    :min="1" 
                    :max="10" 
                    :step="1"
                    align="center"
                    size="small"
                  ></vue-numeric-input>
                </v-col>            
              </v-row>

            <!--  
              <v-text-field
                v-model="editName"
                label="格位"
                single-line
                autofocus
              ></v-text-field>
            -->

            </template>
          </v-edit-dialog>
        </template>

        
        <!--
        <template v-slot:[`item.stockInTag_grid`]="{ item }">
          <v-text-field
            dense
            v-model="item.stockInTag_grid"
          
            class="pe-0 me-2 py-1 my-0 myText"           
            @input="getGrid(item)"         
          ></v-text-field>
        </template>
        -->
        <!-- text field 2 -->
        <template v-slot:[`item.stockInTag_cnt`]="{ item }">
          <v-text-field
            dense
            v-model="item.stockInTag_cnt"
             
            class="centered-input pe-0 me-2 py-1 my-0 myText"           
            @input="getData(item)"         
          ></v-text-field>
        </template>

        <!-- text field 3 -->
        <template v-slot:[`item.stockInTag_comment`]="{ item }">
          <v-text-field
            dense
            v-model="item.stockInTag_comment"
            
            class="pe-0 me-2 py-1 my-0 myText"           
            @input="getComment(item)"         
          ></v-text-field>
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
            <v-toolbar color="red" dark>錯誤訊息!</v-toolbar>          
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

import Common from '../../mixin/common.js'

import Toaster from '../../components/Toaster.vue';

export default {
  name: 'Inventory',

  mixins: [Common],

  components: {
    VueNumericInput, Toaster,
  },

  mounted() {
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));

      this.total_tags = 0;
      //if ("totalTags" in localStorage) {
      //  localStorage.setItem("totalTags", 0);
      //  console.log("...localStorage...");
      //} 
      localStorage.setItem("totalTags", 0);
    };
 
    this.root = document.documentElement;    
  },

  data: () => ({
    currentUser: {},
    permDialog: false,

    tosterTitlt: 'Hello',
    tosterType: 'info',
    tosterBody: '盤點記錄excel存檔完成!',
    tosterTimeout: '3',
    tosterOK: false,
    
    total_tags: 0,

    stockInTag_EmpID: '',   //入庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,

    fromDateMenu: false,
    fromDateVal: null,
    StockDate: '',  //庫存查詢開始日期

    fromDateMenuP: false,
    fromDateValP: null,
    PeriodDate: '',  //庫存查詢開始日期

    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    Employer: '',

    dialog: false, 
    
    drawer: false,
    root: null,
        
    singleSelect: false,
    selected: [],
    //資料表頭
    headers: [      
      { text: 'ID', sortable: true, value: 'id', width: '40px', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '50px' },
      { text: '品名', sortable: true, value: 'stockInTag_reagName', width: '90px' },
      { text: '效期', sortable: true, value: 'stockInTag_reagPeriod', width: '60px' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '60px' },
      { text: '入庫日期', sortable: true, value: 'stockInTag_Date', width: '60px' },
      { text: '入庫人員', sortable: true, value: 'stockInTag_Employer', width: '60px' },
      { text: '格位', sortable: false, value: 'stockInTag_grid', width: '50px' },
      { text: '數量', sortable: false, value: 'stockInTag_cnt', width: '10px' },
      { text: '說明', sortable: false, value: 'stockInTag_comment', width: '120px' },
    ], 
    
    pagination: { 
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
    },

    desserts: [],
    editedIndex: -1,

    editName: '',
    num1: 0,
    num2: 0,
    num3: 0,

    in_drafTags: 0,

    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get reagent table data
  }),

  computed: {
    check_selected() {   
      if (Array.isArray(this.selected) && this.selected.length) {
        // array exists and is not empty
        return true;
      } else {
        return false;
      }
    },

    fromDateDispP() {
      if (this.fromDateValP != null) {
        let yy_value=this.fromDateValP.substring(0, 4);
        let mmdd_value=this.fromDateValP.substring(5, this.fromDateValP.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.PeriodDate = yy_value + '/' + mmdd_value;
      }      
      return this.fromDateValP;
    },

    fromDateDisp() {
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.StockDate = yy_value + '/' + mmdd_value;
      }      
      return this.fromDateVal;
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },

    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
      }
    },

    drawer: {
      handler: function() {
        this.$nextTick(() => {
          if (this.drawer) {
            console.log("disable scrollbar...");
            this.root.style.setProperty('--bar','hidden');
          } else {
            console.log("enable scrollbar...");
            this.root.style.setProperty('--bar','scroll');
          }
        });
      },
      immediate: true,
    },
  },

  created () {
    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listInventorys();
    //this.initialize()
  },

  methods: {
    initialize() {
      this.load_SingleTable_ok=false;
      this.listInventorys();

      this.desserts = [
        /*        
        {
          id: 1000,
          stockInTag_reagID: '123456789',
          stockInTag_reagName: 'ABC',
          stockInTag_reagPeriod: '111/10/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_grid: '1站/4層/6格',
          stockInTag_cnt: 4,
          stockInTag_comment: '',
        },
        {
          id: 2,
          stockInTag_reagID: '234567891',
          stockInTag_reagName: 'ABCD',
          stockInTag_reagPeriod: '111/12/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_grid: '2站/4層/6格',
          //stockInTag_batch: '1110012345C123400055',
          stockInTag_cnt: 2,
          stockInTag_comment: '',
        },
        {
          id: 3,
          stockInTag_reagID: '234567892',
          stockInTag_reagName: 'A11',
          stockInTag_reagPeriod: '111/12/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_grid: '3站/4層/6格',
          //stockInTag_batch: '1110012345B123400033',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 4,
          stockInTag_reagID: '234567893',
          stockInTag_reagName: 'A12',
          stockInTag_reagPeriod: '112/6/30',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_grid: '1站/1層/6格',
          //stockInTag_batch: '1110012345B123400033',
          stockInTag_cnt: 1,
          stockInTag_comment: '',
        },
        {
          id: 5,
          stockInTag_reagID: '234567894',
          stockInTag_reagName: 'B2233',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_grid: '1站/2層/6格',
          //stockInTag_batch: '1110012345B123400022',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 6,
          stockInTag_reagID: '234567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_grid: '1站/3層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 1,
          stockInTag_comment: '',
        },
        {
          id: 7,
          stockInTag_reagID: '234567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_grid: '1站/4層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 8,
          stockInTag_reagID: '234567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_grid: '1站/5層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 5,
          stockInTag_comment: '',
        },
        {
          id: 9,
          stockInTag_reagID: '214567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_grid: '2站/1層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 10,
          stockInTag_reagID: '214567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_grid: '2站/2層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 2,
          stockInTag_comment: '',
        },
        {
          id: 11,
          stockInTag_reagID: '214567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_grid: '2站/3層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 12,
          stockInTag_reagID: '224567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_grid: '3站/4層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 20,
          stockInTag_comment: '',
        },
        {
          id: 13,
          stockInTag_reagID: '224567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_grid: '3站/1層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        {
          id: 14,
          stockInTag_reagID: '224567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_grid: '3站/2層/6格',
          //stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
          stockInTag_comment: '',
        },
        */
      ];
    },

    listInventorys() {    //從後端讀取dataTable的資料
      const path = '/listInventorys';
      console.log("listInventorys, Axios get data...")
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
      console.log("Inventory, exportToExcel, Axios post data...")
      
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

      let object_Desserts = Object.assign([], this.desserts);
      object_Desserts.unshift(obj);
      //console.log("object_Desserts: ",object_Desserts);

      const path = '/exportToExcelForInv';
      var payload= {
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

    saveName(item) {
      this.editName='' + this.num1 +'站/' + '' + this.num2 + '層/' + '' + this.num3 + '格'
      this.editedIndex = this.desserts.indexOf(item);
      
      this.desserts[ this.editedIndex].stockInTag_grid=this.editName;
      
      item.stockInTag_grid = this.editName;      
    },

    openName(item) {
      this.editName=item;
      this.num1=parseInt(this.editName[0]);
      this.num2=parseInt(this.editName[3]);
      this.num3=parseInt(this.editName[6]);
    },

    closeName(item) {
      item=this.editName;
    },

    cancelName() {

    },

    setRowStyle(item) {
      return 'style-1';
    },

    getGrid(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_grid);
    },

    getData(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_cnt);
    },

    getComment(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_comment);
    },

    onWaitTags(value) {
      console.log("total count for tags: ", value);
      this.total_tags=value;

      //if ("totalTags" in localStorage) {
      //  localStorage.removeItem('totalTags');
      //}
      localStorage.setItem("totalTags", this.total_tags);

      console.log("leave onWaitTags()...");
    },

    printSection() {
      console.log("click, printSection()...");
      this.drawer=true;
      /*
      this.$router.push({
        name: 'RenderBarCode',
        params: {
          selectDatas: this.selected,
        }        
      });
      */      
    },

    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar'); 
    },    
  },
}
</script>

<style>
:root {
  --bar: scroll;  
}

html {
  overflow-y: var(--bar) !important; 
} 
</style>

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
  font-size: 0.9em
}
::v-deep .v-label--active {
  font-size: 0.9em;
  font-weight: bold;
}

::v-deep .v-input.myText input {
  font-size: 0.7em;
}

::v-deep .v-data-table-header th:nth-child(1) i {
  color: blue !important;
}

::v-deep .v-data-table-header th:last-child span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(3) span {
  color: #1f4788 !important;
}

::v-deep header { 
  height: 48px !important;
  margin-top: 10px !important;
}

::v-deep .v-toolbar__content { 
  height: 42px !important;
}

::v-deep .v-toolbar__title { 
  height: 40px !important;
}

::v-deep .style-1 td {
  overflow: hidden !important;
  max-height: 28px !important;
  line-height: 16px !important;
  white-space: nowrap !important;
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  min-width: 40px !important;
}

::v-deep .fill-width {
  overflow-x: auto;
  flex-wrap: nowrap;
}

::v-deep .v-small-dialog__actions {
  text-align: center;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 200px !important;
  width: 200px !important;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot {
  max-width: 200px !important;
  width: 200px !important;
}

::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 150px !important;
  width: 150px !important;
}

::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot {
  max-width: 150px !important;
  width: 150px !important;
}

::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 150px !important;
  width: 150px !important;
}

::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot {
  max-width: 150px !important;
  width: 150px !important;
}

::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot > .v-select__slot > .v-select__selections > input {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep .centered-input > .v-input__control> .v-input__slot > .v-text-field__slot > input {
  text-align: center;
}
</style>