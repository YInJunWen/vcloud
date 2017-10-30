/**
 * Created by YIn on 2017/3/4.
 */

// 全局变量
var TS_START = "";
// var Ts


//切换三角
(function () {

    //获取dom
    var products_services = document.getElementById('products_services');
    // var products_services_span = products_services.getElementsByTagName('span')[0];
    var alertView = document.getElementById('alertView');

    //初始计数
    // var current = 0;
    // products_services.onclick = function () {
    //     current = (current + 180) % 360;
    //     products_services_span.style.transform = 'rotate('+current+'deg)';
    //     if (alertView.style.display === 'block') {
    //         alertView.style.display = 'none';
    //     } else {
    //         alertView.style.display = 'block';
    //     }
    // }
})();

/**
 * yDisk-body
 * yDisk-btn触发
 * */
$(function () {
    $('#yDisk-btn').click(function () {
        // 判断是否有内容 有内容清空
        var step = $('#yDisk-body').text();
        if (step.length > 0) {
            $('#yDisk-body').html(' ');
        }

        var move = '<select name="" class="console_select" onchange="yzj_Change(this.options[this.options.selectedIndex].value)"><option value="0">--------</option><option value="1">开机</option><option value="2">关机</option><option value="3">重启</option><option value="4">修改密码</option><option value="5">快照</option></select>';
        // $.ajax({
        //     async: true,
        //     url:'./data.json',
        //     dataType:'json',
        //     success:function(data){
        //         // 判断来的数据源里面 runningor close 设成变量 直接套<td>并给样式
        //         $.each(data,function(k, v){
        //             str = "<tr>"+"<td width='10'><input type='checkbox'></td>"+
        //                 "<td>"+v.name+"</td>"+
        //                 "<td>"+v.ip+"</td>"+
        //                 "<td class='pz'>"+v.pz+"" +
        //                 "<ul id='hideList'><li><h3>云主机类型详情:</h3><div class='table-wapper'><table><tbody><tr><th class='hideTh'>CPU:</th><td class='hideTd'>CPU对应变量</td></tr><tr><th class='hideTh'>RAM:</th><td class='hideTd'>RAM对应变量</td></tr><tr><th class='hideTh'>Disk:</th><td class='hideTd'>Disk对应变量</td></tr><tr><th class='hideTh'>Flux:</th><td class='hideTd'>flux对应变量</td></tr></tbody></table></div></li></ul>" +
        //                 "</td>"+
        //                 "<td>"+v.liuliang+"</td>"+
        //                 "<td style='text-align: center'>"+v.yxq+"</td>"+
        //                 "<td style='text-align: center'>"+v.status+"</td>" + "<td style='text-align: right'>"+move+"</td>"+
        //                 "</tr>";
        //             // 可以用变量代替selete
        //             $('#yDisk-body').append(str);
        //         });
        //     }
        // });
        // $('.noMessage').hide();
    })
});

//点击对应view打开
$(function () {
    // 获取实力li
    $('#shiliViewBar').click(function () {
        $('#shiliView').show();
        $('#yunpanView,#kuaizhaoView,#logView,#manageView,#orderView').hide();
    });
    $('#yunpanbar').bind('click', function () {
        $('#yunpanView').show();
        $('#shiliView,#kuaizhaoView,#logView,#manageView,#orderView').hide();
    });
    $('#kuaizhaobar').bind('click', function () {
        $('#kuaizhaoView').show();
        $('#shiliView,#yunpanView,#logView,#manageView,#orderView').hide();
    });
    $('#logBar').bind('click', function () {
        $('#logView').show();
        $('#kuaizhaoView,#shiliView,#yunpanView,#manageView,#orderView').hide();
    });
    // $('#manageBar').bind('click',function(){
    //     $('#manageView').show();
    //     $('#kuaizhaoView,#shiliView,#yunpanView,#logView,#orderView').hide();
    // });
    $('#orderBar').bind('click', function () {
        $('#orderView').show();
        $('#kuaizhaoView,#shiliView,#yunpanView,#logView,#manageView').hide();
    });
});

// 原本就存在的dom方法不执行再jQuery中
$('.table thead input').click(function () {
    var is_check = $(this)[0].checked;
    $('.table tbody input').each(function () {
        $(this)[0].checked = is_check;
    })
});

