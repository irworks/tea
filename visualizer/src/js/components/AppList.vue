<template>
  <p>Loaded <b>{{ count }}</b> apps.</p>

  <app v-if="currentApp" v-bind="currentApp"></app>

  <table class="table">
    <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
      <th scope="col">Version</th>
      <th scope="col">iOS</th>
      <th scope="col">ATS Exceptions <span @click="sort('ats')">{{ icon('ats') }}</span></th>
      <th scope="col">URLs <span @click="sort('urls')">{{ icon('urls') }}</span></th>
      <th scope="col">Details</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(app, index) in apps">
      <th scope="row">{{ index }}</th>
      <td>{{ app.name }}</td>
      <td>{{ app.version }} ({{ app.build }})</td>
      <td>iOS {{ app.min_os }}+</td>
      <td>{{ app.ats.length }}</td>
      <td>{{ app.urls.length }}</td>
      <td><button class="btn btn-primary" @click="selectApp(app)">Details</button></td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import App from "./App.vue";

export default {
  name: "AppList",
  components: {App},
  data() {
    return {
      apps: {},
      currentApp: null,
      sortOrder: {
        'ats': true,
        'urls': true
      },
      count: 0
    }
  },
  methods: {
    selectApp(app) {
      this.currentApp = app;
      window.scrollTo(0,0);
    },
    icon(field) {
      if (!this.sortOrder.hasOwnProperty(field)) {
        return '';
      }

      return this.sortOrder[field] ? '⬆️' : '⬇️';
    },
    sort(field) {
      this.sortOrder[field] = !this.sortOrder[field];
      let up = this.sortOrder[field];

      this.apps.sort((a, b) => {
        if (up) {
          return a[field].length > b[field].length;
        }

        return a[field].length < b[field].length;
      });
    },
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
