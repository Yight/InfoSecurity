// SpyClient.cpp : 定义控制台应用程序的入口点。
//
#include "stdafx.h"
#include <stdio.h>
#include <windows.h>
#include <tchar.h>
#include <winsvc.h>
#include "StandBy.h"
#include "ServiceCtrl.h"
#include "MonCtrl.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

CWinApp theApp;

using namespace std;

int WriteL(WCHAR *msg)
{

	setlocale(LC_ALL, "chs");
	string m_installpath;
	CRegKey regkeyobj;
	LPCTSTR lpRegPath=_T("Software\\MoniClient");
	LONG IResult=regkeyobj.Open(HKEY_CLASSES_ROOT,lpRegPath,KEY_ALL_ACCESS);
	if(ERROR_SUCCESS==IResult)
	{
		ULONG u_RegStrSize=100;
		TCHAR RegStrBuff[100]={0};
		char c_installpath[100] = {0};
		if(regkeyobj.QueryStringValue(_T("InstallPath"),RegStrBuff,&u_RegStrSize)!=ERROR_SUCCESS)
		{
			regkeyobj.Close();
			return FALSE;
		}
		sprintf(c_installpath,"%s",RegStrBuff);
		m_installpath=c_installpath;
		m_installpath+="\\running.log";
		regkeyobj.Close();
	}

	FILE *fp;
	if ((fp = fopen(m_installpath.c_str(), "a+")) == NULL)
	{
		return -1;
	}

	fwprintf(fp, _T("%ls\n"),  msg);
	fclose(fp);
	return TRUE;
}

int _tmain(int argc, TCHAR* argv[], TCHAR* envp[])
{
	int nRetCode = 0;
	WriteL(_T("standby service BEGIN"));
	//sc <server> create [服务名] [binPath= ] <option1> <option2>...

	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))
	{
		nRetCode = 1;
	}
	else
	{
		WriteL(_T("serviceBEGIN"));
		if (!AfxSocketInit())
		{
			return -1;
		}

		SERVICE_TABLE_ENTRY ServiceTable[2];
		ServiceTable[0].lpServiceName = _T("MonitorStandby");
		ServiceTable[0].lpServiceProc = (LPSERVICE_MAIN_FUNCTION)CmdStart;
	    
		ServiceTable[1].lpServiceName = NULL;
		ServiceTable[1].lpServiceProc = NULL;

		StartServiceCtrlDispatcher(ServiceTable); 

	}

	return nRetCode;
/*	
	// run as win32 application not service
	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))
	{
		// TODO: 更改错误代码以符合您的需要
		_tprintf(_T("错误: MFC 初始化失败\n"));
		nRetCode = 1;
	}
	else
	{
		if (!AfxSocketInit())
		{
			return -1;
		}
		
		CMonCtrl::Instance()->DW_Init();
	}
	return nRetCode;
*/
}
