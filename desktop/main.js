const { app, BrowserWindow, Tray, Menu, nativeImage, shell } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const http = require("http");

let mainWindow = null;
let splashWindow = null;
let tray = null;
let backendProcess = null;
let frontendProcess = null;

const isDev = process.argv.includes("--dev");
const ROOT_DIR = isDev
  ? path.join(__dirname, "..")
  : path.join(process.resourcesPath);

const BACKEND_PORT = 8000;
const FRONTEND_PORT = 3000;

// ─── Splash Screen ────────────────────────────────────────────────

function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 450,
    height: 320,
    frame: false,
    transparent: true,
    resizable: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: { nodeIntegration: false },
  });
  splashWindow.loadFile(path.join(__dirname, "splash.html"));
  splashWindow.center();
}

// ─── Main Window ──────────────────────────────────────────────────

function createMainWindow() {
  const iconPath = path.join(__dirname, "icon.ico");

  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    title: "Tnyfy",
    icon: iconPath,
    backgroundColor: "#0a0a0f",
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.setMenuBarVisibility(false);

  mainWindow.loadURL(`http://localhost:${FRONTEND_PORT}`);

  mainWindow.once("ready-to-show", () => {
    if (splashWindow) {
      splashWindow.close();
      splashWindow = null;
    }
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  mainWindow.on("close", (event) => {
    // Minimize to tray instead of closing
    event.preventDefault();
    mainWindow.hide();
  });

  // Open external links in default browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

// ─── System Tray ──────────────────────────────────────────────────

function createTray() {
  const iconPath = path.join(__dirname, "icon.ico");
  tray = new Tray(iconPath);

  const contextMenu = Menu.buildFromTemplate([
    {
      label: "Ouvrir Tnyfy",
      click: () => {
        if (mainWindow) {
          mainWindow.show();
          mainWindow.focus();
        }
      },
    },
    {
      label: "API Documentation",
      click: () => {
        shell.openExternal(`http://localhost:${BACKEND_PORT}/docs`);
      },
    },
    { type: "separator" },
    {
      label: "Quitter Tnyfy",
      click: () => {
        app.isQuitting = true;
        stopServices();
        app.quit();
      },
    },
  ]);

  tray.setToolTip("Tnyfy - AI E-Commerce Platform");
  tray.setContextMenu(contextMenu);

  tray.on("double-click", () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    }
  });
}

// ─── Backend & Frontend Services ──────────────────────────────────

function startBackend() {
  return new Promise((resolve) => {
    const backendDir = isDev
      ? path.join(ROOT_DIR, "backend")
      : path.join(ROOT_DIR, "backend");

    const venvPython = isDev
      ? path.join(backendDir, ".venv", "Scripts", "python.exe")
      : "python";

    console.log("[Tnyfy] Starting backend...");

    backendProcess = spawn(
      venvPython,
      ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", String(BACKEND_PORT)],
      {
        cwd: backendDir,
        env: { ...process.env, PYTHONUNBUFFERED: "1" },
        stdio: ["ignore", "pipe", "pipe"],
      }
    );

    backendProcess.stdout.on("data", (data) => {
      const msg = data.toString();
      console.log("[Backend]", msg.trim());
      if (msg.includes("Uvicorn running") || msg.includes("Application startup complete")) {
        resolve();
      }
    });

    backendProcess.stderr.on("data", (data) => {
      const msg = data.toString();
      console.log("[Backend]", msg.trim());
      if (msg.includes("Uvicorn running") || msg.includes("Application startup complete")) {
        resolve();
      }
    });

    backendProcess.on("error", (err) => {
      console.error("[Backend] Failed to start:", err.message);
      resolve(); // Don't block, continue without backend
    });

    // Timeout - resolve anyway after 15 seconds
    setTimeout(resolve, 15000);
  });
}

function startFrontend() {
  return new Promise((resolve) => {
    const frontendDir = isDev
      ? path.join(ROOT_DIR, "frontend")
      : path.join(ROOT_DIR, "frontend");

    console.log("[Tnyfy] Starting frontend...");

    if (isDev) {
      // In dev mode, use npm run dev
      const npmPath = path.join("C:", "Program Files", "nodejs", "npm.cmd");
      frontendProcess = spawn(npmPath, ["run", "dev"], {
        cwd: frontendDir,
        env: { ...process.env, PORT: String(FRONTEND_PORT) },
        stdio: ["ignore", "pipe", "pipe"],
        shell: true,
      });

      frontendProcess.stdout.on("data", (data) => {
        const msg = data.toString();
        console.log("[Frontend]", msg.trim());
        if (msg.includes("Ready") || msg.includes("localhost")) {
          resolve();
        }
      });

      frontendProcess.stderr.on("data", (data) => {
        console.log("[Frontend]", data.toString().trim());
      });
    } else {
      // In production, use the standalone server
      const nodePath = process.execPath.includes("electron")
        ? "node"
        : process.execPath;

      frontendProcess = spawn(
        nodePath,
        [path.join(frontendDir, "server.js")],
        {
          cwd: frontendDir,
          env: { ...process.env, PORT: String(FRONTEND_PORT), HOSTNAME: "127.0.0.1" },
          stdio: ["ignore", "pipe", "pipe"],
        }
      );

      frontendProcess.stdout.on("data", (data) => {
        console.log("[Frontend]", data.toString().trim());
        resolve();
      });
    }

    frontendProcess.on("error", (err) => {
      console.error("[Frontend] Failed to start:", err.message);
      resolve();
    });

    // Timeout
    setTimeout(resolve, 20000);
  });
}

function stopServices() {
  console.log("[Tnyfy] Stopping services...");

  if (backendProcess) {
    backendProcess.kill("SIGTERM");
    backendProcess = null;
  }
  if (frontendProcess) {
    frontendProcess.kill("SIGTERM");
    frontendProcess = null;
  }
}

function waitForServer(port, maxAttempts = 30) {
  return new Promise((resolve) => {
    let attempts = 0;
    const check = () => {
      attempts++;
      const req = http.get(`http://127.0.0.1:${port}`, (res) => {
        resolve(true);
      });
      req.on("error", () => {
        if (attempts < maxAttempts) {
          setTimeout(check, 1000);
        } else {
          resolve(false);
        }
      });
      req.setTimeout(2000, () => {
        req.destroy();
        if (attempts < maxAttempts) {
          setTimeout(check, 1000);
        } else {
          resolve(false);
        }
      });
    };
    check();
  });
}

// ─── App Lifecycle ────────────────────────────────────────────────

app.whenReady().then(async () => {
  // Show splash screen
  createSplashWindow();
  createTray();

  // Start services
  await startBackend();
  await startFrontend();

  // Wait for frontend to be ready
  console.log("[Tnyfy] Waiting for frontend server...");
  await waitForServer(FRONTEND_PORT);

  // Show main window
  createMainWindow();
});

app.on("window-all-closed", () => {
  // Don't quit - keep running in tray
});

app.on("before-quit", () => {
  app.isQuitting = true;
  stopServices();
});

app.on("activate", () => {
  if (mainWindow === null) {
    createMainWindow();
  }
});
