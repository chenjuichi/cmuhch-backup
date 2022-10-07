<template>
<v-app>
  <b-navbar justified type="dark" variant="dark" class="navbar custom-nav fixed-top" expand="lg" light bg="light">
    <b-navbar-brand>
      <img :src="home_url"  alt="..." style="height: 4vw;">
    </b-navbar-brand>
    <b-navbar-nav>
      <b-nav-item href="#">首頁</b-nav-item>
      <div v-for="navbar in navbars" :key="navbar.id">
        <b-nav-item-dropdown :text="navbar.text" @click.prevent="open=!open" right>
          <b-dropdown-item :to="navbar.router1">
            <b-avatar variant="success" :icon="navbar.icon1" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name1 }}
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router2">
            <b-avatar variant="success" :icon="navbar.icon2" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name2 }}
          </b-dropdown-item>

          <b-dropdown-item :to="navbar.router3">
            <b-avatar variant="success" :icon="navbar.icon3" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
            {{ navbar.name3 }}
            <v-badge color="green" variant="light" :content="navBar_in_drafTags" v-show="navbar.id==2 && navBar_in_drafTags!=0"></v-badge>            
          </b-dropdown-item>

          <div v-show="navbar.id==1"> 
            <b-dropdown-item :to="navbar.router4">
              <b-avatar variant="success" :icon="navbar.icon4" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
              {{ navbar.name4 }}
            </b-dropdown-item>

            <!--供應商-->
            <!--
            <b-dropdown-item :to="navbar.router5">
              <b-avatar variant="success" :icon="navbar.icon5" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
              {{ navbar.name5 }}
            </b-dropdown-item>           
            -->
            <b-dropdown id="dropdown-2" dropright variant="#FFFFFF" class="ml-3" style="color: #1976d2;">
              <template #button-content>
                <b-avatar variant="success" :icon="navbar.icon5" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt; color: #1976d2;"></b-avatar>
                {{ navbar.name5 }}
              </template>
              <b-dropdown-item :to="navbar.router5">{{ navbar.name5 }}</b-dropdown-item>
              <b-dropdown-item to="/supAndPrd">主要產品類別資料</b-dropdown-item>
            </b-dropdown>           
            
            <b-dropdown-item :to="navbar.router6">
              <b-avatar variant="success" :icon="navbar.icon6" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
              {{ navbar.name6 }}
            </b-dropdown-item>
          </div>
        </b-nav-item-dropdown>
      </div>
    </b-navbar-nav>
    <b-navbar-nav class="ml-auto">
          <em>{{ currentUser.name }}</em>
      <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
        
        
        <!--<b-dropdown-item href="#">Profile</b-dropdown-item>-->
        <b-dropdown-item href="#" @click="logout">          
          
            <div>
              <!--<b-icon-arrow-up></b-icon-arrow-up>-->
              <!--<p class="h5 mb-2">-->
                <!--<b-icon icon="exclamation-circle-fill"></b-icon>-->
                <!--<b-icon icon="box-arrow-left" font-scale="1" style="color: #ff0000;"></b-icon>-->
                <b-avatar variant="danger" icon="box-arrow-left" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
                登出
              <!--</p>-->
            </div>
                 
        </b-dropdown-item>

        <b-dropdown-item href="#" @click="changePassword">          
          
            <div>
                <b-avatar variant="primary" icon="pencil-square" style="width: 1.5rem; height: 1.5rem; margin-bottom: 3pt;"></b-avatar>
                修改密碼
            </div>
                  
        </b-dropdown-item>        
      </b-nav-item-dropdown>      
    </b-navbar-nav>
  </b-navbar>

  <!--<ChangePassword :dialog_data="openDialog" @changePassword="onModifyPassword"></ChangePassword>-->
  <ChangePassword :dialog_data="openDialog"></ChangePassword>
  <div 
    :style="inlineStyle"
           
  ></div>
</v-app>
</template>
 
<script>
import axios from 'axios';

import Common from '../mixin/common.js'

import logo from '../assets/image/china_logo.png'
import main_pic from '../assets/image/hero-bg2.jpg'

import ChangePassword from '../components/changePassword.vue';

// Note: Vue automatically prefixes the directive name with 'v-'
//import { VBHover } from 'bootstrap-vue'
import { VBVisible } from 'bootstrap-vue' 

import {SYSTEM,} from '../mixin/constant'

