const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// vue.config.js
module.exports = {
  devServer: {
    proxy: 'http://127.0.0.1:8000', // redirige las solicitudes al backend
  },
  publicPath: process.env.NODE_ENV === 'production' ? '/Software-Engineering/' : '/',

};
