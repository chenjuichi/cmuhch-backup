<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="80vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"        
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>出庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="900px">
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
                      <v-row mt-n5>
                        <v-col cols="12" md="8">
                        <v-sheet>
                          <v-slide-group multiple show-arrows v-model="selectedCatalogs">
                            <v-slide-item 
                              v-for="n in 25" :key="n" v-slot="{ active, toggle }"
                            >
                              <v-btn 
                                class="mx-2"
                                :input-value="active"
                                active-class="purple white--text"
                                depressed
                                rounded
                                @click="toggle"
                              >
                                Options {{ n }}
                              </v-btn>
                            </v-slide-item>
                          </v-slide-group>
                        </v-sheet>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                          @change="checkSelect"                    
                          :items="items"
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
                      <v-row>
                        <v-col cols="12" md="3">
                          <v-tooltip v-model="errorShowForReagName" top color="error">                        
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field                            
                                v-model="editedItem.stockOutTag_reagID"
                                label="資材碼"
                              ></v-text-field>
                            </template>
                            <span>資材碼錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.stockOutTag_reagName"
                            :value="fromReagIdDisp"
                            label="品名"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockOutTag_reagTemp" 
                            :value="editedItem.stockOutTag_reagTemp"
                            label="保存溫度"                               
                            readonly
                          ></v-text-field>
                        </v-col>                                            
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockOutTag_batch"                            
                            :value="editedItem.stockOutTag_batch"                            
                            label="批號"      
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                        </v-col>
                      </v-row>
                    
                      <!-- 第4列-->                    
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.stockOutTag_reagPeriod"
                            :value="editedItem.stockOutTag_reagPeriod"
                            label="效期"                            
                            readonly
                          ></v-text-field>
                        </v-col>                                          
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.stockOutTag_InDate"
                            :value="editedItem.stockOutTag_InDate"
                            label="入庫日期"                            
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
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

