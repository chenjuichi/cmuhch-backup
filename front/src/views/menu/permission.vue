<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm == 1">
      <v-card width="62vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1" 
          item-key="name"
          :search="search"
          :custom-filter="filterOnlyCapsText"
          :options.sync="pagination"  
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>人員權限資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-text-field v-model="search" label="搜尋(大寫英文)" class="mx-4"></v-text-field>
            </v-toolbar>
          </template>

          <template v-slot:item.perm_checkboxForSystem="{ item }">
            <v-simple-checkbox
              color="indigo"
              v-model="item.perm_checkboxForSystem"
              @input="savePermissions(item)"          
            ></v-simple-checkbox>
          </template>          

          <template v-slot:item.perm_checkboxForAdmin="{ item }">
            <v-simple-checkbox
              color="indigo"
              v-model="item.perm_checkboxForAdmin"          
              @input="savePermissions(item)"          
            ></v-simple-checkbox>
          </template>

          <template v-slot:item.perm_checkboxForMember="{ item }">
            <v-simple-checkbox
              color="indigo"
              v-model="item.perm_checkboxForMember"          
              @input="savePermissions(item)"          
            ></v-simple-checkbox>
          </template>

          <template v-slot:body.append>
              <tr>
                <td></td>
                <td></td>
                <td></td>
               
                <td colspan="3">                
                  <v-checkbox v-model="filter_system" class="myLabel" color="primary" hide-details label="顯示系統"></v-checkbox>                  
                </td>
                <!--
                <td colspan="1">                
                  <!--<v-checkbox v-model="filter_admin" class="myLabel" color="primary" hide-details label="顯示管理者"></v-checkbox>                 
                </td>
                --> 
                <!--<td colspan="4"></td>-->
              </tr>
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
  name: 'Permission',

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

    filter_system: false,
    filter_admin: false,
    filter_member: false,
    //radioGroup: 1,
    search: '',
    myIndex: 0,
    //calories: '',
    /*
    //資料表頭
    headers: [      
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '員工編號', sortable: true, value: 'perm_empID', align: 'start'},
      { text: '姓名', sortable: false, value: 'perm_empName'},
      { text: '組別', sortable: true, value: 'perm_empDep'},
      { text: '管理者', sortable: true, value: 'perm_checkboxForAdmin'},        
      { text: '使用者', sortable: false, value: 'perm_checkboxForMember'},        
    ],
    */    
    desserts: [],
    temp_desserts: [],

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,

    editedIndex: -1,
    editedItem: {},

    load_SingleTable_ok: false, //for get employer table data
    //load_2thTable_ok: false,    //for get department table data
    //load_3thTable_ok: false,    //for get permission table data
  }),

  computed: {
    headers () {
      return [
        { text: '員工編號', sortable: true, value: 'perm_empID', width: '20%', align: 'start'},
        { text: '姓名', sortable: false, value: 'perm_empName', width: '15%'},
        { text: '組別', sortable: true, value: 'perm_empDep', width: '20%'},
        //顯示系統與管理者為 and 的條件
        { text: '系統', sortable: true, value: 'perm_checkboxForSystem', width: '15%',         
          filter: value => {
            //顯示系統權限資料
            if (!this.filter_system) { 
              console.log("hello system...", value);  
              if (!value) {
                return true;
              }
              //顯示管理者權限資料
              //@if (this.filter_admin) {  
                //this.myIndex=0;
              //@  return true
              //@}
              //不顯示管理者權限資料
              //@if (this.myIndex >= this.desserts.length) {
              //@  this.myIndex=0;
              //@}
              //@let k_admin=this.desserts[this.myIndex].perm_checkboxForAdmin
              //@this.myIndex++
              //@if (k_admin)
              //@  return false;
              //@else 
              //@  return true;           
            } else {
            //不顯示系統權限資料
                return true;
            }
          },          
        },

        //顯示系統與管理者為 and 的條件
        { text: '管理者', sortable: true, value: 'perm_checkboxForAdmin', width: '15%',
          /*          
          filter: value => {
            //console.log("hello admin...");  
            //console.log("item: ", this.filter_system)
            //顯示管理者權限資料
            if (this.filter_admin) {
              console.log("hello admin...");  
              //顯示系統權限資料
              if (this.filter_system) {  
                //this.myIndex=0;
                return true
              }
              //不顯示系統權限資料
              if (this.myIndex >= this.desserts.length) {
                this.myIndex=0;
              }
              let k_system=this.desserts[this.myIndex].perm_checkboxForSystem
              this.myIndex++
              if (k_system)
                return false;
              else 
                return true;
            }
            //console.log("perm: ", this.myIndex)
            //不顯示管理者權限資料
            //console.log("b my_index for admin: ", this.myIndex);
            //if (this.myIndex >= this.desserts.length) {
            //  this.myIndex=0;
            //}
            //console.log("my_index for admin: ", this.myIndex);
            //let k_admin=this.desserts[this.myIndex].perm_checkboxForAdmin
            //this.myIndex++
            //console.log("kk: ", k_admin)
            //if (k_admin)
            //  return false;
            //else 
              return true;            
          },
          */          
        },

        { text: '使用者', sortable: false, value: 'perm_checkboxForMember', width: '15%',},        
      ]
    }, 
  },

  watch: {
    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0 || this.currentUser.perm >1) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listPermissions();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listPermissions();    
    },

    listPermissions () { 
      const path = '/listPermissions';
      console.log("Axios get data from permission table...")
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

    savePermissions(item) {
      console.log("item: ", item)

      this.editedIndex = this.desserts.indexOf(item);
      
      this.updatePermissions(item);
      if (!this.tosterOK) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem)        
      }
    },

    updatePermissions(object) {  //編輯 reagent後端table資料
      console.log("---click checkbox for update_permissions data---", object);
      
      const path='/updatePermissions';
      let payload = Object.assign({}, object);      
      axios.post(path, payload)
      .then(res => {
        console.log("update permissions data status: ", res.data.status)
        if (res.data.status) {
          this.tosterOK = false; 
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;
        }        
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true; 
      });      
    },

    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
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

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child td:nth-child(4) > .v-input--selection-controls__input {
  margin-top: -18px;
}

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > td:last-child > label {
  margin-bottom: -4px;
}

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child { 
  background: #7DA79D; 
}

::v-deep .myLabel label  {
  margin-bottom: 1px;  
}

::v-deep .v-data-table-header th:nth-last-child(3) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
</style>