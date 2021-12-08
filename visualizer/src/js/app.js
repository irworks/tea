import {createApp} from 'vue';
import AppList from './components/AppList.vue';

const app = createApp({
    components: {
        AppList
    },
    mounted() {
        console.log('Vue mounted!');
    }
});

app.mount("#app");