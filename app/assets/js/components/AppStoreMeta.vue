<template>
  <div>

    <div v-if="hasResults" class="card mb-3" style="max-width: 540px;">
      <div class="row g-0">
        <div class="col-md-3">
          <img :src="results['artworkUrl512']" alt="App icon" class="img-fluid rounded-start">
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ results['trackName'] }}</h5>
            <p class="card-text mb-1"><small class="text-muted">Developed by <b>{{ results['sellerName'] }}</b></small>
            </p>
            <a :href="appStoreUrl"><img src="/static/img/Download_on_the_App_Store_Badge.svg"
                                           alt="AppStore Download badge"></a>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import ApiMixin from "./ApiMixin.js";
export default {
  name: "AppStoreMeta",
  mixins: [ApiMixin],
  props: ['bundle_id'],
  data() {
    return {
      results: {}
    }
  },
  computed: {
    hasResults: function () {
      return this.results && this.results.hasOwnProperty('trackId');
    },
    appStoreUrl: function () {
      return `itms://itunes.apple.com/app/apple-store/id${this.results['trackId']}`
    }
  },
  methods: {
    fetchAppStoreMeta: function () {
      this.fetchData(`https://itunes.apple.com/lookup?bundleId=${this.bundle_id}`).then((data) => {
        if (!data.hasOwnProperty('resultCount') || data['resultCount'] < 1 || !data.hasOwnProperty('results')) {
          return;
        }

        this.results = data['results'][0];
      });
    }
  },
  mounted() {
    this.fetchAppStoreMeta();
  },
}
</script>

<style scoped>

</style>