/* ==========================================================================
   Halif Auto Repair and Collision — site behaviour
   Requires jQuery (loaded before this file).
   ========================================================================== */

(function ($) {
    "use strict";

    /* ------------------------------------------------ sticky header */
    function stickyHeader() {
        var $menu = $(".mainmenu-area.stricky");
        if (!$menu.length) return;
        var top = $menu.offset().top;
        var $spacer = $('<div class="h-sticky-spacer"></div>').insertAfter($menu).hide();

        function onScroll() {
            if ($(window).width() < 992) {
                $menu.removeClass("stricky-fixed");
                $spacer.hide();
                return;
            }
            if ($(window).scrollTop() > top + 40) {
                if (!$menu.hasClass("stricky-fixed")) {
                    $spacer.height($menu.outerHeight()).show();
                    $menu.addClass("stricky-fixed").css({
                        position: "fixed", top: 0, left: 0, right: 0, zIndex: 900
                    });
                }
            } else {
                $menu.removeClass("stricky-fixed").css({ position: "", top: "", left: "", right: "", zIndex: "" });
                $spacer.hide();
            }
        }
        $(window).on("scroll resize", onScroll);
        onScroll();
    }

    /* ------------------------------------------------ mobile dropdowns */
    function mobileMenu() {
        $(".main-menu .navigation > li.dropdown").each(function () {
            if (!$(this).children(".dropdown-btn").length) {
                $(this).append('<span class="dropdown-btn" role="button" tabindex="0" aria-label="Toggle submenu"><i class="fa fa-angle-down" aria-hidden="true"></i></span>');
            }
        });
        $(".main-menu").on("click keydown", ".dropdown-btn", function (e) {
            if (e.type === "keydown" && e.which !== 13 && e.which !== 32) return;
            e.preventDefault();
            var $ul = $(this).parent().children("ul");
            $(".main-menu .navigation > li > ul").not($ul).slideUp(200);
            $ul.slideToggle(220);
            $(this).find("i").toggleClass("fa-angle-down fa-angle-up");
        });
        // close the collapsed nav after tapping a link
        $(".main-menu .navigation a").on("click", function () {
            if ($(window).width() < 992 && !$(this).parent().hasClass("dropdown")) {
                $(".navbar-collapse").removeClass("in");
            }
        });
    }

    /* ------------------------------------------------ accordions */
    function accordions() {
        $(".accordion-box").each(function () {
            var $box = $(this);
            $box.find(".accord-btn").each(function () {
                var $btn = $(this),
                    expanded = $btn.hasClass("active");
                $btn.attr({ role: "button", tabindex: 0, "aria-expanded": expanded ? "true" : "false" });
                if (expanded) $btn.next(".accord-content").show();
            });
            $box.on("click keydown", ".accord-btn", function (e) {
                if (e.type === "keydown" && e.which !== 13 && e.which !== 32) return;
                e.preventDefault();
                var $btn = $(this),
                    $content = $btn.next(".accord-content");
                if ($btn.hasClass("active")) {
                    $btn.removeClass("active").attr("aria-expanded", "false");
                    $content.slideUp(240);
                } else {
                    $box.find(".accord-btn.active").removeClass("active").attr("aria-expanded", "false")
                        .next(".accord-content").slideUp(240);
                    $btn.addClass("active").attr("aria-expanded", "true");
                    $content.slideDown(240);
                }
            });
        });
    }

    /* ------------------------------------------------ FAQ category tabs */
    function faqTabs() {
        var $tabs = $(".h-tabs [data-faq-tab]");
        if (!$tabs.length) return;

        function show(key) {
            $tabs.removeClass("active").attr("aria-pressed", "false");
            $tabs.filter('[data-faq-tab="' + key + '"]').addClass("active").attr("aria-pressed", "true");
            if (key === "all") {
                $("[data-faq-group]").show();
            } else {
                $("[data-faq-group]").hide();
                $('[data-faq-group="' + key + '"]').show();
            }
        }
        $tabs.on("click", function (e) {
            e.preventDefault();
            show($(this).data("faq-tab"));
        });
        show($tabs.filter(".active").data("faq-tab") || "all");
    }

    /* ------------------------------------------------ photo estimate composer */
    function estimateForm() {
        var $form = $("#estimate-form");
        if (!$form.length) return;

        var PHONE = "19057306089";

        function val(name) {
            var el = $form.find('[name="' + name + '"]');
            if (el.is(":radio")) return $form.find('[name="' + name + '"]:checked').val() || "";
            return ($.trim(el.val() || ""));
        }

        function compose() {
            var lines = ["Hi Halif, I'd like a photo estimate."];
            var name = val("name"), vehicle = val("vehicle"), job = val("job"),
                safe = val("drivable"), ins = val("insurance"), msg = val("message");
            if (name) lines.push("Name: " + name);
            if (vehicle) lines.push("Vehicle: " + vehicle);
            if (job) lines.push("What happened: " + job);
            if (safe) lines.push("Safe to drive: " + safe);
            if (ins) lines.push("Insurance claim: " + ins);
            if (msg) lines.push("Notes: " + msg);
            lines.push("(Photos attached.)");
            return lines.join("\n");
        }

        function missing() {
            var gaps = [];
            if (!val("name")) gaps.push("your name");
            if (!val("vehicle")) gaps.push("your vehicle");
            return gaps;
        }

        function warn(gaps) {
            var $w = $("#estimate-warning");
            if (!gaps.length) { $w.attr("hidden", true).text(""); return false; }
            $w.removeAttr("hidden")
              .text("Add " + gaps.join(" and ") + " so we know whose car it is. You can still send without it.");
            return true;
        }

        $form.on("input change", "input, select, textarea", function () {
            warn([]);
            $("#estimate-preview").text(compose());
        });
        $("#estimate-preview").text(compose());

        $form.on("click", "[data-send]", function (e) {
            e.preventDefault();
            warn(missing());
            var text = compose();
            var how = $(this).data("send");
            if (how === "whatsapp") {
                window.open("https://wa.me/" + PHONE + "?text=" + encodeURIComponent(text), "_blank", "noopener");
            } else {
                window.location.href = "sms:+" + PHONE + "?&body=" + encodeURIComponent(text);
            }
        });

        $form.on("submit", function (e) { e.preventDefault(); });
    }

    /* ------------------------------------------------ today's hours highlight */
    function highlightToday() {
        var $rows = $("[data-day]");
        if (!$rows.length) return;
        var day = new Date().getDay(); // 0 = Sunday
        $rows.filter('[data-day="' + day + '"]').addClass("today");
    }

    /* ------------------------------------------------ scroll to top */
    function scrollTop() {
        var $btn = $(".scroll-to-top");
        if (!$btn.length) return;
        $btn.hide();
        $(window).on("scroll", function () {
            $(this).scrollTop() > 600 ? $btn.fadeIn(200) : $btn.fadeOut(200);
        });
        $btn.on("click keydown", function (e) {
            if (e.type === "keydown" && e.which !== 13 && e.which !== 32) return;
            e.preventDefault();
            $("html, body").animate({ scrollTop: 0 }, 500);
        });
    }

    /* ------------------------------------------------ in-page anchors */
    function smoothAnchors() {
        $('a[href^="#"]:not([href="#"])').on("click", function (e) {
            var $t = $(this.getAttribute("href"));
            if (!$t.length) return;
            e.preventDefault();
            $("html, body").animate({ scrollTop: $t.offset().top - 110 }, 450);
        });
    }

    /* ------------------------------------------------ reveal on scroll */
    function reveal() {
        if (window.WOW && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
            new WOW({ mobile: false, offset: 60 }).init();
        }
    }

    $(document).ready(function () {
        stickyHeader();
        mobileMenu();
        accordions();
        faqTabs();
        estimateForm();
        highlightToday();
        scrollTop();
        smoothAnchors();
        reveal();
    });
})(jQuery);
