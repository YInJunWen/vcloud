/**
 * Created by YIn on 2017/4/10.
 */
$(function () {
    var pre1 = echarts.init(document.getElementById('pre1'));
    var pre2 = echarts.init(document.getElementById('pre2'));
    var pre3 = echarts.init(document.getElementById('pre3'));
    var pre4 = echarts.init(document.getElementById('pre4'));
    var pre5 = echarts.init(document.getElementById('pre5'));

// 若加载完动态 用jQuery
    $.post('/OverviewData/').done(function(data){
        pre1.setOption({
            series: [
                {
                    data: [
                        {value: data.pre1_run, name: data.pre1_run + '台'},
                        {value: data.pre1_odd, name: '主机'}
                    ]
                }
            ]
        });
        pre2.setOption({
            series: [
                {
                    data: [
                        {value: data.pre2_run, name: data.pre2_run + '核'},
                        {value: data.pre2_odd, name: 'CPU'}
                    ]
                }
            ]
        });
        pre3.setOption({
            series: [
                {
                    data: [
                        {value: data.pre3_run, name: data.pre3_run + 'G'},
                        {value: data.pre3_odd, name: '内存'}
                    ]
                }
            ]
        });
        pre4.setOption({
            series: [
                {
                    data: [
                        {value: data.pre1_run, name: data.pre1_run + '个'},
                        {value: data.pre1_odd, name: '浮动'}
                    ]
                }
            ]
        });
    });
    pre1.setOption({
        // title: {
        //     text: '运行主机及未运行主机！',
        //     textStyle:{
        //         fontSize: 15,
        //         verticalAlign: 'bottom'
        //     }
        // },
        series: [
            {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data: [
                    {value: 0, name: '暂无数据'},
                    // {value: 0, name: "主机"}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color: ['#428bca', '#BAC3E2']
    });

    pre2.setOption({
        series: [
            {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data: [
                    {value: 0, name: '暂无数据'},
                    // {value: 0, name: "CPU"}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color: ['#428bca', '#BAC3E2']
    });

    pre3.setOption({
        series: [
            {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data: [
                    {value: 0, name: '暂无数据'},
                    // {value: 0, name: "ROM"}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color: ['#428bca', '#BAC3E2']
    });

    pre4.setOption({
        series: [
            {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data: [
                    {value: 0, name: '暂无数据'},
                    // {value: 0, name: "浮动IP"}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color: ['#428bca', '#BAC3E2']
    });

    pre5.setOption({
        series: [
            {
                type: 'pie',
                radius: '50%',
                center: ['50%', '60%'],
                data: [
                    {value: 0, name: '暂无数据'},
                    // {value: 0, name: "安全组"}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ],
        color: ['#428bca', '#BAC3E2']
    });
});



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