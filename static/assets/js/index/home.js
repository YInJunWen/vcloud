/**
 * Created by YIn on 2017/3/7.
 */
$(function(){
    var fullPage;
    $(function() {
        fullPage = new ddfullscreenslider({
            sliderid: 'fullPage',
            addHash: false,
            onslide: function($slide, index) {
                // alert('滚动到了第 ' + (index + 1) + ' 屏')
                if (index == 1) {
                    $('.slide2Box h1').addClass('animated rubberBand');
                    $('.slide2Box p').addClass('animated bounceInDown');
                    $('.slide2Box .cp_1').addClass('animated bounceInLeft');
                    $('.slide2Box .cp_2').addClass('animated bounceInRight');
                } else {
                    $('.slide2Box h1').removeClass('animated rubberBand');
                    $('.slide2Box p').removeClass('animated bounceInDown');
                    $('.slide2Box .cp_1').removeClass('animated bounceInLeft');
                    $('.slide2Box .cp_2').removeClass('animated bounceInRight');
                }
                if (index == 2) {
                    $('.slide3 .cp_3_wapper').addClass('animated fadeInUpBig');
                } else {
                    $('.slide3 .cp_3_wapper').removeClass('animated fadeInUpBig');
                }
            }
        });
    });

});

//  轮播图
(function(){
    // banner1
    var m = 1;
    var mytime = setInterval(scrollImageFirst, 3000);

    function scrollImageFirst(){
        if (m > 5) {
            m = 0;
        }
        control_imageFirst(m);
        control_iconFirst(m);
        m ++;
    }

    function control_imageFirst(n){
        $(".imglist a").eq(n).css('z-index', 1).fadeTo(500, 1).siblings('a').css('z-index', 0).delay(500).fadeTo(0, 0);
    }

    function control_iconFirst(n) {
        $(".iconlist li").eq(n).addClass('current').siblings('li').removeClass('current');
    }

    // $(".banner").mouseenter(function(){
    //     clearInterval(mytime);
    //     $("#slide_box").show();
    // }).mouseleave(function(){
    //     mytime = setInterval(scrollImageFirst, 3000);
    //     $("#slide_box").hide();
    // });

    var timer = null;
    $(".iconlist li").mouseenter(function(){
        var n = $(this).index();
        timer = setTimeout(function(){
            control_iconFirst(n);
            control_imageFirst(n);
            m = n + 1;
        }, 500)
    }).mouseleave(function(){
        clearTimeout(timer);
    })

    $("#right_slide").click(function(){
        if (m > 5) {
            m = 0;
        }
        control_imageFirst(m);
        control_iconFirst(m);
        m ++;
    });

    $("#left_slide").click(function(){
        m -= 2;
        if (m < 0) {
            m = 5;
        }
        control_iconFirst(m);
        control_imageFirst(m);
        m ++;
    })
})();


// 登录
$(function(){
    $('.userContent li').click(function(){
        $(this).removeClass('current').siblings('li').addClass('current');
    });
    $('.userContent li').eq(0).click(function(){
        $('.loginContent').show();
        $('.registerContent').hide();
    });
    $('.userContent li').eq(1).click(function(){
        $('.loginContent').hide();
        $('.registerContent').show();
    });
    $('.Login-reg').click(function(){
        $(".tanchu").show();
        $(".userContent").show();
    });
    // 弹出层点击关闭登录注册
    $('.tanchu').click(function(){
        $('.tanchu').hide();
        $('.userContent').hide();
    });
});
