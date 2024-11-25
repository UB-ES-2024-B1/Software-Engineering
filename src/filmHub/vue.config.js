const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// vue.config.js
module.exports = {
  devServer: {
    proxy: 'https://filmhub-backend-d0cyacamg5h3e7gb.canadacentral-01.azurewebsites.net:8080', // redirige las solicitudes al backend
  },
  publicPath: '/',

};
