Set WshShell = WScript.CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set shortcut = WshShell.CreateShortcut(strDesktop & "\Tnyfy.lnk")
shortcut.TargetPath = "wscript.exe"
shortcut.Arguments = """D:\Famille Massini\ia tnyfy\launch-tnyfy.vbs"""
shortcut.WorkingDirectory = "D:\Famille Massini\ia tnyfy"
shortcut.IconLocation = "D:\Famille Massini\ia tnyfy\desktop\icon.ico, 0"
shortcut.Description = "Tnyfy - AI E-Commerce Automation Platform"
shortcut.WindowStyle = 1
shortcut.Save
WScript.Echo "Raccourci Tnyfy mis a jour sur le bureau !"
