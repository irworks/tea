export default {
    data: () => ({
        runningRequests: 0,
    }),
    methods: {
        fetchData(url) {
            return this.requestData(url, {});
        },
        postData(url, data) {
            let options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }

            return this.requestData(url, options);
        },
        requestData(url, data) {
            this.runningRequests++;
            return fetch(url, data)
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