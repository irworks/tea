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
      <td>{{ domain.used_in_apps }}</td>
      <td><button class="btn btn-primary">Details</button></td>
    </tr>
    </tbody>
  </table>
  <nav aria-label="Domains navigation">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{disabled: firstPage}"><a class="page-link" href="#" @click="prevPage">Previous</a></li>
      <li class="page-item" v-for="(val, offset) in pagesAround" :class="{active: offset === pagesAround / 2}">
        <a v-if="showPage(offset)" class="page-link" href="#" @click="fetchDomains(pageOffset(offset))">
          {{ pageOffset(offset) }}
        </a>
      </li>
      <li class="page-item" :class="{disabled: finalPage}"><a class="page-link" href="#" @click="nextPage">Next</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "DomainList",
  data() {
    return {
      initialLoadComplete: false,
      pagesAround: 10,
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
    pageRange: function () {
      return Math.min(this.pagination.pages - this.pagination.page, this.pagesAround);
    },
    firstPage: function () {
      return this.pagination.page <= 1;
    },
    finalPage: function () {
      return this.pagination.page === this.pagination.pages;
    }
  },
  methods: {
    showPage(offset) {
      return this.pageOffset(offset) > 0 && this.pageOffset(offset) <= this.pagination.pages;
    },
    pageOffset(offset) {
      return (this.pagination.page + offset) - this.pagesAround / 2;
    },
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