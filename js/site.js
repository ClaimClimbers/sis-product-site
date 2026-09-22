(function () {
  "use strict";

  var mast = document.querySelector(".mast") || document.querySelector(".site-top");
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

  function applyNeedHash() {
    var hash = window.location.hash;
    if (hash === "#review") {
      var reviewBox = document.getElementById("need-review");
      if (reviewBox) reviewBox.checked = true;
    }
    if (hash === "#app") {
      var appBox = document.getElementById("need-app");
      if (appBox) appBox.checked = true;
    }
  }

  applyNeedHash();
  window.addEventListener("hashchange", applyNeedHash);

  var form = document.getElementById("demo-form");
  if (!form) return;

  var status = document.getElementById("form-status");
  var preview = document.getElementById("form-preview");
  var copyBtn = document.getElementById("copy-request");
  var roleSelect = document.getElementById("role");
  var firmField = document.getElementById("firm-field");
  var firmInput = document.getElementById("firm");

  function roleShowsFirm(value) {
    return value === "attorney" || value === "firm";
  }

  function syncFirmField() {
    if (!roleSelect || !firmField) return;
    var show = roleShowsFirm(roleSelect.value);
    firmField.hidden = !show;
    firmField.setAttribute("aria-hidden", show ? "false" : "true");
    if (!show && firmInput) firmInput.value = "";
  }

  if (roleSelect) {
    roleSelect.addEventListener("change", syncFirmField);
    syncFirmField();
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var submitter = event.submitter;
    if (submitter && submitter.name === "need") {
      var matchedNeed = form.querySelector('input[type="checkbox"][name="need"][value="' + submitter.value + '"]');
      if (matchedNeed) matchedNeed.checked = true;
    }

    var data = new FormData(form);
    var needs = data.getAll("need").filter(function (value, index, all) {
      return all.indexOf(value) === index;
    });
    var role = data.get("role") || "";
    var lines = [
      "Security in Social record review request",
      "This note stays on your device until a public inbox is live. Nothing is stored on a server yet. Copy your note and send it through the path your helper shared, or wait until Contact can deliver.",
      "",
      "Name: " + (data.get("name") || ""),
      "Role: " + role,
    ];
    if (roleShowsFirm(role)) {
      lines.push("Firm: " + (data.get("firm") || ""));
    }
    lines.push(
      "Email: " + (data.get("email") || ""),
      "Need: " + (needs.length ? needs.join(", ") : "not specified"),
      "",
      "Notes:",
      data.get("notes") || "(none)"
    );
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
