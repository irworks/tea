<template>
  <div class="card">
    <div class="card-header"><h2>{{ name }}</h2></div>
    <div class="card-body">
      <p><b>Bundle Id:</b> {{bundle_identifier}}</p>
      <p><b>Version:</b> {{version}} ({{build}})</p>
      <p><b>SDK:</b> {{sdk}}</p>
      <p><b>Bundle Id:</b> {{bundle_identifier}}</p>

      <div class="card">
        <div class="card-header">
          ATS Exceptions
        </div>
        <table class="table">
          <thead>
          <tr>
            <th scope="col">State</th>
            <th scope="col">Issue</th>
            <th scope="col">Details</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="atsException in ats">
            <td class="text-center">
              <span class="badge rounded-pill" :class="stateClasses(atsException.status)">
                {{atsException.status }}
              </span></td>
            <td>{{ atsException.issue }}</td>
            <td><small>{{ atsException.description }}</small></td>
          </tr>
          </tbody>
        </table>

        <div class="card">
          <div class="card-header">
            URLs
          </div>
          <ul>
            <li v-for="url in urls.slice(0, 100)">
              {{ url }}
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
  props: ['name', 'bundle_identifier', 'binary', 'version', 'build', 'sdk', 'min_os', 'ats', 'urls'],
  data() {
    return {
      app: {}
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
  },
  computed: {
  },
  created() {
    console.log('App!')
  },
}
</script>

<style scoped>

</style>
