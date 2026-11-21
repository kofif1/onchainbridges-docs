/* Click-to-load video. Nothing is requested from YouTube until the visitor
   presses play, so the page keeps the no-third-party-on-load property that
   privacy.html clause 1.2 (d) and the site footer both state. */
(function () {
  var nodes = document.querySelectorAll('[data-video-id]');
  for (var i = 0; i < nodes.length; i++) {
    (function (el) {
      el.addEventListener('click', function () {
        var frame = document.createElement('iframe');
        frame.setAttribute('width', '560');
        frame.setAttribute('height', '315');
        frame.setAttribute('allowfullscreen', '');
        frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        frame.setAttribute('allow', 'encrypted-media; picture-in-picture; fullscreen');
        frame.setAttribute('title', 'A recorded walkthrough of this flow on TestNet (video).');
        frame.src = 'https://www.youtube-nocookie.com/embed/' +
                    encodeURIComponent(el.getAttribute('data-video-id')) + '?autoplay=1';
        el.replaceChildren(frame);
      });
    })(nodes[i]);
  }
})();
