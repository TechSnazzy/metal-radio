// Minimal service worker: cache the app shell so the PWA launches offline.
// Audio streams are cross-origin and are never intercepted.
const CACHE = "metal-radio-v1";
const SHELL = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/apple-touch-icon.png",
  "icons/favicon-32.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return; // let stream requests pass straight through

  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).catch(() => caches.match("index.html")));
    return;
  }
  e.respondWith(
    caches.match(e.request).then((hit) => hit || fetch(e.request))
  );
});
