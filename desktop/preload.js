const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("tnyfy", {
  platform: process.platform,
  version: "1.0.0",
});

// Expose IPC for splash screen status updates
try {
  const { webFrame } = require("electron");
  // Allow splash screen to receive status updates
  ipcRenderer.on("splash-status", (event, data) => {
    window.postMessage({ type: "splash-status", ...data }, "*");
  });
} catch (e) {
  // Ignore if not available
}
