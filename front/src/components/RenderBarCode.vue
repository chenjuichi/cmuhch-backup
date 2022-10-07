<template>
<v-app> 
  <!--
  <div v-for="field in qrTags" :key="field.work_id">
    <PrintQRCode :stack="field"></PrintQRCode>
  </div>
  -->   
  <!--<MyBarcode :barcode_data="regFields" v-on:scroll.native="handleScroll"></MyBarcode>-->
  <MyBarcode :barcode_data="regFields" @pressPrint="onPressPrint"></MyBarcode>
  <!--
  <v-col cols="12" md="6">
    <v-btn v-on:click="addFormElement('BarCode')" v-show="!isPrint">
      <v-icon left>mdi-qrcode</v-icon>
      {{ $t('FORKIN.ShowQRCode') }}
    </v-btn>
  </v-col>        
  <v-col cols="12" md="6">
    <v-btn v-print="printObj" :class="{'disable-events': !isPrint}">
      <v-icon left>mdi-printer</v-icon>
      {{ $t('FORKIN.PrintQRCode') }}
    </v-btn>        
  </v-col>
  -->
  <!--</v-row>--> 
</v-app>
</template>

<script>
import MyBarcode from '../components/BarCode.vue';
//import print from 'vue-print-nb';

export default {
  name: 'RenderBarCode',

  components: {
    MyBarcode, 
    //print,
  },
  
  props: [
    'sidebar', 'drawer' 
  ],


  data () {
    return {
      /*
      isShow: false,    
      isPrint: false,
      printObj: {
        id: "printMe",
        preview: false,
        previewTitle: "列 印 預 覽",
        popTitle: "cmu-hch print",
        extraCss: "",
        previewPrintBtnLabel: "列 印",
        previewBeforeOpenCallback (vue) {
          console.log('正在下載預覽窗口')
        },
        previewOpenCallback (vue) {
          console.log('已經完成下載預覽窗口')
        },
        beforeOpenCallback (vue) {
          console.log('打開之前')
        },
        openCallback (vue) {
          console.log('執行列印...')
        },
        closeCallback (vue) {
          console.log('關閉列印...')
        },
      },
      */
      /*
      codeInfo: {
        reagID: this.sidebar.stockInTag_reagID,
        reagName: this.sidebar.stockInTag_reagName,
        reagPeriod: this.sidebar.stockInTag_reagPeriod,
        reagTemp: this.sidebar.stockInTag_reagTemp,
        date: this.sidebar.stockInTag_Date,
        empID: this.stockInTag_EmpID,
        employer: this.sidebar.stockInTag_Employer,
        batch: this.sidebar.stockInTag_batch,
        cnt: this.sidebar.stockInTag_cnt
      },
      */
      fields: [],
      show_barcode: false,
      regFields: [],
      waiting_in_total_tags: 0,
    };
  },

  watch: {
    sidebar(val) {
      this.fields.push(val);
      console.log("sidebar:", val);
    },

    drawer(val) {
      if (val) {
        this.show_barcode=val;
        console.log("drawer ok!");
        this.formField();
      }
      console.log("drawer:", val);
    },

    //codeInfo(val) {
    //  this.fields.push(val);
    //  console.log("codeInfo:", val);
    //},
  },

  created () {
    console.log("RenderBarCode, created()...");
    //this.fields = [];
    //this.fields = this.sidebar;
    //console.log('props: ', this.sidebar[0]);
  },

  mounted() {
    console.log("RenderBarCode, mounted()...");
  },

  computed: {

  },

  methods: {
    ////handleScroll(event) {
      // Any code to be executed when the window is scrolled
      //this.isUserScrolling = (window.scrollY > 0);
    ////  console.log('calling handleScroll');
    ////},

    formField() {
      this.regFields=[];
      let temp_len=this.fields.length; 
      for (let i=0; i < temp_len; i++) {
        let temp_tags=this.fields[temp_len-1][i].stockInTag_cnt;
        for (let j=0; j < temp_tags; j++) {
          this.regFields.push(this.fields[temp_len-1][i]);
        }
      }
      this.waiting_in_total_tags=this.regFields.length;
      //this.$emit('waitTags', this.waiting_in_total_tags);
    },

    onPressPrint(value) {
      this.is_print_OK=value;
      if (this.is_print_OK)
        this.$emit('waitTags', this.waiting_in_total_tags);
    },

    /*
    addFormElement(type) {
      this.isShow = true;
      if (this.isShow) {
        this.fields.push({
          'type': type,
          id: this.count++
        });
        this.isPrint = true;
      }
    },
    */ 
  },
}
</script>

<style scoped>

</style>