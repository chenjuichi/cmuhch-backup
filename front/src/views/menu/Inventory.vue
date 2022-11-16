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
      <v-card width="90vw" class="pa-md-4 mt-5 mx-lg-auto">
        <v-data-table
          dense
          :headers="headers"
          :items="dessertsDisplay"

          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
          :options.sync="pagination"
          :item-class="setRowStyle"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title style="height: 40px;">盤點作業</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <!-- 查詢 -->
              <v-spacer></v-spacer>
              <v-text-field v-model="search" placeholder="關鍵字查詢" class="style-0"></v-text-field>
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
              <v-spacer></v-spacer>
              <!-- 入庫日期查詢 -->
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
                    placeholder="入庫開始日期查詢"
                    prepend-icon="event"
                    readonly
                    :value="fromDateDisp"
                    v-model="compareDate"
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
              <!--<v-spacer></v-spacer>-->
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
              <!-- 人員查詢 -->
              <!--
              <v-select
                :items="usersSelected"
                placeholder="入庫人員查詢"
                prepend-icon="mdi-account-group"
                v-model="Employer"
                class="style-4"
              ></v-select>
              -->
              <v-select
                @change="checkSelect"
                :items="itemsForEmployer"
                label="入庫人員查詢"
                prepend-icon="mdi-account-group"
                v-model="selectedEmployers"
                class="style-4"
                dense
                outlined
                multiple
              ></v-select>

              <!-- 按鍵指令 -->
              <v-btn color="primary" class="mt-n1 mr-15 mx-auto excel_wrapper" @click="exportToExcel">
                <v-icon left>mdi-microsoft-excel</v-icon>
                Excel
              </v-btn>
              <div class="flip_wrapper">
                <div class="flip_btn">
                  <v-btn color="primary" class="side default-side mt-n1 mr-15 mx-auto">
                    <v-icon left>mdi-content-save-edit-outline</v-icon>
                    在庫資料更新
                  </v-btn>
                  <v-btn color="primary" class="side hover-side mt-n1 mr-15 mx-auto" @click="updateStockInDataByInv">
                    <v-icon left size="24px">mdi-check-circle-outline</v-icon>
                    確定?
                  </v-btn>
                </div>
              </div>
            </v-toolbar>
          </template>

          <template v-slot:item.stockInTag_grid="props">
            <v-edit-dialog
              @save="saveName(props.item)"
              @open="openName(props.item.stockInTag_grid)"
              @close="props.item.stockInTag_grid = editName"
              :return-value.sync="props.item.stockInTag_grid"
              save-text="確定"
              cancel-text="取消"
              large
            >
              {{ props.item.stockInTag_grid }}
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
          <template v-slot:[`item.stockInTag_cnt`]="{ item, index }">
  <!--T <v-tooltip class="tooltip1"  bottom color="red">-->
  <!--T   <template v-slot:activator="{ on, attrs }">-->
            <div class="row_myText_inv">
                <v-text-field
                  dense
                  readonly
                  v-model="temp_desserts[index].stockInTag_cnt"
                  class="centered-input pe-0 me-2 py-1 my-0 block_myText_inv_cnt"
                  @input="getData(item)"
                ></v-text-field>

  <!--T-->  <v-tooltip class="tooltip2" bottom color="#434343">
  <!--T-->    <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  dense
                  v-model="item.editReagentID"
                  @keydown.enter="modifyIDForPressRet(item)"
                  @blur="modifyIDForBlur(item)"
                  @focus="modifyIDForFocus(item)"

                  v-bind="attrs"
                  v-on="on"

                  class="centered-input pe-0 me-2 py-1 my-0 block_myText_inv_id"
                  :class="{'block_myText_inv_cnt_mdf_color' : item.isEnter}"
                ></v-text-field>
  <!--T-->    </template>
  <!--T-->    <span>選取</span>
  <!--T-->  </v-tooltip>

                <v-text-field
                  dense

                  v-model="item.stockInTag_cnt_inv_mdf"
                  class="centered-input pe-0 me-2 py-1 my-0 block_myText_inv_cnt_mdf"
                  :class="{'block_myText_inv_cnt_mdf_color' : item.isEnter}"
                  @input="getData(item)"
                  @blur="modifyInvCntForBlur(item)"
                  @focus="modifyInvCntForFocus(item)"
                ></v-text-field>
            </div>
  <!--T    </template>-->
  <!--T   <span>修改後, 請寫說明!</span>-->
  <!--T  </v-tooltip>-->
          </template>

          <!-- text field 3 -->
          <template v-slot:[`item.stockInTag_comment`]="{ item }">
  <!--  <v-tooltip class="tooltip2" bottom color="red"> T-->
  <!--    <template v-slot:activator="{ on, attrs }"> T-->
            <v-text-field
              dense
              v-model="item.stockInTag_comment"

              class="pe-0 me-2 py-1 my-0 myText"
              @input="getComment(item)"

            ></v-text-field>
  <!--    </template> T-->
  <!--    <span>請寫說明!</span> T-->
  <!--  </v-tooltip> T-->
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

