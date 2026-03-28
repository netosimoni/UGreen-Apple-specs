/**
 * Audio Modes PWA — Service Worker
 * Strategy: Cache first with network fallback
 * Precaches all app shell assets on install
 */

const CACHE_VERSION = 'audio-modes-v2';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.json',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/icon-maskable-192.png',
  './assets/icon-maskable-512.png',
  './assets/apple-touch-icon.png',
  './assets/favicon-32.png'
];

/* Install — pre-cache app shell */
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

/* Activate — purge old caches */
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

/* Fetch — cache first, fallback to network, then offline page */
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request)
      .then((cached) => {
        if (cached) return cached;

        return fetch(event.request)
          .then((response) => {
            // Only cache successful same-origin responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            const clone = response.clone();
            caches.open(CACHE_VERSION).then((cache) => {
              cache.put(event.request, clone);
            });

            return response;
          })
          .catch(() => {
            // If navigation request fails, serve the cached index
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html');
            }
            return new Response('Offline', { status: 503, statusText: 'Offline' });
          });
      })
  );
});