export default {
  name: 'Navbar',

  directives: {
    //'b-hover': VBHover
    'b-visible': VBVisible   
  }, 

  mixins: [Common],

  components: {
    ChangePassword,
  },

computed: {
  inlineStyle () {
    return {
      backgroundImage: `url(`+ this.main_pic_url +`)`,
      position: `fixed`,
      height: `100vh`,
      width: `100vw`,
      top: `16vh`,
      //backgroundPosition: `center`     
    }
  }
},

  created() {
    //disabled browser's back key
    //history.pushState(null, null, location.href);
    //window.onpopstate = function () {
    //  history.go(1);
    //};

    //console.log("hello! System disabled back key now.");

    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    console.log("current user:",this.currentUser);

    this.initAxios();

  },
  
  mounted() {
    //this.navBar_in_drafTags=this.$route.params.in_drafTags;
    //if (typeof(this.navBar_in_drafTags) === 'undefined') {
    //  this.navBar_in_drafTags=0;
    let temp=localStorage.getItem("totalTags")
    if(typeof(temp)=='undefined' || temp==null)
        this.navBar_in_drafTags=0;
    else 
      this.navBar_in_drafTags=parseInt(temp);

    //if ("totalTags" in localStorage) {
    //  this.navBar_in_drafTags=localStorage.getItem("totalTags")
      //console.log("router undefine!")
    //} else {
    //  this.navBar_in_drafTags=0;
    //  localStorage.setItem("totalTags", 0);
    //}
    console.log("navbar, totalTags: ", this.navBar_in_drafTags);
    //this.navBar_in_drafTags=2;  
    
    //====
    this.$root.$on('bv::dropdown::show', bvEvent => {
      if(bvEvent.componentId === 'dropdown-2') {
        this.isDropdown2Visible = true;
      }
      })
    this.$root.$on('bv::dropdown::hide', bvEvent => {
        if(bvEvent.componentId === 'dropdown-2') {
          this.isDropdown2Visible = false;
        }
        if(this.isDropdown2Visible) {
          bvEvent.preventDefault()
        }
        })

    //===


  },

  data() {
    return {
      openDialog: false,
      open: false,
      navBar_in_drafTags: 0,
      
      navBar_newTags: 0,

      subMenu: false,
      isDropdown2Visible: false,

      home_url: logo,
      main_pic_url: main_pic,
      currentUser: {},
      navbars: [
        { id: 1,
          text: "基本資料維護", 
          icon1: "person-plus", name1: "人員資料", router1: "/emp", 
          icon2: "person-lines-fill", name2: "人員權限資料", router2: "/perm",
          icon3: "clipboard-data", name3: "試劑資料", router3: "/reag",
          icon4: "bookshelf", name4: "儲位設定", router4: "/grid",
          icon5: "briefcase", name5: "供應商資料", router5: "/sup",
          icon6: "people", name6: "組別資料", router6: "/dep"
        },
        { id: 2,
          text: "入庫管理", 
          icon1: "bookmark-plus", name1: "入庫標籤資料", router1: "/inTag", 
          icon2: "bag-plus", name2: "入庫標籤列印", router2: "/inTagPrint",
          icon3: "cart-plus", name3: "入庫作業", router3: "/stockIn",          
        },
        { id: 3,
          text: "出庫管理", 
          icon1: "bookmark-dash", name1: "出庫標籤資料", router1: "/outTag", 
          icon2: "bag-dash", name2: "出庫標籤列印", router2: "/outTagPrint",
          icon3: "cart-dash", name3: "出庫作業", router3: "/app3",          
        },
        { id: 4,
          text: "物料盤點", 
          icon1: "book", name1: "領用記錄查詢", router1: "/reqRec", 
          icon2: "calendar2-check", name2: "庫存紀錄查詢", router2: "/stockRec",
          icon3: "upc-scan", name3: "盤點作業", router3: "/invent",          
        },
      ],
    };
  },

  methods: {
    changePassword() {
      this.openDialog=true;
    },
    /*
    async onModifyPassword(value) {
        let path='/updatePassword';
        let payload= {
          newPassword: value,
          empID: currentUser.emp_id,
        };

        try {
          let res = await axios.post(path, payload);
          console.log("change password ok", res.data.status);
        } catch (err) {
          console.error(err)
        }
    },
    */
    logout() {
      console.log("logout...");
      this.updateSetting();
      let isAuthenticated=false;
      this.setAuthenticated(isAuthenticated);
      this.removeLoginUser();      
      if (this.$route.path != '/') {
        this.$router.push('/');
      }
    },

    updateSetting() {
      console.log("hello setting...")

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      let path='/updateSetting';
      let payload= {
        setting: userData.setting_items_per_page,
        empID: userData.empID,
      };

      axios.post(path, payload)
      .then(res => {
          console.log("update user's setting ok", res.data.status);
      })
      .catch(err => {
          console.error(err);
      });
    },    

    removeLoginUser() {
      localStorage.removeItem('loginedUser');
    },

    setAuthenticated(isLogin) {
      localStorage.setItem('Authenticated', isLogin)
    },

    handleHover(e) {
      console.log("nav-dropdown key press: ", e);
    }
  },
}
</script>
 
<style scoped lang="scss">
  @media (min-width: 992px) { 
    .navbar.custom-nav{
      padding-top:16px;
      padding-bottom:16px;
      background-color: #7DA79D !important;
    }
  }

  span.v-badge__badge {
    background: red !important;
  }

  ::v-deep .dropdown.b-dropdown.subMenu.btn-group {
    background: red !important;
  }

  ::v-deep svg.bi-briefcase.b-icon.bi {
    color: #ffffff !important;
  }
</style>