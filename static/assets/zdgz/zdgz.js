var myChart1 = echarts.init(document.getElementById('chart1'));
var option1 = {
	backgroundColor: 'transparent',
	title: {
		text: '云计算分布',
		textStyle: {
			color: '#fff'
		},
		x:'center',
        y:'top',
		textAlign:'center'
	},
	// visualMap: {
	// 	show: 'false',
	// 	min: 80,
	// 	max: 600,
	// 	inRange: {
	// 		colorLightness: [0, 1]
	// 	}
	// },
	series: [
		{
			name: '访问来源',
			type: 'pie',
			radius: '55%',
			center: ['50%', '50%'],
			data:[
                {value: 335, name: '北京'},
                {value: 310, name: '上海'},
                {value: 274, name: '广州'},
                {value: 235, name: '江苏'},
                {value: 400, name: '浙江'},
			].sort(function (a, b) {return a.value - b.value; }),
			roseType: 'radius',
			label: {
				normal: {
					textStyle: {
						color: 'rgb(255, 255, 255)'
					}
				}
			},
			labelLine: {
				normal: {
					lineStyle: {
						color: 'rgb(255, 255, 255)'
					},
					smooth: 0.2,
					length: 10,
					length2: 20
				}
			},
			itemStyle: {
				normal: {
					color: '#c23531',
					shadowBlur: 200,
					shadowColor: 'rgba(0, 0, 0, 0.5)'
				}
			},
			animationType: 'scale',
			animationEasing: 'elasticOut',
			animationdelay: function(idx) {
				return Math.random() * 200;
			}
		}
	]
};
myChart1.setOption(option1);

var myChart2 = echarts.init(document.getElementById('chart2'));

// 自动获取假数据
function randomData() {
	now = new Date(+now + oneDay);
	value = value + Math.random() * 21 - 10;
	return {
		name: now.toString(),
		value: [
			[now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'),
			Math.round(value)
		]
	}
}

var data = [];
var now = +new Date(2016, 5, 25);
var oneDay = 24 * 3600 * 1000;
var value = Math.random() * 1000;
for (var i = 0; i < 1000; i++) {
	data.push(randomData());
}

var option2 = {
	//核心交换数据
	title: {
		text: '云计算分布',
		textStyle: {
			color: '#fff'
		},
		x:'center',
        y:'top',
		textAlign:'center'
	},
	tooltip: {
		trigger: 'axis',
		formatter: function(params) {
			params = params[0];
			var date = new Date(params.name);
			return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + ':' + params.value[1];
		},
		axisPointer: {
			animation: false
		}
	},
	xAxis: {
		type: 'time',
		splitLine: {
			show: false
		},
		axisLine: {
            lineStyle:{
                color:'#fff',
            }
        }
	},
	yAxis: {
		type: 'value',
        boundaryGap: [0, '100%'],
		splitLine: {
			show: false
		},
        axisLine: {
            lineStyle: {
                color: '#fff'
            }
        }
	},
	series: [{
		name: '模拟数据',
		type: 'line',
		showSymbol: false,
		hoverAnimation: false,
		data: data
	}]
};
myChart2.setOption(option2);

setInterval(function() {
	for (var i = 0; i < 5; i ++) {
		data.shift();
		data.push(randomData());
	}
	myChart2.setOption({
		series: [{
			data: data
		}]
	});
}, 2100);

var myChart3 = echarts.init(document.getElementById('chart3'));
var myChart4 = echarts.init(document.getElementById('chart4'));
var myChart5 = echarts.init(document.getElementById('chart5'));
var option3 = {
	title: {
		text: 'cpu使用率',
		// subtext: '纯属虚构'
		// 标题颜色 subtextStyle为副标题
		textStyle: {
			color: '#fff'
		},
		x:'center',
        y:'top',
		textAlign:'center'
	},
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'cross',
			label: {
				backgroundColor: '#283b56'
			}
		}
	},
	// legend: {
	// 	data: ['最新成交价','预购队列']
	// },
	toolbox: {
		show: true,
		feature: {
			dataView: {readOnly: false},
			restore: {},
			saveAsImage: {}
		}
	},
	dataZoom: {
		show: false,
		start: 0,
		end: 100
	},
	xAxis: [
		{
			type: 'category',
			boundaryGap: true,
			data: (function (){
				var now = new Date();
				var res = [];
				var len = 10;
				while (len--) {
					res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
					now = new Date(now - 2000);
				}
				return res;
			})(),
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            }
		},
		{
			type: 'category',
			boundaryGap: true,
			data: (function (){
				var res = [];
				var len = 10;
				while (len--){
					res.push(len + 1);
				}
				return res;
			})(),
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            }
		},
	],
	yAxis: [
		{
			type: 'value',
			scale: true,
			// name: '价格',
			max: 30,
			min: 0,
			boundaryGap: [0.2, 0.2],
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            }
		},
		{
			type: 'value',
			scale: true,
			// name: '预购量',
			max: 1200,
			min: 0,
			boundaryGap: [0.2, 0.2],
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            }
		}
	],
	series: [
		{
			name: 'CPU使用率',
			// color: '#fff', 可以修改柱形图颜色
			type: 'bar',
			xAxisIndex: 1,
			yAxisIndex: 1,
			data: (function (){
				var res = [];
				var len = 10;
				while (len--) {
					res.push(Math.round(Math.random() * 1000));
				}
				return res;
			})()
		},
		{
            name: '内存使用率',
            color: '#fff',
            type: 'line',
            data: (function (){
                var res = [];
                var len = 0;
                while (len < 10) {
                    res.push((Math.random() * 10 + 5).toFixed(1) - 0);
                    len++;
                }
                return res;
            })(),
            lineStyle: {
            	normal: {
            		color: '#f90'
            	}
            }
		}
	]
};

