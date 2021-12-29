<template>
  <alert v-if="shouldShowAtsDetails" v-on:close="shouldShowAtsDetails = false" :title="currentAtsException.key">
    <template v-slot:header>
      {{ currentAtsException.key }}

      <span class="badge rounded-pill" :class="stateClasses(currentAtsException.status)">
         {{ currentAtsException.status }}
       </span>
    </template>

     <template v-slot:default>
       {{ currentAtsException.description }}
     </template>

    <template v-slot:footer>
      <a :href="currentAtsException.documentation_url" target="_blank" class="btn btn-primary"> Documentation</a>
     </template>
  </alert>

  <div v-if="shouldShowAtsDetails" class="modal-backdrop show"></div>

  <div class="card">
    <div class="card-header"><h2>{{ name }}</h2></div>
    <div class="card-body">
      <p><b>Bundle Id:</b> {{ bundle_id }}</p>
      <p><b>Version:</b> {{ version }} ({{ build }})</p>
      <p><b>SDK:</b> {{ sdk }}</p>

      <div class="card">
        <div class="card-header">
          ATS Exceptions
        </div>
        <table class="table">
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

        <div class="card">
          <div class="card-header">
            Domains
          </div>
          <ul>
            <li v-for="domain in domains">
              {{ domain.name }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Alert from "./Alert.vue";
export default {
  name: "App",
  components: {Alert},
  props: ['id', 'name', 'bundle_id', 'binary', 'version', 'build', 'sdk', 'min_ios', 'domains', 'ats'],
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
      console.log(atsException);
      this.shouldShowAtsDetails = true;
    }
  },
  computed: {},
  mounted() {

  },
}
</script>

<style scoped>

</style>
