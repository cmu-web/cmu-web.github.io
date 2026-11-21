// More From CMU Web: fills a project's More From CMU Web section with a card
// for every other CMU Web project, from https://cmu-web.github.io/projects.json
// (written by tools/projects.py from the projects' own repositories).
//
// The section is the page's own markup, with its heading and a sentence that
// links to CMU Web, so it works without this script:
//
//   <div class="grid column4 grey boxes" data-cmu-web-more="cmu-web-kilt">
//     <h1 id="cmu-web">More From CMU Web</h1>
//     <p class="cmu-grid-full">... <a class="external" href="https://cmu-web.github.io/">CMU Web</a> ...</p>
//   </div>
//   <script src="https://cmu-web.github.io/js/more-from-cmu-web.js" defer></script>
//
// data-cmu-web-more names the page's own repository, which is left out. If
// the list can't be loaded, the section stays as it is.
(function () {
  "use strict";
  var sections = document.querySelectorAll("[data-cmu-web-more]");
  if (!sections.length || !window.fetch) return;
  var script = document.currentScript;
  var source = new URL(
    "../projects.json",
    (script && script.src) || "https://cmu-web.github.io/js/",
  );
  var groups = [
    ["tool", "Tools for Any Site or App"],
    ["theme", "Themes for Other Platforms"],
  ];

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    for (var name in attrs) node.setAttribute(name, attrs[name]);
    if (text) node.textContent = text;
    return node;
  }

  function card(project) {
    var box = el("div");
    var figure = el("figure", { class: "cmu-shot cmu-shot--browser" });
    var picture = el("a", {
      href: project.url,
      tabindex: "-1",
      "aria-hidden": "true",
    });
    picture.appendChild(
      el("img", {
        src: project.image,
        alt: project.alt,
        width: "1040",
        height: "656",
        loading: "lazy",
      }),
    );
    figure.appendChild(picture);
    box.appendChild(figure);
    if (project.eyebrow)
      box.appendChild(el("p", { class: "cmu-eyebrow" }, project.eyebrow));
    var heading = el("h2");
    heading.appendChild(
      el("a", { class: "external", href: project.url }, project.name),
    );
    box.appendChild(heading);
    box.appendChild(el("p", {}, project.description));
    return box;
  }

  fetch(source.href)
    .then(function (response) {
      if (!response.ok) throw new Error(response.status);
      return response.json();
    })
    .then(function (projects) {
      Array.prototype.forEach.call(sections, function (section) {
        var own = section.getAttribute("data-cmu-web-more");
        var added = document.createDocumentFragment();
        groups.forEach(function (group) {
          var cards = projects.filter(function (project) {
            return project.repo !== own && project.kind.indexOf(group[0]) === 0;
          });
          if (!cards.length) return;
          added.appendChild(
            el("p", { class: "cmu-label cmu-grid-full" }, group[1]),
          );
          cards.forEach(function (project) {
            added.appendChild(card(project));
          });
        });
        section.appendChild(added);
      });
    })
    .catch(function () {
      // The section's own sentence and link stay
    });
})();
