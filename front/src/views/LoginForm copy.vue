<template>
  <v-app>
    <div class="container" :class="{'sign-up-active' : signUp}">
      <div class="overlay-container">
        <div class="overlay">
          <div class="overlay-left">
            <h2>
              <img :src="home_url"  alt="..." style="height: 4vw; margin-bottom: 10px;">
              {{ '冷藏藥倉系統' }}
            </h2>          
            <button class="invert" id="signIn" @click="signUp = !signUp">登入</button>
          </div>
          
          <div class="overlay-right">          
            <h2>
              <img :src="home_url"  alt="..." style="height: 4vw; margin-bottom: 10px;">
              {{ '冷藏藥倉系統' }}
            </h2>          
            <button class="invert" id="signUp" @click="signUp = !signUp">註冊</button>
          </div>
        </div>
      </div>
      <form class="sign-up" action="#">
        <h3>{{ '註冊' }}</h3>     
        <v-text-field
          id="registerEmpID"
          label="員工編號"
          name="EmpID"
          class="text-teal"
          prepend-icon="mdi-account"
          type="text"
          required        
          v-model='registerUser.empID' 
        />
        <!-- {{ ErrMsg }} -->
        <small v-text= "empIDErrMsg"></small>    

        <v-text-field
          id="registerName"
          label="員工姓名"
          name="Name"
          class="text-teal"
          prepend-icon="mdi-email"
          type="text"
          required        
          v-model='registerUser.name'         
        />
        <!-- {{ ErrMsg }} -->
        <small v-text= "nameErrMsg"></small>       

        <v-text-field
          id="registerDep"
          label="組別"
          name="Dep"
          class="text-teal"
          prepend-icon="mdi-email"
          type="text"
          required      
          v-model='registerUser.dep'         
        />      
        <!-- {{ ErrMsg }} -->
        <small v-text= "depErrMsg"></small>       

        <v-text-field
          id="registerPassword"
          label="密碼"
          name="Password"
          class="text-teal"
          prepend-icon="mdi-lock"
          required
          :append-icon="eyeShow1 ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="() => (eyeShow1 = !eyeShow1)"
          :type="eyeShow1 ? 'password' : 'text'"
          v-model='registerUser.password' 
        />
        <!-- {{ ErrMsg }} -->
        <small v-text= "passwordErrMsg"></small>       

        <v-text-field
          id="registerConfirmPassword"
          label="確認密碼"
          name="Confirm"
          class="text-teal"
          prepend-icon="mdi-account-check"
          required
          :type="eyeShow1 ? 'password' : 'text'"
          :rules="[passwordConfirmationRule]"
          v-model='registerUser.confirmPassword' 
        />
        <button>註冊</button>
      </form>
      <form class="sign-in" action="#">
        <h3>{{ '登入' }}</h3>        
        <v-text-field
          id="loginEmpID"
          label="員工編號"
          name="EmpID"
          class="text-teal"
          prepend-icon="mdi-account"
          type="text"             
          v-model='loginEmpID' 
        />

        <v-text-field 
          id="loginPassword"
          label="密碼"
          name="Password"
          class="text-teal"
          prepend-icon="mdi-lock"
          :append-icon="eyeShow ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="() => (eyeShow = !eyeShow)"
          :type="eyeShow ? 'password' : 'text'"
          v-model='loginPassword' 
          @keyup.enter="signin"
        />
        <!--<a href="#">{{ '忘記密碼' }}</a>-->
        <button @click="signin">登入</button>
      </form>
    </div>
  </v-app>
</template>

<script>
import header from '../assets/image/china_header.png'

