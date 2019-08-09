<template>
  <div class="bperson-element col-md-7" v-if="bperson.name">
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
              <a href="timeline.html" class="profile-link">{{ bperson.name }}</a>
              <span class="following">following</span>
            </h5>
            <p class="text-muted">Published a photo about 3 mins ago</p>
          </div>
          <user-reactions></user-reactions>
          <div class="line-divider"></div>
          <div class="post-text">
            <p>{{ bperson.phone }}</p>
          </div>
          <div class="line-divider"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserReactions from "./UserReactions";

export default {
  name: "BpersonListElement",
  props: ["bperson"],
  components: {
    UserReactions
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bperson-element {
  margin-left: auto;
  margin-right: auto;
}
</style>
