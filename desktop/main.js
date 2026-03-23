const { app, BrowserWindow, Tray, Menu, shell, ipcMain } = require("electron");
const path = require("path");
const { spawn, execSync } = require("child_process");
const http = require("http");

let mainWindow = null;
let splashWindow = null;
let tray = null;
let backendProcess = null;
let frontendProcess = null;
let dockerProcess = null;

const isDev = process.argv.includes("--dev");
const ROOT_DIR = isDev
  ? path.join(__dirname, "..")
  : path.join(process.resourcesPath);

const BACKEND_PORT = 8000;
const FRONTEND_PORT = 3000;

// ─── Send status to splash screen ────────────────────────────────

function sendSplashStatus(step, state, message, progress) {
  if (splashWindow && !splashWindow.isDestroyed()) {
    splashWindow.webContents.send("splash-status", {
      step,
      state,
      message,
      progress,
    });
  }
}

// ─── Splash Screen ───────────────────────────────────────────────

function createSplashWindow() {
  splashWindow = new BrowserWindow({
    width: 460,
    height: 420,
    frame: false,
    transparent: true,
    resizable: false,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  splashWindow.loadFile(path.join(__dirname, "splash.html"));
  splashWindow.center();
}

// ─── Main Window ─────────────────────────────────────────────────

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
  mainWindow.maximize();

  mainWindow.loadURL(`http://localhost:${FRONTEND_PORT}`);

  mainWindow.webContents.on("did-fail-load", (event, errorCode, errorDesc) => {
    console.log("[Tnyfy] Page load failed, retrying in 2s...", errorDesc);
    setTimeout(() => {
      if (mainWindow && !mainWindow.isDestroyed()) {
        mainWindow.loadURL(`http://localhost:${FRONTEND_PORT}`);
      }
    }, 2000);
  });

  mainWindow.once("ready-to-show", () => {
    if (splashWindow && !splashWindow.isDestroyed()) {
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
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

// ─── System Tray ─────────────────────────────────────────────────

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
        stopAllServices();
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

// ─── Docker (PostgreSQL + Redis) ─────────────────────────────────

function startDocker() {
  return new Promise((resolve) => {
    sendSplashStatus("docker", "active", "Demarrage de la base de donnees...", 5);

    // Check if docker is available
    try {
      execSync("docker info", { stdio: "ignore", timeout: 5000 });
    } catch (e) {
      console.log("[Tnyfy] Docker not available, skipping...");
      sendSplashStatus("docker", "error", "Docker non disponible - mode demo", 10);
      setTimeout(resolve, 500);
      return;
    }

    const composeFile = path.join(ROOT_DIR, "docker-compose.yml");

    sendSplashStatus("docker", "active", "Lancement PostgreSQL + Redis...", 8);

    dockerProcess = spawn("docker", ["compose", "-f", composeFile, "up", "-d"], {
      stdio: ["ignore", "pipe", "pipe"],
      shell: true,
    });

    dockerProcess.on("close", (code) => {
      if (code === 0) {
        console.log("[Tnyfy] Docker services started");
        sendSplashStatus("docker", "done", "Base de donnees prete", 20);
      } else {
        console.log("[Tnyfy] Docker compose failed (code " + code + ")");
        sendSplashStatus("docker", "error", "Base de donnees non disponible - mode demo", 20);
      }
      resolve();
    });

    dockerProcess.on("error", () => {
      sendSplashStatus("docker", "error", "Docker non disponible - mode demo", 20);
      resolve();
    });

    setTimeout(() => resolve(), 30000);
  });
}

// ─── Backend (FastAPI + uvicorn) ─────────────────────────────────

function startBackend() {
  return new Promise((resolve) => {
    sendSplashStatus("backend", "active", "Initialisation du moteur IA...", 25);

    const backendDir = path.join(ROOT_DIR, "backend");

    const venvPython = isDev
      ? path.join(backendDir, ".venv", "Scripts", "python.exe")
      : "python";

    console.log("[Tnyfy] Starting backend from:", backendDir);
    console.log("[Tnyfy] Python:", venvPython);

    backendProcess = spawn(
      venvPython,
      ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", String(BACKEND_PORT)],
      {
        cwd: backendDir,
        env: { ...process.env, PYTHONUNBUFFERED: "1" },
        stdio: ["ignore", "pipe", "pipe"],
      }
    );

    let resolved = false;
    const done = () => {
      if (!resolved) {
        resolved = true;
        sendSplashStatus("backend", "done", "Moteur IA pret", 50);
        resolve();
      }
    };

    backendProcess.stdout.on("data", (data) => {
      const msg = data.toString();
      console.log("[Backend]", msg.trim());
      if (msg.includes("Uvicorn running") || msg.includes("Application startup complete")) {
        done();
      }
    });

    backendProcess.stderr.on("data", (data) => {
      const msg = data.toString();
      console.log("[Backend]", msg.trim());
      sendSplashStatus("backend", "active", "Chargement des agents IA...", 35);
      if (msg.includes("Uvicorn running") || msg.includes("Application startup complete")) {
        done();
      }
    });

    backendProcess.on("error", (err) => {
      console.error("[Backend] Failed to start:", err.message);
      sendSplashStatus("backend", "error", "Erreur moteur IA: " + err.message, 50);
      if (!resolved) {
        resolved = true;
        resolve();
      }
    });

    setTimeout(() => {
      if (!resolved) {
        resolved = true;
        sendSplashStatus("backend", "done", "Moteur IA pret", 50);
        resolve();
      }
    }, 15000);
  });
}

// ─── Frontend (Next.js) ──────────────────────────────────────────

function startFrontend() {
  return new Promise((resolve) => {
    sendSplashStatus("frontend", "active", "Construction de l'interface...", 55);

    const frontendDir = path.join(ROOT_DIR, "frontend");

    console.log("[Tnyfy] Starting frontend from:", frontendDir);

    if (isDev) {
      const npmCmd = process.platform === "win32" ? "npm.cmd" : "npm";
      frontendProcess = spawn(npmCmd, ["run", "dev"], {
        cwd: frontendDir,
        env: { ...process.env, PORT: String(FRONTEND_PORT), BROWSER: "none" },
        stdio: ["ignore", "pipe", "pipe"],
        shell: true,
      });

      let resolved = false;

      frontendProcess.stdout.on("data", (data) => {
        const msg = data.toString();
        console.log("[Frontend]", msg.trim());
        sendSplashStatus("frontend", "active", "Compilation du dashboard...", 65);
        if ((msg.includes("Ready") || msg.includes("localhost") || msg.includes("compiled")) && !resolved) {
          resolved = true;
          sendSplashStatus("frontend", "done", "Interface prete", 80);
          resolve();
        }
      });

      frontendProcess.stderr.on("data", (data) => {
        console.log("[Frontend]", data.toString().trim());
      });

      frontendProcess.on("error", (err) => {
        console.error("[Frontend] Failed:", err.message);
        sendSplashStatus("frontend", "error", "Erreur interface: " + err.message, 80);
        if (!resolved) { resolved = true; resolve(); }
      });

      setTimeout(() => {
        if (!resolved) { resolved = true; resolve(); }
      }, 30000);
    } else {
      const nodePath = process.execPath.includes("electron") ? "node" : process.execPath;
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
        sendSplashStatus("frontend", "done", "Interface prete", 80);
        resolve();
      });

      frontendProcess.on("error", (err) => {
        console.error("[Frontend] Failed:", err.message);
        sendSplashStatus("frontend", "error", "Erreur interface", 80);
        resolve();
      });

      setTimeout(resolve, 20000);
    }
  });
}

// ─── Wait for server ─────────────────────────────────────────────

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

// ─── Stop all services cleanly ───────────────────────────────────

function stopAllServices() {
  console.log("[Tnyfy] Stopping all services...");

  // Kill backend
  if (backendProcess && !backendProcess.killed) {
    try {
      // On Windows, SIGTERM doesn't work well - use taskkill for the process tree
      if (process.platform === "win32") {
        execSync(`taskkill /PID ${backendProcess.pid} /T /F`, { stdio: "ignore" });
      } else {
        backendProcess.kill("SIGTERM");
      }
    } catch (e) { /* process may already be dead */ }
    backendProcess = null;
  }

  // Kill frontend
  if (frontendProcess && !frontendProcess.killed) {
    try {
      if (process.platform === "win32") {
        execSync(`taskkill /PID ${frontendProcess.pid} /T /F`, { stdio: "ignore" });
      } else {
        frontendProcess.kill("SIGTERM");
      }
    } catch (e) { /* process may already be dead */ }
    frontendProcess = null;
  }
}

// ─── App Lifecycle ───────────────────────────────────────────────

app.whenReady().then(async () => {
  // Show splash screen immediately
  createSplashWindow();
  createTray();

  // Step 1: Docker (database)
  await startDocker();

  // Step 2: Backend (AI engine)
  await startBackend();

  // Step 3: Frontend (dashboard)
  await startFrontend();

  // Step 4: Wait for everything to be ready
  sendSplashStatus("ready", "active", "Verification des services...", 85);
  console.log("[Tnyfy] Waiting for frontend server...");
  const frontendReady = await waitForServer(FRONTEND_PORT);

  if (frontendReady) {
    sendSplashStatus("ready", "done", "Tnyfy est pret !", 100);
  } else {
    sendSplashStatus("ready", "error", "Timeout - ouverture quand meme...", 100);
  }

  // Small delay so user sees 100%
  await new Promise((r) => setTimeout(r, 800));

  // Show main window
  createMainWindow();
});

app.on("window-all-closed", () => {
  // Don't quit - keep running in tray
});

app.on("before-quit", () => {
  app.isQuitting = true;
  stopAllServices();
});

app.on("activate", () => {
  if (mainWindow === null) {
    createMainWindow();
  }
});
