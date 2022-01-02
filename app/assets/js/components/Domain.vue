<template>
  <div class="card shadow shadow-sm">
    <div class="card-header">
      <h2 class="float-start">{{ name }}</h2>
      <button type="button" class="btn-close float-end" data-bs-dismiss="modal" aria-label="Close"
              @click="emitClose"></button>
    </div>

    <div class="card-body">
      <p><b>Appears in Apps:</b> {{ apps.length }}</p>
      <p><b>ATS Exceptions:</b> {{ ats_exceptions.length }}</p>

      <div class="card">
        <div class="card-header">
          ATS Exceptions for <b>{{ name }}</b>
        </div>
        <table class="table" v-if="ats_exceptions.length > 0">
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Bundle Id</th>
            <th scope="col">Exception</th>
            <th scope="col">Details</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="ats in ats_exceptions">
            <td>{{ ats.app.name }}</td>
            <td>{{ ats.app.bundle_id }}</td>
            <td>{{ ats.exception.key }}</td>
            <td><a :href="'/apps?app=' + ats.app.id" class="btn btn-primary">View App details</a></td>
          </tr>
          </tbody>
        </table>
        <b v-else class="text-center mt-2 mb-2">
          No ATS exceptions defined.
        </b>
      </div>

      <div class="card mt-4">
        <div class="card-header">
          Apps containing <b>{{ name }}</b>
        </div>
        <table class="table" v-if="apps.length > 0">
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Bundle Id</th>
            <th scope="col">Details</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="app in apps">
            <td>{{ app.name }}</td>
            <td>{{ app.bundle_id }}</td>
            <td><a :href="'/apps?app=' + app.id" class="btn btn-primary">View App details</a></td>
          </tr>
          </tbody>
        </table>

        <b v-else class="text-center mt-2 mb-2">
          No Apps found with this domain.
        </b>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Domain",
  components: {},
  props: ['id', 'name', 'apps', 'ats_exceptions'],
  emits: ['close'],
  data() {
    return {}
  },
  methods: {
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