export default {
  name: 'Inventory',

  mixins: [Common],

  components: {
    VueNumericInput,
  },

  mounted() {
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));

      //this.total_tags = 0;
      ////if ("totalTags" in localStorage) {
      ////  localStorage.setItem("totalTags", 0);
      ////  console.log("...localStorage...");
      ////}
      //localStorage.setItem("totalTags", 0);
    };

    //this.root = document.documentElement;
  },

  data: () => ({
    currentUser: {},
    permDialog: false,

    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',

    //total_tags: 0,

    //stockInTag_EmpID: '',   //入庫人員之員工編號

    //errorShowForEmployer: false,
    //errorShowForReagName: false,

    fromDateMenu: false,
    fromDateVal: null,
    compareDate: '',          //查詢開始日期

    //myIndex: 0,
    //myIndexEnd: 0,

    fromDateMenuEnd: false,
    fromDateValEnd: null,
    compareDateEnd: '',       //查詢截止日期

    fromDateMenuPeriod: false,
    fromDateValP: null,
    compareDatePeriod: '',    //庫存效期日期

    minDate: "2012-07-01",
    maxDate: "2042-06-30",


    //dialog: false,

    //drawer: false,
    //root: null,

    //upHere: false,

    search: '',

    //singleSelect: false,
    //selected: [],

    //資料表頭
    headers: [
      { text: 'ID', sortable: false, value: 'id', width: '4%', align: 'start' },
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '8%' },
      { text: '品名', sortable: true, value: 'stockInTag_reagName', width: '17%' },
      { text: '效期', sortable: true, value: 'stockInTag_reagPeriod', width: '7%' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '8%' },
      { text: '入庫日期', sortable: true, value: 'stockInTag_Date', width: '8%' },
      { text: '入庫人員', sortable: true, value: 'stockInTag_Employer', width: '8%' },
      { text: '格位', sortable: false, value: 'stockInTag_grid', width: '8%' },
      { text: '在庫數 _ 盤點數', sortable: false, value: 'stockInTag_cnt', width: '11%', align: 'center' },
      { text: '說明', sortable: false, value: 'stockInTag_comment', width: '18%' },
    ],

    pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
    },

    itemsForEmployer: [],
    selectedEmployers: [],
    isAllSelected: false,

    //temp_itemsForEmployer: [],

    dessertsDisplayForSelect: [],
    dessertsDisplay: [],
    desserts: [],
    temp_desserts: [],

    editedIndex: -1,

    clickTimes: 0,

    editName: '',
    num1: 0,
    num2: 0,
    num3: 0,

    //in_drafTags: 0,

    //fields: [],

    load_SingleTable_ok: false, //for get employer table data
    //load_2thTable_ok: false,    //for get reagent table data
  }),

  computed: {
    /*
    check_selected() {
      if (Array.isArray(this.selected) && this.selected.length) {
        // array exists and is not empty
        return true;
      } else {
        return false;
      }
    },
    */
    //combineCount(item) {
    //  this.editedIndex = this.desserts.indexOf(item);
    //  return this.temp_desserts[this.editedIndex].stockInTag_cnt + " / ";
    //},

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
    //dialog (val) {
    //  val || this.close()
    //},
    compareDatePeriod(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stockInTag_reagPeriod.split('/');
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
          removedEl.push(this.dessertsDisplay[i].stockInTag_Employer)
        }
        this.itemsForEmployer = [...new Set(removedEl)];
        this.selectedEmployers = Object.assign([], this.itemsForEmployer);
        this.isAllSelected=true;

        this.load_SingleTable_ok=false;
      }
    },

    compareDate(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar1 = obj.stockInTag_Date.split('/');
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
          removedEl.push(this.dessertsDisplay[i].stockInTag_Employer)
        }
        this.itemsForEmployer = [...new Set(removedEl)];
        this.selectedEmployers = Object.assign([], this.itemsForEmployer);
        this.isAllSelected=true;
      }
    },

    compareDateEnd(val) {
      if (val!='') {
        let tem_len=this.desserts.length;
        for (let i=0; i < tem_len; i++) {
          //this.desserts = this.desserts.filter(function( obj ) {
          this.dessertsDisplay = this.dessertsDisplay.filter(function( obj ) {
            let myVar2 = obj.stockInTag_Date.split('/');
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
          removedEl.push(this.dessertsDisplay[i].stockInTag_Employer)
        }
        this.itemsForEmployer = [...new Set(removedEl)];
        this.selectedEmployers = Object.assign([], this.itemsForEmployer);
        this.isAllSelected=true;
      }
    },

    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        //this.desserts = Object.assign([], this.temp_desserts);
        this.desserts =  JSON.parse(JSON.stringify(this.temp_desserts))
        this.desserts = this.desserts.map(v => ({...v, isGridChange: false})) //新增object內的key(isGridChange), false: grid資料沒有更改
        this.desserts = this.desserts.map(v => ({...v, editReagentID: ''}))   //新增object內的key(editReagentID)
        this.desserts = this.desserts.map(v => ({...v, isEnter: false}))      //新增object內的key(editReagentID)

        this.dessertsDisplay = Object.assign([], this.desserts);

        this.dessertsDisplayForSelect =  Object.assign([],this.dessertsDisplay);

        let removedEl=['全部'];
        for (let i = 0; i < this.dessertsDisplay.length; i++) {
          removedEl.push(this.dessertsDisplay[i].stockInTag_Employer)
        }
        this.itemsForEmployer = [...new Set(removedEl)];
        this.selectedEmployers = Object.assign([], this.itemsForEmployer);
        this.isAllSelected=true;

        this.load_SingleTable_ok=false;
        //this.listUsers();
      }
    },
    /*
    load_2thTable_ok(val) {
      console.log("load_2thTable_ok, itemsForEmployer: ", val)

      if (val) {
        this.load_2thTable_ok=false;
        this.itemsForEmployer = this.temp_itemsForEmployer.map(item => Object.values(item)[2]); //從object中copy value至array
      }
    },
    */
    /*
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
    */
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
      console.log("Inventory, exportToExcel, Axios post data...");

      let obj= {
        id: 'ID',
        stockInTag_reagID: '資材碼',
        stockInTag_reagName: '品名',
        stockInTag_reagPeriod: '效期',
        stockInTag_reagTemp: '保存溫度',
        stockInTag_Date: '入庫日期',
        stockInTag_Employer: '入庫人員',
        stockInTag_grid: '儲位',
        stockInTag_cnt: '在庫數',
        stockInTag_cnt_inv_mdf: '盤點數',
        stockInTag_comment: '說明',
        //intag_id: '',
        //stockInTag_grid_station:0,
        //stockInTag_grid_layout:0,
        //stockInTag_grid_pos:0,
        //isGridChange: false,
      }

      //let object_Desserts = Object.assign([], this.desserts);
      let object_Desserts = Object.assign([], this.dessertsDisplay);
      object_Desserts.unshift(obj);

      const path = '/exportToExcelForInv';
      var payload= {
        blocks: object_Desserts,
        //count: this.desserts.length+1,
        count: object_Desserts.length,
        name: this.currentUser.name,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("export into excel status: ", res.data.status, res.data.outputs)
        if (res.data.status) {
          this.snackbar_color='#008184';
          this.snackbar=true;
          this.snackbar_info= '盤點記錄('+ res.data.outputs + ')轉檔完成!';
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

    updateStockInDataByInv() {
      console.log("Inventory, updateStockInDataByInv, Axios post data...");

      const path = '/updateStockInDataByInv';
      var payload= {
        blocks: this.desserts,
        count: this.desserts.length,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("update inTag data status: ", res.data.status)
        if (res.data.status) {
          this.snackbar_color='#008184';
          this.snackbar=true;
          this.snackbar_info= '在庫資料更新完成!';
          this.snackbar_icon_color= "#ffffff";
        } else {
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          this.snackbar_info= '存檔錯誤! ' + res.data.message;
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
        //this.selectedEmployers = [];
        if (this.isAllSelected) {
          this.isAllSelected = false;
          this.selectedEmployers = [];
          for (let i=1; i<e.length; i++) {
            this.selectedEmployers.push(e[i])
          }
        } else {
          console.log('Select all...');
          this.selectedEmployers = [];
          this.isAllSelected = true;
          for (let i=0; i<this.itemsForEmployer.length; i++) {
            this.selectedEmployers.push(this.itemsForEmployer[i])
          }
        }
      } else if (this.isAllSelected) {  //取消全部, 且不是全部的狀態
        console.log('Remove all...');
        this.selectedEmployers = [];
        this.isAllSelected = false;
      } else {  //取消全部, 且不是全部的狀態
        console.log('Click some item...');
        this.selectedEmployers = [];
        for (let i=0; i<e.length; i++) {
          let jj=this.itemsForEmployer.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectedEmployers.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        //console.log('length...', e.length, this.itemsForEmployer.length);
        if (e.length==this.itemsForEmployer.length-1) {
          console.log('Hello end...');
          this.selectedEmployers.unshift('全部')
          this.isAllSelected = true;
        }
      } //end else if

      console.log('item3...');

      if (this.selectedEmployers != []) {
        console.log('item4...');
        //this.dessertsDisplay = this.desserts.filter(val => this.selectedEmployers.includes(val.stockInTag_Employer));
        this.dessertsDisplay = this.dessertsDisplayForSelect.filter(val => this.selectedEmployers.includes(val.stockInTag_Employer));
      }
    },

    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },

    saveName(item) {
      //this.editName='' + this.num1 +'站/' + '' + this.num2 + '層/' + '' + this.num3 + '格'
      //this.editName='' + this.num1 +'站' + this.num2 + '層' + this.num3 + '格'
      this.editName=this.num1 +'站' + this.num2 + '層' + this.num3 + '格'
      //this.editedIndex = this.desserts.indexOf(item);                           //for desserts
      this.editedIndex = this.desserts.map(object => object.id).indexOf(item.id); //for dessertsDisplay
      console.log("saveName, index: ", this.editedIndex);
      //確認儲位已經修改, isGridChange=true
      if (this.temp_desserts[this.editedIndex].stockInTag_grid != this.editName) {
        this.desserts[this.editedIndex].isGridChange=true;
      }

      this.desserts[this.editedIndex].stockInTag_grid = this.editName;
      this.desserts[this.editedIndex].stockInTag_grid_station = this.num1;
      this.desserts[this.editedIndex].stockInTag_grid_layout = this.num2;
      this.desserts[this.editedIndex].stockInTag_grid_pos = this.num3;

      item.stockInTag_grid = this.editName;
    },

    openName(item) {
      this.editName=item;
      this.num1=parseInt(this.editName[0]);
      this.num2=parseInt(this.editName[2]);
      this.num3=parseInt(this.editName[4]);
    },

    //* closeName(item) {
    //*   item=this.editName;
    //* },

    //* cancelName() {
    //*
    //* },

    setRowStyle(item) {
      return 'style-1';
    },

    //getGrid(item) {
    //  this.editedIndex = this.desserts.indexOf(item);
    //  //console.log(this.desserts[this.editedIndex].stockInTag_grid);
    //  //console.log(this.temp_desserts[this.editedIndex].stockInTag_grid);
    //},
    modifyInvCntForBlur(item) {  //mdf, for blur function
      item.isEnter=false;
      let temp_int1=parseInt(item.stockInTag_cnt_inv_mdf);
      let temp_int2=parseInt(item.stockInTag_cnt);
      let temp_str=item.editReagentID.trim();

      if (temp_int1!=temp_int2 && temp_int1!=0 && temp_str==item.stockInTag_reagID) {
        //console.log("1-1, hello writeComm..", item.stockInTag_reagID, this.clickTimes)
        item.stockInTag_comment="異常! "
        item.editReagentID=item.stockInTag_reagID;
        return;
      }

      if (temp_int1==temp_int2 && temp_int1!=0 && temp_str==item.stockInTag_reagID) {
        //console.log("1-2, hello writeComm..", item.stockInTag_reagID, this.clickTimes)
        item.stockInTag_comment="盤點OK! "
        item.editReagentID=item.stockInTag_reagID;
        return;
      }

      item.stockInTag_cnt_inv_mdf='0';
      item.editReagentID='';
    },

    modifyInvCntForFocus(item) {  //mdf, for focus function
      item.isEnter=true;
      this.clickTimes=0;
    },

    modifyIDForBlur(item) {   //id,for blur function
      item.isEnter=false;
      let temp_int1=parseInt(item.stockInTag_cnt_inv_mdf);
      let temp_int2=parseInt(item.stockInTag_cnt);

      if (temp_int1!=temp_int2 && temp_int1!=0 && this.clickTimes!=0) {
        item.stockInTag_comment="異常! "
        item.editReagentID=item.stockInTag_reagID;
        return;
      }

      if (temp_int1==temp_int2 && temp_int1!=0 && this.clickTimes!=0) {
        item.stockInTag_comment="盤點OK! "
        item.editReagentID=item.stockInTag_reagID;
        return;
      }

      //let temp_str=item.editReagentID.trim();
      //if (temp_str!=item.stockInTag_reagID)
        item.editReagentID='';
      //else {
      //  item.stockInTag_comment="異常! "
      // temp_int1= temp_int1 + 1;
      //}
    },

    modifyIDForFocus(item) {     //id, for focus function
      item.stockInTag_cnt_inv_mdf='0';
      item.stockInTag_comment='';
      item.editReagentID='';
      this.clickTimes=0;
      item.isEnter=true;
    },

    modifyIDForPressRet(item) { //id, for press return function
      this.clickTimes=this.clickTimes+1;
      let temp_int=parseInt(item.stockInTag_cnt_inv_mdf);
      let temp_str=item.editReagentID.trim();
      if (temp_str==item.stockInTag_reagID) {
        temp_int= temp_int + 1;
        item.stockInTag_cnt_inv_mdf=temp_int.toString();
      }
      item.editReagentID='';
    },

    getData(item) {
      //this.editedIndex = this.desserts.indexOf(item);                           //for desserts
      this.editedIndex = this.desserts.map(object => object.id).indexOf(item.id); //for dessertsDisplay
      console.log("getData, index: ", this.editedIndex);

      if (this.temp_desserts[this.editedIndex].stockInTag_cnt != item.stockInTag_cnt) {
        this.desserts[this.editedIndex].isGridChange=true;
      }
      //console.log("cnt data: ", this.temp_desserts[this.editedIndex].stockInTag_cnt, item.stockInTag_cnt);
    },

    getComment(item) {
      //this.editedIndex = this.desserts.indexOf(item);                             //for desserts
      this.editedIndex = this.desserts.map(object => object.id).indexOf(item.id); //for dessertsDisplay
      console.log("getComment, index: ", this.editedIndex);

      if (this.temp_desserts[this.editedIndex].stockInTag_comment != item.stockInTag_comment) {
        this.desserts[this.editedIndex].isGridChange=true;
      }
      //console.log("comment data: ", this.temp_desserts[this.editedIndex].stockInTag_comment, item.stockInTag_comment);
    },

    //combineCount(item) {
    //  this.editedIndex = this.desserts.indexOf(item);
    //  return this.temp_desserts[this.editedIndex].stockInTag_cnt + " / ";
    //},

    //get_headers() {
    //  return this.headers.filter(x=>x.invColumn);
    //},

    //enterSelect(item) {
    //  console.log("enterSelect=> ", item);
    //},

    /*
    onWaitTags(value) {
      console.log("total count for tags: ", value);
      this.total_tags=value;

      //if ("totalTags" in localStorage) {
      //  localStorage.removeItem('totalTags');
      //}
      localStorage.setItem("totalTags", this.total_tags);

      console.log("leave onWaitTags()...");
    },
    */

    //* printSection() {
    //*   console.log("click, printSection()...");
    //*   this.drawer=true;
    //*   /*
    //*   this.$router.push({
    //*     name: 'RenderBarCode',
    //*     params: {
    //*       selectDatas: this.selected,
    //*     }
    //*   });
    //*   */
    //* },

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

::v-deep input::placeholder {
  font-size: 14px;
}

::v-deep .v-input.myText input {
  font-size: 0.7em;
}

::v-deep .row_myText_inv {
  /*width: 100%;*/
  width: 170px;
  margin: 0 8px;
  display: flex;
  justify-content: center; /* for centering 3 blocks in the center */
  /* justify-content: space-between; for space in between */
}

::v-deep .block_myText_inv_cnt {
  width: 24px;
  font-size: 14px;
}

::v-deep .block_myText_inv_cnt_mdf {
  width: 24px;
  font-size: 14px;
}

::v-deep .block_myText_inv_cnt_mdf_color input {
  color: #fe484d !important;
}

::v-deep .block_myText_inv_id {
  width: 100px;
  font-size: 14px;
}

/*
::v-deep .block_myText_inv_cnt fieldset{
  height: 32px;
}
*/

/*
::v-deep .v-input.myText_inv input {
  color: red;
  padding: 12px 0px;
}

::v-deep .v-input.myText_inv_id input {
  color: red;
  padding: 12px 0px;
  width: 88px;
}
*/

::v-deep .v-data-table-header th:nth-child(1) i {
  color: blue !important;
}

::v-deep .v-data-table-header th:last-child span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
  margin-left:2.5em;    /* Creating a tab using CSS and HTML */
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
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep div.v-input.style-0 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 70px !important;
  width: 70px !important;
}

::v-deep div.v-input.style-2 > .v-input__control > .v-input__slot {
  max-width: 70px !important;
  width: 70px !important;
}

::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 120px !important;
  width: 120px !important;
}

::v-deep div.v-input.style-3 > .v-input__control > .v-input__slot {
  max-width: 120px !important;
  width: 120px !important;
}
/*-- for v-select begin--*/
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
  font-size: 16px;;
}

