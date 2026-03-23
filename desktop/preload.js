const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("tnyfy", {
  platform: process.platform,
  version: "1.0.0",
});
