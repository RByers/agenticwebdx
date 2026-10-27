// Flag slides whose content doesn't fit the fixed slide size.
//
// The template gives .slide a min-height (not a height), so too much content
// silently makes that slide taller than the others. Content inside an
// overflow:hidden box (e.g. .columns) gets silently clipped instead. This
// finds both cases, outlines the offending slides and logs a warning.
// tools/check-slide-fit.js runs the same check headlessly.
(function () {
  var SLIDE_HEIGHT_EM = 23; // matches the template's --slide-height
  var TOLERANCE_PX = 1;

  function findOverflowingSlides() {
    var problems = [];
    document.querySelectorAll('section.slide').forEach(function (slide, i) {
      var reasons = [];
      var max = parseFloat(getComputedStyle(slide).fontSize) * SLIDE_HEIGHT_EM;
      // offsetHeight and the client/scroll sizes ignore CSS transforms, so
      // this works in both the index view and full-screen mode.
      var h = Math.max(slide.offsetHeight, slide.scrollHeight);
      if (h > max + TOLERANCE_PX)
        reasons.push('slide is ' + Math.round(h - max) + 'px too tall');
      slide.querySelectorAll('*').forEach(function (el) {
        var cs = getComputedStyle(el);
        if (cs.overflowY === 'visible' || cs.display === 'none') return;
        var extra = el.scrollHeight - el.clientHeight;
        if (extra > TOLERANCE_PX)
          reasons.push('<' + el.tagName.toLowerCase() +
            (el.className ? '.' + String(el.className).trim().replace(/\s+/g, '.') : '') +
            '> clips ' + extra + 'px');
      });
      slide.classList.toggle('overflowing', reasons.length > 0);
      if (reasons.length)
        problems.push({index: i + 1, id: slide.id, reasons: reasons});
    });
    return problems;
  }
  window.findOverflowingSlides = findOverflowingSlides;

  function run() {
    findOverflowingSlides().forEach(function (p) {
      console.warn('Slide ' + p.index + ' (#' + p.id + ') overflows: ' +
        p.reasons.join('; '));
    });
  }
  window.addEventListener('load', function () {
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(run);
  });
})();
