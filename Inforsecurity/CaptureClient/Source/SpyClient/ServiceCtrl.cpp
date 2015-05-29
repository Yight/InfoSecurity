#include "stdafx.h"
#include <winsvc.h>
#include <stdio.h>
#include "ServiceCtrl.h"
#include "MainCtrl.h"
#include "LogMod.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

//HANDLE					hMutex;
//LPPROCESSDATA			lpProcessDataHead;
//LPPROCESSDATA			lpProcessDataEnd;
SERVICE_STATUS			ServiceStatus;
SERVICE_STATUS_HANDLE	ServiceStatusHandle;

// 服务初始化
int WINAPI InitService() 
{ 
	//CBase::Instance()->WriteLog("init service"); 
    return 0; 
}

void WINAPI CmdStart(DWORD dwArgc, LPTSTR* lpArgv)	// 执行操作创建服务线程
{

	ServiceStatus.dwServiceType			= SERVICE_WIN32;
	ServiceStatus.dwCurrentState		= SERVICE_START_PENDING;
	ServiceStatus.dwControlsAccepted	= SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
	ServiceStatus.dwServiceSpecificExitCode = 0;
	ServiceStatus.dwWin32ExitCode			= 0;
	ServiceStatus.dwCheckPoint				= 0;
	ServiceStatus.dwWaitHint				= 0;
	Releaseinfo("CmdStart");
	ServiceStatusHandle = RegisterServiceCtrlHandler(_T("MonitorSCPHost"), CmdControl);
	Releaseinfo("ServiceStatusHandle");
	if(ServiceStatusHandle == NULL)
	{
		Releaseinfo("ServiceStatusHandle == NULL");
		return;
	}

	int error = InitService(); 

	if (error < 0) 
	{
	  // Initialization failed
	  Releaseinfo("error < 0");
	  ServiceStatus.dwCurrentState =  SERVICE_STOPPED; 
	  ServiceStatus.dwWin32ExitCode = -1; 
	  SetServiceStatus(ServiceStatusHandle, &ServiceStatus); 
	  
	  return; 
	} 

	ServiceStatus.dwCurrentState	= SERVICE_RUNNING;
	ServiceStatus.dwCheckPoint		= 0;
	ServiceStatus.dwWaitHint		= 0;
	
	if(SetServiceStatus(ServiceStatusHandle, &ServiceStatus) == 0)
	{
		Releaseinfo("SetServiceStatus(ServiceStatusHandle, &ServiceStatus) == 0");
		return;
	}

	//CBase::Instance()->WriteLog("service running");
	//CMonCtrl::Instance()->DW_Init();
	CMainCtrl::SharedInstance()->Init();
	return;
}

void WINAPI CmdControl(DWORD dwCode)	// 接收各种控制命令
{
	CLogMod::SharedInstance()->LogInfo("CmdControl");
	switch(dwCode)
	{
	case SERVICE_CONTROL_STOP: 

		ServiceStatus.dwWin32ExitCode = 0; 
		ServiceStatus.dwCurrentState = SERVICE_STOPPED; 
		SetServiceStatus (ServiceStatusHandle, &ServiceStatus);
		CMainCtrl::SharedInstance()->StopService();
		return;

	case SERVICE_CONTROL_SHUTDOWN:
		ServiceStatus.dwWin32ExitCode = 0; 
		ServiceStatus.dwCurrentState = SERVICE_STOPPED; 
		SetServiceStatus (ServiceStatusHandle, &ServiceStatus);
		CMainCtrl::SharedInstance()->StopService();
		return;

	default:
		break;
	}

	// Report current status
	CLogMod::SharedInstance()->LogInfo("ServiceStatus");
    SetServiceStatus (ServiceStatusHandle, &ServiceStatus);

	return;
}