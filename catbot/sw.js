self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil((async () => {
    const cache = await caches.open('catbot-v1');
    await cache.addAll([
      './', './index.html', './manifest.json', './icons/icon-192.png', './icons/icon-512.png'
    ]);
  })());
});
self.addEventListener('activate', e => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // cache-first for same-origin GET
  if (e.request.method === 'GET' && url.origin === location.origin) {
    e.respondWith((async () => {
      const cached = await caches.match(e.request);
      return cached || fetch(e.request);
    })());
  }
});