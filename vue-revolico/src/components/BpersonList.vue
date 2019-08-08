<template>
  <div class="b-person-list">
    <bperson-list-element v-for="bperson in bpersons" :key="bperson.name" :bperson="bperson"></bperson-list-element>
    <div class="clearfix"></div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import BpersonListElement from "./BpersonListElement";

export default {
  name: "BpersonList",
  data() {
    return {
      bpersons: []
    };
  },
  components: {
    BpersonListElement
  },

  computed: {
    ...mapState(["restApi"])
  },
  methods: {
    getBPersonsData() {
      return this.restApi.getData("bpersons/");
    }
  },
  mounted() {
    this.getBPersonsData().then(result => {
      this.bpersons = result;
    });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
