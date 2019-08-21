<template>
  <div>
    <div class="ads-list">
      <ad-list-element v-for="ad in ads" :key="ad.ad_id" :ad="ad"></ad-list-element>
      <div class="clearfix"></div>
    </div>
    <div
      class="infinite-scroll"
      v-infinite-scroll="loadInfinite"
      infinite-scroll-disabled="busy"
      infinite-scroll-distance="10"
    >
      <div v-if="busy" class="loading-signal">
        <i class="fa fa-spinner fa-pulse fa-4x"></i>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import AdListElement from "./AdListElement";

export default {
  name: "AdsList",
  data() {
    return {
      ads: [],
      page: 1,
      busy: false,
      limit: 1000
    };
  },

  components: {
    AdListElement
  },

  computed: {
    ...mapState(["restApi"])
  },
  methods: {
    getAdsData() {
      return this.restApi.getData("ads/?page=" + this.page);
    },
    loadInfinite() {
      // Only update under certain amount of elements (limit)
      if (this.ads.length < this.limit) {
        this.busy = true;
        this.page++;
        setTimeout(() => {
          this.getAdsData().then(result => {
            this.ads = this.ads.concat(result.results);
          });
          this.busy = false;
        }, 1000);
      }
    }
  },
  mounted() {
    // this.getAdsData().then(result => {
    //   this.ads = result.results;
    // });
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.ads-list {
  text-align: left;
}
</style>
