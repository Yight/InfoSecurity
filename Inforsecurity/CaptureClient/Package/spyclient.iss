[Setup]
AppName = SpyClient
AppVersion = 1.0.0
DefaultDirName = {pf}\SpyClient
DefaultGroupName = SpyClient
UninstallDisplayIcon = {app}\SpyClient.exe
Compression = lzma2
SolidCompression = yes
ShowLanguageDialog = yes
OutputDir = d:\output
[Files]
Source: "log4cplus.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "mfc100chs.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "mfc100.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "mfc100d.dll"; DestDir: "{app}"; Flags: ignoreversionSource: "mfc100u.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "msvcp100.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "msvcr100.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "npf.sys"; DestDir: "{app}"; Flags: ignoreversion
Source: "npf64.sys"; DestDir: "{app}"; Flags: ignoreversion
Source: "npptools.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "Packet.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "pthreadVC.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "SpyClient.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "wpcap.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "sqlite3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "WanPacket.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "readme.txt"; DestDir: "{app}"; Flags: isreadme
Source: "config.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "npf.sys"; DestDir: "{sys}\drivers"; Flags: ignoreversion; check: not IsWin64
Source: "npf64.sys"; DestDir: "{sys}\drivers"; DestName: "npf.sys"; Flags: ignoreversion 64bit; check: IsWin64


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
[Icons]
Name: "{group}\SpyClient"; Filename: "{app}\SpyClient.exe"
Name: "{group}\Uninstall SpyClient"; Filename: "{uninstallexe}";
Name: "{commondesktop}\SpyClient"; Filename:"{app}\SpyClient.exe"; Tasks: desktopicon
;[INI]
;[InstallDelete]
;[Messages][Registry]
Root: HKCR; Subkey: "SOFTWARE\MoniClient"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "cs"; MessagesFile: "compiler:Languages\Chinese.isl"
[Run]
Filename:"{sys}\sc.exe"; Parameters: "create MonitorSCPHost binPath= ""{app}\SpyClient.exe"" start= auto"
Filename:"{sys}\sc.exe"; Parameters: "start MonitorSCPHost"
[UninstallDelete]
 Type:files; Name: "{app}\log4cplus.dll"
 Type:files; Name: "{app}\mfc100.dll"
 Type:files; Name: "{app}\mfc100chs.dll"
 Type:files; Name: "{app}\mfc100d.dll"
 Type:files; Name: "{app}\mfc100u.dll"
 Type:files; Name: "{app}\msvcp100.dll"
 Type:files; Name: "{app}\msvcr100.dll"
 Type:files; Name: "{app}\npf.sys"
 Type:files; Name: "{app}\npf64.sys"
 Type:files; Name: "{app}\npptools.dll"
 Type:files; Name: "{app}\Packet.dll"
 Type:files; Name: "{app}\pthreadVC.dll"
 Type:files; Name: "{app}\SpyClient.exe"
 Type:files; Name: "{app}\wpcap.dll"
 Type:files; Name: "{app}\sqlite3.dll"
 Type:files; Name: "{app}\WanPacket.dll"
 Type:files; Name: "{app}\readme.txt"
 Type:files; Name: "{app}\SpyClient.log"
 Type:files; Name: "{app}\config.ini"
[UninstallRun]
Filename: "{sys}\sc.exe"; Parameters: "stop MonitorSCPHost"  Filename: "{sys}\sc.exe"; Parameters: "delete MonitorSCPHost" 

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
if CurUninstallStep = usUninstall then
if MsgBox('您是否要删除注册信息？', mbConfirmation, MB_YESNO) = IDYES then
RegDeleteKeyIncludingSubkeys(HKEY_CLASSES_ROOT, 'Software\\MoniClient')
end;


