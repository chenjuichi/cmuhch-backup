<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="70vw">
        <!-- desserts為dataTable的資料源-->
        <v-data-table
          :headers="headers"
          :items="desserts"
          :item-class="setRowStyle"
          :options.sync="pagination"          
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>出庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="1000px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                    <v-icon left dark>mdi-table-plus</v-icon>
                    新增資料
                  </v-btn>
                </template>

                <v-card width="82vw">
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>

                    <!-- -->                
                    <ul class="list-unstyled multi-steps">
                      <li id="step-1" :class="{'is-active': active1}">
                        領用日期
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>-1}"></div>
                        </div>
                      </li>
                      <li id="step-2" :class="{'is-active': active2}">
                        主要產品
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>0}"></div>
                        </div>
                      </li>
                      <li id="step-3" :class="{'is-active': active3}">
                        供應商
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>1}"></div>
                        </div>
                      </li>
                      <li id="step-4" :class="{'is-active': active4}">
                        在庫試劑
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans==3}"></div>
                        </div>
                      </li>
                    </ul>                
    <!--                
    <v-btn
      small
      color="primary"
      @click="next"
    >
      Accept
    </v-btn>
    -->
                    <!-- -->

                  </v-card-title>

                  <v-card-text>
                    <v-container fluid>
                      <!-- 第1列-->
                      <v-row align="center" justify="center" >
                        <v-col cols="12" md="3">
                          <v-tooltip v-model="errorShowForEmployer" top color="error">                        
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field                            
                                v-model="editedItem.stockOutTag_EmpID"
                                :value="stockOutTag_EmpID"
                                label="員工編號"
                                readonly
                              ></v-text-field>
                            </template>
                            <span>員工編號錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.stockOutTag_Employer"
                            :value="fromstockOutTagEmpIdDisp"
                            label="領用人員"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <!--
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="領用單位"                               
                            v-model="editedItem.stockOutTag_unit" 
                          ></v-select>
                        </v-col>
                        -->
                        <v-col cols="12" md="4">
                          <v-menu
                            v-model="fromDateMenu"
                            :close-on-content-click="false"
                            :nudge-right="40"
                            
                            transition="scale-transition"
                            offset-y
                            
                            max-width="290px"
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                label="領用日期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.stockOutTag_Date"
                                v-on="on"
                                @blur="setStep1"

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
                      
                      <v-row>                        
                      </v-row>

                      <!-- 第2列-->
                      <v-row mt-n5 align="center" justify="center">                        
                          <label for="main" class="adjLabel">
                            <!--<i class="fas fa-align-left"></i>-->
                            主要產品 (共{{label_count}}項)
                          </label>
                          <v-col cols="12" md="8" ml="2" class="adjTopForSlide">
                            <v-sheet>
                              <v-slide-group 
                                multiple 
                                show-arrows 
                                v-model="selectedCatalogs">
                                <!-- products為slide-item的資料源-->
                                <v-slide-item 
                                  v-for="(product, index) in products"   
                                  :key="index" 
                                  v-slot="{ active, toggle }"
                                >
                                  <v-btn 
                                    class="mx-2"
                                    :input-value="active"
                                    active-class="primary"
                                    depressed
                                    rounded
                                    @click="toggle"
                                  >
                                    {{ product }}
                                  </v-btn>
                                </v-slide-item>
                              </v-slide-group>
                            </v-sheet>
                          </v-col>
                          <v-col cols="12" md="4" ml="2" class="adjTopForSelect">
                            <!-- suppliers為v-select的資料源-->
                            <v-select
                            @change="checkSelect"                    
                            :items="suppliers"
                            label="供應商"
                            outlined
                            multiple
                            class="mt-1 ml-3 mx-auto" 
                            style="width:100px; height:20px;"                      
                            v-model="selectSuppliers"
                          ></v-select>
                          </v-col>
                      </v-row>

                      <!-- 第3列-->
                      <v-row mt-10 align="center" justify="center" >
                        <template>
                          <v-data-table
                            dense
                            v-model="stock_selected"
                            :headers="stock_headers"
                            :items="stock_desserts"
                            style="width: 790px;"
                            item-key="stockIn_reagent_id"
                            show-select
                            class="elevation-1"
                            no-data-text=""
                            :footer-props="{
                              'itemsPerPageText': '每頁的資料筆數',
                              'items-per-page-options':[5]
                            }"
                          >
                            <template v-slot:[`item.count`]="{ item }">
                              <div class="adjNumeric">
                              <vue-numeric-input 
                                v-model="item.count" 
                                :min="1" 
                                :max="item.count" 
                                :step="1"
                                align="center"
                                size="small"
                              ></vue-numeric-input>
                              </div>
                            </template>

                          </v-data-table>
                        </template>
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

          <template v-slot:[`item.stockOutTag_cnt`]="{ item }">
            <v-text-field
              v-model="item.stockOutTag_cnt"
              
              type="number"
              min=1
              max=20
              oninput="if(Number(this.value) > Number(this.max)) this.value = this.max;"            
              @input="getdata(item)"         
            ></v-text-field>
          </template>       


          <template v-slot:[`item.actions`]="{ item }">
            <!--
            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
            </v-icon>
            -->
            <v-icon small  @click="deleteItem(item)" style="color: red;">
              mdi-delete
            </v-icon>
          </template>
          
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
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
import VueNumericInput from 'vue-numeric-input';

