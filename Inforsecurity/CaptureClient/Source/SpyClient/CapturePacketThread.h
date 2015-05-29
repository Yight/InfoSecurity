#pragma once
#include "stdafx.h"
#include <string.h>
#include <pcap.h>
#include <ext_string.h>
#include "ProtoMessage.pb.h"
#include "EmailParse.h"
#include "LogMod.h"
#include "AppConfig.h"
#include "sqlite3.h"
#include "md5.h"
#include <map>
using namespace SpyClient;
using namespace std;


class CapturePacketThread : public CWinThread
{
	DECLARE_DYNCREATE(CapturePacketThread)
protected:
    CapturePacketThread(){}        // protected constructor used by dynamic creation
    virtual ~CapturePacketThread(){}
    virtual BOOL InitInstance();
    virtual int ExitInstance();
	DECLARE_MESSAGE_MAP()
    afx_msg void OnRun(WPARAM wParam, LPARAM lParam);

public:
	void SetDev(string devname,string ipstr);
	static void SetPbThread(CWinThread* pfthread);
	int RunCapture();

private:
	string devname;
	string ipstr;
	static CWinThread* pfthread;
	static int DetectWebMailProvider(std::ext_string tcpdata,int dstport);
	static void CopyEmailObj(EmailPacket *emailpacket, IpPacket *ippacket, EmailParse *emailparse);
	static void PacketHandler(u_char * user,const struct pcap_pkthdr *h,const u_char * p);
	static void TcpPacketHandler(const u_char *tcpdata,IpPacket *ipobj,u_int tcpdatalen,string localip);
	static void UdpPacketHandler(const u_char *udpdata,IpPacket *ipobj,u_int udpdatalen,string localip);
	static void HttpPacketHandler(std::ext_string httpdatastr,IpPacket *ipobj,u_int httpdatalen);
	static void SmtpPacketHandler(const u_char *smtpdata,IpPacket *ipobject,u_int smtplen);
	static int CheckIpPacket(IpPacket *ipobject,string localip);
	//static int CheckDict(map<int,int>::iterator pdictit,map<int,int> *pdict,int port,int pid,string processpath);
	//static int CheckDict(int port,int pid,string processpath,int protocoltype);
	//static map<int,int> *tcppdict = new map<int,int>;
	//static map<int,int> tcppdict;
	//static map<int,int> *udppdict = new map<int,int>;
	//static map<int,int> udppdict;
	//static map<int,int>::iterator pdictit;
};