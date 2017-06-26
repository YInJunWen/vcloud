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
    $('.single-slider').jRange({
        from: 0,
        to: 500,
        step: 1,
        scale: ['0','100G','200G','300G','400G','500G'],
        format: '%s',
        width: 636,
        showLabels: true,
        showScale: true
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
        if($(this).parent().hasClass('ChildType')){
            $('.Form_lx').val($(this).text());
        }
        if($(this).parent().hasClass('ChildCpu')){
            $('.Form_cpu').val($(this).text());
        }
        if($(this).parent().hasClass('ChildMem')){
            $('.Form_mem').val($(this).text());
        }
        if($(this).parent().hasClass('ChildFlux')){
            $('.Form_flux').val($(this).text());
        }
        if($(this).parent().hasClass('ChildBuyTime')){
            $('.Form_time').val($(this).text());
        }
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
    });

    //  select 选择
    $('.os_Option').change(function(){
        var value = $(this).children('option:selected').text();
        $('.Form_os').val(value);
    });

    $('.buy_number').change(function(){
        var value = $(this).val();
        if(value >= 1000){
            value = 1000;
            $(this).val(value);
        }
        $('.Form_sl').val(value+'台');
    });

    //  主机名联动
    $('.Host_Name').keyup(function(){
        $('.zjm').val($(this).val());
    });


    $('.ljgm').click(function(){
        //  判断数据
        var ins_name = $('.zjm').val();
        if ((ins_name == '未填写') || (ins_name == '')){
            alert('未填写主机名！');
            $('.Host_Name').focus();
            return;
        }

        var cpu = parseInt($('.Form_cpu').val());
        var mem = parseInt($('.Form_mem').val());
        var flux = parseInt($('.Form_flux').val());
        if (flux == '512') {
            flux = 0.5;
        }
        var disk = parseInt($('.Form_yp').val());
        var diskType = $('.Form_storage').val();
        var os = $('.Form_os').val();
        if ((os == '--') || (os == '---请选择---')){
            alert('未选择操作系统！');
            return;
        }
        var expired = parseInt($('.Form_time').val());
        var number = parseInt($('.Form_sl').val());
        // console.log(mem);


        //  button disabled 开启防止二次提交


    });

    //  scroll


    var rsfc = function () {
        if ($(window).scrollTop() > 100) {
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
    if ((ins_name == '未填写') || (ins_name == '')){
        alert('未填写主机名！');
        $('.Host_Name').focus();
        return false;
    }
    if ((os == '--') || (os == '---请选择---')){
        alert('未选择操作系统！');
        return false;
    }
}


