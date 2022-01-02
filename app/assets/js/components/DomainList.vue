<template>
    <div v-if="isLoadingData" class="alert alert-info shadow-sm position-fixed start-0 bottom-0 w-100 fixed-bottom">
    <i class="spinner-border spinner-border-sm" role="status"></i> <span class="ms-2">Loading data...</span>
  </div>

  <domain v-if="currentDomain" v-bind="currentDomain" v-on:close="deselectDomain"></domain>

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
      <th scope="col">Appears in Apps <span @click="sort('apps_count')">{{ icon('apps_count') }}</span></th>
      <th scope="col">Apps with ATS Exceptions <span @click="sort('ats_apps_count')">{{ icon('ats_apps_count') }}</span></th>
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
      currentDomain: null,
      sortOrder: {
        apps_count: true,
        ats_apps_count: false,
      }
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
    sort(field) {
      this.sortOrder[field] = !this.sortOrder[field];
      this.fetchDomains(this.pagination.page);
    },
    icon(field) {
      // TODO: Move to mixin!
      if (!this.sortOrder.hasOwnProperty(field)) {
        return '';
      }

      return this.sortOrder[field] ? '⬆️' : '⬇️';
    },
    fetchDomains(page) {
      UrlHelper.setParameter('page', page);
      let options = {
        order: this.sortOrder
      };

      this.postData(`/api/domains/paginate/${page}`, options).then((data) => {
        this.domains = data.domains;
        this.pagination = data.pagination;
      });
    },
    fetchDomainDetails(domainId) {
      return this.fetchData(`/api/domains/${domainId}`).then((data) => {
        let domainModel = {};
        Object.assign(domainModel, data.domain);
        this.assignDomainModel(domainModel, data);
        UrlHelper.setParameter('domain', domainId);
      });
    },
    assignDomainModel(domainModel, data) {
      domainModel.apps = data.apps;
      domainModel.ats_exceptions = data.ats_exceptions;

      this.currentDomain = domainModel;
    },
    deselectDomain() {
      this.currentDomain = null;
      UrlHelper.setParameter('domain', '');
    },
  },
  mounted() {
    this.pagination.page = UrlHelper.getParameter('page', 1);
    this.fetchDomains(this.pagination.page);

    let domainId = UrlHelper.getParameter('domain', -1);
    if (domainId > 0) {
      this.fetchDomainDetails(domainId);
    }
  }
}
</script>

<style scoped>

</style>