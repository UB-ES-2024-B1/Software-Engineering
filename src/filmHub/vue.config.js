const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// vue.config.js
module.exports = {
  devServer: {
    //proxy: 'https://filmhub-backend.azurewebsites.net', // redirige las solicitudes al backend
    proxy: 'http://localhost:8000', // for tests with selenium
  },
  publicPath: '/',

};
