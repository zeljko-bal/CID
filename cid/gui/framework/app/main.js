const electron = require('electron')
// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow
// communication with renderer
const {ipcMain} = require('electron')
// child_process
const child_process = require('child_process');
// file system utils
const fs = require('fs');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({width: 1000, height: 800})

  // and load the index.html of the app.
  mainWindow.loadURL(`file://${__dirname}/index.html`)

  // Open the DevTools.
  //mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

let bat = null;

ipcMain.on('execute_command', (event, arg) => {
	mainWindow.close()
	console.log('__EXECUTE_COMMAND__:' + arg.cli_string)
})

ipcMain.on('close', () => {
	app.quit()
})

// helper commands

ipcMain.on('file_exists', (event, arg) => {
	event.returnValue = fs.existsSync(arg);
})

ipcMain.on('is_file', (event, arg) => {
	event.returnValue = fs.lstatSync(arg).isFile();
})

ipcMain.on('is_directory', (event, arg) => {
	event.returnValue = fs.lstatSync(arg).isDirectory();
})
