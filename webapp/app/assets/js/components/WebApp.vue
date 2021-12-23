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
      <div v-show="isActive('apps')"><app-list/></div>
      <div v-show="isActive('domains')"><domain-list/></div>
    </div>
</main>
</template>

<script>
import AppList from "./AppList.vue";
import DomainList from "./DomainList.vue";

export default {
  name: "WebApp",
  components: {DomainList, AppList},
  data() {
    return {
      runningRequests: 0,
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
      }
    }
  },
  methods: {
    switchView(viewKey, event) {
      this.activeView = viewKey;
      history.pushState({}, this.views[viewKey].name, viewKey);
      event.preventDefault();
    },
    isLoadingData() {
      return this.runningRequests > 0;
    },
    activeClass(viewKey) {
      return this.isActive(viewKey) ? 'active' : '';
    },
    isActive(viewKey) {
      return viewKey === this.activeView;
    }
  }
}
</script>

<style scoped>

</style>