Set WshShell = WScript.CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set shortcut = WshShell.CreateShortcut(strDesktop & "\Tnyfy.lnk")
shortcut.TargetPath = "D:\Famille Massini\ia tnyfy\start-tnyfy.bat"
shortcut.WorkingDirectory = "D:\Famille Massini\ia tnyfy"
shortcut.IconLocation = "D:\Famille Massini\ia tnyfy\tnyfy.ico, 0"
shortcut.Description = "Tnyfy - AI E-Commerce Automation Platform"
shortcut.WindowStyle = 1
shortcut.Save
WScript.Echo "Raccourci Tnyfy cree sur le bureau !"
