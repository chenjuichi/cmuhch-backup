<template> 
<div id="app">
  <router-view/>
</div>
</template>
 
<script>
export default {
  name: 'Menu',
  data() {
    return {

    };
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
</style>