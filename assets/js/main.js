/* Tap Trench — interactions. Page content is static HTML; this only adds behaviour. */
(function () {
  "use strict";
  var TT = window.TT || {};
  var root = document.documentElement;
  var EMAIL = document.body.getAttribute("data-email") || "";
  var ME = document.currentScript && document.currentScript.src.match(/[?&]v=([\w-]+)/);
  var AV = ME ? "?v=" + ME[1] : "";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  /* ---------- Theme ---------- */
  function isDark() { var t = root.getAttribute("data-theme"); return t ? t === "dark" : !!(window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches); }
  function syncThemeBtn() { $$("[data-theme-toggle]").forEach(function (b) { var d = isDark(); b.setAttribute("aria-label", d ? "Switch to light mode" : "Switch to dark mode"); $(".i-sun", b).toggleAttribute("hidden", !d); $(".i-moon", b).toggleAttribute("hidden", d); }); }
  syncThemeBtn();

  /* ---------- Forms (Google Forms embeds) ---------- */
  function formEmbed(url, title) {
    if (url) return '<iframe src="' + esc(url) + '" title="' + esc(title) + '" loading="lazy">Loading…</iframe>';
    return '<div class="form-fallback"><h3>Our form is getting a polish.</h3><p class="muted">In the meantime, email us and we\'ll reply within one business day.</p><a class="btn btn-copper" href="mailto:' + esc(EMAIL) + "?subject=" + encodeURIComponent(title) + '">' + esc(EMAIL) + '</a><p class="muted" style="font-size:14px">Email: <span style="user-select:all">' + esc(EMAIL) + "</span></p></div>";
  }

  /* ---------- Brand carousel (two rows, any number of brands) ---------- */
  var rows = $("[data-brands]");
  if (rows && (TT.brands || []).length) {
    var list = TT.brands, a = [], b = [];
    list.forEach(function (x, i) { (i % 2 ? b : a).push(x); });
    if (list.length < 12) { b = a = list; }
    function row(items, rev) {
      var one = items.map(function (x) { return '<div class="brand" title="' + esc(x.name) + '">' + (x.logo ? '<img src="' + esc(x.logo + AV) + '" alt="' + esc(x.name) + '" loading="lazy" decoding="async">' : '<span class="wordmark">' + esc(x.name) + "</span>") + "</div>"; }).join("");
      var dur = Math.max(30, items.length * 4.2);
      return '<div class="marquee' + (rev ? " reverse" : "") + '"><div class="marquee-track" style="--dur:' + dur + 's">' + one + one.replace(/class="brand"/g, 'class="brand" aria-hidden="true"') + "</div></div>";
    }
    rows.innerHTML = row(a, false) + row(b, true);
  }

  /* ---------- Shop filter ---------- */
  $$("[data-filter]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var f = btn.getAttribute("data-filter");
      $$("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === btn)); });
      $$("[data-cat]").forEach(function (c) { c.hidden = !(f === "all" || c.getAttribute("data-cat") === f); });
    });
  });

  /* ---------- Product gallery: thumbs, swipe, keyboard ---------- */
  var gal = $("[data-gallery]");
  if (gal) {
    var imgs = $$("img", gal), thumbs = $$("[data-thumb]"), cur = 0;
    function show(i) {
      cur = (i + imgs.length) % imgs.length;
      imgs.forEach(function (im, k) { im.classList.toggle("on", k === cur); });
      thumbs.forEach(function (t, k) { t.setAttribute("aria-current", String(k === cur)); });
    }
    thumbs.forEach(function (t, k) { t.addEventListener("click", function () { show(k); }); });
    var x0 = null;
    gal.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    gal.addEventListener("touchend", function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    gal.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") show(cur + 1); if (e.key === "ArrowLeft") show(cur - 1); });
  }

  /* ---------- Modal + drawer ---------- */
  var modal = $("[data-modal]"), drawer = $("[data-drawer]"), drawerBack = $("[data-drawer-back]"), lastFocus = null;
  function openWaitlist(what) {
    lastFocus = document.activeElement;
    var sub = $("[data-modal-sub]");
    sub.textContent = what === "checkout"
      ? "We're between production runs. Reserve your plates now and we'll contact you the moment the next batch is ready."
      : "This one sold out fast. Leave your details and we'll reserve one for you from the next production run.";
    var mb = $("[data-modal-body]");
    if (window.TTForms) {
      window.TTForms.render(mb, "waitlist", true);
      var match = what && what !== "checkout" ? $$('input[type="checkbox"]', mb).filter(function (c) { return what.indexOf(c.value.split(" — ")[0]) === 0; })[0] : null;
      if (match) match.checked = true;
    } else mb.innerHTML = formEmbed((TT.forms || {}).waitlist, "Tap Trench waitlist");
    modal.classList.add("open"); document.body.style.overflow = "hidden";
    setTimeout(function () { var c = $("[data-modal-close]"); if (c) c.focus(); }, 40);
  }
  function closeModal() { if (!modal) return; modal.classList.remove("open"); document.body.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
  function openDrawer() { drawer.classList.add("open"); drawerBack.classList.add("open"); }
  function closeDrawer() { drawer.classList.remove("open"); drawerBack.classList.remove("open"); }

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (t.closest("[data-theme-toggle]")) {
      var next = isDark() ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("tt-theme", next); } catch (err) {}
      syncThemeBtn();
    } else if (t.closest("[data-cart-open]")) openDrawer();
    else if (t.closest("[data-drawer-close]") || t.closest("[data-drawer-back]")) closeDrawer();
    else if (t.closest("[data-waitlist]")) { e.preventDefault(); closeDrawer(); openWaitlist(t.closest("[data-waitlist]").getAttribute("data-waitlist")); }
    else if (t.closest("[data-modal-close]") || t === modal) closeModal();
    else if (t.closest("[data-menu]")) {
      var m = $("#mobile-menu"), b = t.closest("[data-menu]"), open = m.classList.toggle("open");
      if (open) m.style.top = Math.max(0, $(".site-header").getBoundingClientRect().bottom) + "px";
      b.setAttribute("aria-expanded", String(open));
      $(".i-menu", b).toggleAttribute("hidden", open); $(".i-close", b).toggleAttribute("hidden", !open);
      document.body.style.overflow = open ? "hidden" : "";
    }
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeModal(); closeDrawer(); } });

  /* ---------- Header shadow ---------- */
  var hdr = $(".site-header");
  function onScroll() { if (hdr) hdr.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Reveal on scroll + number counters ---------- */
  function count(el) {
    var target = +el.getAttribute("data-count"), pre = el.getAttribute("data-prefix") || "", suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1700;
    if (reduce || !target) { el.textContent = pre + target.toLocaleString("en-AU") + suf; return; }
    (function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = pre + Math.round(target * e).toLocaleString("en-AU") + suf; if (k < 1) requestAnimationFrame(step); })(performance.now());
  }
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        $$("[data-count]", en.target).forEach(function (c) { if (!c._d) { c._d = 1; count(c); } });
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    $$(".reveal, [data-counters]").forEach(function (r) { io.observe(r); });
  } else {
    $$(".reveal").forEach(function (r) { r.classList.add("in"); });
    $$("[data-count]").forEach(count);
  }

  /* ---------- Tilt (mouse) + gentle scroll parallax (phones) ---------- */
  if (!reduce) {
    $$("[data-tilt]").forEach(function (el) {
      el.classList.add("tilt");
      el.addEventListener("pointermove", function (e) {
        if (e.pointerType !== "mouse") return;
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        el.style.transform = "perspective(900px) rotateY(" + (x * 8).toFixed(2) + "deg) rotateX(" + (-y * 8).toFixed(2) + "deg)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
    var par = $$("[data-parallax]");
    if (par.length) {
      var ticking = false;
      window.addEventListener("scroll", function () {
        if (ticking) return; ticking = true;
        requestAnimationFrame(function () {
          par.forEach(function (el) {
            var r = el.getBoundingClientRect(), mid = r.top + r.height / 2 - window.innerHeight / 2;
            el.style.translate = "0 " + (mid * -(+el.getAttribute("data-parallax") || .06)).toFixed(1) + "px";
          });
          ticking = false;
        });
      }, { passive: true });
    }
  }
})();
