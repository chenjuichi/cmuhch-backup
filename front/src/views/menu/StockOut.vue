<template>
  <v-app>
    <v-card 
      class="overflow-hidden mx-auto mt-3" 
      width="60vw"
    >
      <v-toolbar flat color="blue">
        <v-row style="margin-bottom: -36px; margin-top: -12x;">
        <v-col      
          <!--<v-toolbar-title></v-toolbar-title>-->
        </v-col>
        <v-col>       
          <v-text-field                            
            v-model="stockOutTag_reagID"
            label="資材碼"
            :value="stockOutTag_reagID"
          ></v-text-field>   
        </v-col>
        <v-col> 
          <v-btn icon>
            <v-icon>mdi-heart</v-icon>
          </v-btn>

          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </v-col>
        </v-row> 
      </v-toolbar>
      <v-sheet
        id="scrolling-techniques-7"
        class="overflow-y-auto"
        max-height="600"
      >
        <v-container>      
          <v-card-text>
          <v-list two-line>
            <v-list-item-group
              v-model="selected"
              active-class="pink--text"
              multiple
            >
              <!--<template v-for="(item, index) in items">-->
                <!--<v-list-item :key="item.stockOutTag_reagName">-->
              <template v-for="(item, index) in filteredItems">
                <v-list-item :key="item.stockOutTag_reagID">
                  <template v-slot:default="{ active }">
                    <v-list-item-content>
                      <v-list-item-title class="font-weight-bold" v-text="`品名:${item.stockOutTag_reagName}`"></v-list-item-title>
                      <v-list-item-subtitle class="mb-3" v-text="`效期:${item.stockOutTag_reagPeriod}  保存溫度: ${item.stockOutTag_reagTemp}  批號: ${item.stockOutTag_batch}`"></v-list-item-subtitle>

                      <v-list-item-subtitle
                        class="text--primary font-weight-bold"
                        v-text="`入庫人員: ${item.stockOutTag_Employer}  入庫日期: ${item.stockOutTag_Date}`"
                      ></v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                      <!--<v-list-item-action-text v-text="item.stockOutTag_batch"></v-list-item-action-text>-->
                      <img v-show="active" :src="home_url" alt="Loading" style="height: 2.5vw;">

                    </v-list-item-action>
                  </template>
                </v-list-item>

                <v-divider
                  v-if="index < items.length - 1"
                  :key="index"
                ></v-divider>
              </template>
            </v-list-item-group>
          </v-list>
          </v-card-text>    
        </v-container> 
      </v-sheet>
    </v-card>    
   </v-app>
</template>

<script>
import logo from '../../assets/image/icons8-light-on.gif'
import _ from 'lodash'

export default {
  name: 'StockOut',

  data: () => ({
    home_url: logo,

    stockOutTag_reagID: '',

    grids: [],

    selected: [2],
    items: [
      {
        //id: 1,
        stockOutTag_reagID: '123456789',
        stockOutTag_reagName: 'ABC',
        stockOutTag_reagPeriod: '111/10/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400066',
        stockOutTag_cnt: 4,
        active: false,
      },
      {
        //id: 2,
        stockOutTag_reagID: '234567891',
        stockOutTag_reagName: 'ABCD',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345C123400055',
        stockOutTag_cnt: 2,
        active: false,
      },
      {
        //id: 3,
        stockOutTag_reagID: '234567892',
        stockOutTag_reagName: 'A11',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400033',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 4,
        stockOutTag_reagID: '234567893',
        stockOutTag_reagName: 'A12',
        stockOutTag_reagPeriod: '112/6/30',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400033',
        stockOutTag_cnt: 1,
        active: false,
      },
      {
        //id: 5,
        stockOutTag_reagID: '234567894',
        stockOutTag_reagName: 'B2233',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400022',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 6,
        stockOutTag_reagID: '234567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 1,
        active: false,
      },
      {
        //id: 7,
        stockOutTag_reagID: '234567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 8,
        stockOutTag_reagID: '234567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 5,
        active: false,
      },
      {
        //id: 9,
        stockOutTag_reagID: '214567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 10,
        stockOutTag_reagID: '214567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 2,
        active: false,
      },
      {
        //id: 11,
        stockOutTag_reagID: '214567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 12,
        stockOutTag_reagID: '224567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 20,
        active: false,
      },
      {
        //id: 13,
        stockOutTag_reagID: '224567898',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 14,
        stockOutTag_reagID: '224567899',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
      },
    ],
  }),

  computed: {
    filteredItems() {
    //透過filter()函式的第一參數, callback函式所指定的過濾條件，返回一個新陣列
    //透過includes(), 回傳是否包含該元素的 Boolean 值，true 代表包含，false 則代表不包含
      let temp_array=[];
      temp_array=
             _.orderBy(this.items.filter(item => {
              return item.stockOutTag_reagID.toLowerCase().includes(this.stockOutTag_reagID.toLowerCase());
            }), 'stockOutTag_reagID');
      console.log("filter: ", temp_array)
      return temp_array;

    },
  },

  created () {

    this.initialize();

    this.addGrids();
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
      this.grids = [
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
        {
          //id: 7,
          grid_reagID: '234567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 6,
        },
        {
          //id: 8,
          grid_reagID: '234567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 3,
          grid_pos: 6,
        },
        {
          //id: 9,
          grid_reagID: '214567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 4,
          grid_pos: 6,
        },
        {
          //id: 10,
          grid_reagID: '214567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 6,
        },
        {
          //id: 11,
          grid_reagID: '214567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 7,
        },
        {
          //id: 13,
          grid_reagID: '224567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 14,
          grid_reagID: '224567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 15,
          grid_reagID: '224567899',
          grid_reagName: 'B3344',
          grid_station: 1,
          grid_layout: 5,
          grid_pos: 8,
        },

      ];    
    },

    toggle(index) {
      const i = this.selected.indexOf(index)

      if (i > -1) {
          this.selected.splice(i, 1)
      } else {
          this.selected.push(index)
      }
    },

    addGrids() {
      for (let i = 0; i < this.items.length; i++) {
        let obj = this.grids.find(o => o.grid_reagID === this.items[i].stockOutTag_reagID)
        if (typeof(obj) !== 'undefined') {
          this.items[i].grid_station=obj.grid_station;
          this.items[i].grid_layout=obj.grid_layout;
          this.items[i].grid_pos=obj.grid_pos;
        }
      };
      console.log("find: ", this.items);
    },
  },
}
</script>

<style lang="scss" scoped>

html {
  overflow: hidden !important;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

.v-card.on-hover.theme--dark {
  background-color: rgba(255, 255, 255, 0.8);  
}

.v-card.on-hover.theme--dark > .v-card__text {
    color: #000;      
}
</style>