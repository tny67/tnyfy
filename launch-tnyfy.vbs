Set WshShell = WScript.CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\Famille Massini\ia tnyfy\desktop"
WshShell.Run "cmd /c ""set PATH=C:\Program Files\nodejs;%PATH% && npx electron . --dev""", 0, False
