const { defineConfig } = require('@vue/cli-service')
module.exports = ({
  transpileDependencies: true,
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
    }
})
// 修改或新增html-webpack-plugin的值，在index.html里面能读取htmlWebpackPlugin.options.title
chainWebpack: config =>{
  config.plugin('html').tap(args => {
      args[0].title = '你想要设置的title';
      return args;
  })
}
// module.exports = {
//   publicPath: './',//静态资源包打包为相对路径
//   outputDir: 'dist',//输出文件
//   devServer: {
//     // historyApiFallback: true,
//     allowedHosts: "all",
//     open: false,
//     host: '0.0.0.0',
//     port: 8080,
//     hot: true,
//     proxy: {
//       '/api': {
//         target: 'http://aa7415157.e2.luyouxia.net:28152', // 你请求的第三方接口
//         changeOrigin: true, // 在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样服务端和服务端进行数据的交互就不会有跨域问题
//         pathRewrite: {  // 路径重写，
//           '^/Api': ''  // 替换target中的请求地址，也就是说以后你在请求http://api.wpbom.com这个地址的时候直接写成/Api即可。
//         }
//       }
//     },
//   }
// }
