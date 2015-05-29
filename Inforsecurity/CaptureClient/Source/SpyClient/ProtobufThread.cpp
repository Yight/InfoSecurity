#include "stdafx.h"
#include <iostream>
#include "ProtobufThread.h"
#include "AppConfig.h"
#include "LogMod.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

IMPLEMENT_DYNCREATE(ProtobufThread, CWinThread)

BEGIN_MESSAGE_MAP(ProtobufThread, CWinThread)
    ON_THREAD_MESSAGE(PROTOBUF_IP_MESSAGE, OnIPMessage)
    ON_THREAD_MESSAGE(PROTOBUF_HTTP_MESSAGE, OnHTTPMessage)
	ON_THREAD_MESSAGE(PROTOBUF_EMAIL_MESSAGE,OnEmailMessage)
END_MESSAGE_MAP()

BOOL ProtobufThread::InitInstance()
{
	BOOL worked=CWinThread::InitInstance();

	email_vector = new vector<EmailPacket>;
	http_vector = new vector<HttpPacket>;
	ippacket_vector = new vector<IpPacket>;

    CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
    MSG msg;
    PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
    return TRUE;
}

int ProtobufThread::ExitInstance()
{
    return CWinThread::ExitInstance();
}

void ProtobufThread::SetSdThread(CWinThread* sdthread)
{
	ProtobufThread::sdthread=sdthread;
}

void ProtobufThread::OnEmailMessage(WPARAM wParam,LPARAM lParam)
{
	timeobj = CTime::GetCurrentTime();
	static int emailpacketcount = 0;
	static int emailbegintime = timeobj.GetMinute()*60+timeobj.GetSecond();
	static int emailendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	EmailPacket *emailobj = (EmailPacket *)lParam;
	email_vector->push_back(*emailobj);
	delete emailobj;
	emailobj = NULL;
	emailpacketcount++;
	emailendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	if(emailpacketcount>0 || (emailendtime-emailbegintime)>20)
	{
		//send email packet 
		vector<EmailPacket> *emailvector;
		emailvector=email_vector;
		email_vector = new vector<EmailPacket>;
		sdthread->PostThreadMessage(SENDDATA_REC_EMAILMESSAGE,0,(LPARAM)emailvector);
		emailvector = NULL;
		emailpacketcount = 0;
		timeobj = CTime::GetCurrentTime();
		emailbegintime =  timeobj.GetMinute()*60+timeobj.GetSecond();
	}
}

void ProtobufThread::OnIPMessage(WPARAM wParam, LPARAM lParam){
	timeobj = CTime::GetCurrentTime();
	static int ippacketcount = 0;
	static int ipbegintime = timeobj.GetMinute()*60+timeobj.GetSecond();
	static int ipendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	IpPacket *ipobj = (IpPacket *)lParam;
	ippacket_vector->push_back(*ipobj);
	delete ipobj;
	ipobj = NULL;
	ippacketcount++;
	ipendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	if(ippacketcount>20 || (ipendtime-ipbegintime)>20)
	{
		//send email packet 
		vector<IpPacket> *ippacketvector;
		ippacketvector = ippacket_vector;
		ippacket_vector = new vector<IpPacket>;
		sdthread->PostThreadMessage(SENDDATA_REC_IPMESSAGE,0,(LPARAM)ippacketvector);
		ippacketvector = NULL;
		ippacketcount = 0;
		timeobj = CTime::GetCurrentTime();
		ipbegintime =  timeobj.GetMinute()*60+timeobj.GetSecond();
	}

}

void ProtobufThread::OnHTTPMessage(WPARAM wParam, LPARAM lParam)
{
	timeobj = CTime::GetCurrentTime();
	static int httppacketcount = 0;
	static int httpbegintime = timeobj.GetMinute()*60+timeobj.GetSecond();
	static int httpendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	HttpPacket *httpobj = (HttpPacket *)lParam;
	http_vector->push_back(*httpobj);
	delete httpobj;
	httpobj = NULL;
	httppacketcount++;
	httpendtime = timeobj.GetMinute()*60+timeobj.GetSecond();
	if(httppacketcount>20 || (httpendtime-httpbegintime)>20 )
	{
		//send http packet;
		vector<HttpPacket> *httpvector;
		httpvector = http_vector;
		http_vector = new vector<HttpPacket>;
		sdthread->PostThreadMessage(SENDDATA_REC_HTTPMESSAGE,0,(LPARAM)httpvector);
		httpvector = NULL;
		httppacketcount = 0;
		timeobj = CTime::GetCurrentTime();
		httpbegintime = timeobj.GetMinute()*60+timeobj.GetSecond();
	}
}

void ProtobufThread::OnQuit(WPARAM wParam, LPARAM lParam) 
{
    AfxEndThread(0);
}