var app = {};
app.count = 11;
setInterval(function (){
	axisData = (new Date()).toLocaleTimeString().replace(/^\D*/,'');
    var data0 = option3.series[0].data;
    var data1 = option3.series[1].data;
    data0.shift();
    data0.push(Math.round(Math.random() * 1000));
    data1.shift();
    data1.push((Math.random() * 10 + 5).toFixed(1) - 0);

    option3.xAxis[0].data.shift();
    option3.xAxis[0].data.push(axisData);
    option3.xAxis[1].data.shift();
    option3.xAxis[1].data.push(app.count++);

    myChart3.setOption(option3);
    myChart4.setOption(option3);
    myChart5.setOption(option3);
}, 2100);

var myChart6 = echarts.init(document.getElementById('chart6'));
var option6 = {
	// backgroundColor: '#060f4c',
	series:[{
		type: 'pie',
		radius: ['35%', '55%'],
		silent: true,
		data: [{
			value: 1,
			itemStyle: {
				normal: {
					color: '#050f58',
					borderColor: '#162abb',
					borderWidth: 2,
					shadowBlur: 50,
					shadowColor: 'rgba(21,41,185,.75)'
				}
			}
		}]
	}, {
		type: 'pie',
		radius: ['35%', '55%'],
		silent: true,
		label: {
			normal: {
				show: false,
			}
		},
		data:[{
			value: 1,
			itemStyle: {
				normal: {
					color: '#050f58',
					shadowBlur: 50,
					shadowColor: 'rgba(21,41,185,.75)'
				}
			}
		}]
	},{
		name: '占比',
		type: 'pie',
		radius: ['39%', '52%'],
		hoverAnimation: false,

		data: [{
			value: 70,
			name: '电信',
			itemStyle: {
				normal: {
					label: {
						show: true,
						textStyle: {
							fontSize: 15,
							fontWeight: 'blod'
						},
						position: 'center'
					},
					color: new echarts.graphic.LinearGradient(0,0,0,1,[{
						offset: 0,
						color: 'rgba(5,193,255,1)'
					},{
						offset: 1,
						color: 'rgba(15,15,90,1)'
					}])
				}
			},
			label: {
				normal: {
					position: 'outside',
					textStyle: {
						color: '#fff',
						fontSize: 14
					},
					formatter: '{b}: 21Mbps\n\n{a}: {c}%'
				}
			},
			labelLine: {
				normal: {
					show: true,
					length: 20,
					length2: 30,
					smooth: false,
					lineStyle: {
						width: 1,
						color: '#2141b5'
					}
				}
			}
		},{
			value: 30,
			name: '联通',
			itemStyle: {
				normal: {
					label: {
						show: true,
						textStyle: {
							fontSize: 15,
							fontWeight: 'blod'
						},
						position: 'center'
					},
					color: new echarts.graphic.LinearGradient(0,0,0,1,[{
						offset: 0,
						color: 'rgba(5,15,88,1)'
					},{
						offset: 1,
						color: 'rgba(235,122,255,1)'
					}])
				}
			},
			label: {
				normal: {
					position: 'outside',
					textStyle: {
						color: '#fff',
						fontSize: 14
					},
					formatter: '{b}: 9Mbps\n\n{a}: {c}%'
				}
			},
			labelLine: {
				normal: {
					show: true,
					length: 20,
					length2: 40,
					smooth: false,
					lineStyle: {
						width: 1,
						color: '#2141b5'
					}
				}
			}
		}]
	}, {
		name: '',
		type: 'pie',
		clockWise: true,
		hoverAnimation: false,
		radius: [200, 200],
		label: {
			normal: {
				position: 'center'
			}
		},
		data: [{
			value: 0,
			label: {
				normal: {
					formatter: '30Mbps',
					textStyle: {
						color: '#fe8b53',
						fontSize: 25,
						fontWeight: 'blod'
					}
				}
			}
		}, {
			tooltip: {
				show: false
			},
			label: {
				normal: {
					formatter: '\n总宽带',
					textStyle: {
						color: '#bbeaf9',
						fontSize: 14
					}
				}
			}
		}]
	}]
};
myChart6.setOption(option6);


