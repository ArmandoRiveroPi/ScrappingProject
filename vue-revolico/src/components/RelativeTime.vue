<template>
  <span class="relative-date">{{ timeString }}</span>
</template>

<script>
import TimeAgo from "javascript-time-ago";
import es from "javascript-time-ago/locale/es";
TimeAgo.addLocale(es);

export default {
  name: "RelativeDate",
  props: ["datetime"],
  computed: {
    timeString() {
      let formatter = new TimeAgo("es-US");
      let time = new Date(this.datetime);
      let tString = formatter.format(time);
      return tString;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
