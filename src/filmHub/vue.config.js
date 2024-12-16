const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: 'https://filmhub-backend-prepro.azurewebsites.net', // redirige las solicitudes al backend
  },

  publicPath: '/',
});
