<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card max-width="35vw" class="pa-md-4 mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :item-class="setRowStyle"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>組別資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px" content-class="add_modalbox">
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
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            label="組別"
                            type="text"
                            prepend-icon="mdi-account-group"
                            @focus="fieldFocus"
                            v-model="editedItem.dep_name"
                          />
                          <small class="msgErr" v-text= "depErrMsg"></small>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <!--<v-btn color="blue darken-1" text @click="save">儲存</v-btn>-->
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>
                    <v-tooltip v-model="tosterOK" bottom :position-x="toster_pos_x" :position-y="toster_pos_y" color="error">
                      <span>組別資料重複!</span>
                    </v-tooltip>
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
            <v-icon class="mr-2" @click="editItem(item)" style="color: blue;" size="16">
              mdi-pencil
            </v-icon>
            <v-icon  @click="deleteItem(item)" style="color: red;" size="16">
              mdi-delete
            </v-icon>
          </template>
          <!--
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
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
  name: 'Department',

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
    dialog: false,
    dialogDelete: false,
    //disbtn : true,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 350,
    toster_delay:3,

    depErrMsg: '',

    //資料表頭
    headers: [
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      {text: '組    別', sortable: true, value: 'dep_name', width: '80%', align: 'center'},
      {text: 'Actions', sortable: false, value: 'actions', width: '20%'},
    ],
    desserts: [],
    temp_desserts: [],

    editedIndex: -1,
    editedItem: {
      id: '',
      dep_name: '',
    },
    defaultItem: {
      id: '',
      dep_name: '',
    },

    load_SingleTable_ok: false,   //true: get department table data is ok
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    checkDataForSaveButton() {
      if (!!this.editedItem.dep_name && this.depErrMsg == '') {
        return false;
      } else {
        return true
      }
    }
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
    },

    'editedItem.dep_name': function (){
      let isDepRule = /^([a-zA-Z\u4e00-\u9fa5_.-]+)$/;
      // /^([a-zA-Z0-9\u0600-\u06FF\u0660-\u0669\u06F0-\u06F9 _.-]+)$/
      let result = this.editedItem.dep_name.search(isDepRule);
      let len=this.editedItem.dep_name.length
      result = (len==0)?0:result
      //console.log("result, len: ", result, len);
      this.depErrMsg = '';
      if (result==-1 || len > 12) {
        this.depErrMsg = '資料格式錯誤!';
        //this.disbtn = true;
      } else{
        this.depErrMsg = '';
        //this.disbtn = false;
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listDepartment();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listDepartment();
      /*
      this.desserts = [
        {
          //id: 1,
          dep_name: '機器人設計部',
        },
        {
          dep_name: '護理科',
        },
        {
          dep_name: '醫事科',
        },
        {
          dep_name: '檢驗科',
        }
      ]
      */
    },

    listDepartment() {
      const path = '/listDepartments';
      console.log("listDepartments, Axios get data...")
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

    fieldFocus() {
      this.depErrMsg = '';
    },

    editItem (item) {
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      this.removeDepartment(this.editedItem.id);

      if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      }
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

    removeDepartment(id) {   //依 department id來刪除後端table資料
      let path='/removeDepartment';
      let payload= {
        ID: id,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("remove department status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err)
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    save () {
      console.log("click save button, editedIndex: ", this.editedIndex);

      if (this.editedIndex == -1) {    //add
        this.createDepartment(this.editedItem);
        if (!this.tosterOK) {
          this.desserts.push(this.editedItem);
          this.close();
        }
      } else {    //edit
        this.updateDepartment(this.editedItem);
        if (!this.tosterOK) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
          this.close();
        }
      }
    },

    updateDepartment(object) {  //編輯 product後端table資料
      console.log("---click update_department data---", object);

      const path='/updateDepartment';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("update department data status: ", res.data.status)
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    createDepartment(object) { //新增 department後端table資料
      console.log("---click create_department data---");
      console.log("department object: ", object);

      const path='/createDepartment';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save department data status: ", res.data.status)

        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
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

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

::v-deep .style-1 td {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

::v-deep .style-1 td:nth-last-child(1) {
  text-align: center !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th:nth-last-child(1) {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: center !important;
}
/*
::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}
*/
</style>