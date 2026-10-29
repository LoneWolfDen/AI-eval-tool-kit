/* Builds the route map from the JSON embedded in the page.
   Sections: storage, DOM helper, rendering, filtering, progress. */
(function () {
  "use strict";

  var STORAGE_KEY = "ai-learning-route-progress-v1";
  var TYPE_NAMES = { all: "All", course: "Courses", read: "Reading", repo: "Repos", guidance: "Guidance" };

  var map = JSON.parse(document.getElementById("map-data").textContent);
  var done = readProgress();
  var activeType = "all";

  /* ---------- storage (wrapped: it can be blocked or empty) ---------- */

  function readProgress() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (error) {
      return {};
    }
  }

  function writeProgress() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(done));
    } catch (error) {
      /* Storage unavailable: progress lasts until the page is closed. */
    }
  }

  /* ---------- small DOM helper ---------- */

  function el(tag, props, children) {
    var node = document.createElement(tag);
    Object.keys(props || {}).forEach(function (key) {
      if (key === "text") node.textContent = props[key];
      else if (key === "class") node.className = props[key];
      else node.setAttribute(key, props[key]);
    });
    (children || []).forEach(function (child) {
      node.appendChild(child);
    });
    return node;
  }

  function setLineColors(node, stage) {
    node.style.setProperty("--c-light", stage.color);
    node.style.setProperty("--c-dark", stage.color_dark);
  }

  /* ---------- stop ids ---------- */

  function gateId(stage) {
    return stage.id + ":gate";
  }

  function stopIds(stage) {
    return stage.resources.map(function (r) { return r.id; }).concat(gateId(stage));
  }

  /* ---------- rendering ---------- */

  function renderStrip() {
    var strip = document.getElementById("strip");
    map.stages.forEach(function (stage) {
      var fill = el("span", { class: "seg-fill", "data-fill": stage.id });
      var link = el("a", { class: "seg", href: "#stage-" + stage.id }, [
        el("span", { class: "seg-bar" }, [fill]),
        el("span", { class: "seg-name", text: stage.short })
      ]);
      setLineColors(link, stage);
      strip.appendChild(link);
    });
  }

  function renderFilters() {
    var container = document.getElementById("filters");
    Object.keys(TYPE_NAMES).forEach(function (type) {
      var chip = el("button", { class: "chip", type: "button", "data-type": type, text: TYPE_NAMES[type] });
      chip.addEventListener("click", function () {
        activeType = type;
        applyFilter();
      });
      container.appendChild(chip);
    });
  }

  function renderStop(id, extraClass, textChildren) {
    var box = el("input", { class: "stop-box", type: "checkbox", "data-id": id });
    box.checked = !!done[id];
    box.addEventListener("change", function () {
      if (box.checked) done[id] = true;
      else delete done[id];
      writeProgress();
      refreshProgress();
    });

    var label = el("label", { class: "stop-row" }, [
      box,
      el("span", { class: "dot", "aria-hidden": "true" }),
      el("span", { class: "stop-text" }, textChildren)
    ]);
    return el("li", { class: "stop " + extraClass }, [label]);
  }

  function renderResource(resource) {
    var link = el("a", { href: resource.url, text: resource.title });
    if (!resource.internal) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    }
    var meta = el("span", { class: "meta" }, [
      el("span", { class: "tag", text: resource.type }),
      document.createTextNode(resource.cost)
    ]);
    var item = renderStop(resource.id, resource.tier === "deeper" ? "deeper" : "", [
      el("span", { class: "title" }, [link]),
      meta,
      el("span", { class: "note", text: resource.note })
    ]);
    item.setAttribute("data-type", resource.type);
    return item;
  }

  function renderGate(stage) {
    var item = renderStop(gateId(stage), "gate", [
      el("span", { class: "title", text: "Stage gate: build it" }),
      el("span", { class: "note", text: stage.gate.build }),
      el("span", { class: "check-line", text: "Check yourself: " + stage.gate.check })
    ]);
    return item;
  }

  function renderStopList(resources) {
    return el("ul", { class: "stops" }, resources.map(renderResource));
  }

  function renderStage(stage) {
    var start = stage.resources.filter(function (r) { return r.tier === "start"; });
    var deeper = stage.resources.filter(function (r) { return r.tier === "deeper"; });

    var section = el("section", { class: "stage", id: "stage-" + stage.id }, [
      el("div", { class: "stage-head" }, [
        el("span", { class: "hub", "aria-hidden": "true" }),
        el("h2", { text: stage.title }),
        el("p", { class: "goal", text: stage.goal }),
        el("p", { class: "stage-count", "data-count": stage.id })
      ]),
      renderStopList(start)
    ]);

    if (deeper.length) {
      section.appendChild(
        el("details", { class: "more", "data-more": stage.id }, [
          el("summary", { "data-more-label": stage.id }),
          renderStopList(deeper)
        ])
      );
    }
    section.appendChild(el("ul", { class: "stops" }, [renderGate(stage)]));
    setLineColors(section, stage);
    return section;
  }

  function renderStages() {
    var container = document.getElementById("stages");
    map.stages.forEach(function (stage) {
      container.appendChild(renderStage(stage));
    });
  }

  /* ---------- filtering ---------- */

  function applyFilter() {
    document.querySelectorAll(".chip").forEach(function (chip) {
      chip.setAttribute("aria-pressed", String(chip.getAttribute("data-type") === activeType));
    });

    document.querySelectorAll(".stop[data-type]").forEach(function (item) {
      item.hidden = activeType !== "all" && item.getAttribute("data-type") !== activeType;
    });

    map.stages.forEach(function (stage) {
      var more = document.querySelector('[data-more="' + stage.id + '"]');
      if (!more) return;
      var visible = more.querySelectorAll(".stop:not([hidden])").length;
      more.hidden = visible === 0;
      more.querySelector("summary").textContent = "Go deeper (" + visible + ")";
    });
  }

  /* ---------- progress ---------- */

  function countDone(ids) {
    return ids.filter(function (id) { return done[id]; }).length;
  }

  function refreshProgress() {
    var total = 0;
    var finished = 0;

    map.stages.forEach(function (stage) {
      var ids = stopIds(stage);
      var count = countDone(ids);
      total += ids.length;
      finished += count;

      document.querySelector('[data-fill="' + stage.id + '"]').style.width = (100 * count) / ids.length + "%";
      document.querySelector('[data-count="' + stage.id + '"]').textContent = count + " of " + ids.length + " stops";
    });

    document.getElementById("overall").textContent = finished + " of " + total + " stops visited";
  }

  function clearProgress() {
    if (!window.confirm("Clear all ticked stops on this device?")) return;
    done = {};
    writeProgress();
    document.querySelectorAll(".stop-box").forEach(function (box) { box.checked = false; });
    refreshProgress();
  }

  /* ---------- start ---------- */

  renderStrip();
  renderFilters();
  renderStages();
  applyFilter();
  refreshProgress();
  document.getElementById("reset").addEventListener("click", clearProgress);
})();
