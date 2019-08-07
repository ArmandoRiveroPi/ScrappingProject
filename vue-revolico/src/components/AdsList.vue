<template>
  <div class="ads-list">
    <div v-for="ad in ads" :key="ad.title">
      <h2>{{ad.title}}</h2>
      <p>{{ad.content}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdsList"
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