export default {
  name: 'stockOutTag',

  mounted() {
    console.log("stockOutTag, mounted()...");    
  },
  
  data: () => ({
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

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockOutTag_reagID', width: '10%' },
      { text: '品名', sortable: false, value: 'stockOutTag_reagName', width: '10%' },
      { text: '效期', sortable: true, value: 'stockOutTag_reagPeriod', width: '10%' },
      { text: '保存溫度', sortable: false, value: 'stockOutTag_reagTemp', width: '10%' },
      { text: '入庫日期', sortable: true, value: 'stockOutTag_InDate', width: '10%' },
      { text: '領用日期', sortable: true, value: 'stockOutTag_Date', width: '10%' },
      { text: '領用人員', sortable: true, value: 'stockOutTag_Employer', width: '13%' },
      { text: '批號', sortable: false, value: 'stockOutTag_batch', width: '11%', align: 'center' },
      { text: '領用單位', sortable: false, value: 'stockOutTag_unit', width: '11%', align: 'center' },
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

    stockOutTag_Desserts: [
      {
        //id: 1,
        stockOutTag_reagID: '123456789',
        stockOutTag_reagName: 'ABC',
        stockOutTag_reagPeriod: '111/10/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345D123400888',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 2,
        stockOutTag_reagID: '234567891',
        stockOutTag_reagName: 'ABCD',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345D123405555',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 3,
        stockOutTag_reagID: '234567892',
        stockOutTag_reagName: 'A11',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345D123400011',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 4,
        stockOutTag_reagID: '234567893',
        stockOutTag_reagName: 'A12',
        stockOutTag_reagPeriod: '112/6/30',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345B123400012',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 5,
        stockOutTag_reagID: '234567894',
        stockOutTag_reagName: 'B2233',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345B123400022',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 6,
        stockOutTag_reagID: '234567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 7,
        stockOutTag_reagID: '234567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 8,
        stockOutTag_reagID: '234567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 9,
        stockOutTag_reagID: '214567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 10,
        stockOutTag_reagID: '214567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 11,
        stockOutTag_reagID: '214567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '室溫',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 12,
        stockOutTag_reagID: '224567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 13,
        stockOutTag_reagID: '224567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
      {
        //id: 14,
        stockOutTag_reagID: '224567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '室溫',
        stockOutTag_batch: '1110012345A123400001',
        //stockOutTag_unit: '盒',
      },
    ],    

    in_newTags: 0,
    in_drafTags: 0,
    desserts: [],
    editedIndex: -1,
    editedItem: {
      //id: 0,
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      stockOutTag_batch: '',
    },
    defaultItem: {
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      stockOutTag_batch: '',
    },

    isAllSelected: false,
    selectSuppliers: [],

    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get reagent table data
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

    fromReagIdDisp () { 
      if (this.editedItem.stockOutTag_reagID != '') {
        //console.log("result 1...");
        const result = this.stockOutTag_Desserts.find(x => x.stockOutTag_reagID === this.editedItem.stockOutTag_reagID);
        //console.log("result 1-2...", result);
                    
        if (result != 'undefined' && result != null) {
          console.log("result 2...", result);          
          this.editedItem.stockOutTag_reagName=result.stockOutTag_reagName;
          this.editedItem.stockOutTag_reagPeriod=result.stockOutTag_reagPeriod;
          this.editedItem.stockOutTag_reagTemp=result.stockOutTag_reagTemp;
          this.errorShowForReagName=false;
          return result.stockOutTag_reagName;          
        } else {
          this.editedItem.stockOutTag_reagName='';
          this.editedItem.stockOutTag_reagPeriod='';
          this.editedItem.stockOutTag_reagTemp='';
          this.errorShowForReagName=true;
          return '';
        }        
      } 
    },       

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

    load_SingleTable_ok(val) {
      if (val) {
        this.getSingleTableData();
      }
    }
  },

  created () {
    console.log("stockOutTag, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

    ////load 入庫草案資料
    //this.in_drafTags=0
    //if ("tags_draft" in localStorage) {
    //  let tempDesserts = JSON.parse(localStorage.getItem("tags_draft") || "[]");
    //  console.log("# of desserts: ", tempDesserts.length, tempDesserts);
    //  this.in_drafTags=tempDesserts.length; 
    //}

    this.initialize()
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
      this.desserts = [
        
        {
          //id: 1,
          stockOutTag_reagID: '123456789',
          stockOutTag_reagName: 'ABC',
          stockOutTag_reagPeriod: '111/10/31',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345B123400066',
          stockOutTag_unit: '盒',
        },
        {
          //id: 2,
          stockOutTag_reagID: '234567891',
          stockOutTag_reagName: 'ABCD',
          stockOutTag_reagPeriod: '111/12/31',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345C123400055',
          stockOutTag_unit: '盒',
        },
        {
          //id: 3,
          stockOutTag_reagID: '234567892',
          stockOutTag_reagName: 'A11',
          stockOutTag_reagPeriod: '111/12/31',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
        },
        {
          //id: 4,
          stockOutTag_reagID: '234567893',
          stockOutTag_reagName: 'A12',
          stockOutTag_reagPeriod: '112/6/30',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
        },
        {
          //id: 5,
          stockOutTag_reagID: '234567894',
          stockOutTag_reagName: 'B2233',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/10/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345B123400022',
          stockOutTag_unit: '盒',
        },
        {
          //id: 6,
          stockOutTag_reagID: '234567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 7,
          stockOutTag_reagID: '234567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 8,
          stockOutTag_reagID: '234567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/09/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 9,
          stockOutTag_reagID: '214567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 10,
          stockOutTag_reagID: '214567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 11,
          stockOutTag_reagID: '214567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 12,
          stockOutTag_reagID: '224567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 13,
          stockOutTag_reagID: '224567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/03/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },
        {
          //id: 14,
          stockOutTag_reagID: '224567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/05/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
        },        
      ];

      this.items = [
        '全部',
       'pmcA', 'pmcB', '3234', 'pmcC', 'pmcD'
      ]
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
      } //end else if
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
</style>