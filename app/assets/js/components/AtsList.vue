<template>
  <h2>ATS Exception Overview</h2>
  <p>
    Here you can find an overview over all checked <a
      href="https://developer.apple.com/documentation/security/preventing_insecure_network_connections" target="_blank">App
    Transport Security (ATS)</a> exceptions including their assigned score, classification, description
    and a direct link to the Apple Developer Documentation.
  </p>
  <table class="table table-responsive">
    <thead>
    <tr>
      <th scope="col">Exception</th>
      <th scope="col">State</th>
      <th scope="col">Description</th>
      <th scope="col">Score</th>
      <th scope="col">Details</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="atsException in atsExceptions">
      <th scope="row">{{ atsException.key }}</th>
      <td>
        <span class="badge rounded-pill" :class="stateClasses(atsException.state)">
          {{ atsException.state }}
        </span>
      </td>
      <td><small>{{ atsException.description }}</small></td>
      <td>{{ atsException.score }}</td>
      <td><a class="btn btn-primary" :href="atsException.documentation_url" target="_blank">Details</a></td>
    </tr>
    </tbody>
  </table>
</template>

<script>
import ApiMixin from "./ApiMixin.js";
import ClassificationMixin from "./ClassificationMixin.js";

export default {
  name: "AppList",
  mixins: [ApiMixin, ClassificationMixin],
  props: ['atsExceptions'],
  data() {
    return {
    }
  },
  computed: {
  },
  methods: {
  },
  created() {
  },
}
</script>

<style scoped>

</style>
