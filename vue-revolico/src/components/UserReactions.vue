<template>
  <div class="reaction">
    <!-- <a class="btn text-green" @click="vote_up">
      <i class="icon ion-thumbsup"></i>
      {{votesUp}}
    </a>
    <a class="btn text-red" @click="vote_down">
      <i class="fa fa-thumbs-down"></i>
      {{ votesDown }}
    </a>-->
  </div>
</template>

<script>
export default {
  name: "UserReactions",
  data() {
    return {
      votesUp: 0,
      votesDown: 0
    };
  },
  methods: {
    vote_up() {
      this.votesUp++;
    },
    vote_down() {
      this.votesDown++;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
