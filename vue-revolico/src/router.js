/* eslint-disable no-unused-vars */
import PageHome from "./components/pages/PageHome";
import PageAds from "./components/pages/PageAds";
import VueRouter from "vue-router";

const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      component: PageHome
    },
    {
      path: "/anuncios",
      component: PageAds
    }
  ]
});

export default router;
