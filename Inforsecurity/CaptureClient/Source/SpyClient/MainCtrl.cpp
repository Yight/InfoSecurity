#include "StdAfx.h"
#define WIN32_LEAN_AND_MEAN
#include <winsock.h>
#include <pcap.h>
#include <string>
#include <afxinet.h>
#include "MainCtrl.h"
#include "ProtobufThread.h"
#include "CapturePacketThread.h"
#include "SendDataThread.h"
#include "LogMod.h"
#include "AppConfig.h"
//#include "Dict.h"
#include "ProcessMap.h"
#include "Utils.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif
using namespace std;
CMainCtrl* CMainCtrl::_instance = NULL;


/* From tcptraceroute, convert a numeric IP address to a string */
#define IPTOSBUFFERS    12
char *iptos(u_long in)
{
	static char output[IPTOSBUFFERS][3*4+3+1];
	static short which;
	u_char *p;

	p = (u_char *)&in;
	which = (which + 1 == IPTOSBUFFERS ? 0 : which + 1);
	_snprintf_s(output[which], sizeof(output[which]), sizeof(output[which]),"%d.%d.%d.%d", p[0], p[1], p[2], p[3]);
	return output[which];
}


CMainCtrl*  CMainCtrl::SharedInstance()
{	if (_instance == NULL)
	{
		_instance = new CMainCtrl;
	}
	return _instance;
}

CMainCtrl::~CMainCtrl(void)
{
	delete _instance;
}
//RunCapturePacket函数  Author:Zelong Yin
//RunCapturePacket函数的主要功能是把protobuf线程句柄传递到CapturePacketThread,并为每个网卡申请一个线程进行捕包
bool CMainCtrl::RunCapturePacket(CWinThread* pfthread)
{
	pcap_if_t *alldevs;
	pcap_if_t *d;
	int i;
	char errbuf[PCAP_ERRBUF_SIZE];
    //设置protobufthread的句柄pfthread
	CapturePacketThread::SetPbThread(pfthread); //**--**//997755+9++++/*++//**
	//Releaseinfo("RunCapture input");
	//寻找本机网络网卡，并将网卡列表赋值给alldevs
    if (pcap_findalldevs_ex(PCAP_SRC_IF_STRING, NULL, &alldevs, errbuf) == -1)
    {
		//Releaseinfo("pcap find fails");
		//CLogMod::SharedInstance()->LogError("Error in pcap_findalldevs");
        //fprintf(stderr,"Error in pcap_findalldevs: %s\n", errbuf);
        return false;
    }
    
    //给本地主机的每一个网卡创建线程
    for(d=alldevs,i=0; d; d=d->next,i++)
    {
		CapturePacketThread *pThread = (CapturePacketThread *)AfxBeginThread(RUNTIME_CLASS(CapturePacketThread), 
																				THREAD_PRIORITY_NORMAL, 
																				0, 
																				CREATE_SUSPENDED
																				);
		
		
		string ipstr("");
		pcap_addr_t *a;
		for(a=d->addresses;a;a=a->next) {
			if(AF_INET == a->addr->sa_family)
			{
				ipstr = iptos(((struct sockaddr_in *)a->addr)->sin_addr.s_addr);
			}
		}
		string devname = d->name;
		pThread->SetDev(devname,ipstr); //将IP地址和网卡名字赋值给CapturePacketThread
		pThread->ResumeThread(); //运行该线程
    }

    pcap_freealldevs(alldevs); //释放所有网卡
	//Releaseinfo("pcap_freealldevs");
	if(0==i)
    	return false;
    else
		return true;
}

void CMainCtrl::TestPostData()
{
	CInternetSession session;
	session.SetOption(INTERNET_OPTION_CONNECT_TIMEOUT, 1000 * 20);
	session.SetOption(INTERNET_OPTION_CONNECT_BACKOFF, 1000);
	session.SetOption(INTERNET_OPTION_CONNECT_RETRIES, 1);

	CHttpConnection* pConnection = session.GetHttpConnection( "192.168.0.224",(INTERNET_PORT)1337);
	CHttpFile* pFile = pConnection->OpenRequest( CHttpConnection::HTTP_VERB_POST,
		"/put/pc/ippackets",
		NULL,
		1,
		NULL,
		"HTTP/1.1",
		INTERNET_FLAG_RELOAD);

	//需要提交的数据
	CString szHeaders   = "Content-Type: application/x-www-form-urlencoded;";

	//下面这段编码，则是可以让服务器正常处理
	CHAR* strFormData = "username=WaterLin&password=TestPost";
	pFile->SendRequest( szHeaders,
		szHeaders.GetLength(),
		(LPVOID)strFormData,
		strlen(strFormData));

	DWORD dwRet;
	pFile->QueryInfoStatusCode(dwRet);

	if(dwRet != HTTP_STATUS_OK)
	{
		CString errText;
		errText.Format("POST出错，错误码：%d", dwRet);
	}
	else
	{
		int len = pFile->GetLength();
		char buf[2000];
		int numread;
		CString filepath;
		CString strFile = "result.html";
		filepath.Format(".\\%s", strFile);
		CFile myfile(filepath,
			CFile::modeCreate|CFile::modeWrite|CFile::typeBinary);
		while ((numread = pFile->Read(buf,sizeof(buf)-1)) > 0)
		{
			buf[numread] = '\0';
			strFile += buf;
			myfile.Write(buf, numread);
		}
		myfile.Close();
	}
	session.Close();
	pFile->Close(); 
	delete pFile;
}


//CMainCtrl 初始化函数 author:Zelong Yin

int CMainCtrl::Init(void)
{
	CLogMod::SharedInstance()->Init(); //CLogMod类的初始化,初始化日志模块
	if(!AppConfig::SharedInstance()->Init()) // CLogMod类的初始化。初始化配置文件
		return FALSE;
	//Releaseinfo("AppConfig success");
	std::cout<<"mac addr:"<<GetEthernetMacAddr()<<endl;
	std::cout<<"GetHostIp:"<<AppConfig::SharedInstance()->GetHostIp()<<endl;
	std::cout<<"pcid:"<<AppConfig::SharedInstance()->GetPcID()<<endl;
	//CLogMod::SharedInstance()->LogError("Make sure winpcap is installed and run as administrator!");
	//创建发送数据线程SendDataThread,并运行
	ProcessMap::SharedInstance()->Init();
	SendDataThread *sdthread = (SendDataThread *)AfxBeginThread(RUNTIME_CLASS(SendDataThread));
	sdthread->ResumeThread();
	
	//创建Protobuf线程用于对捕获的数据进行处理，并运行
	ProtobufThread *pfthread = (ProtobufThread *)AfxBeginThread(RUNTIME_CLASS(ProtobufThread));
	pfthread->SetSdThread(sdthread);//将发送数据的线程句柄赋给Protobuf线程，实现Protobuf线程向SendDataThread线程发送数据
	pfthread->ResumeThread();

	//捕包函数 RunCapturePacket 参数：pfthread传递给捕包线程，用于实现捕包线程向Protobuf线程发送数据
	if(!RunCapturePacket(pfthread))
	{
		Releaseinfo("RunCapture Error");
		//CLogMod::SharedInstance()->LogError("Make sure winpcap is installed and run as administrator!");
		exit(-1);
	}
	
	while(1)
	{
		Sleep(10000);
	}
	return 1;
}

void CMainCtrl::StopService(void)
{

}
