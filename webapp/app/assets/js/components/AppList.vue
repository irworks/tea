<template>
  <div v-if="isLoadingData" class="alert alert-info shadow-sm position-fixed start-0 bottom-0 w-100 fixed-bottom">
    <i class="spinner-border spinner-border-sm" role="status"></i> <span class="ms-2">Loading data...</span>
  </div>

  <app v-if="currentApp" v-bind="currentApp" v-on:close="deselectApp"></app>

  <div class="overall-stats" v-if="initialLoadComplete">
    <h2>Overview</h2>
    <div class="chart-wrapper w-25 mb-2">
      <PieChart :chartData="chartData"/>
    </div>
    <p>Analyzed <b>{{ count }}</b> apps. Of those <b>{{ countAppsWithAts }}</b> have ATS exceptions.</p>

    <hr>
  </div>

  <h2>App results</h2>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
      <th scope="col">Version</th>
      <th scope="col">iOS</th>
      <th scope="col">ATS Exceptions <span @click="sort('ats')">{{ icon('ats') }}</span></th>
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
      <td><button class="btn btn-primary" @click="selectApp(app)">Details</button></td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import App from "./App.vue";
import {PieChart} from "vue-chart-3";
import {ArcElement, Chart, PieController, Tooltip} from "chart.js";
import ApiMixin from "./ApiMixin.js";
import {UrlHelper} from "./UrlHelper";

export default {
  name: "AppList",
  components: {PieChart, App},
  mixins: [ApiMixin],
  data() {
    return {
      initialLoadComplete: false,
      atsExceptions: {},
      apps: {},
      currentApp: null,
      sortOrder: {
        'ats': true,
        'urls': true
      },
      count: 0,
      countAppsWithAts: 0,
    }
  },
  computed: {
    chartData: function () {
      return {
        labels: ["Apps without ATS exceptions", "Apps with ATS exceptions"],
        datasets: [
          {
            label: "Data One",
            backgroundColor: ["#41B883", "#E46651"],
            data: [this.count - this.countAppsWithAts, this.countAppsWithAts]
          }
        ]
      }
    },
  },
  methods: {
    selectApp(app) {
      this.fetchAppDetails(app.id).then((data) => {
        let appModel = {};
        Object.assign(appModel, app);
        this.assignAppModel(appModel, data);
      });
      window.scrollTo(0,0);
      UrlHelper.setParameter('app', app.id);
    },
    assignAppModel(appModel, data) {
      appModel.domains = data.domains;

        let appAts = [];
        for (const atsAppEx of data.ats_exceptions) {
          const atsEx = this.atsExceptions[atsAppEx.exception_id];

          appAts.push({
            status: atsEx.state,
            key: atsEx.key,
            domain: atsAppEx.domain,
            parent: atsEx.parent_id,
            description: atsEx.description,
            documentation_url: atsEx.documentation_url
          });
        }

        appModel.ats = appAts;
        this.currentApp = appModel;
    },
    deselectApp() {
      this.currentApp = null;
      UrlHelper.setParameter('app', '');
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
      this.fetchData('/api/exceptions/ats').then((data) => {
        for (const i in data) {
          this.atsExceptions[data[i].id] = data[i];
        }
      });
    },
    fetchApps() {
      this.fetchData('/api/apps').then((data) => {
        this.apps = data.apps;

        this.countAppsWithAts = data.ats_apps_count;
        this.count = this.apps.length;
        this.initialLoadComplete = true;
      });
    },
    fetchAppDetails(appId) {
      return this.fetchData(`/api/apps/${appId}`);
    },
  },
  created() {
    Chart.register(PieController, ArcElement, Tooltip);

    this.fetchAtsExceptions();
    this.fetchApps();

    let appId = UrlHelper.getParameter('app', -1);
    if (appId > 0) {
      this.fetchAppDetails(appId).then((data) => {
        this.assignAppModel(data.app, data);
      });
    }
  },
}
</script>

<style scoped>

</style>
