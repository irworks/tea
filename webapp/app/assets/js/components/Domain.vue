<template>
  <div class="card">
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
          Apps
        </div>
        <table class="table">
          <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">ATS Exceptions</th>
            <th scope="col">Details</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="app in apps">
            <td>{{ app.name }}</td>
            <td>{{ 'TODO' }}</td>
            <td>{{ 'TODO' }}</td>
          </tr>
          </tbody>
        </table>

        <div class="card">
          <div class="card-header">
            ATS Exceptions
          </div>
          <ul>
            <li v-for="ats in ats_exceptions">
              {{ ats }}
            </li>
          </ul>
        </div>
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
