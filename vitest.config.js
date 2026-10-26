import { defineConfig } from 'vitest/config';
import { argosVitestPlugin } from '@argos-ci/vitest/plugin';

export default defineConfig({
  plugins: [
    argosVitestPlugin({
      // Upload screenshots to Argos when CI is enabled
      uploadToArgos: !!process.env.CI, CI:true
    }),
  ],
  test: {
    // Ensure browser mode is enabled for screenshots
    browser: {
      enabled: true,
      provider: 'playwright',
      instances: [{ browser: 'chromium' }],
    },
  },
});
