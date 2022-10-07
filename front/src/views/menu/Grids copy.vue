<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="55vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"        
          :options.sync="pagination"        
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>儲位資料</v-toolbar-title>
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
                          <v-tooltip v-model="errorShow" top color="error">                        
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field                            
                                v-model="editedItem.grid_reagID"
                                label="資材碼"
                              ></v-text-field>
                            </template>
                            <span>資材碼錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.grid_reagName"
                            :value="fromReagIdDisp"
                            label="品名"
                            readonly
                          ></v-text-field>
                        </v-col>                                            
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">站別</div>
                          <vue-numeric-input  v-model="editedItem.grid_station" :min="1" :max="3" :step="1"></vue-numeric-input>
                        </v-col>
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">層別</div>
                          <vue-numeric-input  v-model="editedItem.grid_layout" :min="1" :max="5" :step="1"></vue-numeric-input>
                        </v-col>              
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">格位別</div>
                          <vue-numeric-input  v-model="editedItem.grid_pos" :min="1" :max="10" :step="1"></vue-numeric-input>
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
import VueNumericInput from 'vue-numeric-input';

import Common from '../../mixin/common.js'

export default {
  name: 'Grids',

  mixins: [Common],

  components: {
    VueNumericInput,
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

  data: () => ({
    currentUser: {
      	//empID: null,
        //name: null,
				//dep: null,
        //perm: 0,    //member: 0001b, admin: 0010b, all:0011b
    },
    permDialog: false,

    currentUser: {},

    errorShow: false,
    dialog: false,
    dialogDelete: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'grid_reagID', width: '10%' },
      { text: '品名', sortable: false, value: 'grid_reagName', width: '10%' },
      { text: '站別', sortable: true, value: 'grid_station', width: '10%' },
      { text: '層別', sortable: false, value: 'grid_layout', width: '10%' },
      { text: '格位別', sortable: false, value: 'grid_pos', width: '10%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },        
    ],
    
    reagent_Desserts: [
      {
        //id: 1,
        reag_id: '123456789',
        reag_name: 'ABC',         
      },
      {
        //id: 2,
        reag_id: '234567891',
        reag_name: 'ABCD',
      },
      {
        //id: 3,
        reag_id: '234567892',
        reag_name: 'A11',
      },
      {
        //id: 4,
        reag_id: '234567893',
        reag_name: 'A12',
      },
      {
        //id: 5,
        reag_id: '234567894',
        reag_name: 'B2233',
      },
      {
        //id: 6,
        reag_id: '234567897',
        reag_name: 'B3347',
      },
      {
        //id: 7,
        reag_id: '234567898',
        reag_name: 'B3348',
      },
      {
        //id: 8,
        reag_id: '234567899',
        reag_name: 'B3349',
      },
      {
        //id: 9,
        reag_id: '214567897',
        reag_name: 'B3397',
      },
      {
        //id: 10,
        reag_id: '214567898',
        reag_name: 'B3398',
      },
      {
        //id: 11,
        reag_id: '214567899',
        reag_name: 'B3399',
      },
      {
        //id: 12,
        reag_id: '224567897',
        reag_name: 'B3356',
      },
      {
        //id: 13,
        reag_id: '224567898',
        reag_name: 'B3357',
      },
      {
        //id: 14,
        reag_id: '224567899',
        reag_name: 'B3366',
      },
    ],

    desserts: [],
    temp_desserts: [],

    editedIndex: -1,
    editedItem: {
      grid_reagID: '',
      grid_reagName: '',
      grid_station: 1,
      grid_layout: 1,
      grid_pos: 1,     
    },
    defaultItem: {
      grid_reagID: '',
      grid_reagName: '',
      grid_station: 1,
      grid_layout: 1,
      grid_pos: 1,     
    },
    load_SingleTable_ok: false, //for get grids table data
    //load_2thTable_ok: false,    //for get reagent table data
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },
    fromReagIdDisp () { 
      if (this.editedItem.grid_reagID != '') {
        console.log("result 1...");
        const result = this.reagent_Desserts.find(x => x.reag_id === this.editedItem.grid_reagID);
        //this.reagent_Desserts.find(x => x.reag_id === this.editedItem.grid_reagID || { value: null }).value;
        //console.log("value: ", value, typeof(value)); 
        console.log("result 1-2...", result);
                    
        if (result != 'undefined' && result != null) {
          console.log("result 2...", result);
          let val= Object.values(result);
          this.editedItem.grid_reagName=val[1];
          this.errorShow=false;
          console.log("result: ", result, typeof(result), val[1]);             
          return val[1];          
        } else {
          this.editedItem.grid_reagName='';
          this.errorShow=true;
          return '';
        }        
      } 
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
    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listGrids();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listGrids();
      /*
      this.desserts = [
        {
          //id: 1,
          grid_reagID: '123456789',
          grid_reagName: 'ABC',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 4,         
        },
        {
          //id: 2,
          grid_reagID: '234567891',
          grid_reagName: 'ABCD',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 5,
        },
        {
          //id: 3,
          grid_reagID: '234567892',
          grid_reagName: 'A11',
          grid_station: 2,
          grid_layout: 1,
          grid_pos: 6,
        },
        {
          //id: 4,
          grid_reagID: '234567893',
          grid_reagName: 'A12',
          grid_station: 2,
          grid_layout: 3,
          grid_pos: 5,
        },
        {
          //id: 5,
          grid_reagID: '234567894',
          grid_reagName: 'B2233',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 2,
        },
        {
          //id: 6,
          grid_reagID: '234567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 1,
          grid_pos: 6,
        },
      ];    
      */
    },

    listGrids() { 
      const path = '/listGrids';
      console.log("listGrids, Axios get data...")
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