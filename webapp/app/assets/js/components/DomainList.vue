<template>
  <domain v-if="currentDomain" v-bind="currentDomain"></domain>

  <h2>All Domains</h2>
  <p>
    <small>
    You are on page <b>{{ pagination.page }}</b> of <b>{{ pagination.pages }}</b>.
    In total <b>{{ pagination.total }}</b> domains are on record.
  </small>
  </p>

  <table class="table">
    <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Domain</th>
      <th scope="col">Appears in Apps</th>
      <th scope="col">Apps with ATS Exceptions</th>
      <th scope="col">Details</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="domain in domains">
      <th scope="row">{{ domain.id }}</th>
      <td>{{ domain.name }}</td>
      <td>{{ domain.used_in_apps }}</td>
      <td>{{ domain.ats_apps_count }}</td>
      <td>
        <button class="btn btn-primary" @click="fetchDomainDetails(domain.id)">Details</button>
      </td>
    </tr>
    </tbody>
  </table>
  <nav aria-label="Domains navigation">
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{disabled: firstPage}"><a class="page-link" href="#" @click="prevPage">Previous</a>
      </li>
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
import ApiMixin from "./ApiMixin.js";
import PaginationMixin from "./PaginationMixin.js";
import {UrlHelper} from "./UrlHelper.js";
import Domain from "./Domain.vue";

export default {
  name: "DomainList",
  components: {Domain},
  mixins: [ApiMixin, PaginationMixin],
  data() {
    return {
      initialLoadComplete: false,
      domains: {},
      currentDomain: null
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
      UrlHelper.setParameter('page', page);

      this.fetchData(`/api/domains/paginate/${page}`).then((data) => {
        this.domains = data.domains;
        this.pagination = data.pagination;
      });
    },
    fetchDomainDetails(domainId) {
      this.fetchData(`/api/domains/${domainId}`).then((data) => {
        let domainModel = {};
        Object.assign(domainModel, data.domain);
        domainModel.apps = data.apps;
        domainModel.ats_exceptions = data.ats_exceptions;

        this.currentDomain = domainModel;
      });
    },
  },
  mounted() {
    this.pagination.page = UrlHelper.getParameter('page', 1);
    this.fetchDomains(this.pagination.page);
  }
}
</script>

<style scoped>

</style>