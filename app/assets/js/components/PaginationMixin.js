export default {
    data: () => ({
        pagination: {
            'page': 1,
            'pages': 1,
            'per_page': 25,
            'total': 0
        },
        pagesAround: 10,
    }),
    methods: {
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
    }
}