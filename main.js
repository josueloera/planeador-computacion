const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { machineIdSync } = require('node-machine-id');
const crypto = require('crypto');

const SECRET_KEY = 'PLANEADOR_COMPUTACION_2026_MASTER_SECRET_KEY';
let store;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    },
    autoHideMenuBar: true
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(async () => {
  const Store = (await import('electron-store')).default;
  store = new Store();

  if (!store.has('firstOpen')) {
    store.set('firstOpen', Date.now());
  }

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.handle('get-license-info', () => {
  if(!store) return { isActivated: false, daysRemaining: 0, machineId: machineIdSync() };

  const isActivated = store.get('activated', false);
  const firstOpen = store.get('firstOpen', Date.now());
  const now = Date.now();
  const msInDay = 24 * 60 * 60 * 1000;
  
  const daysPassed = Math.floor((now - firstOpen) / msInDay);
  const daysRemaining = Math.max(0, 3 - daysPassed);

  return {
    isActivated,
    daysRemaining,
    machineId: machineIdSync()
  };
});

ipcMain.handle('activate-license', (event, key) => {
  if(!store) return { success: false, message: 'Inicializando, intenta de nuevo.' };

  const hardwareId = machineIdSync();
  const expectedKey = crypto.createHmac('sha256', SECRET_KEY)
                            .update(hardwareId)
                            .digest('hex')
                            .substring(0, 12)
                            .toUpperCase();

  if (key === expectedKey) {
    store.set('activated', true);
    store.set('licenseKey', key);
    return { success: true };
  } else {
    return { success: false, message: 'Clave inválida para este equipo.' };
  }
});
