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
            <p class="text-muted">
              {{ ad.phone }} -
              <relative-time :datetime="ad.datetime"></relative-time>
            </p>
          </div>
          <user-reactions></user-reactions>
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
import UserReactions from "./UserReactions";
import RelativeTime from "./RelativeTime";

export default {
  name: "AdListElement",
  props: ["ad"],
  components: {
    UserReactions,
    RelativeTime
  },
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
