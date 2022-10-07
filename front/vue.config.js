const path = require('path')

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        //////1/2- target: 'http://192.168.32.178:5050', // target host, for zh
        target: 'http://192.168.0.13:5050',   // target host, for home
        //////1/2- target: 'http://192.168.43.117:5050', // target host, for mobile
        
        changeOrigin: true, // needed for virtual hosted sites
        ws:true,            // proxy websockets 
        pathRewrite: {
          '^/api': ''       // remove base path
        }
      },
    },
    //port: 8080,
    host: '0.0.0.0',
    //https: false,
    //hotOnly: false,   //每次更新資料都會重新刷新畫面的話, false:取消
    disableHostCheck: true,   //Keep getting [WDS] Disconnected! error
  },

};


  