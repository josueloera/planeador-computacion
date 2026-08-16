const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('licenseAPI', {
  getLicenseInfo: () => ipcRenderer.invoke('get-license-info'),
  activateLicense: (key) => ipcRenderer.invoke('activate-license', key)
});