::v-deep .v-list--dense .v-list-item, .v-list-item--dense {
    min-height: 30px !important;
    height: 30px !important;
}
::v-deep .v-select.v-input--dense .v-select__selection--comma {
  font-size: 12px !important;
  margin: 5px 4px 3px 0 !important;
}

::v-deep div.v-input.style-4 > .v-input__control > .v-input__slot {
  max-width: 100px !important;
  width: 120px !important;
  height: 40px !important;

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
/*-- for v-select end--*/
::v-deep .centered-input > .v-input__control> .v-input__slot > .v-text-field__slot > input {
  text-align: center;
}

::v-deep .v-tooltip__content {
  margin-top: -30px !important;
  font-size: 12px !important;
}

/*----------*/

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

/*::v-deep .v-data-table__wrapper > table > tbody > tr > td:nth-last-child(2) > .v-input > .v-input__control > .v-input__slot > .v-text-field__slot > .v-text-field__prefix {*/
::v-deep td:nth-last-child(2) .v-text-field__prefix {
  color:#1f4788;
  font-size: 12px;
}

::v-deep .v-data-table__wrapper > table > tbody > tr > td:nth-last-child(2) > .v-input > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  text-align: start;
}

/*
::v-deep th[role=columnheader] > span {
  font-size: 1.2em;
}
*/
/*----------*/
.excel_wrapper {
    position: relative;
    top: -14px !important;
    right: -40px !important;
    width: 90px !important;
}

.flip_wrapper {
    perspective: 800px;
}

.flip_btn {
    position: relative;
    top: -18px !important;
    height: 20px;
    width: 130px;
    transform-style: preserve-3d;
    transition: transform 500ms ease-in-out;
    transform: translateZ(-20px);
}

.flip_btn:hover {
    transform: rotateX(-90deg) translateY(20px);
}

.side {
    position: absolute;
    backface-visibility: hidden;
    width: 100%;
    height: 100%;
    display: flex;
    /*justify-content: center;
    align-items: center;*/
    /*font-size: 4em;
    font-weight: bold;*/
}

.default-side {
    transform: translateZ(20px);
}

.hover-side {
    transform: rotateX(90deg) translateZ(20px);
}
</style>