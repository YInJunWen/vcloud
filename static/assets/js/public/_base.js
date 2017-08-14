/**
 * Created by YIn on 2017/7/19.
 */

/*====================django ajax ======*/
jQuery(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
/*===============================django ajax end===*/


$('#datepicker input').datepicker({
    language: "zh-CN",
    todayHighlight: true
});


var log_username = $('#rightBarlist6>a').text();
var log_num_count = $('.log_num_count').text();
$('#pageTool').Paging({pagesize: 10, count: log_num_count});

$('#manageBar').click(function () {
    return false;
});

/***
 * actionObject
 * operationType
 * username
 * ip
 * logintime
 */

$('#logTable').DataTable({
    ajax: '/accessLog/',
    columns: [
        {data: 'log_user'},
        {data: 'log_type'},
        {data: 'log_detail'},
        {data: 'log_ip'},
        {data: 'log_opt'}
    ],
    "fnInitComplete": function () {
        if ($('#Logtbody tr').length > 1) {
            $('.log_noMessage').hide();
        }
    }
});

// order 工单页面

// $('#orderTable').DataTable({
//     ajax: '/accessOrder/',
//     columns: [
//         {data: 'id'},
//         {data: 'add_time'},
//         {data: 'reason'},
//         {data: 'username'},
//         {data: 'state'}
//     ],
//     "fnInitComplete": function () {
//         if ($('#order tr').length > 1) {
//             $('.order_noMessage').hide();
//         }
//     }
// });

$.ajax({
    url: '/accessOrder/',
    success: function (data) {
        $.each(data.data, function (key, value) {
            tbody = '<tr><td style="text-indent: 0;text-align: center;">' + value.pid + '</td><td style="text-indent: 100px;">' + value.created_at + '</td><td>创建云主机</td><td>' + value.status + '</td><td>' + '<a href="javascript:void(0)" onclick="Approval(this)">撤销&nbsp;</a>' + '<a href="javascript:void(0)" onclick="Approval(this)">&nbsp;删除</a>' + '</td></tr>';
            $('#orderTable').append(tbody);
            if ($('#orderTable tr').length >= 1) {
                $('.order_noMessage').hide();
            }
        })
    }
});

$.ajax({
    url: '/accessIns/',
    success: function (data) {
        $.each(data.data, function (key, value) {
            tbody = '<tr><td style="text-align: center;">' + value.name + '</td><td style="text-align: center;text-indent: 30px;">255.255.255.255</td><td class="pz">详细配置<ul id="hideList"><li><h3>云主机类型详情:</h3><div class="table-wapper"><table><tbody><tr><th class="hideTh">CPU</th><td class="hideTd">' + value.vcpus + '核</td></tr><tr><th class="hideTh">内存</th><td class="hideTd">' + value.memory + 'GB</td></tr><tr><th class="hideTh">Disk</th><td class="hideTd">' + value.disk + 'GB</td></tr><tr><th class="hideTh">带宽</th><td class="hideTd">' + value.bandwidth + 'MB</td></tr><tr><th class="hideTh">系统</th><td class="hideTd">' + value.os + '</td></tr></tbody></table></div></li></ul></td><td>1 MB</td><td>1</td>' + '<td>' + value.status + '</td>' + '<td style="text-align:center"><select name="" class="console_select" onchange="yzj_Change(this.options[this.options.selectedIndex].value)"><option value="0">--------</option><option value="1">开机</option><option value="2">关机</option><option value="3">重启</option><option value="4">修改密码</option><option value="5">快照</option></select></td></tr>';
            $('#yDisk-body').append(tbody);
            if ($('#yDisk-body tr').length >= 1) {
                $('.ins_noMessage').hide();
            }
        })
    }
});

//  管理吐数据
// $.ajax({
//     url: '/approval/',
//     success: function (data) {
// console.log(data.data);
// $.each(data.data, function (key, value) {
//     tbody = '<tr><td style="text-indent: 0;text-align: center;">' + value.pid + '</td><td style="text-indent: 100px;">' + value.created_at + '</td><td>创建云主机</td><td>' + value.created_user + '</td><td>' + value.status + '</td><td>' + '<a href="javascript:void(0)" onclick="Approval(this)">同意&nbsp;</a>' + '<a href="javascript:void(0)" onclick="Approval(this)">&nbsp;拒绝</a>' + '</td></tr>';
//     $('.yChecking-body').append(tbody);
//     if ($('.yChecking-body tr').length >= 1) {
//         $('.orderCk_noMessage').hide();
//     }
// })
//     }
// });

//  修改密码
$('#change_psw').click(function () {
    $('.change_psw_Wapper').show();
    $('#old_psw').focus();
});

$('.change_psw_ok').click(function () {
    var old_psw = $('#old_psw').val();
    var new_psw = $('#new_psw').val();
    var confirm_psw = $('#confirm_psw').val();
    if (new_psw.length < 8) {
        $('.mistake').show();
        $('#old_psw, #new_psw, #confirm_psw').val('');
        $('#old_psw').focus();
        return false;
    }
    if (new_psw !== confirm_psw) {
        $('.nosame').show();
        $('#old_psw, #new_psw, #confirm_psw').val('');
        $('#old_psw').focus();
        return false;
    }
    $.ajax({
        url: '/change_psw/',
        method: "POST",
        type: "json",
        data: {
            'old_psw': old_psw,
            'new_psw': new_psw,
            'confirm_psw': confirm_psw
        },
        success: function (req) {
            if (req.data == '1') {
                $('.change_psw_Wapper').hide();
                window.location.href = '/login/'
            } else {
                $('.mistake').show();
                $('#old_psw, #new_psw, #confirm_psw').val('');
                $('#old_psw').focus();
                return false;
            }
        }
    });
    return false;
});

$('.closeBtnBar').click(function () {
    $('.nosame,.mistake').hide();
    $('#old_psw, #new_psw, #confirm_psw').val('');
});

function Approval(obj) {
    // console.log($(obj).parent().parent().children().get(0).innerHTML);
    var id = $(obj).parent().parent().children().get(0).innerHTML;
    $.post('/approval/', {'_id': id}, function (data) {
        console.log(data.data[0]);
        $('.yChecking-body').empty();
        $.each(data.data, function (key, value) {
            // console.log(value);
            var data = '<tr><td style="text-indent: 0;text-align: center;">' + value.pid + '</td><td style="text-indent: 100px;">' + value.created_at + '</td><td>创建云主机</td><td>' + value.created_user + '</td><td>' + value.status + '</td><td><a href="javascript:void(0)" onclick="Approval(this)">同意&nbsp;</a><a href="javascript:void(0)">&nbsp;拒绝</a></td></tr>';
            // console.log(1);
            $('.yChecking-body').append(data)
        });
    });
}