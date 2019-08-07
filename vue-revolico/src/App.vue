<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/anuncios">Anuncios</router-link>
    </nav>
    <router-view></router-view>
    <div v-for="ad in ads" :key="ad.title">
      <h2>{{ad.title}}</h2>
      <p>{{ad.content}}</p>
    </div>
    <div v-for="bperson in bpersons" :key="bperson.name">
      <h2>{{bperson.name}}</h2>
      <p>{{bperson.phone}}</p>
    </div>
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
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
