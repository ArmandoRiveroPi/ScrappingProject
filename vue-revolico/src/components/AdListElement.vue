<template>
  <div class="col-md-7">
    <div class="post-content">
      <div class="post-container">
        <img
          v-if="false"
          src="images/users/user-5.jpg"
          alt="user"
          class="profile-photo-md pull-left"
        />
        <div class="post-detail">
          <div class="user-info">
            <h5>
              <a href="timeline.html" class="profile-link">{{ ad.title }}</a>
              <span class="following"></span>
            </h5>
            <p class="text-muted">{{ ad.phone }} - 3 mins ago</p>
          </div>
          <div class="reaction">
            <a class="btn text-green">
              <i class="icon ion-thumbsup"></i> 13
            </a>
            <a class="btn text-red">
              <i class="fa fa-thumbs-down"></i> 0
            </a>
          </div>
          <div class="line-divider"></div>
          <div class="post-text">
            <p
              class="content-parag"
              v-for="parag in contentParagraphs(ad.content)"
              :key="parag"
            >{{ parag }}</p>
          </div>
          <div class="line-divider"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdListElement",
  props: ["ad"],
  methods: {
    contentParagraphs(content) {
      return content.split("\n");
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.content-parag {
  /* text-align: justify; */
  margin-bottom: 0;
}
</style>
