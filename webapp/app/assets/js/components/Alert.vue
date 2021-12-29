<template>
  <div id="exampleModal" class="modal fade show d-block" tabindex="-1" role="dialog" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title"><slot name="header">{{ title }}</slot></h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="emitClose"></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <slot name="footer"></slot>
          <button @click="emitClose" type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Alert",
  components: {},
  props: ['title'],
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
