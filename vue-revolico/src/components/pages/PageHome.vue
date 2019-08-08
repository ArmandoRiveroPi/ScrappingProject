<template>
  <div class="home-page">
    <h1>Negociantes</h1>
    <bperson-list></bperson-list>
  </div>
</template>

<script>
import BpersonList from "../BpersonList";

export default {
  name: "PageHome",
  components: {
    BpersonList
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  text-align: left;
  margin-left: 30px;
}
</style>
