

#include "stdafx.h"

#include <winsvc.h>
#include <stdio.h>
#include "ServiceCtrl.h"
#include "MonCtrl.h"


//HANDLE					hMutex;
//LPPROCESSDATA			lpProcessDataHead;
//LPPROCESSDATA			lpProcessDataEnd;
SERVICE_STATUS			ServiceStatus;
SERVICE_STATUS_HANDLE	ServiceStatusHandle;

// 服务初始化
int WINAPI InitService() 
{ 
 
    return 0; 
}

int WriteLog(WCHAR *msg)
{
/*
	setlocale(LC_ALL, "chs");

	FILE *fp;
	if ((fp = fopen("d:\\record_1.txt", "a+")) == NULL)
	{
		return -1;
	}

	fwprintf(fp, _T("%ls\n"),  msg);
	fclose(fp);
*/
	return 0;
}

void WINAPI CmdStart(DWORD dwArgc, LPTSTR* lpArgv)	// 执行操作创建服务线程
{
	WriteLog(_T("serviceBEGIN"));

	ServiceStatus.dwServiceType			= SERVICE_WIN32;
	ServiceStatus.dwCurrentState		= SERVICE_START_PENDING;
	ServiceStatus.dwControlsAccepted	= SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
	ServiceStatus.dwServiceSpecificExitCode = 0;
	ServiceStatus.dwWin32ExitCode			= 0;
	ServiceStatus.dwCheckPoint				= 0;
	ServiceStatus.dwWaitHint				= 0;

	ServiceStatusHandle = RegisterServiceCtrlHandler(_T("MonitorStandby"), CmdControl);
	
	if(ServiceStatusHandle == NULL)
	{
		return;
	}

	int error = InitService(); 

	if (error < 0) 
	{
	  // Initialization failed
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
		return;
	}


	CMonCtrl::Instance()->DW_Init();

	return;
}

void WINAPI CmdControl(DWORD dwCode)	// 接收各种控制命令
{
	switch(dwCode)
	{
	case SERVICE_CONTROL_STOP: 

		ServiceStatus.dwWin32ExitCode = 0; 
		ServiceStatus.dwCurrentState = SERVICE_STOPPED; 
		SetServiceStatus (ServiceStatusHandle, &ServiceStatus);
		CMonCtrl::Instance()->DW_Destory();
		return;

	case SERVICE_CONTROL_SHUTDOWN:
		ServiceStatus.dwWin32ExitCode = 0; 
		ServiceStatus.dwCurrentState = SERVICE_STOPPED; 
		SetServiceStatus (ServiceStatusHandle, &ServiceStatus);
		CMonCtrl::Instance()->DW_Destory();
		return;

	default:
		break;
	}

	// Report current status
    SetServiceStatus (ServiceStatusHandle, &ServiceStatus);

	return;
}