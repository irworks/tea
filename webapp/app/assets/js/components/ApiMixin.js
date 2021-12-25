export default {
    data: () => ({
        runningRequests: 0,
    }),
    methods: {
        fetchData(url) {
            this.runningRequests++;
            return fetch(url)
                .then(response => {
                    this.runningRequests--;
                    return response.json();
                }).catch(error => {
                    console.log(error);
                });
        }
    },
    computed: {
        isLoadingData() {
            return this.runningRequests > 0;
        },
    }
}