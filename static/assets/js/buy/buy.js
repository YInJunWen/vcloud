/**
 * Created by YIn on 2017/3/9.
 */
$(function(){
    //入门型
    $('.rumen').click(function(){
        $('.chanpinleixin').val('入门型');
        $('.cpu').val('1核');
        $('.neicun').val('1G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('1');
        $('.input-mem').val('1');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    //标准型
    $('.biaozhun').click(function(){
        $('.chanpinleixin').val('标准型');
        $('.cpu').val('2核');
        $('.neicun').val('2G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('2');
        $('.input-mem').val('2');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    //商务型
    $('.shangwu').click(function(){
        $('.chanpinleixin').val('商务型');
        $('.cpu').val('2核');
        $('.neicun').val('4G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('2');
        $('.input-mem').val('4');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    //舒适型
    $('.shushi').click(function(){
        $('.chanpinleixin').val('舒适型');
        $('.cpu').val('4核');
        $('.neicun').val('4G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('4');
        $('.input-mem').val('4');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    //企业型
    $('.qiye').click(function(){
        $('.chanpinleixin').val('企业型');
        $('.cpu').val('4核');
        $('.neicun').val('8G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('4');
        $('.input-mem').val('8');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    //豪华型
    $('.haohua').click(function(){
        $('.chanpinleixin').val('豪华型');
        $('.cpu').val('8核');
        $('.neicun').val('16G');
        $('.yingpan').val('50G');
        $('.daikuan').val('1Mbps');

        $('.input-cpu').val('8');
        $('.input-mem').val('16');
        $('.input-disk').val('50');
        $('.input-flux').val('1M');
    });
    // 分散存
    $('.fensanCun').click(function(){
        $('.chucunmoshi').html('SAS型硬盘');
    });

    // 操作系统所对应的写在2016  570  580   dom添加时才可以操作

    $('.service-content').click(function(){
       console.log($('.service-content .config-service-txt').text());
    });

    // 购买时长
    $('#J_renewTimeContainerDom dt').click(function(){
        $('.goumaishichang').val(($(this).text()));
        $('.input-expired').val(($(this).index()));
    });
});

function chk_buy() {
    var _os = $('.caozuoxit').val();
    if ((_os == "--") || (_instance_name == "")){
        alert('没有选择系统或未填写主机名');
        return false;
    } else {
        return true;
    }
}

