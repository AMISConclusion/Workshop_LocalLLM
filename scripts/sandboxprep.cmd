curl -L "https://update.code.visualstudio.com/latest/win32-x64/stable" --output C:\users\WDAGUtilityAccount\Downloads\vscode.exe
REM curl -L "https://releases.lmstudio.ai/windows/0.2.27/latest/LM-Studio-0.2.27-Setup.exe" --output C:\users\WDAGUtilityAccount\Downloads\LM-Studio-0.2.27-Setup.exe
curl -L "https://ollama.com/download/OllamaSetup.exe" --output C:\users\WDAGUtilityAccount\Downloads\OllamaSetup.exe
C:\users\WDAGUtilityAccount\Downloads\OllamaSetup.exe /verysilent
C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Ollama\ollama.exe pull dolphin-mistral:7b
curl -L https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe --output C:\users\WDAGUtilityAccount\Downloads\python.exe
C:\users\WDAGUtilityAccount\Downloads\python.exe -Wait /PrependPath=1 /quiet InstallAllUsers=1 TargetDir="C:\python" Include_test=0
curl -L https://aka.ms/vs/17/release/vs_BuildTools.exe --output C:\users\WDAGUtilityAccount\Downloads\vs_BuildTools.exe
C:\users\WDAGUtilityAccount\Downloads\vs_BuildTools.exe --wait --includeRecommended --quiet --add Microsoft.Component.MSBuild --add Microsoft.VisualStudio.Component.CoreBuildTools --add Microsoft.VisualStudio.Component.VC.CoreBuildTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.VC.Redist.14.Latest --add Microsoft.VisualStudio.Component.VC.CoreIde --add Microsoft.VisualStudio.Component.Windows11SDK.22621 --add Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core --add Microsoft.VisualStudio.Workload.MSBuildTools --add Microsoft.VisualStudio.Workload.VCTools
REM curl -L "https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda_12.3.2_546.12_windows.exe" --output C:\users\WDAGUtilityAccount\Downloads\cuda_12.3.2_546.12_windows.exe
REM C:\users\WDAGUtilityAccount\Downloads\cuda_12.3.2_546.12_windows.exe -s 
REM curl -L https://github.com/Kitware/CMake/releases/download/v3.24.0/cmake-3.24.0-windows-x86_64.msi --output C:\users\WDAGUtilityAccount\Downloads\cmake.msi
REM msiexec /i C:\users\WDAGUtilityAccount\Downloads\cmake.msi ALLUSERS=1 ADD_CMAKE_TO_PATH=System /qn
c:\python\Scripts\pip.exe install llama_index llama-index-embeddings-huggingface chromadb onnxruntime openai
C:\users\WDAGUtilityAccount\Downloads\vscode.exe /verysilent /suppressmsgboxes /MERGETASKS=!runcode
"C:\Program Files\Microsoft VS Code\Code.exe" C:\users\WDAGUtilityAccount\Documents\Projects\demo --disable-workspace-trust

