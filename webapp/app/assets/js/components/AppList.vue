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
      <th scope="row">{{ app.id }}</th>
      <td>{{ app.name }}</td>
      <td>{{ app.version }} ({{ app.build }})</td>
      <td>iOS {{ app.min_ios }}+</td>
      <td>{{ app.ats }}</td>
      <td>{{ 0 }}</td>
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
          return a[field] > b[field];
        }

        return a[field] < b[field];
      });
    },
    fetchApps() {
      console.log('Fetching apps...');
      fetch('/api/apps').then((response) => {
        response.json().then((data) => {
          this.apps = data;
          this.count = this.apps.length;
        });
      });
    },
  },
  created() {
    this.fetchApps();
  },
}
</script>

<style scoped>

</style>
