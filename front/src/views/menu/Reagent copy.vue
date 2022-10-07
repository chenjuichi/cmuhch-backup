<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="80vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"        
          :options.sync="pagination"        
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>試劑資料</v-toolbar-title>
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
                          <v-text-field
                            v-model="editedItem.reag_id"
                            label="資材碼"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.reag_name"
                            label="品名"
                          ></v-text-field>
                        </v-col>                                            
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="入庫單位"                               
                            v-model="editedItem.reag_In_unit" 
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="出庫單位"                               
                            v-model="editedItem.reag_Out_unit" 
                          ></v-select>
                        </v-col>              
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.reag_scale"
                            label="比例"
                          ></v-text-field>
                        </v-col>
                        
                        <v-col cols="12" md="5">
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
                                label="效期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.reag_period"
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

                      <!-- 第3列-->
                      <v-row>                   
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.reag_stock"
                            label="安全存量"
                          ></v-text-field>
                        </v-col>                        
                        <v-col cols="12" md="4">
                          <v-select
                            :items="['室溫','2~8度C','-20度C']"
                            label="保存溫度"                               
                            v-model="editedItem.reag_temp" 
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-select
                            :items="['醫全','實用','貝克曼', '尚上','伯昂','裕利','育聖']"
                            label="供應商"                               
                            v-model="editedItem.reag_supplier" 
                          ></v-select>
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
  name: 'Reagent',

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
    currentUser: { },
    permDialog: false,

    fromDateMenu: false,
    fromDateVal: null,

    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'reag_id', width: '10%' },
      { text: '品名', sortable: false, value: 'reag_name', width: '10%' },
      { text: '入庫單位', sortable: false, value: 'reag_In_unit', width: '10%' },
      { text: '出庫單位', sortable: false, value: 'reag_Out_unit', width: '10%' },
      { text: '比例', sortable: false, value: 'reag_scale', width: '10%' },
      { text: '效期', sortable: true, value: 'reag_period', width: '10%' },
      { text: '安全存量', sortable: false, value: 'reag_stock', width: '10%' },
      { text: '保存溫度', sortable: false, value: 'reag_temp', width: '10%' },
      { text: '供應商', sortable: true, value: 'reag_supplier', width: '10%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },        
    ],

    desserts: [],
    temp_desserts: [],

    suppliers: [],
    temp_suppliers: [],

    editedIndex: -1,
    editedItem: {
      //id: 0,
      reag_id: '',
      reag_name: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: 0,
      reag_period: '',
      reag_stock: 0,
      reag_temp: '',
      reag_supplier: '',      
    },
    defaultItem: {
      reag_id: '',
      reag_name: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: 0,
      reag_period: '',
      reag_stock: 0,
      reag_temp: '',
      reag_supplier: '',      
    },

    load_SingleTable_ok: false,
    load_2thTable_ok: false
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromDateDisp() {
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.reag_period = yy_value + '/' + mmdd_value;
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

    load_2thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
        this.listSuppliers();
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listReagent();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listReagent();
    },

    listReagent () { 
      const path = '/listReagents';
      console.log("Axios get data...")
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
      //} catch (err) {
      //  console.error(err)
      //}
    },

    listSuppliers() { 
      const path = '/listSuppliers';
      console.log("listSuppliers, Axios get data...")
      axios.get(path)
      .then((res) => {
        //this.temp_suppliers = res.data.outputs;
        this.temp_suppliers = res.data.outputs.map(item => Object.values(item)[2]); //從object中copy value至array

        console.log("GET ok, total records:", res.data.outputs.length);        
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
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
        this.desserts.push(this.editedItem)
      }
      this.close()
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
  font-size: 1em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
}

::v-deep .v-label {
  font-size: 1em
}
::v-deep .v-label--active {
  font-size: 1.2em;
  font-weight: bold;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
</style>