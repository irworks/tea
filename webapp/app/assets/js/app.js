import {createApp} from 'vue';
import WebApp from './components/WebApp.vue';

const app = createApp({
    components: {
        WebApp
    },
    mounted() {
        console.log('Vue mounted!');
    }
});

app.mount("#app");