import axios from 'axios';
export default {
  data() {
    return {
      home_url: header,
      signUp: false,

      loginEmpID: null,
      loginPassword: null,

			empIDErrMsg: '',
      nameErrMsg: '',
      depErrMsg: '',
      passwordErrMsg: '',

      eyeShow: true,
      eyeShow1: true,
      eyeShow2: true,

      registerUser: {
				empID: null,
        name: null,
				dep: null,
				password: null,
				confirmPassword: null,
			},

      rules: {
        required: value => !!value || 'Required.',
      },
      load_SingleTable_ok: false, //for get employer table data
    };
  },

  created() {

  },

  beforeCreate () {

  },

  beforeDestroy () {

  },

  computed: {
    passwordConfirmationRule() {
      return () => (this.registerUser.password === this.registerUser.confirmPassword) || '密碼不相同!'
    },
  },

  watch: {    
    'registerUser.empID': function () {  
      let isEmpIDRule = /^[A,D,N,T][0-9]{5}$/;

      this.empIDErrMsg = '';
      let result = this.registerUser.empID.search(isEmpIDRule);

      if (result != -1) {
        this.empIDErrMsg = '';
      } else {
        this.empIDErrMsg = '員工編號資料格式錯誤!';
      }      
    },	//end 'empID': function()

    'registerUser.name': function () {  
      let isNameRule = /^[\u4e00-\u9fa5_a-zA-Z]+$/;

      this.nameErrMsg = '';
      let result = this.registerUser.name.search(isNameRule);
      let len=this.registerUser.name.length
      console.log("result, len: ", result, len);

      this.nameErrMsg = '';
      if (result==-1 || len>10) {
          this.nameErrMsg = '資料格式錯誤或資料長度太長!';
      }
    },	//end 'name': function()    

    'registerUser.dep': function () {  
      let isDepRule = /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/;

      this.depErrMsg = '';
      let result = this.registerUser.dep.search(isDepRule);
      let len=this.registerUser.dep.length
      console.log("result, len: ", result, len);

      this.depErrMsg = '';
      if (result==-1 || len > 20) {
        this.depErrMsg = '資料格式錯誤或資料長度太長!';
      }
    },	//end 'dep': function()  

    'registerUser.password': function () {
      //Regular expression Testing
      /* Here is an explanation:
      /^
            (?=.*\d)            // should contain at least one digit
            (?=.*[0-9])
            (?=.*[a-z])         // should contain at least one lower case
            (?=.*[A-Z])         // should contain at least one upper case
            (?=.*[!@#\$%\^&\*]) // should contain at least one special character
            (?=.{8,})
            (?=.*[a-zA-Z0-9]{8,30} // should contain 8 ~ 30 from the mentioned characters
      $/
      */
      //let isPasswordRule = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,12}$/;
      let isPasswordRule = /^(?=.*\d)(?=.*[a-z])[0-9a-zA-Z]{8,12}$/;

      this.passwordErrMsg = '';
      let result = this.registerUser.password.search(isPasswordRule);
      console.log("password regular: ", result);

      if (result != -1) {
        this.passwordErrMsg = '';        
      } else {
        this.passwordErrMsg = '資料格式或資料長度錯誤!';        
      }
    },  //end 'password': function() 
  }, 

  methods: {
    signin() {
      console.log("---click_signin---");

      let isAuthenticated=true;
      this.setAuthenticated(isAuthenticated);
      this.$router.push('/navbar'); 
    },

    setAuthenticated(isLogin) {
      localStorage.setItem('Authenticated', isLogin)
    },
  },
};
</script>

<style lang="scss" scoped>
@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

#app {
  background: #092525;
}

.container {
  position: relative;
  width: 768px;
  height: 480px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2), 0 10px 10px rgba(0, 0, 0, 0.2);
  background: linear-gradient(to bottom, #efefef, #ccc);
  margin-top: 10vh;

  .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform 0.5s ease-in-out;
    z-index: 100;
  }

  .overlay {
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    background: linear-gradient(to bottom right, #7fd625, #009345);
    color: #fff;
    transform: translateX(0);
    transition: transform 0.5s ease-in-out;
  }

  @mixin overlays($property) {
    position: absolute;
    top: 0;
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-direction: column;
    padding: 70px 40px;
    /*width: calc(50% - 80px);*/
    width: calc(50% - 40px);
    height: calc(100% - 140px);
    text-align: center;
    transform: translateX($property);
    transition: transform 0.5s ease-in-out;
  }

  .overlay-left {
    @include overlays(-20%);
  }

  .overlay-right {
    @include overlays(0);
    right: 0;
  }
}

h2, h3 {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

p {
  margin: 20px 0 30px;
}

a {
  color: #222;
  text-decoration: none;
  margin: 15px 0;
  font-size: 1rem;
}

button {
  border-radius: 20px;
  border: 1px solid #009345;
  background-color: #009345;
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  padding: 10px 40px;
  margin-top: 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: transform 0.1s ease-in;

  &:active {
    transform: scale(0.9);
  }

  &:focus {
    outline: none;
  }
}

button.invert {
  background-color: transparent;
  border-color: #fff;
}

form {
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-direction: column;
  padding: 90px 60px;
  /*width: calc(50% - 120px);*/
  width: calc(50% - 0px);
  /*height: calc(100% - 180px);*/
  height: calc(100% - 0px);
  text-align: center;
  background: linear-gradient(to bottom, #efefef, #ccc);
  transition: all 0.5s ease-in-out;

  div {
    font-size: 1rem;
  }

  
}

.sign-in {
  left: 0;
  z-index: 2;
}

.sign-up {
  left: 0;
  z-index: 1;
  opacity: 0;
}

.sign-up-active {
  .sign-in {
    transform: translateX(100%);
  }

  .sign-up {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    animation: show 0.5s;
  }

  .overlay-container {
    transform: translateX(-100%);
  }

  .overlay {
    transform: translateX(50%);
  }

  .overlay-left {
    transform: translateX(0);
  }

  .overlay-right {
    transform: translateX(20%);
  }
}

@keyframes show {
  0% {
    opacity: 0;
    z-index: 1;
  }
  49% {
    opacity: 0;
    z-index: 1;
  }
  50% {
    opacity: 1;
    z-index: 10;
  }
}

button.v-icon {
  /*background: yellow;*/
  padding-left: 10px;
  padding-right: 10px;
  height: 20px;
  width: 30px;
  border-style: none;
  background: linear-gradient(to bottom, #efefef, #ccc);
  margin-left: calc(100% + 50px);
}

.v-text-field {
  min-width: 17vw;;
}
/*
.text-teal input {
  color: #4dc0b5 !important;
}

.text-teal input::placeholder {
  color: red!important;
  opacity: 1;
}
*/
.text-teal .v-label {
  color: #909090;
  opacity: 1;
  font-size: 16px;
}

.v-messages__message {
  color: #FF5c4E;
  font-size: 12px;
}

small {
  font-size: 80%;
  color: red;
  margin-top: -20px;
}
</style>
