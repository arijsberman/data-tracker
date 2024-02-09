Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run "myvenv\Scripts\python.exe main.py", 0
Set WshShell = Nothing
