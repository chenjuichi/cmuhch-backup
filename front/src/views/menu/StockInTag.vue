<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="75vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          :item-class="setRowStyle"
          :options.sync="pagination"      
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>入庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                    <v-icon left dark>mdi-table-plus</v-icon>
                    新增資料
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <!-- 第1列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-tooltip v-model="errorShowForEmployer" top color="error">                        
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field                            
                                v-model="editedItem.stockInTag_EmpID"
                                :value="stockInTag_EmpID"
                                label="員工編號"
                                readonly
                              ></v-text-field>
                            </template>
                            <span>員工編號錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.stockInTag_Employer"
                            :value="fromStockInTagEmpIdDisp"
                            label="入庫人員"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-menu
                            v-model="fromDateMenu"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            lazy
                            transition="scale-transition"
                            offset-y
                            full-width
                            max-width="290px"
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                label="入庫日期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.stockInTag_Date"
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
                        </v-col>                                                                                 
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-tooltip v-model="errorShowForReagName" top color="error">                        
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field                            
                                v-model="editedItem.stockInTag_reagID"
                                label="資材碼"
                              ></v-text-field>
                            </template>
                            <span>資材碼錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.stockInTag_reagName"
                            :value="fromReagIdDisp"
                            label="品名"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_reagPeriod"
                            :value="editedItem.stockInTag_reagPeriod"
                            label="效期"                            
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_reagTemp" 
                            :value="editedItem.stockInTag_reagTemp"
                            label="保存溫度"                               
                            readonly
                          ></v-text-field>
                        </v-col>                                            
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_batch"                            
                            :value="editedItem.stockInTag_batch"                            
                            label="批號"      
                          ></v-text-field>
                        </v-col>                                            
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save">儲存</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">確定刪除這筆資料?</v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm">刪除</v-btn>
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>

          <template v-slot:[`item.stockInTag_cnt`]="{ item }">
            <v-text-field
              v-model="item.stockInTag_cnt"
              
              type="number"
              min=1
              max=20
              oninput="if(Number(this.value) > Number(this.max)) this.value = this.max;"            
            
              @input="getdata(item)"         
            ></v-text-field>
          </template>       

          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
            </v-icon>
            <v-icon small  @click="deleteItem(item)" style="color: red;">
              mdi-delete
            </v-icon>
          </template>
          
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
          </template>
          
          <!--
          <template v-slot:no-data>
            <div></div>
          </template>          
          -->
          <!--
          <template v-slot:body.append>
            <v-row align="center" justify="center" v-show="in_drafTags != 0">
              <v-col cols="12" md="4">
                <v-btn color="primary" dark class="ma-2" @click.prevent="tags_draftButton">
                  暫存
                </v-btn>
              </v-col>
              <v-col cols="12" md="4">
              </v-col>
              <v-col cols="12" md="4">
                <v-btn color="primary" dark class="ma-2" @click.prevent="tags_saveButton">
                  確定
                </v-btn>
              </v-col>
            </v-row>
          </template>
          -->          
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

