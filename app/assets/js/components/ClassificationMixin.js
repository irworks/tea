export default {
    methods: {
        stateClasses: function (state) {
            const states = {
                info: 'bg-info text-dark',
                insecure: 'bg-danger',
                warning: 'bg-warning',
                secure: 'bg-success'
            };
            return states[state];
        },
    }
}