<template>
  <nav class="ps-2 navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">tlsanalyzer</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li v-for="view in views" class="nav-item" :class="activeClass(view.key)">
                <a class="nav-link" :href="view.key" @click="switchView(view.key, $event)">{{ view.name }}</a>
            </li>
        </ul>
    </div>
</nav>

<main>
    <div class="container mt-2">
      <div v-show="isActive('apps')"><app-list :ats-exceptions="atsExceptions" :ignored-domains="ignoredDomains"/></div>
      <div v-show="isActive('domains')"><domain-list/></div>
      <div v-show="isActive('ats')"><ats-list :ats-exceptions="atsExceptions"/></div>
    </div>
</main>
</template>

<script>
import AppList from "./AppList.vue";
import DomainList from "./DomainList.vue";
import AtsList from "./AtsList.vue";
import ApiMixin from "./ApiMixin.js";

export default {
  name: "WebApp",
  components: {DomainList, AppList, AtsList},
  mixins: [ApiMixin],
  data() {
    return {
      runningRequests: 0,
      atsExceptions: [],
      ignoredDomains: [],
      activeView: 'apps',
      views: {
        apps: {
          name: 'App Overview',
          key: 'apps'
        },
        domains: {
          name: 'Domain Overview',
          key: 'domains'
        },
        ats: {
          name: 'ATS Overview',
          key: 'ats'
        },
      }
    }
  },
  methods: {
    switchView(viewKey, event) {
      this.activeView = viewKey;
      history.pushState({}, this.views[viewKey].name, viewKey);
      event.preventDefault();
    },
    activeClass(viewKey) {
      return this.isActive(viewKey) ? 'active' : '';
    },
    isActive(viewKey) {
      return viewKey === this.activeView;
    },
    fetchAtsExceptions() {
      this.fetchData('/api/exceptions/ats').then(data => this.atsExceptions = data);
    },
    fetchIgnoredDomains() {
      this.fetchData('/api/domains/ignored').then(data => this.ignoredDomains = data);
    },
  },
  computed: {
    isLoadingData() {
      return this.runningRequests > 0;
    },
  },
  created() {
    this.fetchAtsExceptions();
    this.fetchIgnoredDomains();
  },
  mounted() {
    // after site load -> try to find view
    const path = document.location.pathname.replace('/', '');
    if (this.views.hasOwnProperty(path)) {
      this.activeView = path;
    }
  }
}
</script>