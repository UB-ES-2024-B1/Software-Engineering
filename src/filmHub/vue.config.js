const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    //proxy: 'http://127.0.0.1:8000',
    proxy: 'https://filmhub-backend-prepro.azurewebsites.net', // redirige las solicitudes al backend
  },

  publicPath: '/',
});
