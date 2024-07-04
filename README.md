# Windows Sandbox with various LLM tools Pre-Installed
## Script to launch Windows Sandbox

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

Once Windows Sandbox is launched, it will download and install required files for the workshop. The download process consists of several Gbs and can take a while

Read the document [here](https://github.com/AMISConclusion/Workshop_LocalLLM/blob/main/workshop%20local%20model.docx)  for the complete workshop 