var myChart7 = echarts.init(document.getElementById('chart7'));
var option7 = {
	// color: colors, 皮肤颜色
	title: {
		text: '云主机数量',
		textStyle: {
			color: '#fff'
		},
		x:'center',
        y:'top',
		textAlign:'center'
	},
	tooltip: {
		trigger: 'none',
		axisPointer: {
			type: 'cross'
		}
	},
	legend: {
		data:['实时','在线']
	},
	grid: {
		top: 70,
		bottom: 50
	},
	xAxis: [
		{
			type: 'category',
			axisTick: {
				alignWithLabel: true
			},
			axisLine: {
				onZero: false,
				lineStyle: {
					// color: colors[1]
				}
			},
			axisPointer: {
				label: {
					formatter: function (params) {
						return '实时数量' + params.value + (params.seriesData.length ?':' + params.seriesData[0].data :'');visualMap
					},
					textStyle: {
                    	color: '#f90'
                    },
                    backgroundColor: '#1E2428'
				}
			},
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            },
			data: ['2017-1','2017-2','2017-3','2017-4','2017-5','2017-6','2017-7','2017-8','2017-9','2017-10','2017-11','2017-12']
		},
		{
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLine: {
                onZero: false,
                lineStyle: {
                    // color: colors[0]
                }
            },
            axisPointer: {
                label: {
                    formatter: function (params) {
                        return '在线数量' + params.value + (params.seriesData.length ?':' + params.seriesData[0].data :'');
                    },
                    textStyle: {
                    	color: '#f90'
                    },
                    backgroundColor: '#1E2428'
                }
            },
            axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            },
            data: ['2017-1','2017-2','2017-3','2017-4','2017-5','2017-6','2017-7','2017-8','2017-9','2017-10','2017-11','2017-12']
        }
	],
	yAxis: [
		{
			type: 'value',
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            },
            axisPointer: {
            	label: {
            		textStyle: {
                    	color: '#f90'
                    },
                    backgroundColor: '#1E2428'
            	}
            }
		}
	],
	series: [
		{
			name: '2017 实时',
			type: 'line',
			xAxisIndex: 1,
			smooth: true,
			data: [2.6,5.9,9.0,26.4,28.7,70.7,175.6,182.2,182.3,183.8,196.0,202.3]
		},{
            name: '2017 在线',
            type: 'line',
            smooth: true,
            data: [3.9,5.9,11.1,18.7,48.3,69.2,171.6,176.6,175.4,178.4,179.3,180.7]
        }
	]
};
myChart7.setOption(option7);

// chart8
var myChart8 = echarts.init(document.getElementById('chart8'));
var option8 = {
	title: {
		text: '防火墙流量',
		textStyle: {
			color: '#fff'
		},
		x:'center',
        y:'top',
		textAlign:'center'
	},
	tooltip: {
		trigger: 'axis'
	},
	// legend: {
	// 	data: ['蒸发量','降水量']
	// },
	toolbox: {
		show: true,
		feature: {
			dataView: {show: true,rendOnly: false},
			magicType: {show: true, type:['line','bar']},
			restore: {show:true},
			saveAsImage: {show: true}
		}
	},
	calculable: true,
	xAxis:[
		{
			type: 'category',
			data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'],
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            },
		}
	],
	yAxis: [
		{
			type: 'value'
		}
	],
	series: [
		{
			name: '攻击时段',
			type: 'bar',
			data: [2.0,4.9,7.0,23.2,25.6,76.7,135.6,162.2,32.6,20.0,6.4,3.3],
			axisLine:{
                lineStyle:{
                    color:'#fff',
                }
            },
			markPoint: {
				data: [
					{type: 'max',name: '最大值'},
					{type: 'min',name: '最小值'}
				]
			},
			markLine: {
				data: [
					{type: 'average', name: '平均值'}
				]
			}
		},
		{
			name: '攻击频率',
			type: 'bar',
			data: [2.6,5.9,9.0,26.4,28.7,70.7,175.6,182.2,48.7,18.8,6.0,2.3],
			markPoint: {
				data: [
					{name: '年最高', value: 182.2, xAxis: 7,yAxis: 183},
					{name: '年最低', value: 2.3, xAxis: 11, yAxis: 3}
				]
			},
			markLine: {
				data: [
					{type:'average', name: '平均值'}
				]
			}
		}
	]
};
myChart8.setOption(option8);


// 屏幕自适应
window.onresize = myChart1.resize;
window.onresize = myChart2.resize;
window.onresize = myChart3.resize;
window.onresize = myChart4.resize;
window.onresize = myChart5.resize;
window.onresize = myChart6.resize;
window.onresize = myChart7.resize;
window.onresize = myChart8.resize;