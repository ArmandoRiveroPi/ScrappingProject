<template>
  <header id="header">
    <nav class="navbar navbar-default navbar-fixed-top menu">
      <div class="container">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button
            type="button"
            class="navbar-toggle collapsed"
            data-toggle="collapse"
            data-target="#bs-example-navbar-collapse-1"
            aria-expanded="false"
          >
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <router-link to="/">
            <img src="/assets/images/logo.png" alt="logo" />
          </router-link>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav navbar-right main-menu">
            <li class="dropdown">
              <router-link to="/">Negociantes</router-link>
            </li>
            <li class="dropdown">
              <router-link to="/anuncios/">Anuncios</router-link>
            </li>
          </ul>
          <form class="navbar-form navbar-right hidden-sm">
            <div class="form-group">
              <i class="icon ion-android-search"></i>
              <input type="text" class="form-control" placeholder="Buscar negociantes y anuncios" />
            </div>
          </form>
        </div>
        <!-- /.navbar-collapse -->
      </div>
      <!-- /.container -->
    </nav>
  </header>
</template>

<script>
export default {
  name: "VueHeader"
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#header {
  min-height: 0;
}
.navbar {
  min-height: 0;
  margin-top: 0;
}
#header > nav > div > div.navbar-header > a > img {
  margin-top: 8px;
}
</style>
