"undefined" == typeof WJF && (WJF = {}), WJF.namespace = WJF.namespace || function (e) {
        if (e) {
            e = e.split(".");
            for (var t = window, n = 0, i = e.length; i > n; n++)t = t[e[n]] = t[e[n]] || {}
        }
    }, WJF.apply = function (e, t) {
    if (e && t && "object" == typeof t)for (var n in t)e[n] = t[n];
    return e
}, WJF.override = function (e, t) {
    if (t) {
        var n = e.prototype;
        WJF.apply(n, t), n.toString = t.toString
    }
}, WJF.extend = function () {
    var e = function (e) {
        for (var t in e)this[t] = e[t]
    }, t = Object.prototype.constructor;
    return function (n, i, o) {
        "object" == typeof i && (o = i, i = n, n = o.constructor != t ? o.constructor : function () {
                i.apply(this, arguments)
            });
        var s, r = function () {
        }, a = i.prototype;
        return r.prototype = a, s = n.prototype = new r, s.constructor = n, n.superclass = a, a.constructor == t && (a.constructor = i), n.override = function (e) {
            WJF.override(n, e)
        }, s.superclass = s.supr = function () {
            return a
        }, s.override = e, WJF.override(n, o), n.extend = function (e) {
            return WJF.extend(n, e)
        }, n
    }
}(), $.cookie = $.cookie || function (e, t, n) {
        if ("undefined" == typeof t) {
            var i = null;
            if (document.cookie && "" != document.cookie)for (var o = document.cookie.split(";"), s = 0; s < o.length; s++) {
                var r = jQuery.trim(o[s]);
                if (r.substring(0, e.length + 1) == e + "=") {
                    i = decodeURIComponent(r.substring(e.length + 1));
                    break
                }
            }
            return i
        }
        n = n || {}, null === t && (t = "", n = $.extend({}, n), n.expires = -1);
        var a = "";
        if (n.expires && ("number" == typeof n.expires || n.expires.toUTCString)) {
            var l;
            "number" == typeof n.expires ? (l = new Date, l.setTime(l.getTime() + 24 * n.expires * 60 * 60 * 1e3)) : l = n.expires, a = "; expires=" + l.toUTCString()
        }
        var c = n.path ? "; path=" + n.path : "", u = n.domain ? "; domain=" + n.domain : "", h = n.secure ? "; secure" : "";
        document.cookie = [e, "=", encodeURIComponent(t), a, c, u, h].join("")
    }, WJF.namespace("WJF.util"), WJF.util = {
    extend: jQuery.extend, log: function () {
        console && console.log.apply(console, arguments)
    }, error: function (e) {
        return console ? 1 == arguments.length && arguments[0] instanceof Error ? (console.error(e.message), void console.error(e.stack)) : void console.error.apply(console, arguments) : void 0
    }, json2str: function (e) {
        return JSON.stringify(e || {})
    }, generateUUid: function (e) {
        e = e || "";
        for (var t, n = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split(""), i = n, o = new Array(36), s = 0, r = 0; 36 > r; r++)8 == r || 13 == r || 18 == r || 23 == r ? o[r] = "-" : 14 == r ? o[r] = "4" : (2 >= s && (s = 33554432 + 16777216 * Math.random() | 0), t = 15 & s, s >>= 4, o[r] = i[19 == r ? 3 & t | 8 : t]);
        return e + o.join("").replace(/-/g, "")
    }, dataFormat: function (e, t) {
        t = t || new Date;
        var n = {
            "M+": t.getMonth() + 1,
            "d+": t.getDate(),
            "h+": t.getHours(),
            "m+": t.getMinutes(),
            "s+": t.getSeconds(),
            "q+": Math.floor((t.getMonth() + 3) / 3),
            S: t.getMilliseconds()
        };
        /(y+)/.test(e) && (e = e.replace(RegExp.$1, (t.getFullYear() + "").substr(4 - RegExp.$1.length)));
        for (var i in n)new RegExp("(" + i + ")").test(e) && (e = e.replace(RegExp.$1, 1 == RegExp.$1.length ? n[i] : ("00" + n[i]).substr(("" + n[i]).length)));
        return e
    }, getUrlParams: function (e) {
        var t = new RegExp("(^|&)" + e + "=([^&]*)(&|$)"), n = window.location.search.substr(1).match(t);
        return null != n ? unescape(n[2]) : null
    }, cookie: function (e, t, n) {
        $.cookie(e, t, n)
    }
}, WJF.namespace("WJF.uiTool"), WJF.uiTool = {
    initTab: function (e, t) {
        t = t || {};
        var n = (t.activeCls ? t.activeCls + " active" : "") || "active", i = $("#" + e), o = i.find("a.active"), s = o.attr("data-target"), r = null;
        $("#" + s).removeClass(n).addClass(n), i.on("click", "li", function (i) {
            if (!t.onBeforeChange || t.onBeforeChange(e, $(this), i) !== !1) {
                $("#" + s).removeClass(n), o.removeClass(n), r = o, o = $(this).find("a"), o.removeClass(n).addClass(n);
                var a = o.attr("data-target");
                $("#" + a).removeClass(n).addClass(n), a != s && t.onTabChange && t.onTabChange(e, $(this), a, s, r, o, i), s = a
            }
        })
    }, placeholder: function (e) {
        "placeholder" in document.createElement("input") || $(e || "[placeholder]").focus(function () {
            var e = $(this);
            e.val() == e.attr("placeholder") && (e.val(""), e.removeClass("placeholder"))
        }).blur(function () {
            var e = $(this);
            "" == e.val() || e.val() == e.attr("placeholder") ? (e.hasClass("placeholder") || e.addClass("placeholder"), e.val(e.attr("placeholder"))) : e.removeClass("placeholder")
        }).blur()
    }
}, WJF.namespace("WJF.html"), WJF.html = {
    getAreaData: function (e) {
        for (var t = $("#" + e).serializeArray(), n = {}, i = 0, o = t.length; o > i; i++) {
            var s = t[i];
            n[s.name] = s.value
        }
        return n
    }, clearAreaData: function (e) {
        var t = null;
        e && (t = $("string" == typeof e ? "#" + e : e), $("input,select,textarea", t).each(function () {
            var e = this.type, t = this.tagName.toLowerCase();
            if ("disabled" != $(this).attr("disabled"))if ("text" == e || "hidden" == e || "password" == e || "textarea" == t) this.value = ""; else if ("file" == e) {
                var n = $(this);
                n.after(n.clone().val("")), n.remove()
            } else"checkbox" == e || "radio" == e ? this.checked = !1 : "select" == t && (this.selectedIndex = -1)
        }))
    }, setAreaData: function (e, t) {
        if (!$.isEmptyObject(t)) {
            var n = null;
            n = $("string" == typeof e ? "#" + e : e);
            for (var i in t) {
                var o = n.find("[name=" + i + "]");
                if (o.length) {
                    var s = o[0];
                    if ("radio" == s.type || "checkbox" == s.type) {
                        var r = t[i];
                        r instanceof Array || (r = [r]);
                        for (var a = 0, l = r.length; l > a; a++)for (var c = 0, u = o.length; u > c; c++)o[c].value == r[a] && (o[c].checked = !0)
                    }
                    if ("select-one" == s.type && o.each(function () {
                            $(this).val(t[i])
                        }), "select-multiple" == s.type) {
                        var r = t[i];
                        r instanceof Array || (r = [r]), o.each(function () {
                            for (var e = $(this).find("option"), t = 0, n = e.length; n > t; t++)for (var i = 0, o = r.length; o > i; i++)e[t].value == r[i] && (e[t].selected = !0)
                        })
                    }
                    ("text" == s.type || "hidden" == s.type) && o.each(function () {
                        $(this).val(t[i])
                    })
                }
            }
        }
    }
}, WJF.event = function () {
    function e(e) {
        var t = ++o + "";
        return e ? e + t : t
    }

    function t(e, n, i, o) {
        e._events = e._events || {};
        var s = null;
        if (o) {
            if (!e._listenId || !e._listeners)return;
            if (s = e._listenId, o.objId !== s)return
        }
        if (s)if (n) {
            for (var r = e._events[n] || [], a = 0; a < r.length; a++) {
                var l = r[a];
                if (i) {
                    if (l.callback === i && l.listening.objId === s) {
                        r.splice(a, 1);
                        break
                    }
                } else l.listening && l.listening.objId === s && (r.splice(a, 1), a--)
            }
            0 == r.length && (e._events = void 0)
        } else {
            var c = e._events;
            for (var u in c)t(e, u, i, o)
        } else {
            if (!n)return void delete e._events;
            if (!i)return void delete e._events[n];
            for (var r = e._events[n] || [], a = 0, h = r.length; h > a; a++) {
                var l = r[a];
                if (l.callback === i) {
                    r.splice(a, 1);
                    break
                }
            }
            0 == r.length && (e._events = void 0)
        }
    }

    function n(e, t, n, i, o) {
        var s = e._events || (e._events = {}), r = s[t] || (s[t] = []), i = i || e;
        if (o) {
            var a = e._listeners || (e._listeners = {});
            a[o.id] = o
        }
        r.push({callback: n, context: i, ctx: e, listening: o})
    }

    function i(e, t) {
        e._events = e._events || {};
        var n = e._events[t];
        if (n)for (var i = Array.prototype.slice.call(arguments, 2), o = !0, s = 0, r = n.length; r > s; s++) {
            var a = n[s];
            if (o = a.callback.apply(a.context, i), o === !1)return
        }
    }

    var o = 0;
    return {
        extend: function (e) {
            for (var t in WJF.event)"function" == typeof WJF.event[t] && (e[t] = WJF.event[t]);
            return e
        }, fire: function (e) {
            if (!e)throw"Error: fire function ��������ȷ !";
            var t = Array.prototype.slice.call(arguments, 0);
            return t.splice(0, 0, this), i.apply(this, t), this
        }, on: function (e, t, i) {
            if (!e || !t)throw"Error: ���� on ��������ȷ, eventName = " + e + " callback = " + t;
            return n(this, e, t, i), this
        }, once: function (e, t, n) {
            if (!e || !t)throw"Error: ���� once ��������ȷ, ��������ȷ��";
            var i = t;
            if (!e || !t)throw"error: eventName = " + e + " callback = " + t;
            var o = this;
            return t = function () {
                return o.off(e, t), i.apply(this, arguments)
            }, this.on(e, t, n), this
        }, off: function (e, n) {
            return t(this, e, n), this
        }, listenTo: function (t, i, o, s) {
            if (!t || !i || !o)throw"Error: listenToOnce ��������ȷ��";
            var r = t._listenId || (t._listenId = e("l")), a = this._listeningTo || (this._listeningTo = {}), l = a[r];
            if (!l) {
                var c = this._listenId || (this._listenId = e("l"));
                l = a[r] = {obj: t, objId: r, id: c, listeningTo: a, count: 0}
            }
            return n(t, i, o, s, l), this
        }, listenToOnce: function (e, n, i, o) {
            if (!e || !n || !i)throw"Error: listenToOnce ��������ȷ��";
            var s = this, r = i;
            return i = function () {
                return t(e, n, i, s._listeningTo[e._listenId]), r.apply(this, arguments)
            }, this.listenTo(e, n, i, o), this
        }, stopListening: function (e, n, i) {
            var o = this._listeningTo;
            if (!o)return this;
            var s;
            if (e) s = [e._listenId]; else {
                s = [];
                for (var r in o)s.push(r)
            }
            for (var a = 0; a < s.length; a++) {
                var l = o[s[a]];
                if (!l)break;
                t(l.obj, n, i, l)
            }
            var c = !1;
            for (var r in o) {
                c = !0;
                break
            }
            return c || (this._listeningTo = void 0), this
        }
    }
}(), WJF.event.bind = WJF.event.on, WJF.event.unbind = WJF.event.off, WJF.event.trigger = WJF.event.fire, WJF.namespace("WJF.ui"), WJF.ui.componentMgr = function () {
    var e = {};
    return {
        get: function (t) {
            return e[t]
        }, reg: function (t) {
            e[t.getId()] = t
        }, remove: function (t) {
            e[t] = void 0
        }, clear: function () {
            e = {}
        }
    }
}(), WJF.namespace("WJF.ui"), WJF.ui.component = function (e) {
    if (!this.validateParam(e))throw"component [ " + this.getClassName() + " ] params validate fail ...";
    this.options = e, this.id = e.id, this.params = e.params, this.com = $("#" + e.dom), this.id || (this.id = this.generateId()), this.com && (this.com.attr("componentId", this.id), this.com.attr("componentType", this.getClassName())), this._init(e), WJF.ui.componentMgr.reg(this), this._afterInit(this.options)
}, WJF.event.extend(WJF.ui.component.prototype), WJF.apply(WJF.ui.component.prototype, {
    constructor: WJF.ui.component,
    _super: function () {
        var e, t, n = arguments.callee.caller;
        for (var i in this)if (n === this[i]) {
            e = i;
            break
        }
        t = WJF.ui.component.prototype[e], "function" == typeof t && t.apply(this, arguments)
    },
    events: null,
    proxyDom: null,
    _proxyEvent: function (e) {
        var t = this;
        if (this.events) {
            var n = this.events, i = this.proxyDom || this.com;
            for (var o in n) {
                var s = "_" == o ? null : o, r = n[o];
                for (var a in r) {
                    var l = r[a];
                    e ? (r[a] = function (e) {
                            return function (n) {
                                return e ? e.call(t, this, n) : void 0
                            }
                        }(l), i.on(a, s, r[a])) : i.off(a, s, l)
                }
            }
        }
    },
    rebindEvent: function () {
        this._proxyEvent(!1), this.regEvent && this.regEvent(), this._proxyEvent(!0)
    },
    _init: function (e) {
        this.init(e), this._proxyEvent(!0)
    },
    _afterInit: function (e) {
        this.afterInit && this.afterInit(e), e.validateInit === !0 && this.validate()
    },
    init: function () {
    },
    getId: function () {
        return this.id
    },
    validateParam: function () {
        return !0
    },
    show: function () {
        this.com.show()
    },
    hide: function () {
        this.com.hide()
    },
    isVisible: function () {
        return this.com.is(":visible")
    },
    toggle: function () {
        this.isVisible() ? this.hide() : this.show()
    },
    generateId: function () {
        for (var e, t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".split(""), n = t, i = new Array(36), o = 0, s = 0; 36 > s; s++)8 == s || 13 == s || 18 == s || 23 == s ? i[s] = "-" : 14 == s ? i[s] = "4" : (2 >= o && (o = 33554432 + 16777216 * Math.random() | 0), e = 15 & o, o >>= 4, i[s] = n[19 == s ? 3 & e | 8 : e]);
        return i.join("").replace(/-/g, "")
    },
    focus: function () {
        this.com.focus()
    },
    set: function (e, t) {
        this.options[e] = t
    },
    get: function (e) {
        return e ? this.options[e] : this.options
    },
    validate: function (e) {
        return this.options.validateable !== !0 ? !0 : this._commonValidate(e)
    },
    _commonValidate: function () {
        var e = this.options.validType || [], t = this.options.errorMsg || [];
        "string" == typeof e && (e = [e]), "string" == typeof t && (t = [t]);
        for (var n, i, o, s = !0, r = "", a = this.getValue(), l = 0, c = e.length; c > l; l++)if (n = e[l], "function" == typeof n ? i = n : (/([a-zA-Z0-9_]+)\[(.*)\]/.test(n) ? (o = RegExp.$2, o = o.split(","), n = RegExp.$1) : o = null, i = WJF.validator.base[n]), i && (s = i.call(this, a, o), s === !1)) {
            r = t[l];
            break
        }
        return s
    },
    clear: function () {
    },
    clearErrorInfo: function () {
    },
    getClassName: function () {
        return "WJF.ui.component"
    },
    getName: function () {
        return this.options.name
    },
    destroy: function () {
        this.off(), this.stopListening(), this.com.off(), this._proxyEvent(!1), this.params = null, this.proxyDom = null, this.com.remove(), WJF.ui.componentMgr.remove(this.id), this.com = null, this.options = null, this.id = null
    }
}), WJF.namespace("WJF.ui.select"), WJF.ui.select = WJF.extend(WJF.ui.component, {
    init: function (e) {
        this.conf = e = WJF.apply({
            placeholder: "��ѡ��",
            width: 150,
            selContainerW: null,
            selContainerH: "auto",
            selContainerMaxHeight: 400,
            data: [],
            defaultValue: null,
            selectContainerSelector: null,
            autoFill: !0
        }, e), this.render(), this.adjustStyle(), this.regEvent()
    }, regEvent: function () {
        this.events = {
            _: {
                click: function () {
                    this.com.hasClass("wjf-ui-select-disabled") || this.selectContainer.toggle(), WJF.event.fire("WJF-UI-SELECT-ACTIVE", this)
                }
            }
        };
        var e = this;
        this.selectContainer.on("click", "li.item", function (t) {
            return $(this).hasClass("disabled") || (e.selectItem($(this)), e.selectContainer.hide()), t.stopPropagation(), !1
        }), this.selectContainer.on("mouseover", "li.item", function () {
            $(this).hasClass("wjf-ui-select-item-hover") || $(this).addClass("wjf-ui-select-item-hover")
        }).on("mouseleave", "li.item", function () {
            $(this).removeClass("wjf-ui-select-item-hover")
        }), $(document).on("click", function (t) {
            $(t.target).hasClass("wjf-ui-select") || e.selectContainer.hide()
        }), WJF.event.on("WJF-UI-SELECT-ACTIVE", function (t) {
            e !== t && e.selectContainer.hide()
        })
    }, render: function () {
        var e = this.conf;
        if (this.com.removeClass("wjf-ui-select").addClass("wjf-ui-select"), null == e.selectContainerSelector) {
            var t = [];
            t.push('<ul class="wjf-ui-select-container">');
            var n = '<i class="trangle-arrow pngFix"></i>';
            e.showPlaceholder === !0 && t.push('<li class="item first' + (null == e.defaultValue || "" == e.defaultValue ? "selected" : "") + '" data-value="">' + e.placeholder + n + "</li>");
            for (var i = 0, o = e.data.length; o > i; i++) {
                var s = e.data[i];
                "string" == typeof s && (s = {value: s, desc: s});
                var r = null != e.defaultValue && s.value == e.defaultValue ? " selected " : "";
                0 == i && e.showPlaceholder !== !0 && (r += " first "), i == o - 1 && (r += " last "), t.push('<li class="item ' + r + '" data-value="' + s.value + '" data-desc="' + s.desc + '">' + s.desc + (0 == i ? n : "") + "</li>")
            }
            t.push("</ul>"), this.selectContainer = $(t.join("")).insertAfter(this.com)
        } else this.selectContainer = $(e.selectContainerSelector);
        var a = this.selectContainer.find("li.selected");
        a.length && this.selectItem(a)
    }, adjustStyle: function () {
        var e = this.conf;
        this.com.width(e.width - 2 - 8 - 15), null == e.selectContainerSelector && (this.selectContainer.width(e.selContainerW || e.width - 2), this.selectContainer.height(e.selContainerH)), e.selContainerMaxHeight && this.selectContainer.css("max-height", e.selContainerMaxHeight + "px"), this.com.css("background-position", e.width - 2 - 8 - 15 + 9 + "px -42px")
    }, afterInit: function () {
    }, selectItem: function (e) {
        if (e = e || this.selectContainer.find("li.selected"), 0 != e.length || (e = this.selectContainer.find("li").eq(0), 0 != e.length)) {
            var t = e.attr("data-desc");
            null == t && (t = e.text());
            var n = e.html(), i = e.attr("data-value");
            this.selectContainer.find("li.item").removeClass("selected"), e.addClass("selected"), this.conf.onSelect && this.conf.onSelect.call(this, i, t, e), this.conf.autoFill !== !1 && this.com.html(n)
        }
    }, unselectAll: function () {
        this.selectContainer.find("li").removeClass("selected"), this.selectItem()
    }, expandItems: function () {
        this.selectContainer.show()
    }, collapseItems: function () {
        this.selectContainer.hide()
    }, enableItem: function (e) {
        this.selectContainer.find("li").eq(e).removeClass("disabled")
    }, disableItem: function (e) {
        this.selectContainer.find("li").eq(e).addClass("disabled")
    }
}), WJF.apply(WJF.ui.select.prototype, {
    getClassName: function () {
        return "WJF.ui.select"
    }, getValue: function () {
        var e = this.selectContainer.find("li.selected");
        return e.length ? e.attr("data-value") : null
    }, setValue: function (e) {
        var t = null, n = this.selectContainer.find("li.item");
        n.each(function () {
            return $(this).attr("data-value") == e ? (t = $(this), !1) : void 0
        }), t && this.selectItem(t)
    }, disable: function () {
        this.selectContainer.hide(), this.com.addClass("wjf-ui-select-disabled")
    }, enable: function () {
        this.com.removeClass("wjf-ui-select-disabled")
    }
});