<template>
  <div @mouseover="onOver" @mouseleave="onLeave">
      <b-dropdown id="dropdown-1" text="Dropdown Button" ref="dropdown" class="m-md-2">
         <b-dropdown-item>First Action</b-dropdown-item>
         <b-dropdown-item>Second Action</b-dropdown-item>
         <b-dropdown-item>Third Action</b-dropdown-item>
      </b-dropdown>
  </div>
</template>

<style>
  body { padding: 1rem; }
</style>

<script>
  export default {
      methods: {
        onOver() {
          this.$refs.dropdown.visible = true;
        },
        onLeave() {
          this.$refs.dropdown.visible = false;
        }
      }
  }
</script>