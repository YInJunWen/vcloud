/**
 * Created by YIn on 2017/6/21.
 */
$(function(){

    // 标题弹框
    $('.tipso').tipso({
        useTitle: false,
        background: '#b2d8ff'
    });

    // 滑块
    // $('.single-slider').jRange({
    //     from: 0,
    //     to: 500,
    //     step: 1,
    //     scale: ['0','100G','200G','300G','400G','500G'],
    //     format: '%s',
    //     width: 636,
    //     showLabels: true,
    //     showScale: true
    // });

    // 硬盘滑块
    $(".slider_Disk")
        .slider({
            max: 1000,
            values: [50]
        })
        .slider("pips", {
            step: 100,
            rest: "label",
            labels: { first: "0", last: "1000"}
        })
        // .slider("float")
        .on("slidechange", function(e, num) {
            console.log(num.value);
            $('.Form_yp').val(num.value + "GB");
            $('.h_Form_yp').val(num.value);
            calculatePrice();
        });

    // 带宽滑块
    $(".slider_Flux")
        .slider({
            max: 10,
            values: [1]
        })
        .slider("pips", {
            step: 1,
            rest: "label",
            labels: { first: "0", last: "10"}
        })
        // .slider("float")
        .on("slidechange", function(e, num) {
            console.log(num.value);
            $('.Form_flux').val(num.value + "Mbps");
            $('.h_Form_flux').val(num.value);
            calculatePrice();
        });



    // 二级联动
    var currentShowCity = 0;
    $('#os_Name').change(function(){
        $('#os_Name option').each(function(i, o){
            if($(this).attr('selected')){
                $('.os_Option').hide();
                $('.os_Option').eq(i).show();
                currentShowCity = i;
            }
        })
    });
    $('#os_Name').change();

    //  Child > a
    $('.ChildType a, .ChildCpu a, .ChildMem a, .ChildFlux a, .ChildBuyTime a').click(function(){
        $(this).addClass('a_class').siblings('.ChildType a, .ChildCpu a, .ChildMem a, .ChildFlux a, .ChildBuyTime a').removeClass('a_class');
        // 处理返回数量
        var number = parseInt($(this).text());
        // 判断带宽512
        if (number === 512) {
            number = 0.5;
        }
        if($(this).parent().hasClass('ChildType')){
            $('.Form_lx').val($(this).text());
        }
        if($(this).parent().hasClass('ChildCpu')){
            $('.Form_cpu').val($(this).text());
            $('.h_Form_cpu').val(number);
        }
        if($(this).parent().hasClass('ChildMem')){
            $('.Form_mem').val($(this).text());
            $('.h_Form_mem').val(number);
        }
        if($(this).parent().hasClass('ChildFlux')){
            $('.Form_flux').val($(this).text());
            $('.h_Form_flux').val(number);
        }
        if($(this).parent().hasClass('ChildBuyTime')){
            $('.Form_time').val($(this).text());
            $('.h_Form_time').val(number);
        }
        calculatePrice();
    });

    // 初始 商务型 3
    $('.ChildType a:nth-child(4)').click(function(){
        var number = parseInt($(this).text());
        $('.ChildCpu a:nth-child(3)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(4)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("2核");
        $('.h_Form_cpu').val('2');
        $('.Form_mem').val("4G");
        $('.h_Form_mem').val("4");
        calculatePrice();
    });

    // 入门型 1
    $('.ChildType a:nth-child(2)').click(function(){
        $('.ChildCpu a:nth-child(2)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(2)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("1核");
        $('.h_Form_cpu').val('1');
        $('.Form_mem').val("1G");
        $('.h_Form_mem').val("1");
        calculatePrice();
    });

    // 标准型 2
    $('.ChildType a:nth-child(3)').click(function(){
        $('.ChildCpu a:nth-child(3)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(3)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("2核");
        $('.h_Form_cpu').val('2');
        $('.Form_mem').val("2G");
        $('.h_Form_mem').val("2");
        calculatePrice();
    });

    // 舒适型 4
    $('.ChildType a:nth-child(5)').click(function(){
        $('.ChildCpu a:nth-child(4)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(4)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("4核");
        $('.h_Form_cpu').val('4');
        $('.Form_mem').val("4G");
        $('.h_Form_mem').val("4");
        calculatePrice();
    });

    // 企业型 5
    $('.ChildType a:nth-child(6)').click(function(){
        $('.ChildCpu a:nth-child(4)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(5)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("4核");
        $('.h_Form_cpu').val('4');
        $('.Form_mem').val("8G");
        $('.h_Form_mem').val("8");
        calculatePrice();
    });

    // 豪华型 6
    $('.ChildType a:nth-child(7)').click(function(){
        $('.ChildCpu a:nth-child(5)').addClass('a_class').siblings('.ChildCpu a').removeClass('a_class');
        $('.ChildMem a:nth-child(6)').addClass('a_class').siblings('.ChildMem a').removeClass('a_class');
        $('.Form_cpu').val("8核");
        $('.h_Form_cpu').val('8');
        $('.Form_mem').val("16G");
        $('.h_Form_mem').val("16");
        calculatePrice();
    });



    //  购买数量
    $('.buyNumber .jia').click(function () {
        //  获取购买数量
        var Numbers = parseInt($(this).parents('.buyNumber').find('input').val());
        Numbers++;
        if(Numbers >= 1000){
            Numbers = 1000;
            $(this).addClass('buyNumberEnd');
        }
        $(this).prev().prev().removeClass('buyNumberEnd');
        $(this).parents('.buyNumber').find('input').val(Numbers);
        $('.Form_sl').val(Numbers+'台');
        $('.h_Form_sl').val(Numbers);
        calculatePrice();
    });
    $('.buyNumber .jian').click(function () {
        //  获取购买数量
        var Numbers = parseInt($(this).parents('.buyNumber').find('input').val());
        Numbers--;
        if(Numbers <= 1){
            Numbers = 1;
            $(this).addClass('buyNumberEnd');
        }
        if(Numbers>1 && Numbers<1000){
            $('.jia').removeClass('buyNumberEnd');
        }
        $(this).prev().prev().removeClass('buyNumberEnd');
        $(this).parents('.buyNumber').find('input').val(Numbers);
        $('.Form_sl').val(Numbers+'台');
        $('.h_Form_sl').val(Numbers);
        calculatePrice();
    });

    //  select 选择
    $('.os_Option').change(function(){
        var value = $(this).children('option:selected').text();
        $('.Form_os').val(value);
        $('.h_Form_os').val(value);
    });

    $('.buy_number').change(function(){
        var value = $(this).val();
        if(value >= 1000){
            value = 1000;
            $(this).val(value);
        }
        $('.Form_sl').val(value+'台');
        $('.h_Form_sl').val(value);
        calculatePrice();
    });

    $('.h_Form_yp').change(function(){
        calculatePrice();
    });


    //  主机名联动
    $('.Host_Name').keyup(function(){
        $('.zjm').val($(this).val());
        $('.h_zjm').val($(this).val());
    });


    // $('.ljgm').click(function(){
    //     //  判断数据
    //     var ins_name = $('.zjm').val();
    //     if ((ins_name == '未填写') || (ins_name == '')){
    //         alert('未填写主机名！');
    //         $('.Host_Name').focus();
    //         return;
    //     }
    //
    //     var cpu = parseInt($('.Form_cpu').val());
    //     var mem = parseInt($('.Form_mem').val());
    //     var flux = parseInt($('.Form_flux').val());
    //     if (flux == '0') {
    //         alert('系统赠送50G系统盘！')
    //     }
    //     var disk = parseInt($('.Form_yp').val());
    //     var diskType = $('.Form_storage').val();
    //     var os = $('.Form_os').val();
    //     if ((os == '--') || (os == '---请选择---')){
    //         alert('未选择操作系统！');
    //         return;
    //     }
    //     var expired = parseInt($('.Form_time').val());
    //     var number = parseInt($('.Form_sl').val());
    //     // console.log(mem);
    //
    //
    //     //  button disabled 开启防止二次提交
    //
    //
    // });

    //  scroll


    var rsfc = function () {
        if ($(window).scrollTop() > 210) {
            $(".gobuyFormWapper").addClass("fixed");
        } else {
            $(".gobuyFormWapper").removeClass("fixed");
        }
    };

    $(window).scroll(rsfc);
    $(window).resize(rsfc);
    rsfc();

});

/**
 *
 * 1.硬盘滑块数量改变值在 range.js中 已记录
 *
 */

function checkForm() {
    var ins_name = $('.zjm').val();
    var os = $('.Form_os').val();
    var disk = $('.h_Form_yp').val();
    var login_password = $('.login_password').val();
    var confirm_login_password = $('.confirm_login_password').val();
    if ((ins_name == '未填写') || (ins_name == '')){
        alert('未填写主机名！');
        $('.Host_Name').focus();
        return false;
    }
    if ((os == '--') || (os == '---请选择---')){
        alert('未选择操作系统！');
        return false;
    }
    if (disk < 50) {
        alert('硬盘必须大于等于50G');
        return false;
    }
    if ((login_password == "") || (confirm_login_password == "") || (confirm_login_password !== login_password)
     || (login_password.length<8) || (login_password.length>20) || (confirm_login_password.length<8) || (confirm_login_password.length>20)){
        $('.login_password').val("");
        $('.confirm_login_password').val("");
        $('.login_password').focus();
        alert('密码格式错误或输出不一致！');
        return false;
    }
    $('.h_password').val(login_password);
}



// calculate price
function calculatePrice(){
    $.post('/calculatePrice/',
        {
            'cpu': $('.h_Form_cpu').val(),
            'mem': $('.h_Form_mem').val(),
            'flux': $('.h_Form_flux').val(),
            'disk': $('.h_Form_yp').val(),
            'expired': $('.h_Form_time').val(),
            'buyNumber': $('.h_Form_sl').val()
        },
        function(data){
            var price = parseInt(data.price);
            $('#price').text('￥'+ price);
            $('#oldPrice').text('￥'+ price / 0.8)
    })
}