#pragma once
#include "stdafx.h"
#include <string>
#include "ProtoMessage.pb.h"
#include <ext_string.h>
#include "EmailParse.h"
#include "PacketStruct.h"
#include "CapturePacketThread.h"
using namespace SpyClient;
using namespace std;
// CDealPacketThread

class CDealPacketThread : public CWinThread
{
	DECLARE_DYNCREATE(CDealPacketThread)

protected:
	CDealPacketThread();           // 动态创建所使用的受保护的构造函数
	virtual ~CDealPacketThread();

public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();
	virtual void OnFinalRelease();
    void SetPbThread(CWinThread* pfthread);
	int DetectWebMailProvider(std::ext_string httppostdata,std::ext_string host,std::ext_string url);
	void CopyEmailObj(EmailPacket *emailpacket, IpPacket *ippacket, EmailParse *emailparse);
	void TcpPacketHandler(const u_char *tcpdata,IpPacket *ipobj,u_int tcpdatalen);
	void UdpPacketHandler(const u_char *udpdata,IpPacket *ipobj,u_int udpdatalen);
	void HttpPacketHandler(std::ext_string httpdatastr,IpPacket *ipobj,u_int httpdatalen);
private:
    CWinThread* pfthread;

protected:
	DECLARE_MESSAGE_MAP()
	afx_msg void OnDealPacketMessage(WPARAM wParam, LPARAM lParam);

};


