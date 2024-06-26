curl -L "https://update.code.visualstudio.com/latest/win32-x64/stable" --output C:\users\WDAGUtilityAccount\Downloads\vscode.exe
curl -L "https://releases.lmstudio.ai/windows/0.2.25/latest/LM-Studio-0.2.25-Setup.exe" --output C:\users\WDAGUtilityAccount\Downloads\LM-Studio-0.2.25-Setup.exe
curl -L "https://ollama.com/download/OllamaSetup.exe" --output C:\users\WDAGUtilityAccount\Downloads\OllamaSetup.exe
curl -L https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe --output C:\users\WDAGUtilityAccount\Downloads\python.exe
C:\users\WDAGUtilityAccount\Downloads\python.exe -Wait /PrependPath=1 /quiet InstallAllUsers=1 TargetDir="C:\python" Include_test=0
C:\users\WDAGUtilityAccount\Downloads\vscode.exe /verysilent /suppressmsgboxes /MERGETASKS=!runcode
"C:\Program Files\Microsoft VS Code\Code.exe" C:\users\WDAGUtilityAccount\Documents\Projects\demo

