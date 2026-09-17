(function () {
  "use strict";

  var mast = document.querySelector(".mast");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && mast && nav) {
    toggle.addEventListener("click", function () {
      var open = mast.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });

    nav.addEventListener("click", function (event) {
      if (event.target.tagName === "A" && mast.classList.contains("is-open")) {
        mast.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.textContent = "Menu";
      }
    });
  }

  var hash = window.location.hash;
  if (hash === "#review") {
    var reviewBox = document.getElementById("need-review");
    if (reviewBox) reviewBox.checked = true;
  }
  if (hash === "#app") {
    var appBox = document.getElementById("need-app");
    if (appBox) appBox.checked = true;
  }

  var form = document.getElementById("demo-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var preview = document.getElementById("form-preview");
  var copyBtn = document.getElementById("copy-request");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var data = new FormData(form);
    var needs = data.getAll("need");
    var lines = [
      "Security in Social record review request",
      "This form stays on your device. Nothing was sent to a server. Copy this request and send it to the person who shared this site. A public inbox will be listed on Contact when one is live.",
      "",
      "Name: " + (data.get("name") || ""),
      "Firm: " + (data.get("firm") || ""),
      "Role: " + (data.get("role") || ""),
      "Email: " + (data.get("email") || ""),
      "Need: " + (needs.length ? needs.join(", ") : "not specified"),
      "",
      "Notes:",
      data.get("notes") || "(none)"
    ];
    var message = lines.join("\n");

    if (preview) preview.textContent = message;
    if (status) {
      status.classList.add("show");
      status.focus();
    }

    if (copyBtn) {
      copyBtn.onclick = function () {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(message).then(function () {
            copyBtn.textContent = "Copied";
            window.setTimeout(function () {
              copyBtn.textContent = "Copy request";
            }, 1600);
          });
        }
      };
    }
  });
})();
