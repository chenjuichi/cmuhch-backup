<template>
<v-app>
  
    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="text-h5">修改密碼</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    label="新密碼*"
                    v-model="newPassword"
                    required
                    prepend-icon="mdi-lock"
                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="showPassword ? 'text' : 'password'"                      
                    class="mb-6 text-teal"
                    @click:append="showPassword = !showPassword"
                  ></v-text-field>
                  <!-- {{ ErrMsg }} -->
                  <small class='errormsg' v-text= "passwordErrMsg"></small>  
                </v-col>
                <v-col cols="12" md="6" align="center" style="margin-top: 35px">
                  <v-progress-linear                    
                    :color="score.color"
                    :value="score.value"                    
                  ></v-progress-linear>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="確認密碼*"
                    v-model="confirmPpassword"
                    :type="showPassword ? 'text' : 'password'"                      
                    required
                    prepend-icon="mdi-account-check"
                    :rules="[passwordConfirmationRule]"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="save">儲存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>  
</v-app>
</template>

<script>
import axios from 'axios';

import Common from '../mixin/common'

import { zxcvbn, zxcvbnOptions } from '@zxcvbn-ts/core'
//import zxcvbnCommonPackage from '@zxcvbn-ts/language-common'
//import zxcvbnEnPackage from '@zxcvbn-ts/language-en'

export default {
  name: 'ChangePassword',

  mixins: [Common],

  computed: {
    passwordConfirmationRule() {
      return () => (this.newPassword === this.confirmPpassword) || '密碼不相同!'
    },

    score() {
      const result = zxcvbn(this.newPassword);
      
      switch (result.score) {
        case 4:
          return {
            color: "light-blue",
            value: 100
          };
        case 3:
          return {
            color: "light-green",
            value: 75
          };
        case 2:
          return {
            color: "yellow",
            value: 50
          };
        case 1:
          return {
            color: "orange",
            value: 25
          };
        default:
          return {
            color: "red",
            value: 0
          };
      }    
    },
  },  

  props: ['dialog_data'],

  watch: {
    dialog_data (val) {
      if (val) {
       this.dialog=true;
      }
    },
    
    newPassword(val) {
      let isPasswordRule = /^(?=.*\d)(?=.*[a-z])[0-9a-zA-Z]{8,12}$/;

      this.passwordErrMsg = '';
      let result = val.search(isPasswordRule);
      console.log("password regular: ", result);

      if (result != -1) {
        this.changeOK=true;
        this.passwordErrMsg = '';        
      } else {
        this.changeOK=false;
        this.passwordErrMsg = '資料格式或資料長度錯誤!';        
      }
    },
  }, 

  created() {
 
  },
  
  mounted() {

  },

  data() {
    return {
      currentUser: {
      	//empID: null,
        //name: null,
				//dep: null,
        //perm: 0,    //member: 2, admin: 1, none:0
      },
      showPassword: false,
      newPassword: '',
      confirmPpassword: '',
      changeOK: false,
      passwordErrMsg: '',
      dialog: false,
      /*
      rules: {
        required: value => !!value || '請輸入密碼',
        min: v => v.length >= 8 || '密碼長度至少需要8個字',
        max: v => v.length <= 12 || '密碼長度最多12個字',
        strength: v => zxcvbn(v).score >= 3 || 'Please choose a stronger password. Try a mix of letters and numbers.',
      },
      */
    };
  },

  methods: {
    save () {
      this.dialog = false
      this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
      console.log("click, save()..., currentUser ID: ", this.currentUser.empID);

      const path='/updatePassword';
      var payload= {
        newPassword: this.newPassword,
        empID: this.currentUser.empID,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("update password is ok!", res.data.status)
        //if (this.newPassword == this.confirmPpassword && this.changeOK && res.data.status)
        //  this.$emit('changePassword', this.newPassword);    
      })
      .catch(err => {
        console.error(err);
      });      
    },
  },
}
</script> 

<style scoped lang="scss">
/*
 ::v-deep .v-application--wrap {
    min-height: 0hv;
}
*/

small.errormsg {
  font-size: 80%;
  color: red;
  
  position: relative;
  top: -35px;
  left: 35px;

}
</style>
 