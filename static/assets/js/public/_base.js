/**
 * Created by YIn on 2017/7/19.
 */

var REASON_ID = "";  // 定义拒绝的订单ID
var REASON_STATUS = "";  // 定义拒绝的状态

jQuery(document).ajaxSend(function (event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
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
        return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
            (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
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
    REASON_ID = $(obj).parent().parent().children().get(0).innerText;
    var status = $.trim($(obj).text());
    if (status === '同意'){
        status = 'y';
        // var id = $(obj).parent().parent().children().get(0).innerText;
        $.post('/approval/', {'_id': REASON_ID, '_status': status}, function(data){
            if (data.a === '0'){
                alert('failed！')
            }else{
                alert('success!')
            }
            window.location.reload();
        });
    } else {
      status = 'n';
      REASON_STATUS = 'n';
    }

    // 如果审批拒绝就弹窗
    if (status == 'n'){
        $('.reasonOrderBar').show();
    }
    // var id = $(obj).parent().parent().children().get(0).innerText;
    // $.post('/approval/', {'_id': id, '_status': status}, function(data){
    //     if (data.a === '0'){
    //         alert('failed！')
    //     }else{
    //         alert('success!')
    //     }
    //     window.location.reload();
    // });
}

$('.reasonBtnComputer').click(function(){
    $('.reasonOrderBar').hide();
    $.post('/approval/', {'_id': REASON_ID, '_status': REASON_STATUS, 'reason': $('.reasonValue').val()}, function(data){
        if (data.a === '0'){
            alert('failed！')
        }else{
            alert('success!')
        }
        window.location.reload();
    });
});


function Finished(obj) {
    var status = $.trim($(obj).text());
    if (status === '撤销'){
        status = 'back';
    } else {
      status = 'del'
    }
    var id = $(obj).parent().parent().children().get(0).innerText;
    $.post('/finished/', {'_id': id, '_status': status}, function(data){
        if (data.status == '1'){
            alert('success!');
            window.location.reload();
        } else {
            alert('云计算中心已审核！无法撤回;');
        }
    });
}