import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

import StepProgress from 'vue-step-progress';
import 'vue-step-progress/dist/main.css';

import axios from 'axios';

import Common from '../../mixin/common.js'

export default {
  name: 'stockOutTag',

  mixins: [Common],

  components: {
    VueNumericInput, 
    'step-progress': StepProgress
  },

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
    
    //const step1 = document.getElementById("step-1");
    //const step2 = document.getElementById("step-2");
    //const step3 = document.getElementById("step-3");
    //const step4 = document.getElementById("step-4");
  },
  
  data: () => ({
    /*
        mySteps: ['Step 1', 'Step 2', 'Step 3'],
        currentStep: 0,
        activeColor: 'red',
        passiveColor: 'gray',
        lineThickness: 2,
        activeThickness: 2,
        passiveThickness: 2,
    */
//--stock-datatable--//
        label_count: 0,
        active1: true,
        active2: false,
        active3: false,
        active4: false,
        step: 'step0',
        step_trans: -1,

        editedStockIndex: -1,

        stock_singleSelect: false,
        stock_selected: [],
        stock_headers: [
          { text: '資材碼', value: 'stockIn_reagent_id', align: 'start', sortable: true, width: '180px' },
          { text: '品名', value: 'stockIn_reagent_name', sortable: false, width: '120px' },
          { text: '供應商', value: 'stockIn_supplier', sortable: true, width: '100px' },
          { text: '效期', value: 'stockIn_reagent_period', sortable: true, width: '100px' },
          { text: '入庫日期', value: 'stockIn_date', sortable: true, width: '100px' },
          //{ text: '批號', value: 'protein', sortable: false, width: '18%' },
          { text: '領用單位', value: 'stockIn_reagent_Out_unit', sortable: false, width: '90px' },
          { text: '數量', value: 'stockIn_reagent_Out_cnt', sortable: false, width: '16%' },
        ],
        stock_desserts: [
          /*
          {
            stockIn_reagent_id: 'Frozen Yogurt',
            stockIn_reagent_name: 159,
            stockIn_reagent_period: 6.0,
            stockIn_date: 24,
            //protein: 4.0,
            stockIn_reagent_Out_unit: '1%',
            stockIn_reagent_Out_cnt: 1,
          },
          {
            stockIn_reagent_id: 'Ice cream sandwich',
            stockIn_reagent_name: 237,
            stockIn_reagent_period: 9.0,
            stockIn_date: 37,
            //protein: 4.3,
            stockIn_reagent_Out_unit: '1%',
            stockIn_reagent_Out_cnt: 2,
          },
          {
            stockIn_reagent_id: 'Eclair',
            stockIn_reagent_name: 262,
            stockIn_reagent_period: 16.0,
            stockIn_date: 23,
            //protein: 6.0,
            stockIn_reagent_Out_unit: '7%',
            stockIn_reagent_Out_cnt: 3,
          },
          {
            stockIn_reagent_id: 'Cupcake',
            stockIn_reagent_name: 305,
            stockIn_reagent_period: 3.7,
            stockIn_date: 67,
            //protein: 4.3,
            stockIn_reagent_Out_unit: '8%',
            stockIn_reagent_Out_cnt: 1,
          },
          {
            stockIn_reagent_id: 'Gingerbread',
            stockIn_reagent_name: 356,
            stockIn_reagent_period: 16.0,
            stockIn_date: 49,
            //protein: 3.9,
            stockIn_reagent_Out_unit: '16%',
            stockIn_reagent_Out_cnt: 2,
          },
          {
            stockIn_reagent_id: 'Jelly bean',
            stockIn_reagent_name: 375,
            stockIn_reagent_period: 0.0,
            stockIn_date: 94,
            //protein: 0.0,
            stockIn_reagent_Out_unit: '0%',
            stockIn_reagent_Out_cnt: 3,
          },
          {
            stockIn_reagent_id: 'Lollipop',
            stockIn_reagent_name: 392,
            stockIn_reagent_period: 0.2,
            stockIn_date: 98,
            //protein: 0,
            stockIn_reagent_Out_unit: '2%',
            stockIn_reagent_Out_cnt: 4,
          },
          {
            stockIn_reagent_id: 'Honeycomb',
            stockIn_reagent_name: 408,
            stockIn_reagent_period: 3.2,
            stockIn_date: 87,
            //protein: 6.5,
            stockIn_reagent_Out_unit: '45%',
            stockIn_reagent_Out_cnt: 5,
          },
          {
            stockIn_reagent_id: 'Donut',
            stockIn_reagent_name: 452,
            stockIn_reagent_period: 25.0,
            stockIn_date: 51,
            //protein: 4.9,
            stockIn_reagent_Out_unit: '22%',
            stockIn_reagent_Out_cnt: 1,
          },
          {
            stockIn_reagent_id: 'KitKat',
            stockIn_reagent_name: 518,
            stockIn_reagent_period: 26.0,
            stockIn_date: 65,
            //protein: 7,
            stockIn_reagent_Out_unit: '6%',
            stockIn_reagent_Out_cnt: 1,
          },
          */
        ],
        temp_stock_desserts: [],
//--

    currentUser: {},
    permDialog: false,

    stockOutTag_EmpID: '',   //入庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,

    fromDateMenu: false,
    fromDateVal: null,
    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    selectedCatalogs: [],

    pagination: { },

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockOutTag_reagID', width: '10%' },
      { text: '品名', sortable: false, value: 'stockOutTag_reagName', width: '13%' },
      { text: '效期', sortable: true, value: 'stockOutTag_reagPeriod', width: '10%' },
      //{ text: '保存溫度', sortable: false, value: 'stockOutTag_reagTemp', width: '10%' },
      { text: '入庫日期', sortable: true, value: 'stockOutTag_InDate', width: '10%' },
      { text: '領用日期', sortable: true, value: 'stockOutTag_Date', width: '10%' },
      { text: '領用人員', sortable: true, value: 'stockOutTag_Employer', width: '8%' },
      //{ text: '批號', sortable: false, value: 'stockOutTag_batch', width: '11%', align: 'center' },
      { text: '領用單位', sortable: false, value: 'stockOutTag_unit', width: '8%', align: 'start' },
      { text: '領用數量', sortable: false, value: 'stockOutTag_cnt', width: '8%', align: 'start' },
      { text: 'Actions', sortable: false, value: 'actions', width: '6%' },        
    ], 
    /*
    stockOutTag_employer_desserts: [
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
    /*
    stockOutTag_Desserts: [
      {
        //id: 1,
        stockOutTag_reagID: '123456789',
        stockOutTag_reagName: 'ABC',
        stockOutTag_reagPeriod: '111/10/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345D123400888',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 2,
        stockOutTag_reagID: '234567891',
        stockOutTag_reagName: 'ABCD',
        stockOutTag_reagPeriod: '111/12/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345D123405555',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 3,
        stockOutTag_reagID: '234567892',
        stockOutTag_reagName: 'A11',
        stockOutTag_reagPeriod: '111/12/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345D123400011',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 4,
        stockOutTag_reagID: '234567893',
        stockOutTag_reagName: 'A12',
        stockOutTag_reagPeriod: '112/6/30',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345B123400012',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 5,
        stockOutTag_reagID: '234567894',
        stockOutTag_reagName: 'B2233',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345B123400022',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 6,
        stockOutTag_reagID: '234567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 7,
        stockOutTag_reagID: '234567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 8,
        stockOutTag_reagID: '234567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 9,
        stockOutTag_reagID: '214567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 10,
        stockOutTag_reagID: '214567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 11,
        stockOutTag_reagID: '214567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '室溫',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 12,
        stockOutTag_reagID: '224567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 13,
        stockOutTag_reagID: '224567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '2~8度C',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 14,
        stockOutTag_reagID: '224567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        //stockOutTag_reagTemp: '室溫',
        //stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
    ],    
    */
    in_newTags: 0,
    in_drafTags: 0,

    desserts: [],         //dataTable的資料
    temp_desserts: [],

    products: [],         //slide-item的主要產品資料
    temp_products: [],
    
    suppliers: [],        //v-select的供應商資料 
    temp_suppliers: [],

    items: [],
    temp_items: [],    

    editedIndex: -1,
    editedItem: {
      //id: 0,
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      //stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      //stockOutTag_batch: '',
      stockOutTag_cnt: '',
    },
    defaultItem: {
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      //stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      //stockOutTag_batch: '',
      stockOutTag_cnt: '',
    },

    isAllSelected: false,
    selectSuppliers: [],

    load_SingleTable_ok: false, //true: temp_desserts ok
    load_2thTable_ok: false,    //true: temp_products ok
    load_3thTable_ok: false,    //true: temp_suppliers ok
    load_4thTable_ok: false,    //true: temp_suppliers ok
    load_5thTable_ok: false,    //true: temp_stock_desserts ok
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromstockOutTagEmpIdDisp() {
      if (this.stockOutTag_EmpID != '') {
        if (this.editedItem.stockOutTag_EmpID == '') {
          this.editedItem.stockOutTag_EmpID=this.currentUser.empID;
          this.editedItem.stockOutTag_Employer=this.currentUser.name;
        }
        this.errorShowForEmployer=false;
        return this.editedItem.stockOutTag_Employer;         
      } else {
        this.this.editedItem.stockOutTag_EmpID='';
        this.editedItem.stockOutTag_Employer='';
        this.errorShowForEmployer=true;
        return '';
      }        
    },
    /*
    fromReagIdDisp() { 
      if (this.editedItem.stockOutTag_reagID != '') {
        //console.log("result 1...");
        const result = this.stockOutTag_Desserts.find(x => x.stockOutTag_reagID === this.editedItem.stockOutTag_reagID);
        //console.log("result 1-2...", result);
                    
        if (result != 'undefined' && result != null) {
          console.log("result 2...", result);          
          this.editedItem.stockOutTag_reagName=result.stockOutTag_reagName;
          this.editedItem.stockOutTag_reagPeriod=result.stockOutTag_reagPeriod;
          //this.editedItem.stockOutTag_reagTemp=result.stockOutTag_reagTemp;
          this.errorShowForReagName=false;
          return result.stockOutTag_reagName;          
        } else {
          this.editedItem.stockOutTag_reagName='';
          this.editedItem.stockOutTag_reagPeriod='';
          //this.editedItem.stockOutTag_reagTemp='';
          this.errorShowForReagName=true;
          return '';
        }        
      } 
    },       
    */
    fromDateDisp() {  //output: editedItem.stockOutTag_Date 
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.stockOutTag_Date = yy_value + '/' + mmdd_value;
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

    //selectSuppliers(val) {
    //  let uniqueArray_for_suppliers = val.filter(function(item, pos, self) {
    //      return self.indexOf(item) == pos;
    //  });
    //
    //  this.selectSuppliers=uniqueArray_for_suppliers;
    //},
    stock_selected(val) {
      if (val.length > 0 && this.step=='step3')
        this.next();
    },

    //selectedCatalogs(val) {
    selectedCatalogs(newValue, oldValue) {
      console.log("selectedCatalogs: ", newValue, oldValue, newValue.length);

      if (newValue!=oldValue) {
        //this.load_3thTable_ok=false;
        this.listSuppliersBySelect();
      }

      //if (newValue.length > 0 && this.step=='step1')
      if (this.step=='step1')
        this.next();
    },

    //selectSuppliers(val) {
    selectSuppliers(newValue, oldValue) {
      console.log("selectSuppliers: ", newValue, oldValue, newValue.length)

      if (newValue!=oldValue) {
        this.listStockInDataBySelect();
      }

      //if (newValue.length > 0 && this.step=='step2') {
      if (this.step=='step2') {
        console.log("hello keyin supplier...")
        this.next();
      }
    },

    load_5thTable_ok(val) {
      console.log("load_5thTable_ok, suppliers: ", val)

      if (val) {
        this.load_5thTable_ok=false;

        this.stock_desserts = Object.assign([], this.temp_stock_desserts);
      }
    },

    load_4thTable_ok(val) {
      console.log("load_4thTable_ok, suppliers: ", val)

      if (val) {
        this.load_4thTable_ok=false;

        this.suppliers = Object.assign([], this.temp_suppliers);

        this.stock_desserts = Object.assign([], this.temp_stock_desserts);
      }
    },

    load_3thTable_ok(val) {
      console.log("load_3thTable_ok, suppliers: ", val)

      if (val) {
        this.load_3thTable_ok=false;
        this.suppliers = this.temp_suppliers.map(item => Object.values(item)[2]); //從object中copy value至array
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok, products: ", val)
      //this.items = Object.assign([], this.temp_items);    
      //this.items = this.temp_items.map(item => Object.values(item)[2]); //從object中copy value至array
      if (val) {
        this.label_count=this.temp_products.length
        this.products = Object.assign([], this.temp_products);    

        this.load_2thTable_ok=false;
        //this.load_3thTable_ok=false;
        this.listSuppliers();
      }
    },

    load_SingleTable_ok(val) {
    console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
        //this.load_2thTable_ok=false;
        this.listProducts();
      }
    },

    //step(val) {
    //  this.next();
    //}
  },

  created () {
    //console.log("stockOutTag, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    ////load 入庫草案資料
    //this.in_drafTags=0
    //if ("tags_draft" in localStorage) {
    //  let tempDesserts = JSON.parse(localStorage.getItem("tags_draft") || "[]");
    //  console.log("# of desserts: ", tempDesserts.length, tempDesserts);
    //  this.in_drafTags=tempDesserts.length; 
    //}

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockOutData();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listStockOutData();
      /*      
      this.desserts = [
        
        {
          //id: 1,
          stockOutTag_reagID: '123456789',
          stockOutTag_reagName: 'ABC',
          stockOutTag_reagPeriod: '111/10/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400066',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '2',
        },
        {
          //id: 2,
          stockOutTag_reagID: '234567891',
          stockOutTag_reagName: 'ABCD',
          stockOutTag_reagPeriod: '111/12/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345C123400055',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '4',
        },
        {
          //id: 3,
          stockOutTag_reagID: '234567892',
          stockOutTag_reagName: 'A11',
          stockOutTag_reagPeriod: '111/12/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 4,
          stockOutTag_reagID: '234567893',
          stockOutTag_reagName: 'A12',
          stockOutTag_reagPeriod: '112/6/30',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 5,
          stockOutTag_reagID: '234567894',
          stockOutTag_reagName: 'B2233',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/10/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400022',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '5',
        },
        {
          //id: 6,
          stockOutTag_reagID: '234567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '4',
        },
        {
          //id: 7,
          stockOutTag_reagID: '234567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 8,
          stockOutTag_reagID: '234567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/09/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 9,
          stockOutTag_reagID: '214567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '10',
        },
        {
          //id: 10,
          stockOutTag_reagID: '214567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 11,
          stockOutTag_reagID: '214567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '2',
        },
        {
          //id: 12,
          stockOutTag_reagID: '224567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 13,
          stockOutTag_reagID: '224567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/03/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 14,
          stockOutTag_reagID: '224567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/05/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },        
      ];
      */

      //this.items = [
      //  '全部',
      // 'pmcA', 'pmcB', '3234', 'pmcC', 'pmcD'
      //]
    },

    listStockOutData() {    //從後端讀取dataTable的資料
      const path = '/listStockOutData';
      console.log("listStockOutData, Axios get data...")
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
    
    listSuppliers() {       //從後端讀取v-select的供應商資料 
      const path = '/listSuppliers';
      console.log("listSuppliers, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_suppliers = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);        
        this.load_3thTable_ok=true;   //true: v-select的供應商資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_3thTable_ok=false;
      });
    },
    
    listSuppliersBySelect() {       //從後端讀取v-select的供應商資料及v-data-table的stockIn資料  
      console.log("listSuppliersBySelect, Axios post data...")
      const path = '/listSuppliersBySelect';

      let arr_for_products=[]
      for (let i=0; i<this.selectedCatalogs.length; i++) {
        arr_for_products.push(this.products[this.selectedCatalogs[i]])          
      }

      //let arr_for_suppliers=[]
      //for (let i=0; i<this.selectSuppliers.length; i++) {
      //  arr_for_suppliers.push(this.suppliers[this.selectSuppliers[i]])          
      //}

      console.log("payload: ", arr_for_products)
      var payload= {
        //catalogs: this.selectedCatalogs,
        catalogs: arr_for_products,
        //suppliers: arr_for_suppliers,
      };      
      axios.post(path, payload)
      .then((res) => {
        this.temp_stock_desserts = res.data.outputs_for_stockOut;

        this.temp_suppliers = res.data.outputs_for_supplier.filter(function(item, pos, self) {
          return self.indexOf(item) == pos;
        });
        this.temp_suppliers.unshift('全部');
        console.log("POST ok, and return total records: (supplier)", res.data.outputs_for_supplier.length, " (stock)", res.data.outputs_for_stockOut.length);        
        this.load_4thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_4thTable_ok=false;
      });
    },
    
    listStockInDataBySelect() {
      console.log("listStockInDataBySelect, Axios post data...")
      const path = '/listStockInDataBySelect';

      let arr_for_suppliers=[]
      for (let i=0; i<this.selectSuppliers.length; i++) {
        arr_for_suppliers.push(this.selectSuppliers[i])          
      }
      //let uniqueArray_for_suppliers = arr_for_suppliers.filter(function(item, pos, self) {
      //    return self.indexOf(item) == pos;
      //});
      //let new_arr_for_suppliers=uniqueArray_for_suppliers.shift();

      let arr_for_products=[]
      for (let i=0; i<this.selectedCatalogs.length; i++) {
        arr_for_products.push(this.products[this.selectedCatalogs[i]])          
      }
      console.log("payload: ", arr_for_products, arr_for_suppliers)
      var payload= {
        catalogs:  arr_for_products,
        suppliers: arr_for_suppliers,
        //suppliers: new_arr_for_suppliers,
      };
      axios.post(path, payload)
      .then((res) => {
        //this.temp_stock_desserts = res.data.outputs_for_stockOut;

        this.temp_stock_desserts = res.data.outputs_for_stockOut.filter((value, index, self) =>
          index === self.findIndex((t) => (
            t.stockIn_reagent_id === value.stockIn_reagent_id
          ))
        )

        console.log("POST ok, and return total records: ", "(temp)", res.data.outputs_for_stockOut.length, "(real)", this.temp_stock_desserts.length);        
        this.load_5thTable_ok=true;       //true: dataTable的stockIn資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_5thTable_ok=false;   //true: slide-item的主要產品資料ok
      });
    },
    
    listProducts() {    //從後端讀取slide-item的主要產品資料 
      const path = '/listProducts';
      console.log("listProducts, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_products = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);        
        this.load_2thTable_ok=true;   //true: slide-item的主要產品資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },    

    setRowStyle(item) {
      return 'style-1';
    },

    getdata(item) {
      this.editedStockIndex = this.stock_desserts.indexOf(item);
      console.log(this.stock_desserts[this.editedStockIndex].stockIn_reagent_Out_cnt);
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
          for (let i=0; i<this.suppliers.length; i++) {
            this.selectSuppliers.push(this.suppliers[i])
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
          let jj=this.suppliers.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectSuppliers.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        console.log('length...', e.length, this.suppliers.length);
        if (e.length==this.suppliers.length-1) {
            this.selectSuppliers.push('全部')
            this.isAllSelected = true;
        }
      } //end else if

      this.next();      
    },    

    editItem (item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
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

    setStep1() {
      console.log("set step is...");
      //this.step = 'step0';
      if (this.step=='step0') {
        this.next();
      }
    },

    next() {
      if (this.step === 'step0') {
        console.log("current step0....");

        this.step = 'step1';
        this.step_trans++;
        this.active1=false;
        this.active2=true;
        return;
      }
      if (this.step === 'step1') {
        console.log("current step1....");

        this.step = 'step2';
        this.step_trans++;
        //this.active1=false;
        //this.active2=true;
        this.active2=false;
        this.active3=true;
        return;
      } 
      if (this.step === 'step2') {
        console.log("current step2....");

        this.step = 'step3';
        this.step_trans++;
        this.active3=false;
        this.active4=true;
        return;
      } 
      if (this.step === 'step3') {
        console.log("current step3....");

        this.step = 'step4';  //#
        //#this.step = 'complete';
        this.step_trans++;
        //this.active3=false;
        //this.active4=true;
        this.active4=false;
        return;
      } 
      if (this.step === 'step4') {
        console.log("current step4....");
        this.active4=false;

        this.step = 'complete';
        //#this.active4=false;
        return;
      }
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

::v-deep .v-select__selections {
  overflow-y: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap;
  max-height: 50px;  
}

.adjTopForSelect {
  top: -33px;
  left: 100px;
}

.adjTopForSlide {
  top: -13px;
  left: 100px;
  border-color: gray; 
  border-style: solid;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.adjLabel {
  position: absolute; 
  top: 215px; 
  z-index: 11; 
  left: 150px; 
  background-color: white;
  padding: 0 5px;
  font-weight: 600;
}

::v-deep div.vue-numeric-input.small {
  width: 6vw !important; 
  height: 4vh !important;
}

::v-deep .multi-steps > li.is-active ~ li:before, .multi-steps > li.is-active:before {
  content: counter(stepNum);
  font-family: inherit;
  font-weight: 700;
}

::v-deep .multi-steps > li.is-active ~ li:after, .multi-steps > li.is-active:after {
  background-color: #e1e1e1;
}
::v-deep .multi-steps {
  display: table;
  table-layout: fixed;
  width: 100%;
}

::v-deep .multi-steps > li {
  counter-increment: stepNum;
  text-align: center;
  display: table-cell;
  position: relative;
  color: #7DA79D; //#027f00;
  z-index: 2;
}

::v-deep .multi-steps > li:before {
  content: "";
  content: "✓;";
  content: "𐀃";
  content: "𐀄";
  content: "✓";
  display: block;
  margin: 0 auto 4px;
  background-color: #7DA79D; //#027f00;
  width: 36px;
  height: 36px;
  line-height: 32px;
  text-align: center;
  font-weight: bold;
  border-width: 2px;
  border-style: solid;
  border-color: #7DA79D; //#027f00;
  border-radius: 50%;
  color: white;
}

::v-deep .multi-steps > li:last-child:after {
  display: none;
}

::v-deep .multi-steps > li.is-active:before {
  background-color: #fff;
  border-color: #7DA79D; //#027f00;
  color: #7DA79D; //#027f00;
  animation: pulse 2s infinite;
  z-index: 2; //
}

::v-deep .multi-steps > li.is-active ~ li {
  color: #808080;
}

::v-deep .multi-steps > li.is-active ~ li:before {
  background-color: #e1e1e1;
  border-color: #e1e1e1;
  color: #808080;
  z-index: 2; //
}

::v-deep .is-complete {
  //background: linear-gradient(to right, #027f00 50%, #e1e1e1 50%);
  background: linear-gradient(to right, #7DA79D 50%, #e1e1e1 50%);
  background-size: 200% 100%;
  background-position: right bottom;
  transition: all 0.5s ease-out;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 #7DA79D; //#027f0070;
  }
  100% {
    box-shadow: 0 0 0 10px #027f0000;
  }
}
@keyframes nextStep {
  0% {
    width: 0%;
  }
  100% {
    width: 100%;
  }
}

::v-deep .progress-bar {
  cursor: pointer;
  user-select: none;
}

::v-deep .progress-bar {
  background-color: #e1e1e1;
  height: 7px;
  overflow: hidden;
  position: absolute;
  left: 50%;
  bottom: calc(50% + 7px);
  width: 100%;
  z-index: 1; //-1
}

::v-deep .progress-bar--success {
  background-color: #7DA79D; //#027f00;
  z-index: -1;
}

::v-deep .progress-bar__bar {
  background-color: #e1e1e1;
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  transition: all 500ms ease-out;
}

::v-deep .progress-bar__trans {
  transform: translateX(100%);  
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

::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
</style>