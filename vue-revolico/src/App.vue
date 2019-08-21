<template>
  <div id="app">
    <vue-header></vue-header>
    <router-view></router-view>
    <vue-footer></vue-footer>
    <back-to-top bottom="50px" right="50px">
      <button type="button" class="btn btn-info btn-to-top">
        <i class="fa fa-chevron-up"></i>
      </button>
    </back-to-top>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import VueHeader from "./components/VueHeader";
import VueFooter from "./components/VueFooter";
import { mapState } from "vuex";

export default {
  name: "app",
  components: {
    VueHeader,
    VueFooter
  },
  data() {
    return {
      ads: [],
      bpersons: []
    };
  },
  computed: {
    ...mapState(["restApi"])
  }
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
