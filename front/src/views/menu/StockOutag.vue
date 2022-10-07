<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center">
      <v-card width="80vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>出庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
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
  </v-container>
</v-app>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Reagent',

  data: () => ({
    fromDateMenu: false,
    fromDateVal: null,

    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockOutTag_reagID', width: '10%' },
      { text: '品名', sortable: false, value: 'stockOutTag_reagName', width: '20%' },
      { text: '效期', sortable: true, value: 'stockOutTag_reagPeriod', width: '10%' },
      { text: '保存溫度', sortable: false, value: 'stockOutTag_reagTemp', width: '10%' },
      { text: '出庫日期', sortable: true, value: 'stockOutTag_outDate', width: '10%' },
      { text: '領用人員', sortable: true, value: 'stockOutTag_outEmployer', width: '10%' },
      { text: '批號', sortable: false, value: 'stockOutTag_batch', width: '20%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },        
    ],    
    desserts: [],
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

    load_SingleTable_ok(val) {
      if (val) {
        this.getSingleTableData();
      }
    }
  },

  created () {
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
          reag_id: '123456789',
          reag_name: 'ABC',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 4,
          reag_period: '111/10/31',
          reag_stock: 0,
          reag_temp: '2~8度C',
          reag_supplier: '貝克曼',           
        },
        {
          //id: 2,
          reag_id: '234567891',
          reag_name: 'ABCD',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 5,
          reag_period: '111/12/31',
          reag_stock: 2,
          reag_temp: '2~8度C',
          reag_supplier: '貝克曼',
        },
        {
          //id: 3,
          reag_id: '234567892',
          reag_name: 'A11',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 10,
          reag_period: '111/12/31',
          reag_stock: 0.5,
          reag_temp: '2~8度C',
          reag_supplier: '醫全', 
        },
        {
          //id: 4,
          reag_id: '234567893',
          reag_name: 'A12',
          reag_In_unit: '盒',
          reag_Out_unit: '條',
          reag_scale: 5,
          reag_period: '112/6/30',
          reag_stock: 2,
          reag_temp: '2~8度C',
          reag_supplier: '醫全',
        },
        {
          //id: 5,
          reag_id: '234567894',
          reag_name: 'B2233',
          reag_In_unit: '盒',
          reag_Out_unit: '個',
          reag_scale: 10,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '2~8度C',
          reag_supplier: '醫全', 
        },
        {
          //id: 6,
          reag_id: '234567897',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 7,
          reag_id: '234567898',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 8,
          reag_id: '234567899',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 9,
          reag_id: '214567897',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 10,
          reag_id: '214567898',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 11,
          reag_id: '214567899',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 12,
          reag_id: '224567897',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 13,
          reag_id: '224567898',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
        {
          //id: 14,
          reag_id: '224567899',
          reag_name: 'B3344',
          reag_In_unit: '盒',
          reag_Out_unit: '瓶',
          reag_scale: 6,
          reag_period: '111/8/31',
          reag_stock: 1,
          reag_temp: '常溫',
          reag_supplier: '裕利',
        },
      ];
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
        this.editedItem.id=this.desserts.length+1;
        this.desserts.push(this.editedItem)
      }
      this.close()
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
</style>