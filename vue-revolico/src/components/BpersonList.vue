<template>
  <div>
    <div class="bperson-list">
      <bperson-list-element
        v-for="bperson in bpersons"
        :key="bperson.bperson_id"
        :bperson="bperson"
      ></bperson-list-element>
      <div class="clearfix"></div>
    </div>
    <div
      class="infinite-scroll"
      v-infinite-scroll="loadInfinite"
      infinite-scroll-disabled="busy"
      infinite-scroll-distance="10"
    ></div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import BpersonListElement from "./BpersonListElement";

export default {
  name: "BpersonList",
  data() {
    return {
      bpersons: [],
      page: 1,
      busy: false
    };
  },

  components: {
    BpersonListElement
  },

  computed: {
    ...mapState(["restApi"])
  },
  methods: {
    getAdsData() {
      return this.restApi.getData("bpersons/?page=" + this.page);
    },
    loadInfinite() {
      this.busy = true;
      this.page++;
      setTimeout(() => {
        this.getAdsData().then(result => {
          this.bpersons = this.bpersons.concat(result.results);
        });
        this.busy = false;
      }, 1000);
    }
  },
  mounted() {
    this.getAdsData().then(result => {
      this.bpersons = result.results;
    });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bperson-list {
  text-align: left;
}
</style>
