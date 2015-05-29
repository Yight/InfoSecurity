reg add HKCR\SOFTWARE\MoniClient
reg add HKCR\SOFTWARE\MoniClient /v InstallPath /t REG_SZ /d E:\Dropbox\CaptureClient\Source\Release
reg add HKCR\SOFTWARE\MoniClient /v UserID /t REG_SZ /d 50fccfbb2f31932315d2e9ec
sc create MonitorSCPHost binPath= "E:\Dropbox\CaptureClient\Source\Release\SpyClient.exe" start= auto
sc start MonitorSCPHost