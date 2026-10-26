import { defineConfig } from "@playwright/test";
import { createArgosReporterOptions } from "@argos-ci/playwright/reporter";

export default defineConfig({
  // ... Keep your existing configuration options here

  // Configure Reporters
  reporter: [
    // Use standard reporters for console readability
    process.env.CI ? ["dot"] : ["list"],
    // Add the Argos reporter
    [
      "@argos-ci/playwright/reporter",
      createArgosReporterOptions({
        // Automatically uploads to Argos when running in a CI environment
        uploadToArgos: !!process.env.CI,
      }),
    ],
  ],

  use: {
    // Collect artifacts automatically to enrich the Argos build context
    trace: "on-first-retry",
    screenshot: "only-on-failure",

    // Essential flags: Prevents anti-aliasing text flakiness between platforms
    launchOptions: {
      args: ["--enable-lcd-text", "--font-render-hinting=none"],
    },
  },
});
                                 
