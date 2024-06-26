# Windows Sandbox with VS Code Pre-Installed
## Script to launch Windows Sandbox with latest VS Code installed

Windows Sandbox needs PRO version of the OS.   

To enable Windows Sandbox execute Powershell with Administrative privileges and execute the following:

```shell
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online
```

Make sure Git is installed locally (https://git-scm.com/download/gui/windows)

```shell
# Switch to root of c:
cd c:\

# Git clone with the folder name as sandbox
git clone https://github.com/AMISConclusion/Workshop_LocalLLM.git sandbox

# Run Windows Sandbox with this config
c:\sandbox\vscode.wsb
```

Once Windows Sandbox is launched, it will download and install the latest version of Visual Studio Code.  
Also the `C:\sandbox\Projects` folder will be available inside Windows Sandbox under `Documents/Projects`
