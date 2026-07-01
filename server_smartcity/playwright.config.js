const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  
  // PERBAIKAN: Memunculkan rincian teks penjelasan di terminal (list) sekaligus membuat laporan HTML
  reporter: [['list'], ['html']], 

  use: {
    headless: false,
    viewport: null, 
    launchOptions: {
      slowMo: 1000, 
      args: [
        '--start-maximized', 
      ],
    },
  },
});