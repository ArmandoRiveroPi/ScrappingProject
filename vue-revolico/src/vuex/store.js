import Vue from "vue";
import Vuex from "vuex";
import RestApi from "../classes/RestApi";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    // eslint-disable-next-line no-undef
    restApi: new RestApi(
      "http://localhost:8000/api/v1/"
    ) /* the vueData comes from wp_localize */
  },

  mutations: {},

  getters: {}
});
