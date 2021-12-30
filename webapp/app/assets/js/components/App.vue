<template>
  <alert v-if="shouldShowAtsDetails" v-on:close="shouldShowAtsDetails = false" :title="currentAtsException.key">
    <template v-slot:header>
      {{ currentAtsException.key }}

      <small>
      <span class="badge rounded-pill" :class="stateClasses(currentAtsException.status)">
         {{ currentAtsException.status }}
       </span>
      </small>
    </template>

     <template v-slot:default>
       {{ currentAtsException.description }}
     </template>

    <template v-slot:footer>
      <a :href="currentAtsException.documentation_url" target="_blank" class="btn btn-primary"> Documentation</a>
     </template>
  </alert>

  <div v-if="shouldShowAtsDetails" class="modal-backdrop show"></div>

  <div class="card shadow shadow-sm">
    <div class="card-header">
      <h2 class="float-start">{{ name }}</h2>
      <button type="button" class="btn-close float-end" data-bs-dismiss="modal" aria-label="Close" @click="emitClose"></button>
    </div>
    <div class="card-body">
      <p><b>Bundle Id:</b> {{ bundle_id }}</p>
      <p><b>Version:</b> {{ version }} ({{ build }})</p>
      <p><b>SDK:</b> {{ sdk }}</p>

      <app-store-meta :bundle_id="bundle_id"></app-store-meta>

      <div class="card">
        <div class="card-header">
          ATS Exceptions
        </div>
        <table class="table" v-if="ats.length > 0">
          <thead>
          <tr>
            <th scope="col">State</th>
            <th scope="col">Issue</th>
            <th scope="col">Domain</th>
            <th scope="col">Details</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="atsException in ats">
            <td :class="paddingClasses(atsException)" class="text-center">
              <span class="badge rounded-pill" :class="stateClasses(atsException.status)">
                {{ atsException.status }}
              </span></td>
            <td :class="paddingClasses(atsException)">{{ atsException.key }}</td>
            <td :class="paddingClasses(atsException)">{{ atsException.domain }}</td>
            <td :class="paddingClasses(atsException)">
              <small>
                <button @click="showAtsDetails(atsException)" class="btn btn-sm btn-secondary">Learn more</button>
            </small></td>
          </tr>
          </tbody>
        </table>
        <b v-else class="text-center mt-2 mb-2">
          No ATS exceptions defined.
        </b>
        </div>

        <div class="card mt-4">
          <div class="card-header">
            Domains
          </div>
          <ul v-if="domains.length > 0">
            <li v-for="domain in domains">
              <a :href="'/domains?domain=' + domain.id" target="_blank">{{ domain.name }}</a>
            </li>
          </ul>
          <b v-else class="text-center mt-2 mb-2">
          No domains found in this app.
        </b>
        </div>
    </div>
  </div>
</template>

<script>
import Alert from "./Alert.vue";
import AppStoreMeta from "./AppStoreMeta.vue";
export default {
  name: "App",
  components: {AppStoreMeta, Alert},
  props: ['id', 'name', 'bundle_id', 'binary', 'version', 'build', 'sdk', 'min_ios', 'domains', 'ats', 'score'],
  emits: ['close'],
  data() {
    return {
      shouldShowAtsDetails: false,
      currentAtsException: {
        key: '',
        description: '',
        status: ''
      },
    }
  },
  methods: {
    stateClasses: function (state) {
      const states = {
        info: 'bg-info text-dark',
        insecure: 'bg-danger',
        warning: 'bg-warning',
        secure: 'bg-success'
      };
      return states[state];
    },
    paddingClasses: function (atsException) {
      if (atsException.parent) {
        return 'ps-5';
      }

      return '';
    },
    showAtsDetails: function(atsException) {
      this.currentAtsException = atsException;
      this.shouldShowAtsDetails = true;
    },
    emitClose: function () {
      this.$emit('close');
    }
  },
  computed: {},
  mounted() {

  },
}
</script>

<style scoped>

</style>