// select对应打开逻辑
$(function () {
    //  取消按钮点击
    $('.closeBtnBar').click(function () {
        $('.openWapper,.closeWapper,.restartWapper,.changeWapper,.snapshotWapper,.change_psw_Wapper').hide();
        $('.Ts_select').children().first().attr('selected', 'selected');
        window.location.reload();
    });

    //  开启云主机
    $('.openBtnComputer').click(function () {
        $('.openWapper').hide();
        $('.Ts_select').children().first().attr('selected', 'selected');
        $('#loading_icon').show();
        //给服务器发送关闭请求
        $.post('/open_pc/', {'ins_name': TS_START}, function(data){
            // console.log(data.status);
            if (data.status == '0') {
                // console.log(data.status)
                alert('虚拟机已开启!');
                $('#loading_icon').hide();
                window.location.reload();
            }else{
                alert('开启失败, 请联系管理员!');
                window.location.reload();
            }
        });
    });

    //  关闭云主机
    $('.closeBtnComputer').click(function () {
        $('.closeWapper').hide();
        //给服务器发送关闭请求
        $('.Ts_select').children().first().attr('selected', 'selected');
        $('#loading_icon').show();
        // console.log(TS_START);
        //给服务器发送关闭请求
        $.post('/close_pc/', {'ins_name': TS_START}, function(data){
            // console.log(data.status);
            if (data.status == '0') {
                // console.log(data.status)
                alert('虚拟机已关闭！');
                $('#loading_icon').hide();
                window.location.reload();
            }else{
                alert('关机失败, 请联系管理员!');
                window.location.reload();
            }
        });
    });

    // 重启云主机
    $('.restartBtnComputer').click(function () {
        $('.restartWapper').hide();
        //给服务器发送关闭请求
        $('.Ts_select').children().first().attr('selected', 'selected');
        $('#loading_icon').show();
        // 移除运行状态图标 改为重启
        $('#reboot').removeClass().addClass('fa fa-refresh fa-spin');
        $('#reboot_loading').text('  重启中');
        // 给服务器发送关闭请求
        $.post('/reboot_pc/', {'ins_name': TS_START}, function(data){
            // console.log(data.status);
            if (data.status == '0') {
                alert('虚拟机已完成重启!');
                $('#loading_icon').hide();
                window.location.reload();
            }else{
                alert('重启失败, 请联系管理员!');
                window.location.reload();
            }
        });
    });

    // 更改密码
    $('.changeBtnpassword').click(function () {
        $('.changeWapper').hide();
        //给服务器发送关闭请求

    });

    // 创建快照
    $('.snapshotBtnComputer').click(function () {
        $('.snapshotWapper').hide();
        //给服务器发送关闭请求

    });

    // 修改登陆密码

});

function yzj_Change(a, b) {
    if (a == '1') {
        TS_START = b;
        $('.openWapper').show();
    }
    if (a == '2') {
        TS_START = b;
        $('.closeWapper').show();
    }
    if (a == '3') {
        TS_START = b;
        $('.restartWapper').show();
    }
    if (a == '4') {
        TS_START = b;
        $('.changeWapper').show();
    }
    if (a == '5') {
        TS_START = b;
        $('.snapshotWapper').show();
    }
}

// 工单撤销对应逻辑
(function () {
    $('.orderBtnOpen').on('click', function () {
        $('.withdrawWapper').show();
    });

    $('.order_deleteBtnOpen').on('click', function () {
        $('.deleteOrderBar').show();
    });

    //对应关闭
    $('.closeBtnBar').click(function () {
        $('.withdrawWapper,.deleteOrderBar,.reasonOrderBar').hide()
    });
})();

// 对应撤销按钮发送请求
var order_id = $('.order_id').text();
$('.withdrawBtnComputer').click(function () {
    $(".withdrawWapper").hide();
    $.post('/order_rollback/', {'order_index': order_id}, function () {
        window.location.href = "/order/";
    })
});

$('.deleteBtnComputer').click(function () {
    $(".deleteOrderBar").hide();
    $.post('/order_delete/', {'order_index': order_id}, function () {
        window.location.href = "/order/";
    })
});

// 切换skin按钮 

$('.body_skin1').click(function () {
    // 每次都存cookie
    var skin1 = "/static/assets/css/public/body_skin1.css";
    $("#skin_id").attr("href", skin1);
    $.cookie("the_skin", skin1, {expires: 7, path: '/'});
});

$('.body_skin2').click(function () {
    var skin2 = "/static/assets/css/public/body_skin2.css";
    $('#skin_id').attr("href", skin2);
    $.cookie('the_skin', skin2, {expires: 7, path: '/'});
});

$('.body_skin3').click(function () {
    var skin3 = "/static/assets/css/public/body_skin3.css";
    $('#skin_id').attr("href", skin3);
    $.cookie('the_skin', skin3, {expires: 7, path: '/'});
});

// 页面每次加载都去读取存在的皮肤cookie
$(function () {
    var cookie_skin = $.cookie('the_skin');
    $("#skin_id").attr('href', cookie_skin);
});


// 日志页 分页跳转

// $(function(){
//     // 每次刷新获取一遍li
//     var li_list = $('li[data-page]');
//     li_list.on('click',function(){
//         console.log($(this).text());
//         console.log(li_list);
//     })

// })

function dataPage(data) {
    var count = data.getAttribute('data-page');
    console.log(count);
    $.get('/log_show/', {'page': count});
}


//  管理界面隐藏显示关闭

$('#manageBar').mouseenter(function () {
    $('.manage_hidden').slideDown('500');
});