window._browserIsNotSupported = true;
if(window.attachEvent){
  window.attachEvent('onload', function(){
    var lowestSupportedIEVersion = 9;
    if(window.LOWEST_IE_VERSION != undefined){
      lowestSupportedIEVersion = window.LOWEST_IE_VERSION;
    }
    var el = document.createElement('div'),
        elStyle = el.style,
        docBody = document.getElementsByTagName('body')[0],
        linkStyle = 'color:#06F;text-decoration: underline;';
    el.innerHTML =  '尊敬的用户：<br />'+
        '使用控制台需要安装Internet Explorer更新版本的浏览器，'+
        '请<a href="http://windows.microsoft.com/zh-cn/internet-explorer/download-ie" style="'+linkStyle+'" target="_blank">下载安装IE' + lowestSupportedIEVersion + '</a>（或更新）。'+
        '也可以在其他浏览器，'+
        '如<a href="http://www.google.com/intl/zh-CN/chrome/" style="'+linkStyle+'" target="_blank">Chrome</a>'+
        '或<a href="http://www.firefox.com.cn/download/" style="'+linkStyle+'" target="_blank">Firefox</a>火狐中打开控制台。';
    // elStyle.width = '100%';
    elStyle.width = '720px';
    elStyle.color = '#000';
    elStyle.fontSize = '14px';
    elStyle.lineHeight = '180%';
    elStyle.margin = '60px auto';
    elStyle.backgroundColor = '#fffbd5';
    elStyle.border = '1px solid #CCC';
    elStyle.padding = '24px 48px';
    // elStyle.background = '#F00 url(styles/images/not-support-ie67.png) 48px 48px no-repeat';
    // elStyle.padding = '40px 40px 48px 160px';
    docBody.innerHTML = '';
    docBody.appendChild(el);
    // docBody.insertBefore(el,docBody.firstChild);
  });
}