<template>
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
            <td :class="paddingClasses(atsException)"><small>{{ "atsException.description" }}</small></td>
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
export default {
  name: "App",
  components: {},
  props: ['id', 'name', 'bundle_id', 'binary', 'version', 'build', 'sdk', 'min_os', 'domains', 'ats'],
  data() {
    return {}
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
  },
  computed: {},
  mounted() {

  },
}
</script>

<style scoped>

</style>
