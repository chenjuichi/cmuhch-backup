<template>
    <p class="text_style">
      格位:{{myText.id}}
    </p>
</template>
<script type="station1">
export default {
  name: 'TempText',

  props: ['myText'],

  mounted() {
    this.$emit('closeTempText');
  },
  created() {
    //this.size++
    console.log("TempText...", this.myText);
    //this.buf.push(this.myText);
    //let temp_size= myText.size * 29;
    //document.documentElement.style.setProperty("--wd", temp_size + 'px');
    //let new_ledMessage = this.$el.querySelector("#temp_text_" + this.myText.id);
    //console.log("TempText component, ", this.myText.id, new_ledMessage);
  },

  data() {
    return {
      //hover: false,
      //buf: [],
      //size: 0,
    };
  },

  //beforeDestroy() {
  //  console.log('Hook: beforeDestroy');
  //},
}
</script>

<style scoped>
  @import url(
    'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
  );

  p {
    /*margin: 0;*/
    font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
    font-size:10px;
    font-weight:600;
  }

  .text_style {
    width: 42px;
    text-align:center;
    display: table-cell;
    vertical-align: middle;
  }

</style>