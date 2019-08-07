<template>
  <div class="b-person-list">
    <div v-for="bperson in bpersons" :key="bperson.name">
      <h2>{{bperson.name}}</h2>
      <p>{{bperson.phone}}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "BPersonList"
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
