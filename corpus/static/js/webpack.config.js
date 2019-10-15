var webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')

var path = require('path');

const ASSET_PATH = process.env.ASSET_PATH || "/static";

let entries = {
    'guest.index': "./src/guest/index.js",
    
    'admin.dashboard': "./src/admin/dashboard.js",
    'admin.users': "./src/admin/users.js",
    'admin.languages': './src/admin/languages.js',
    'admin.translation_tasks': './src/admin/translation_tasks.js',
    'admin.import_export': './src/admin/import_export.js',

    'user.translation': "./src/user/translation.js",
    'user.profile': "./src/user/profile.js",
    'accounts.login': "./src/accounts/login.js",
    
    default: './src/default/app.js',
};

let outputs = {};

let plugins = [
    // This makes it possible for us to safely use env vars on our code
    new webpack.DefinePlugin({
      'process.env.ASSET_PATH': JSON.stringify(ASSET_PATH),
    }),
    new VueLoaderPlugin(),
    new VuetifyLoaderPlugin()
];

module.exports = {
    mode: 'development',
    entry: entries,
    output: {
        path: __dirname + '/dist/',
        publicPath: process.env.ASSET_PATH,
        filename: chunkData => chunkData.chunk.name.split('.').join('/') + '.js'
    },
    plugins: plugins,
    resolve: { 
        alias: { vue: 'vue/dist/vue.esm.js' },
        extensions: ['.js', '.jsx', '.css', '.styl']
    },
    module: {
        rules: [
            { 
                test: /\.css$/, 
                use: [
                    {loader: 'vue-style-loader'},
                    {loader: 'style-loader'},
                    {loader: 'css-loader'},
                    {
                        loader: 'postcss-loader',
                        options: {
                          ident: 'postcss',
                          plugins: [
                            require('tailwindcss'),
                            require('autoprefixer'),
                          ],
                        }
                    }
                ]
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                  // Creates `style` nodes from JS strings
                  'style-loader',
                  // Translates CSS into CommonJS
                  'css-loader',
                  // Compiles Sass to CSS
                  'sass-loader',
                ],
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                  {
                    loader: 'file-loader',
                    options: {
                      name: '[name].[ext]',
                      outputPath:  "../fonts/",
                      publicPath: "/static/fonts/"
                    }
                  }
                ]
            },
            {test: /\.vue$/, loader: 'vue-loader'},
            { test: /\.styl$/, loader: 'style-loader!css-loader!stylus-loader' },
            {
                test: /\.m?js$/,
                exclude: /(node_modules|bower_components)/,
                use: {
                  loader: 'babel-loader',
                  options: {
                    presets: ['@babel/preset-env']
                  }
                }
            }
        ]
    }
}
