<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card width="50vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>員工資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="500px" :content-class='temp_css'>
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
                        <v-col cols="12" md="4">
                          <v-text-field
                            label="員工編號"
                            prepend-icon="mdi-account"
                            v-model="editedItem.emp_id"
                            :readonly="formTitle === '編輯資料'"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "IDErrMsg"></small>

                        </v-col>

                        <v-col cols="12" md="4">
                          <v-text-field
                            label="姓名"
                            prepend-icon="mdi-account-edit"
                            v-model="editedItem.emp_name"
                            @focus="fieldFocus"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="departments"
                            label="組別"
                            prepend-icon="mdi-account-group"
                            v-model="editedItem.emp_dep"
                            @focus="fieldFocus"
                          ></v-select>
                          <!--
                          <v-text-field
                            v-model="editedItem.emp_dep"
                            label="組別"
                          ></v-text-field>
                          -->
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>

                    <v-tooltip v-model="tosterOK" bottom :position-x="toster_pos_x" :position-y="toster_pos_y" color="error">
                      <span>員工編號重複!</span>
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
            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
            </v-icon>
            <v-icon small  @click="deleteItem(item)" style="color: red;">
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
  name: 'Employer',

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

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 400,
    toster_delay:3,

	  IDErrMsg: '',
    nameErrMsg: '',

    //資料表頭
    headers: [
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '員工編號', sortable: true, value: 'emp_id', width: '20%', align: 'start'},
      { text: '姓名', sortable: false, value: 'emp_name', width: '30%' },
      { text: '組別', sortable: true, value: 'emp_dep', width: '30%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },
    ],

    desserts: [],
    temp_desserts: [],

    departments: [],
    temp_departments: [],

    editedIndex: -1,
    editedItem: {
      //id: 0,
      emp_id: '',
      emp_name: '',
      emp_dep: '',
    },
    defaultItem: {
      emp_id: '',
      emp_name: '',
      emp_dep: '',
    },
    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get department table data
    //temp_css: 'add_modalbox',
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    checkDataForSaveButton() {
      if (!!this.editedItem.emp_id && !!this.editedItem.emp_name &&
          !!this.editedItem.emp_dep &&
          this.IDErrMsg == '' && this.nameErrMsg == '') {
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    dialog (val) {
      !val || this.fieldFocus();
      val || this.close();
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    'editedItem.emp_id': function () {
      let isEmpIDRule = /^[A,D,N,T][0-9]{5}$/;

      this.IDErrMsg = '';
      let result = this.editedItem.emp_id.search(isEmpIDRule);
      let len=this.editedItem.emp_id.length

      if (result != -1 || len==0) {
        this.IDErrMsg = '';
      } else {
        this.IDErrMsg = '員工編號資料格式錯誤!';
      }
    },	//end 'empID': function()

    'editedItem.emp_name': function () {
      let isNameRule = /^[\u4e00-\u9fa5_a-zA-Z]+$/;

      this.nameErrMsg = '';
      let result = this.editedItem.emp_name.search(isNameRule);
      let len=this.editedItem.emp_name.length
      console.log("result, len: ", result, len);

      this.nameErrMsg = '';
      if (result==-1 || len>10) {
          this.nameErrMsg = '資料格式錯誤或資料長度太長!';
      }
    },	//end 'name': function()

    load_2thTable_ok(val) {
      if (val) {
        this.departments = Object.assign([], this.temp_departments);
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
        this.listDepartments();
      }
    },
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listUsers();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listUsers();
    },

    listUsers() {
      const path = '/listUsers';
      console.log("listUsers, Axios get data...")
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

    listDepartments() {
      const path='/listDepartments';
      axios.get(path)
      .then((res) => {
        //this.temp_departments = res.data.outputs;
        this.temp_departments = res.data.outputs.map(item => Object.values(item)[0]); //從object中copy value至array

        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok = true;  //true: 資料download成功
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok = false;
      });
    },

    fieldFocus() {
      this.tosterOK=false;
      this.IDErrMsg='';
      this.nameErrMsg='';
    },
    /*
    updateSetting() {
      console.log("hello setting...")
      let path='/updateSetting';
      let payload= {
        setting: this.pagination.itemsPerPage,
        empID: this.currentUser.empID,
      };

      axios.post(path, payload)
      .then(res => {
          console.log("update user's setting ok", res.data.status);
      })
      .catch(err => {
          console.error(err);
      });
    },
    */
    editItem (item) { //open 編輯dialog(edit與create)
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem (item) { //open remove confirm dialog
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm () {  //確定刪除資料
      this.removeUser(this.editedItem.emp_id);

      if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      }
    },

    close () {  //close 編輯dialog(edit與create)
      this.dialog = false

      this.IDErrMsg='';
      this.nameErrMsg='';

      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete () {  //close remove confirm dialog
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    removeUser(id) {  //依user id來刪除後端table資料
      let path='/removeUser';
      let payload= {
        ID: id,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("remove user status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
          //this.editedItem={
          //  emp_id: '',
          //  emp_name: '',
          //  emp_dep: '',
          //};
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err)
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    save () { //確定 新增/編輯 user資料
      console.log("click save button, editedIndex: ", this.editedIndex);

      if (this.editedIndex == -1) {    //add
        this.createUser(this.editedItem);
        if (!this.tosterOK) {
          this.desserts.push(this.editedItem);
          this.close();
        }
      } else {    //edit
        this.updateUser(this.editedItem);
        if (!this.tosterOK) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
          this.close();
        }
      }
    },

    updateUser(object) {  //編輯 user後端table資料
      console.log("---click update_user data---", object);

      const path='/updateUser';
      var payload= {
        emp_id: object.emp_id,
        emp_name: object.emp_name,
        dep: object.emp_dep,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("update user data status: ", res.data.status)
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
          //this.editedItem={
          //  emp_id: '',
          //  emp_name: '',
          //  emp_dep: '',
          //};
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        //this.registerOK= false;
      });

      //this.signUp=false;  //註冊OK, 則轉為登入畫面
    },

    createUser(object) {  //新增 user後端table資料
      console.log("---click create_user data---");

      const defaultPassword='a12345678';
      const path='/createUser';
      var payload= {
        emp_id: object.emp_id,
        emp_name: object.emp_name,
        password: defaultPassword,
        dep: object.emp_dep,
        //perm_id: 4,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("save user data status: ", res.data.status)

        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
          //this.editedItem={
          //  emp_id: '',
          //  emp_name: '',
          //  emp_dep: '',
          //};
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
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
/*
th.text-start{
  font-size: 24px;
}

@mixin name {

}
*/
::v-deep .v-data-table-header {
  background-color: #7DA79D;
}

::v-deep .v-data-table-header th {
  font-size: 1em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}

::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}

</style>