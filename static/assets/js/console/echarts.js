/**
 * Created by YIn on 2017/4/10.
 */
var pre1 = echarts.init(document.getElementById('pre1'));
var pre2 = echarts.init(document.getElementById('pre2'));
var pre3 = echarts.init(document.getElementById('pre3'));
var pre4 = echarts.init(document.getElementById('pre4'));
var pre5 = echarts.init(document.getElementById('pre5'));

// 若加载完动态 用jQuery
// $.get('data.json').done(function (data) {
//     myChart.setOption({
//         title: {
//             text: '异步数据加载示例'
//         },
//         tooltip: {},
//         legend: {
//             data:['销量']
//         },
//         xAxis: {
//             data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
//         },
//         yAxis: {},
//         series: [{
//             name: '销量',
//             type: 'bar',
//             data: [5, 20, 36, 10, 10, 20]
//         }]
//     });
// });

pre1.setOption({
    series:[
        {
            type: 'pie',
            radius : '50%',
            center : ['50%', '60%'],
            data : [
                {value : 2, name : '2台'},
                {value : 8, name : "主机"}
            ],
            itemStyle : {
                emphasis : {
                    shadowBlur : 10,
                    shadowOffsetX : 0,
                    shadowColor : 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ],
    color:['#428bca', '#BAC3E2']
});

pre2.setOption({
    series:[
        {
            type: 'pie',
            radius : '50%',
            center : ['50%', '60%'],
            data : [
                {value : 5, name : '5核'},
                {value : 15, name : "CPU"}
            ],
            itemStyle : {
                emphasis : {
                    shadowBlur : 10,
                    shadowOffsetX : 0,
                    shadowColor : 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ],
    color:['#428bca', '#BAC3E2']
});

pre3.setOption({
    series:[
        {
            type: 'pie',
            radius : '50%',
            center : ['50%', '60%'],
            data : [
                {value : 5, name : '5G'},
                {value : 45, name : "ROM"}
            ],
            itemStyle : {
                emphasis : {
                    shadowBlur : 10,
                    shadowOffsetX : 0,
                    shadowColor : 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ],
    color:['#428bca', '#BAC3E2']
});

pre4.setOption({
    series:[
        {
            type: 'pie',
            radius : '50%',
            center : ['50%', '60%'],
            data : [
                {value : 0, name : '无'},
                {value : 50, name : "浮动IP"}
            ],
            itemStyle : {
                emphasis : {
                    shadowBlur : 10,
                    shadowOffsetX : 0,
                    shadowColor : 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ],
    color:['#428bca', '#BAC3E2']
});

pre5.setOption({
    series:[
        {
            type: 'pie',
            radius : '50%',
            center : ['50%', '60%'],
            data : [
                {value : 1, name : '1组'},
                {value : 9, name : "安全组"}
            ],
            itemStyle : {
                emphasis : {
                    shadowBlur : 10,
                    shadowOffsetX : 0,
                    shadowColor : 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ],
    color:['#428bca', '#BAC3E2']
});
// window.onresize = pre1.resize;
// window.onresize = pre2.resize;
// window.onresize = pre3.resize;
// window.onresize = pre4.resize;
// window.onresize = pre5.resize;
