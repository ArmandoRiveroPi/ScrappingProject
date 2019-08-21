<template>
  <div class="ads-page">
    <h1>Anuncios</h1>
    <ads-list></ads-list>
  </div>
</template>

<script>
import AdsList from "../AdsList";

export default {
  name: "PageAds",
  components: {
    AdsList
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.ads-page {
  margin-top: 80px;
}
h1 {
  text-align: left;
  margin-left: 30px;
}
</style>
