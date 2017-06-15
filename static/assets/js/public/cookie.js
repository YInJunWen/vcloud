/**  * 设置cookie
	* @param key cookie的键值
	* @param value cookie的值
	* @param date 过期的时间点 date对象 默认 关闭浏览器cookie消失
	* @param path cookie的有效路径 		默认当前目录
	* @param domain cookie的有效域名 	默认当前域名
	* @param secure 是否只在https下使用 	默认 fasle
*/
function setCookie(key, value, date, path, domain, secure) {
	var date_string="";
	if (date !== undefined) {
		date_string = ";expires="+date.toUTCString();
	}

	var path_string = "";
	if (path !== undefined) {
		path_string = ";path="+path;
	}

	var domain_string = "";
	if (domain !== undefined) {
		domain_string = ";domain="+domain;
	}

	var secure_string = "";
	if (secure !== undefined) {
		secure_string = ";true";
	}

	document.cookie = key+"="+value+date_string+path_string+domain_string+secure_string;
}

/*删除cookie的方法*/
function deleteCookie(key, path) {
	var path_string = "";
	if (path !== undefined) {
		path_string = ";path="+path;
	}
	var date = new Date();
	date.setTime(date.getTime() - 1);

	setCookie(key, "", date, path);
}

/*读取cookie的方法*/
function getCookie(key) {
	console.log(document.cookie);
	//把字符串分割为数组
	var cookie_list = document.cookie.split("; ");

	console.log(cookie_list);
	//遍历数组
	for (var i =0 ; i < cookie_list.length; i ++) {
		var cookie_item = cookie_list[i].split("=");
		if (cookie_item[0] === key) {
			return cookie_item[1];
		}
	}
}