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
      ats_exceptions: {},
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
      this.fetchAppDetails(app.id).then((data) => {
        let appModel = {};
        Object.assign(appModel, app);
        appModel.domains = data.domains;

        let appAts = [];
        for (const atsAppEx of data.ats_exceptions) {
          const atsEx = this.ats_exceptions[atsAppEx.exception_id];

          appAts.push({
            status: atsEx.state,
            key: atsEx.key,
            domain: atsAppEx.domain_id,
          });
        }

        appModel.ats = appAts;
        this.currentApp = appModel;
      });
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
    fetchAtsExceptions() {
      fetch('/api/exceptions/ats').then((response) => {
        response.json().then((data) => {
          for (const i in data) {
            this.ats_exceptions[data[i].id] = data[i];
          }
        });
      });
    },
    fetchApps() {
      fetch('/api/apps').then((response) => {
        response.json().then((data) => {
          this.apps = data;
          this.count = this.apps.length;
        });
      });
    },
    fetchAppDetails(appId) {
      return fetch(`/api/apps/${appId}`).then(response => {
        return response.json();
      });
    },
  },
  created() {
    this.fetchAtsExceptions();
    this.fetchApps();
  },
}
</script>

<style scoped>

</style>
