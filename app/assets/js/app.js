import {createApp} from 'vue';
import WebApp from './components/WebApp.vue';

const app = createApp({
    components: {
        WebApp
    }
});

app.mount("#app");