<template>
  <p>Loaded <b>{{ count }}</b> apps.</p>
</template>

<script>
export default {
  name: "AppList",
  components: {},
  data() {
    return {
      apps: {},
      count: 0
    }
  },
  methods: {
    fetchApps() {
      this.loadJsonResults((response) => {
        // Parse JSON string into object
        this.apps = JSON.parse(response);
        this.count = this.apps.length;
      });
    },
    loadJsonResults(callback) {
      const request = new XMLHttpRequest();
      request.overrideMimeType('application/json');
      request.open('GET', '../../tlsanalyzer/results.json', true);
      request.onreadystatechange = function () {
        if (request.readyState === 4 && request.status === 200) {
          callback(request.responseText);
        }
      };
      request.send(null);
    }
  },
  created() {
    this.fetchApps();
  },
}
</script>

<style scoped>

</style>
