// /**
//  * Created by YIn on 2017/3/7.
//  */
// $(function(){
//     var fullPage;
//     $(function() {
//         fullPage = new ddfullscreenslider({
//             sliderid: 'fullPage',
//             addHash: false,
//             onslide: function($slide, index) {
//                 // alert('滚动到了第 ' + (index + 1) + ' 屏')
//                 if (index == 1) {
//                     $('.slide2Box h1').addClass('animated rubberBand');
//                     $('.slide2Box p').addClass('animated bounceInDown');
//                     $('.slide2Box .cp_1').addClass('animated bounceInLeft');
//                     $('.slide2Box .cp_2').addClass('animated bounceInRight');
//                 } else {
//                     $('.slide2Box h1').removeClass('animated rubberBand');
//                     $('.slide2Box p').removeClass('animated bounceInDown');
//                     $('.slide2Box .cp_1').removeClass('animated bounceInLeft');
//                     $('.slide2Box .cp_2').removeClass('animated bounceInRight');
//                 }
//                 if (index == 2) {
//                     $('.slide3 .cp_3_wapper').addClass('animated fadeInUpBig');
//                 } else {
//                     $('.slide3 .cp_3_wapper').removeClass('animated fadeInUpBig');
//                 }
//             }
//         });
//     });
//
// });
//
// //  轮播图
// (function(){
//     // banner1
//     var m = 1;
//     var mytime = setInterval(scrollImageFirst, 3000);
//
//     function scrollImageFirst(){
//         if (m > 5) {
//             m = 0;
//         }
//         control_imageFirst(m);
//         control_iconFirst(m);
//         m ++;
//     }
//
//     function control_imageFirst(n){
//         $(".imglist a").eq(n).css('z-index', 1).fadeTo(500, 1).siblings('a').css('z-index', 0).delay(500).fadeTo(0, 0);
//     }
//
//     function control_iconFirst(n) {
//         $(".iconlist li").eq(n).addClass('current').siblings('li').removeClass('current');
//     }
//
//     // $(".banner").mouseenter(function(){
//     //     clearInterval(mytime);
//     //     $("#slide_box").show();
//     // }).mouseleave(function(){
//     //     mytime = setInterval(scrollImageFirst, 3000);
//     //     $("#slide_box").hide();
//     // });
//
//     var timer = null;
//     $(".iconlist li").mouseenter(function(){
//         var n = $(this).index();
//         timer = setTimeout(function(){
//             control_iconFirst(n);
//             control_imageFirst(n);
//             m = n + 1;
//         }, 500)
//     }).mouseleave(function(){
//         clearTimeout(timer);
//     })
//
//     $("#right_slide").click(function(){
//         if (m > 5) {
//             m = 0;
//         }
//         control_imageFirst(m);
//         control_iconFirst(m);
//         m ++;
//     });
//
//     $("#left_slide").click(function(){
//         m -= 2;
//         if (m < 0) {
//             m = 5;
//         }
//         control_iconFirst(m);
//         control_imageFirst(m);
//         m ++;
//     })
// })();
//
//
// // 登录
// $(function(){
//     $('.userContent li').click(function(){
//         $(this).removeClass('current').siblings('li').addClass('current');
//     });
//     $('.userContent li').eq(0).click(function(){
//         $('.loginContent').show();
//         $('.registerContent').hide();
//     });
//     $('.userContent li').eq(1).click(function(){
//         $('.loginContent').hide();
//         $('.registerContent').show();
//     });
//     $('.Login-reg').click(function(){
//         $(".tanchu").show();
//         $(".userContent").show();
//     });
//     // 弹出层点击关闭登录注册
//     $('.tanchu').click(function(){
//         $('.tanchu').hide();
//         $('.userContent').hide();
//     });
// });


var mySwiper = new Swiper('.swiper-container', {
    autoplay: 3000,
    pagination: '.swiper-pagination',
    slidesPerView: 1,
    paginationClickable: true,
    spaceBetween: 0,
    loop: true,
    autoplayDisableOnInteraction: false,
    onSlideChangeStart: function (swiper) {
        // 每个文字都执行一遍animate还有图片
    }
});

// nav hover
$(function () {
    $('.topbarWapper .common-topbar-nav-list li').hover(function () {
        $('span', this).stop().css('height', '2px');
        $('span', this).animate({
            left: '0',
            width: '100%',
            right: '0'
        }, 200);
    }, function () {
        $('span', this).stop().animate({
            left: '50%',
            width: '0'
        }, 200);
    });
    var a = null;
    $('.video_link').click(function () {
        $('#my-player').css({
            "width": "100%",
            "height": "100%"
        });
        $(this).hide();
        $('.cha').show();
        var options = {autoplay: true};
        var player = videojs("my-player", options, function onPlayerReady() {
            this.src('/static/assets/video/trailer.mp4');
            this.play();
            this.enterFullWindow();
            a = player;
        });
        $('.vjs-button').click();
    });
    $('.cha').click(function () {
        $(this).hide();
        $('.video_link').show();
        a.pause();
        $('#my-player').css({
            "width": "0",
            "height": "0"
        });
    });
});