// static/js/serviceworker.js
const CACHE_NAME = 'techassist-minimal-v1';
const ASSETS = [
    '/static/css/bootstrap.min.css',
    '/static/js/main.js'
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});