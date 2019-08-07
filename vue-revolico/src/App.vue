<template>
  <div id="app">
    <div>
      Header
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/anuncios">Anuncios</router-link>
      </nav>
    </div>
    <router-view></router-view>
    <div>Footer</div>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import RestApi from "./classes/RestApi";
export default {
  name: "app",
  components: {
    // VueRouter
  },
  data() {
    return {
      restApi: new RestApi("http://localhost:8000/api/v1/"),
      ads: [],
      bpersons: []
    };
  },
  computed: {
    // ads() {
    //   let ads = this.restApi.getData("ads/");
    //   console.log(ads);
    //   return ads; //this.restApi.getData("ads/");
    // }
  },
  methods: {
    getAdsData() {
      return this.restApi.getData("ads/");
    },
    getBPersonsData() {
      return this.restApi.getData("bpersons/");
    }
  },

  mounted() {
    this.getAdsData().then(result => {
      this.ads = result;
    });
    this.getBPersonsData().then(result => {
      this.bpersons = result;
    });
  }
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.router-link-active {
  margin-right: 10px;
}
</style>
