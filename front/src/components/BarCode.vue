<template>
  <v-app ref="barcode">
    <v-container class="scroll-y">
      <v-layout align-center justify-center id="layout">
        <v-flex xs12>
          <v-col class="text-right">             
          <!--
          <v-btn color="primary" dark class="mb-2" @click="printBarcode">
            <v-icon left dark>mdi-keyboard-return</v-icon>返回
          </v-btn>
          &nbsp;&nbsp;
          -->
            <!--<v-btn color="primary" dark class="mb-2" @click="printBarcode">-->
            <v-btn color="primary" dark class="mb-2" v-print="printObj" @click="printBarcode">
              <v-icon left dark>mdi-printer</v-icon>列印
            </v-btn>
          </v-col>
          <v-btn v-scroll="onScroll" v-show="fab" fab dark fixed bottom right color="primary"
              @click="toTop"  
          >                     
            <v-icon>keyboard_arrow_up</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs12>
          <v-card id="printMe">
          <div v-for="(field, index) in barcode_data" :key="index" style="text-align:center">
            <div>中國醫藥大學新竹附設醫院</div>
            <barcode :value="field.stockInTag_reagID"></barcode>
            <span>入庫人員: {{ field.stockInTag_Employer }}</span>
            <v-spacer></v-spacer>
          </div>  
          <!--
          <div>中國醫藥大學新竹附設醫院</div>
          <barcode :value="1234567890" lineColor="#007bff"></barcode>
          <span>入庫人員: {{}}</span>
          -->
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>  

<script>
import VueBarcode from 'vue-barcode';
import * as easings from 'vuetify/lib/services/goto/easing-patterns';
import print from 'vue-print-nb';

export default {
  name: 'BarCode',

  components: {
    'barcode': VueBarcode,
  },

  props: ['barcode_data'],

  directives: {
    print   
  },

  mounted() {
    console.log("BarCode, mounted()...");

    this.startTimer();
  },

  created() {
    console.log("BarCode, created()...");
  },

  computed: {

  },
  
  watch: {

  },
  
  data() {
    return {
      fab: false,

      myTimer: '',            //在component內設定timer, timer的handle
      myTimerId: '',          //timer的id

      printObj: {
        id: "printMe",
        preview: false,
        //previewTitle: "列 印 預 覽",
        popTitle: "cmu-hch print",
        extraCss: "",
        //previewPrintBtnLabel: "列 印",
        //previewBeforeOpenCallback (vue) {
        //  console.log('正在下載預覽窗口')
        //},
        //previewOpenCallback (vue) {
        //  console.log('已經完成下載預覽窗口')
        //},
        beforeOpenCallback (vue) {
          console.log('打開之前',vue)
        },
        openCallback (vue) {
          console.log('執行列印...', vue)
        },
        closeCallback (vue) {
          console.log('關閉列印...', vue)
        },        
      },      
    };
  },

  destoyed() {
    clearInterval(this.myTimer);
  }, 

  beforeRouteLeave(to, from, next) {    
    clearInterval(this.myTimer);
    next();
  },  

  methods: {
    printBarcode() {
      console.log("click, printBarcode()...", this.barcode_data);
      this.$emit('pressPrint', true);    
    },

    startTimer() {
      this.myTimer = setInterval(() => {
        let elem = document.querySelector('#layout');
        if(!elem) return;
        let myPos=elem.getBoundingClientRect().top;
        //console.log('calling handleScroll: ', myPos);
        this.fab = myPos <= 10;
      }, 500);

      this.myTimerId = this.myTimer._id;
    },

    onScroll (e) {      
      //if (typeof window === 'undefined') return
      //const top = window.pageYOffset || e.target.scrollTop || 0
      //this.fab = top > 20
    },

    toTop () {
      //this.$vuetify.goTo(0)    
      document.getElementById("layout").scrollIntoView();
    },
  },
}
</script>

<style scoped>

</style>