const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: process.env.USE_SELE_CONFIG === 'true' 
      ? 'https://filmhub-backend.azurewebsites.net' 
      : 'http://localhost:8000', // You can modify this line based on your environment
  },

  publicPath: '/',
});
