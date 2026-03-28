const express = require('express');
const path = require('path');
const app = express();
const PORT = 5000;

// Serve static files with proper MIME types and caching
app.use(express.static(path.join(__dirname), {
  maxAge: '1h',
  setHeaders: (res, filePath) => {
    // Service worker must not be cached
    if (filePath.endsWith('sw.js')) {
      res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    }
    // Manifest
    if (filePath.endsWith('.json')) {
      res.setHeader('Content-Type', 'application/json');
    }
  }
}));

// SPA fallback
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Audio Modes PWA running on port ${PORT}`);
});
