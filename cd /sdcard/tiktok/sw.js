const CACHE_NAME = 'catbot-cache-v1';
const ASSETS = [
  './',
  './index.html',
  './style.css',   // kalau ada file CSS terpisah
  './script.js',   // kalau ada JS terpisah
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

// ===== Install Service Worker =====
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// ===== Activate Service Worker =====
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.map(key => key !== CACHE_NAME ? caches.delete(key) : null)
    ))
  );
  self.clients.claim();
});

// ===== Fetch Handler =====
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => {
      return resp || fetch(event.request).then(fetchResp => {
        return caches.open(CACHE_NAME).then(cache => {
          // hanya cache GET requests
          if(event.request.method === 'GET') cache.put(event.request, fetchResp.clone());
          return fetchResp;
        });
      }).catch(() => {
        // fallback jika offline dan request tidak ada di cache
        if(event.request.destination === 'document') return caches.match('./index.html');
      });
    })
  );
});