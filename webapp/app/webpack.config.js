const {VueLoaderPlugin} = require("vue-loader");
const path = require("path");

module.exports = {
    entry: ['./assets/js/app.js'],
    output: {
        path: path.resolve(__dirname, 'static', 'js'),
        filename: 'main.js',
    },
    resolve: {
        alias: {
            // this isn't technically needed, since the default `vue` entry for bundlers
            // is a simple `export * from '@vue/runtime-dom`. However having this
            // extra re-export somehow causes webpack to always invalidate the module
            // on the first HMR update and causes the page to reload.
            'vue': 'vue/dist/vue.esm-bundler.js'
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            }
        ],
    },
    plugins: [
        new VueLoaderPlugin()
    ]
};
