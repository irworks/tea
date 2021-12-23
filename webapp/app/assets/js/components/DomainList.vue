<template>
  <h2>All Domains</h2>
  <table class="table">
    <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Domain</th>
      <th scope="col">Used in Apps</th>
      <th scope="col">Details</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="domain in domains">
      <th scope="row">{{ domain.id }}</th>
      <td>{{ domain.name }}</td>
      <td>{{ -1 }}</td>
      <td><button class="btn btn-primary">Details</button></td>
    </tr>
    </tbody>
  </table>
  <nav aria-label="Page navigation example">
    <ul class="pagination">
      <li class="page-item" v-show="!firstPage"><a class="page-link" href="#" @click="prevPage">Previous</a></li>
      <li class="page-item" v-show="!finalPage"><a class="page-link" href="#" @click="nextPage">Next</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "DomainList",
  data() {
    return {
      initialLoadComplete: false,
      domains: {},
      pagination: {
        'page': 1,
        'pages': 1,
        'per_page': 25,
        'total': 0
      },
      currentDomain: null
    }
  },
  computed: {
    firstPage: function () {
      return this.pagination.page <= 1;
    },
    finalPage: function () {
      return this.pagination.page === this.pages;
    }
  },
  methods: {
    nextPage() {
      this.fetchDomains(this.pagination.page + 1);
    },
    prevPage() {
      this.fetchDomains(this.pagination.page - 1);
    },
    fetchDomains(page) {
      this.fetchData(`/api/domains/paginate/${page}`).then((data) => {
        this.domains = data.domains;
        this.pagination = data.pagination;
      });
    },
    fetchData(url) {
      // TODO: Generalize!
      return fetch(url)
          .then(response => {
            return response.json();
          }).catch(error => {
            console.log(error);
          });
    }
  },
  mounted() {
    this.fetchDomains(1);
  }
}
</script>

<style scoped>

</style>