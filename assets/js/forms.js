/* Tap Trench — native on-page forms.
   Each form posts straight into its Google Form, so every response still lands in the
   "Tap Trench — Website form responses" Google Sheet. No embedded Google box, no double scrolling.
   Field "entry" numbers come from the live Google Forms; don't change them unless the forms change. */
(function () {
  "use strict";

  var PLATES = ["Star Tile — Google Review Tap Plate (square)", "Menu Tile — Tap-to-Order Menu Plate (square)", "Menu Disc — Tap-to-Order Menu Plate (round)"];

  var FORMS = {
    activate: {
      id: "1FAIpQLSelJHY2-ykU2Tcx6N6MfOp8g4mNb7dVfue6CrZJ1WusC9VIUw",
      gPages: 4, /* sections in the Google Form (the website groups them into 3 steps) */
      submit: "Activate my plates",
      done: ["You're all set", "We'll program and lock your plates and email you as soon as they're ready."],
      pages: [
        { title: "You", fields: [
          { e: 1191842036, l: "Your name", req: 1, ac: "name" },
          { e: 977231918, l: "Email", t: "email", req: 1, h: "We'll confirm here once your plates are ready.", ac: "email" },
          { e: 1121151606, l: "Business name", req: 1, h: "As it appears on Google.", ac: "organization" },
          { e: 2078343194, l: "Mobile", t: "tel", ph: "+61 400 000 000", ac: "tel" }
        ] },
        { title: "Your plates", fields: [
          { t: "qty", req: 1, l: "How many of each?", e: 1881732209, qe: 837839969, o: [
            { v: PLATES[0], n: "Star Tile", d: "Google review · square", k: "review" },
            { v: PLATES[1], n: "Menu Tile", d: "Menu · square", k: "menu" },
            { v: PLATES[2], n: "Menu Disc", d: "Menu · round", k: "menu" }
          ] },
          { e: 1661595896, l: "Where did you get them?", t: "radio", inline: 1, def: 0, o: ["In person from a Tap Trench rep", "Tap Trench website", "A Tap Trench reseller"] },
          { e: 1059352874, l: "Order number", h: "Only if you bought online. It's in your order confirmation email." }
        ] },
        { title: "Your link", intro: "This is the page your customers see when they tap. Once programmed, it's locked for security and can't be changed, so please double-check it.", fields: [
          { e: 1454471007, l: "Google review link", t: "url", show: "review", ph: "https://g.page/r/…/review", guide: [
            "Open Google Maps and find your business (sign in with the account that manages it).",
            "Tap “Get more reviews” (or “Ask for reviews”).",
            "Tap “Copy link” and paste it here."
          ], h: "Can't find it? Leave it blank and we'll help you by email." },
          { e: 1394165780, l: "Menu or ordering link", t: "url", show: "menu", ph: "https://", h: "Open your online menu and copy the address from the address bar. Can't find it? Leave it blank and we'll help." },
          { e: 1917050677, l: "Different links for different plates?", t: "textarea", rows: 2, h: "e.g. one plate per location. Tell us which link goes on which plate." },
          { e: 1073334593, l: "Please confirm", t: "checkbox", req: 1, o: ["I have checked my link(s). I understand they will be permanently locked into my plate(s) and can't be changed afterwards."] },
          { e: 75011998, l: "Anything else?", t: "textarea", rows: 2 }
        ] }
      ]
    },
    contact: {
      id: "1FAIpQLSfKthNAHmzDUIqPO019fQp1FeY0tbluP2kq6H6indL0T3vzVg",
      submit: "Send message",
      done: ["Message sent", "Thanks for getting in touch. We'll reply within one business day."],
      pages: [{ fields: [
        { e: 439858152, l: "Your name", req: 1, ac: "name", half: 1 },
        { e: 1839830431, l: "Email address", t: "email", req: 1, ac: "email", half: 1 },
        { e: 72893454, l: "Phone (optional)", t: "tel", ac: "tel", half: 1 },
        { e: 53414566, l: "Business name (optional)", ac: "organization", half: 1 },
        { e: 14704229, l: "What is it about?", t: "select", req: 1, o: ["A question about our plates", "My order or shipping", "Help activating my plate", "Bulk or multi-venue order", "Reselling Tap Trench", "Something else"] },
        { e: 1232290927, l: "Your message", t: "textarea", req: 1, rows: 6 }
      ] }]
    },
    reseller: {
      id: "1FAIpQLScsPGbOgSkFe8vy9XreZ3D2eiPoPhlGFFlsInR5eMmXDTRd3A",
      submit: "Send application",
      done: ["Application received", "Thanks for your interest in reselling Tap Trench. Our team will be in touch soon."],
      pages: [{ fields: [
        { e: 1739788179, l: "Your full name", req: 1, ac: "name", half: 1 },
        { e: 1502747306, l: "Email address", t: "email", req: 1, ac: "email", half: 1 },
        { e: 1823687491, l: "Mobile number (with country code)", t: "tel", req: 1, ac: "tel", half: 1 },
        { e: 922586716, l: "Company name", ac: "organization", half: 1 },
        { e: 1030268805, l: "Country", req: 1, ac: "country-name", half: 1 },
        { e: 1357244596, l: "City / region", req: 1, ac: "address-level2", half: 1 },
        { e: 1152966478, l: "Website or social page" },
        { e: 429060613, l: "What best describes you?", t: "checkbox", req: 1, o: ["Marketing or digital agency", "Web designer / developer", "POS, printing or signage supplier", "Business consultant", "Retail store", "Hospitality supplier"], other: 1 },
        { e: 1942020601, l: "How many businesses could you reach each month?", t: "radio", req: 1, o: ["1–10", "11–50", "51–200", "200+"], inline: 1 },
        { e: 778545400, l: "Tell us a bit about how you'd sell Tap Trench", t: "textarea" }
      ] }]
    },
    waitlist: {
      id: "1FAIpQLSfNkJOBpv83-4DCIfs3AF4ynWyCVLx0c0_VzwwMpOjKveO1Tw",
      submit: "Join the waitlist",
      done: ["You're on the list", "We'll email you before the next batch ships so you can confirm your order."],
      pages: [{ fields: [
        { e: 1272522977, l: "Your name", req: 1, ac: "name", half: 1 },
        { e: 264932925, l: "Email address", t: "email", req: 1, ac: "email", half: 1 },
        { e: 421401668, l: "Mobile number (optional)", t: "tel", ac: "tel", half: 1 },
        { e: 195636436, l: "Business name", req: 1, ac: "organization", half: 1 },
        { e: 1134026545, l: "Country", req: 1, ac: "country-name", half: 1 },
        { e: 1927094654, l: "Roughly how many?", half: 1 },
        { e: 27757956, l: "Which plates would you like?", t: "checkbox", req: 1, o: PLATES },
        { e: 760654126, l: "Keep me posted", t: "checkbox", req: 1, o: ["Email me when the next batch is ready"] }
      ] }]
    }
  };

  var EMAIL = document.body.getAttribute("data-email") || "";
  var uid = 0;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function qtyHtml(f, key) {
    var rows = f.o.map(function (p, i) {
      var id = "q-" + key + "-" + i;
      return '<div class="f-qty-row"><label for="' + id + '"><b>' + esc(p.n) + "</b><small>" + esc(p.d) + '</small></label>' +
        '<div class="f-stepper"><button type="button" data-step-btn="-1" aria-label="One fewer ' + esc(p.n) + '">−</button>' +
        '<input id="' + id + '" type="number" inputmode="numeric" min="0" max="999" value="0" data-qty="' + esc(p.v) + '" data-qname="' + esc(p.n) + '" data-kind="' + p.k + '">' +
        '<button type="button" data-step-btn="1" aria-label="One more ' + esc(p.n) + '">+</button></div></div>';
    }).join("");
    return '<fieldset class="f-field f-qty" data-qty-group data-e="' + f.e + '" data-qe="' + f.qe + '"><legend>' + esc(f.l) + ' <span class="req" aria-hidden="true">*</span></legend>' + rows + '<p class="f-err" role="alert"></p></fieldset>';
  }

  function fieldHtml(f, key) {
    if (f.t === "qty") return qtyHtml(f, key);
    var id = "f-" + key + "-" + f.e, t = f.t || "text", req = f.req ? " required" : "";
    var star = f.req ? ' <span class="req" aria-hidden="true">*</span>' : ' <span class="opt">optional</span>';
    var help = f.h ? '<p class="f-help" id="' + id + '-h">' + esc(f.h) + "</p>" : "";
    var desc = f.h ? ' aria-describedby="' + id + '-h"' : "";
    var guide = f.guide ? '<ol class="f-guide">' + f.guide.map(function (g) { return "<li>" + esc(g) + "</li>"; }).join("") + "</ol>" : "";
    var cls = "f-field" + (f.half ? " half" : "");
    if (t === "radio" || t === "checkbox") {
      var opts = f.o.map(function (o, i) {
        return '<label class="f-choice"><input type="' + t + '" name="entry.' + f.e + '" value="' + esc(o) + '"' + (t === "radio" && f.req ? " required" : "") + (f.def === i ? " checked" : "") + '><span>' + esc(o) + "</span></label>";
      }).join("");
      if (f.other) opts += '<label class="f-choice f-other"><input type="' + t + '" name="entry.' + f.e + '" value="__other_option__" data-other><span>Other:</span><input type="text" class="f-input" name="entry.' + f.e + '.other_option_response" aria-label="' + esc(f.l) + ' (other)" disabled></label>';
      return '<fieldset class="' + cls + '"' + (t === "checkbox" && f.req ? ' data-req-group="entry.' + f.e + '"' : "") + desc + '><legend>' + esc(f.l) + star + "</legend>" + help + '<div class="f-choices' + (f.inline ? " inline" : "") + '">' + opts + '</div><p class="f-err" role="alert"></p></fieldset>';
    }
    var input;
    if (t === "textarea") input = '<textarea class="f-input" id="' + id + '" name="entry.' + f.e + '" rows="' + (f.rows || 3) + '"' + req + desc + "></textarea>";
    else if (t === "select") input = '<select class="f-input" id="' + id + '" name="entry.' + f.e + '"' + req + desc + '><option value="">Choose one…</option>' + f.o.map(function (o) { return '<option>' + esc(o) + "</option>"; }).join("") + "</select>";
    else input = '<input class="f-input" id="' + id + '" type="' + t + '" name="entry.' + f.e + '"' + req + desc + (f.ph ? ' placeholder="' + esc(f.ph) + '"' : "") + (f.ac ? ' autocomplete="' + f.ac + '"' : "") + (t === "url" ? ' inputmode="url" autocapitalize="off" spellcheck="false"' : "") + ">";
    return '<div class="' + cls + '"' + (f.show ? ' data-show="' + f.show + '"' : "") + '><label for="' + id + '">' + esc(f.l) + star + "</label>" + guide + help + input + '<p class="f-err" role="alert"></p></div>';
  }

  function render(el, key, compact) {
    var def = FORMS[key]; if (!def) return;
    var n = def.pages.length, multi = n > 1, fid = "tf" + (++uid);
    var steps = multi ? '<ol class="f-steps" aria-label="Form progress">' + def.pages.map(function (p, i) { return '<li data-step="' + i + '"' + (i === 0 ? ' class="on" aria-current="step"' : "") + "><span>" + (i + 1) + "</span>" + esc(p.title) + "</li>"; }).join("") + "</ol>" : "";
    var pages = def.pages.map(function (p, i) {
      return '<section class="f-page" data-page="' + i + '"' + (i ? " hidden" : "") + ">" + (multi ? '<h3 class="f-title">' + (i + 1) + ". " + esc(p.title) + "</h3>" : "") + (p.intro ? '<p class="f-intro">' + esc(p.intro) + "</p>" : "") + '<div class="f-grid">' + p.fields.map(function (f) { return fieldHtml(f, fid); }).join("") + "</div></section>";
    }).join("");
    var nav = '<div class="f-nav"><button type="button" class="btn btn-ghost" data-back' + (multi ? " hidden" : " hidden") + '>Back</button><span class="f-spacer"></span>' +
      (multi ? '<button type="button" class="btn btn-primary" data-next>Next</button>' : "") +
      '<button type="submit" class="btn btn-copper"' + (multi ? " hidden" : "") + ">" + esc(def.submit) + "</button></div>";
    var terms = key === "activate" ? '<p class="f-terms">By sending, you agree to our <a href="terms.html" target="_blank" rel="noopener">Terms of use</a> and <a href="privacy.html" target="_blank" rel="noopener">Privacy policy</a>.</p>' : "";
    el.innerHTML = '<form class="tform' + (compact ? " compact" : "") + '" novalidate>' + steps + pages + terms + nav + '<p class="f-status" role="status" aria-live="polite"></p></form>' +
      '<div class="f-done" hidden tabindex="-1"><span class="f-tick" aria-hidden="true"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg></span><h3>' + esc(def.done[0]) + "</h3><p>" + esc(def.done[1]) + '</p><p class="f-help">Questions? Email ' + esc(EMAIL) + "</p></div>";
    wire(el, def);
  }

  /* "g.page/r/abc", "www.site.com", "http//x.com" → "https://…" */
  function fixUrl(v) {
    v = v.replace(/\s+/g, "");
    if (/^https?:\/\//i.test(v)) return v;
    v = v.replace(/^(https?)?:?\/*/i, "");
    return "https://" + v;
  }
  function setErr(scope, msg) { var p = scope.querySelector(".f-err"); if (p) p.textContent = msg || ""; scope.classList.toggle("bad", !!msg); }

  function validatePage(page) {
    var ok = true, first = null;
    page.querySelectorAll(".f-field").forEach(function (fs) {
      var msg = "";
      if (fs.hasAttribute("data-qty-group")) {
        var total = 0; fs.querySelectorAll("[data-qty]").forEach(function (q) { total += Math.max(0, parseInt(q.value, 10) || 0); });
        setErr(fs, total ? "" : "Add at least one plate.");
        if (!total) { ok = false; if (!first) first = fs; }
        return;
      }
      if (fs.hidden) return;
      var group = fs.getAttribute("data-req-group");
      var inputs = fs.querySelectorAll("input, textarea, select");
      if (group) {
        if (!fs.querySelector('input[name="' + group + '"]:checked')) msg = "Please choose at least one option.";
      } else {
        inputs.forEach(function (i) {
          if (msg || i.disabled || i.type === "checkbox") return;
          var v = (i.value || "").trim();
          if (i.type === "radio") { if (i.required && !fs.querySelector('input[type="radio"]:checked')) msg = "Please choose one option."; return; }
          if (v && i.type === "url") { v = fixUrl(v); i.value = v; }
          if (i.required && !v) msg = "This field is required.";
          else if (v && i.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Please enter a valid email address.";
          else if (v && i.type === "url" && !/^https?:\/\/[^\s\/.]+(\.[^\s\/.]+)+(\/\S*)?$/i.test(v)) msg = "That doesn’t look like a web link. Please copy it from your browser’s address bar (e.g. https://g.page/r/…/review).";
        });
      }
      var other = fs.querySelector("[data-other]:checked");
      if (!msg && other) { var t = fs.querySelector(".f-other .f-input"); if (!t.value.trim()) msg = "Please fill in “Other”."; }
      setErr(fs, msg);
      if (msg) { ok = false; if (!first) first = fs; }
    });
    if (first) { first.scrollIntoView({ behavior: "smooth", block: "center" }); var f = first.querySelector("input:not([disabled]), textarea, select"); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 300); }
    return ok;
  }

  function wire(el, def) {
    var form = el.querySelector("form"), pages = form.querySelectorAll(".f-page"), cur = 0;
    var back = form.querySelector("[data-back]"), next = form.querySelector("[data-next]"), submit = form.querySelector('[type="submit"]'), status = form.querySelector(".f-status");
    function syncLinks() {
      var kinds = {};
      form.querySelectorAll("[data-qty]").forEach(function (q) { if ((parseInt(q.value, 10) || 0) > 0) kinds[q.getAttribute("data-kind")] = 1; });
      var any = Object.keys(kinds).length > 0;
      form.querySelectorAll("[data-show]").forEach(function (fs) {
        var on = !any || !!kinds[fs.getAttribute("data-show")];
        fs.hidden = !on; fs.querySelectorAll("input, textarea").forEach(function (x) { x.disabled = !on; });
      });
    }
    function show(i) {
      syncLinks();
      pages[cur].hidden = true; cur = i; pages[cur].hidden = false;
      form.querySelectorAll("[data-step]").forEach(function (s, k) { s.classList.toggle("on", k === cur); s.classList.toggle("done", k < cur); if (k === cur) s.setAttribute("aria-current", "step"); else s.removeAttribute("aria-current"); });
      back.hidden = cur === 0; if (next) next.hidden = cur === pages.length - 1; submit.hidden = cur !== pages.length - 1;
      var top = form.getBoundingClientRect().top + window.scrollY - 110;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
      var f = pages[cur].querySelector("input, textarea, select"); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 250);
    }
    if (next) next.addEventListener("click", function () { if (validatePage(pages[cur])) show(cur + 1); });
    back.addEventListener("click", function () { show(cur - 1); });
    form.addEventListener("change", function (e) {
      var t = e.target, fs = t.closest(".f-field");
      if (fs) { var o = fs.querySelector(".f-other .f-input"); if (o) { var on = !!fs.querySelector("[data-other]:checked"); o.disabled = !on; if (on && t.hasAttribute("data-other")) o.focus(); } if (fs.classList.contains("bad")) setErr(fs, ""); }
    });
    form.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-step-btn]"); if (!btn) return;
      var inp = btn.parentNode.querySelector("[data-qty]");
      inp.value = Math.min(999, Math.max(0, (parseInt(inp.value, 10) || 0) + (+btn.getAttribute("data-step-btn"))));
      inp.dispatchEvent(new Event("input", { bubbles: true }));
    });
    form.addEventListener("focusout", function (e) {
      if (e.target.hasAttribute && e.target.hasAttribute("data-qty")) e.target.value = Math.min(999, Math.max(0, parseInt(e.target.value, 10) || 0));
    });
    form.addEventListener("focusout", function (e) { var t = e.target; if (t.type === "url" && t.value.trim()) t.value = fixUrl(t.value.trim()); });
    form.addEventListener("input", function (e) { var fs = e.target.closest(".f-field"); if (fs && fs.classList.contains("bad")) setErr(fs, ""); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validatePage(pages[cur])) return;
      var data = new URLSearchParams();
      form.querySelectorAll("input, textarea, select").forEach(function (i) {
        if (!i.name || i.disabled) return;
        if ((i.type === "checkbox" || i.type === "radio") && !i.checked) return;
        var v = (i.value || "").trim(); if (!v) return;
        data.append(i.name, v);
      });
      form.querySelectorAll("[data-qty-group]").forEach(function (g) {
        var parts = [];
        g.querySelectorAll("[data-qty]").forEach(function (q) {
          var n = parseInt(q.value, 10) || 0; if (n < 1) return;
          data.append("entry." + g.getAttribute("data-e"), q.getAttribute("data-qty"));
          parts.push(n + " × " + q.getAttribute("data-qname"));
        });
        data.append("entry." + g.getAttribute("data-qe"), parts.join(", "));
      });
      var gp = def.gPages || pages.length;
      if (gp > 1) data.append("pageHistory", Array.from({ length: gp }, function (_, k) { return k; }).join(","));
      data.append("fvv", "1");
      submit.disabled = true; submit.textContent = "Sending…"; status.textContent = "";
      fetch("https://docs.google.com/forms/d/e/" + def.id + "/formResponse", { method: "POST", mode: "no-cors", body: data })
        .then(function () {
          form.hidden = true; var d = el.querySelector(".f-done"); d.hidden = false; d.focus();
          d.scrollIntoView({ behavior: "smooth", block: "center" });
        })
        .catch(function () {
          submit.disabled = false; submit.textContent = def.submit;
          status.textContent = "We couldn't send that. Please check your connection and try again, or email " + EMAIL + ".";
        });
    });
  }

  window.TTForms = { render: render, defs: FORMS };
  document.querySelectorAll("[data-form]").forEach(function (el) { render(el, el.getAttribute("data-form"), false); });
})();