export default {
  name: 'StockInTag',

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

  data: () => ({
    currentUser: {},
    permDialog: false,

    stockInTag_EmpID: '',   //入庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,

    fromDateMenu: false,
    fromDateVal: null,
    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    pagination: {},

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '10%' },
      { text: '品名', sortable: false, value: 'stockInTag_reagName', width: '180px' },
      { text: '效期', sortable: true, value: 'stockInTag_reagPeriod', width: '90px' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '10%' },
      { text: '入庫日期', sortable: false, value: 'stockInTag_Date', width: '90px' },
      { text: '入庫人員', sortable: false, value: 'stockInTag_Employer', width: '10%' },
      { text: '批號', sortable: false, value: 'stockInTag_batch', width: '180px' },
      { text: '數量', sortable: false, value: 'stockInTag_cnt', width: '50px' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%', align: 'center' },        
    ], 
    /*
    stockInTag_employer_desserts: [
      {
        //id: 1,
        stkIn_empID: 'A12345',
        stkIn_empName: '陳瑞琪',
      },
      {
        //id: 2,
        stkIn_empID: 'A12342',
        stkIn_empName: '林政仰',       
      },
      {
        //id: 3,
        stkIn_empID: 'N12345',
        stkIn_empName: '陳健南',      
      },
      {
        //id: 4,
        stkIn_empID: 'N12345',
        stkIn_empName: '周明慶',    
      },
      {
        //id: 5,
        stkIn_empID: 'D12345',
        stkIn_empName: '顏榮俊',       
      },
      {
        //id: 6,
        stkIn_empID: 'T12345',
        stkIn_empName: '林成興',  
      },
      {
        //id: 7,
        stkIn_empID: 'T87654',
        stkIn_empName: '吳仲偉',
      },
    ],
    */

    stockInTag_Desserts: [
      {
        //id: 1,
        stockInTag_reagID: '123456789',
        stockInTag_reagName: 'ABC',
        stockInTag_reagPeriod: '111/10/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123400888',
        stockInTag_cnt: 1,
      },
      {
        //id: 2,
        stockInTag_reagID: '234567891',
        stockInTag_reagName: 'ABCD',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123405555',
        stockInTag_cnt: 1,
      },
      {
        //id: 3,
        stockInTag_reagID: '234567892',
        stockInTag_reagName: 'A11',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123400011',
        stockInTag_cnt: 1,
      },
      {
        //id: 4,
        stockInTag_reagID: '234567893',
        stockInTag_reagName: 'A12',
        stockInTag_reagPeriod: '112/6/30',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345B123400012',
        stockInTag_cnt: 1,
      },
      {
        //id: 5,
        stockInTag_reagID: '234567894',
        stockInTag_reagName: 'B2233',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345B123400022',
        stockInTag_cnt: 1,
      },
      {
        //id: 6,
        stockInTag_reagID: '234567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 7,
        stockInTag_reagID: '234567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 8,
        stockInTag_reagID: '234567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 9,
        stockInTag_reagID: '214567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 10,
        stockInTag_reagID: '214567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 11,
        stockInTag_reagID: '214567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '室溫',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 12,
        stockInTag_reagID: '224567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 13,
        stockInTag_reagID: '224567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 14,
        stockInTag_reagID: '224567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '室溫',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
    ],    

    in_newTags: 0,
    in_drafTags: 0,
    
    desserts: [],
    temp_desserts: [],

    editedIndex: -1,
    editedItem: {
      //id: 0,
      stockInTag_reagID: '',
      stockInTag_reagName: '',
      stockInTag_reagPeriod: '',
      stockInTag_reagTemp: '',
      stockInTag_Date: '',
      stockInTag_EmpID: '',
      stockInTag_Employer: '',
      stockInTag_batch: '',
      stockInTag_cnt: '',
    },
    defaultItem: {
      stockInTag_reagID: '',
      stockInTag_reagName: '',
      stockInTag_reagPeriod: '',
      stockInTag_reagTemp: '',
      stockInTag_Date: '',
      stockInTag_EmpID: '',
      stockInTag_Employer: '',
      stockInTag_batch: '',
      stockInTag_cnt: '',
    },

    load_SingleTable_ok: false, //for get employer table data
    //load_2thTable_ok: false,    //for get reagent table data
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromStockInTagEmpIdDisp() {
      if (this.stockInTag_EmpID != '') {
        if (this.editedItem.stockInTag_EmpID == '') {
          this.editedItem.stockInTag_EmpID=this.currentUser.empID;
          this.editedItem.stockInTag_Employer=this.currentUser.name;
        }
        this.errorShowForEmployer=false;
        return this.editedItem.stockInTag_Employer;         
      } else {
        this.this.editedItem.stockInTag_EmpID='';
        this.editedItem.stockInTag_Employer='';
        this.errorShowForEmployer=true;
        return '';
      }        
    },

    fromReagIdDisp () { 
      if (this.editedItem.stockInTag_reagID != '') {
        //console.log("result 1...");
        const result = this.stockInTag_Desserts.find(x => x.stockInTag_reagID === this.editedItem.stockInTag_reagID);
        //console.log("result 1-2...", result);
                    
        if (result != 'undefined' && result != null) {
          console.log("result 2...", result);          
          this.editedItem.stockInTag_reagName=result.stockInTag_reagName;
          this.editedItem.stockInTag_reagPeriod=result.stockInTag_reagPeriod;
          this.editedItem.stockInTag_reagTemp=result.stockInTag_reagTemp;
          this.errorShowForReagName=false;
          return result.stockInTag_reagName;          
        } else {
          this.editedItem.stockInTag_reagName='';
          this.editedItem.stockInTag_reagPeriod='';
          this.editedItem.stockInTag_reagTemp='';
          this.errorShowForReagName=true;
          return '';
        }        
      } 
    },       

    fromDateDisp() {  //output: editedItem.stockInTag_Date 
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.stockInTag_Date = yy_value + '/' + mmdd_value;
      }      
      return this.fromDateVal;
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.stockInTag_EmpID = this.currentUser.empID;

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockInData();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listStockInData();      
      /*
      this.desserts = [        
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
          stockInTag_cnt: '1',

        },
        {
          //id: 2,
          stockInTag_reagID: '234567891',
          stockInTag_reagName: 'ABCD',
          stockInTag_reagPeriod: '111/12/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345C123400055',
          stockInTag_cnt: '2',
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
          stockInTag_cnt: '1',
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
          stockInTag_cnt: '5',
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
          stockInTag_cnt: '1',
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
          stockInTag_cnt: '1',
        },
        {
          //id: 7,
          stockInTag_reagID: '234567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '1',
        },
        {
          //id: 8,
          stockInTag_reagID: '234567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '1',
        },
        {
          //id: 9,
          stockInTag_reagID: '214567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '2',
        },
        {
          //id: 10,
          stockInTag_reagID: '214567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '10',
        },
        {
          //id: 11,
          stockInTag_reagID: '214567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '1',
        },
        {
          //id: 12,
          stockInTag_reagID: '224567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '5',
        },
        {
          //id: 13,
          stockInTag_reagID: '224567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '1',
        },
        {
          //id: 14,
          stockInTag_reagID: '224567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: '1',
        },        
      ];
      */
    },

    listStockInData() {
      const path = '/listStockInData';
      console.log("listStockInData, Axios get data...")
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

    setRowStyle(item) {
      return 'style-1';
    },

    getdata(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_cnt);
    },

    editItem (item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      console.log("edit item: ", item, this.editedItem)
    },

    deleteItem (item) {
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      this.desserts.splice(this.editedIndex, 1)
      this.closeDelete()
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem)
      } else {
        //this.editedItem.id=this.desserts.length+1;
        this.desserts.push(this.editedItem);
        this.in_drafTags++;        
      }
      this.close()
    },

    tags_draftButton () {
      console.log("press draf Button...");

      localStorage.setItem("tags_draft", JSON.stringify(this.desserts));

      this.$router.push({
        name: 'Navbar',
        params: {
          in_drafTags: this.in_drafTags,
        }        
      });
    },

    tags_saveButton () {
      console.log("press save Button...");

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
  font-size: 1.2em;
  font-weight: bold;
}

::v-deep .style-1 td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th:nth-last-child(1) {
  padding-right: 8px !important;
  text-align: center !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}
</style>