#include "StdAfx.h"
#include <sstream>
#include <stdlib.h>
#include <time.h>
#include "PacketStruct.h"
#include "CapturePacketThread.h"
#include "ProcessMap.h"
#include <string>

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

#define PROVIDER_COUNT 8
ext_string emailfilters[PROVIDER_COUNT][3] = {
	{"163_126_yeah","cwebmail.mail.163.com","name%3d%22action%22%3edeliver"},
	{"qq","mail.qq.com","cginame=compose_send"},
	{"yahoo","","\"simplebody\""},
	{"sina","","content-disposition: form-data; name=\"from\""},
	{"sohu","","addressbook_use_flag"},
	{"139","","<string name=\"account\">"},
	{"foxmail","","x-mailer: foxmail"},
	{"normalsmtp","",""}
};


CWinThread* CapturePacketThread::pfthread = NULL;

IMPLEMENT_DYNCREATE(CapturePacketThread, CWinThread)

BEGIN_MESSAGE_MAP(CapturePacketThread, CWinThread)
    ON_THREAD_MESSAGE(WM_RUN, OnRun)
END_MESSAGE_MAP()


BOOL CapturePacketThread::InitInstance()
{
	BOOL worked=CWinThread::InitInstance();
	CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
	MSG msg;
	RunCapture();
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	
    return TRUE;
}

int CapturePacketThread::ExitInstance()
{
    return CWinThread::ExitInstance();
}

void CapturePacketThread::OnRun(WPARAM wParam, LPARAM lParam) {
    RunCapture();
}

void CapturePacketThread::SetDev(string devname,string ipstr)
{
    std::cout<<"got dev:"<<devname<<std::endl;
    this->devname = devname;
	this->ipstr = ipstr;
}

void CapturePacketThread::SetPbThread(CWinThread* pfthread)
{
	CapturePacketThread::pfthread = pfthread;
}

int CapturePacketThread::RunCapture()
{
	Releaseinfo("RunCapture  input");
    pcap_t *adhandle;
    char errbuf[PCAP_ERRBUF_SIZE];
    u_int netmask=0xffffff;
    struct bpf_program fp;
    
    if((adhandle= pcap_open(devname.c_str(),          // name of the device
                              65536,            // portion of the packet to capture
                                                // 65536 guarantees that the whole packet will be captured on all the link layers
                              PCAP_OPENFLAG_PROMISCUOUS,    // promiscuous mode
                              1000,             // read timeout
                              NULL,             // authentication on the remote machine
                              errbuf            // error buffer
                              ) ) == NULL)
    {
		Releaseinfo("pcap_open fails");
        fprintf(stderr,"\nUnable to open the adapter. %s is not supported by WinPcap\n", devname.c_str());
        return -1;
    }
	string filter("");
	string host_str("");
	host_str = AppConfig::SharedInstance()->GetHostIp();
	filter+="host ";
	filter+=ipstr;
	filter+=" and (tcp or udp) and (not host ";
	filter+=host_str;
	filter+=")";
	//char test_filter[100]={0};
	//strcpy(test_filter,filter.c_str());
	//Releaseinfo(test_filter);
    if(pcap_compile(adhandle, &fp, filter.c_str(), 0, netmask) == -1) {
		Releaseinfo("pcap_compile fails");
        fprintf(stderr, "Error calling pcap_compile\n");
        return -1;
    }
 
    if(pcap_setfilter(adhandle, &fp) == -1) {
		Releaseinfo("pcap_setfilter fails");
        fprintf(stderr, "Error setting filter\n");
        return -1;
    }
	char user_ip[20]={0};
	strcpy(user_ip,ipstr.c_str());
    pcap_loop(adhandle, 0, PacketHandler, (u_char*)user_ip);
    return 0;
}

int CapturePacketThread::DetectWebMailProvider(std::ext_string tcpdata,int dstport)
{

    tcpdata.tolower(); 
	if(dstport == 25)
	{
		if(string::npos!=tcpdata.find("x-mailer: foxmail") && string::npos!=tcpdata.find("from") && string::npos!=tcpdata.find("subject") )
			return PROVIDER_COUNT-2;
		else
		{
			if(string::npos!=tcpdata.find("from") && string::npos!=tcpdata.find("subject"))
				return PROVIDER_COUNT-1;
		}
	}
    for(int i=0;i<PROVIDER_COUNT-2;i++)
    {
        if(string::npos!=tcpdata.find(emailfilters[i][2]))
		{	
            return i;
		}
    }

    return -1;
}

void CapturePacketThread::HttpPacketHandler(std::ext_string httpdatastr,IpPacket *ipobj,u_int httpdatalen)
{
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
	//int ByVarNum = url.length() + 1;
	//byte *ByVar;
	//ByVar = (byte *)malloc(sizeof(byte)*ByVarNum);
	//memset(ByVar,0,ByVarNum);
	//byte ByVar[255] = {0};
	//for (int i=0;i<url.length();i++)
	//{
	//	ByVar[i] =(byte)url[i];
	//}
    ext_string httpurl_ext = "http://"+host+url;
	//httpurl_ext.append((char *)ByVar);
	if(httpurl_ext.length()>7)
	{
	  HttpPacket* httpobj = new HttpPacket();
	  httpobj->set_processname(ipobj->processname());
	  httpobj->set_processmd5(ipobj->processmd5());
	  httpobj->set_sip(ipobj->sip());
	  httpobj->set_dip(ipobj->dip());
	  httpobj->set_sport(ipobj->sport());
	  httpobj->set_dport(ipobj->dport());
	  httpobj->set_datetime(ipobj->datetime());
	  httpobj->set_httpurl(httpurl_ext.c_str());
	  pfthread->PostThreadMessage(PROTOBUF_HTTP_MESSAGE, 0, (LPARAM)httpobj);
	  httpobj=NULL;
	}
    //CLogMod::SharedInstance()->LogInfo(httpurl_ext.c_str());
	//#BUG print bug here
   // cout<<"httpurl_ext:"<<httpurl_ext<<endl;
}

void CapturePacketThread::UdpPacketHandler(const u_char *udpdata,IpPacket *ipobj,u_int udpdatalen,string localip)
{
    PROTOCOL_DEFINE::UDP_HEADER *udp=(PROTOCOL_DEFINE::UDP_HEADER *)udpdata;
    ipobj->set_dport(ntohs(udp->dport));
    ipobj->set_sport(ntohs(udp->sport));
	ipobj->set_protocoltype(UDP_PROTOCOL);
	if(CheckIpPacket(ipobj,localip))
	{
		delete ipobj;
		return ;
	}
	
	Releaseinfo("catch udp");
	pfthread->PostThreadMessage(PROTOBUF_IP_MESSAGE, 0, (LPARAM)ipobj);
	ipobj = NULL;
	udp = NULL;
	

}

void CapturePacketThread::CopyEmailObj(EmailPacket *emailobj, IpPacket *ipobj, EmailParse *emailparse)
{
	emailobj->set_sip(ipobj->sip());
	emailobj->set_dip(ipobj->dip());
	emailobj->set_sport(ipobj->sport());
	emailobj->set_dport(ipobj->dport());
	emailobj->set_datetime(ipobj->datetime());
	emailobj->set_processname(ipobj->processname());
	emailobj->set_processmd5(ipobj->processmd5());
	emailobj->set_sendfrom(emailparse->GetSendMailObj());
	emailobj->set_sendto(emailparse->GetToMailObj());
	emailobj->set_sendcc(emailparse->GetCcMailObj());
	emailobj->set_sendbcc(emailparse->GetBccMailObj());
	emailobj->set_subject(emailparse->GetSubJectObj());
	emailobj->set_emailtype(emailparse->Getemailtype());
}

void CapturePacketThread::TcpPacketHandler(const u_char *tcpdata,IpPacket *ipobj,u_int tcpdatalen,string localip)
{   
    PROTOCOL_DEFINE::TCP_HEADER *tcp=(PROTOCOL_DEFINE::TCP_HEADER *)tcpdata;
    ipobj->set_dport(ntohs(tcp->dport));
    ipobj->set_sport(ntohs(tcp->sport));
	ipobj->set_protocoltype(TCP_PROTOCOL);
	if(CheckIpPacket(ipobj,localip))
	{
		delete ipobj;
		return ;
	}

	Releaseinfo("catch tcp");
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
		int emailprovider = DetectWebMailProvider(tcpdatastr,ipobj->dport());
		if(-1 != emailprovider)
		{
			cout<<"found emailprovider:"<<emailprovider<<endl;
            EmailParse* emailparse = new EmailParse();
            emailparse->SetEmailProvider(emailprovider);
            emailparse->RunParse(tcpdatastr);
			ext_string from_ext;
			from_ext = emailparse->GetSendMailObj();

			char teststr[100]={0};
			strcpy(teststr,from_ext.c_str());
			Releaseinfo("email:");
			Releaseinfo(teststr);

			if(string::npos!=from_ext.find("@"))
			{
				char teststr1[100]={0};
				strcpy(teststr1,from_ext.c_str());
				Releaseinfo("email1:");
				Releaseinfo(teststr1);
				EmailPacket *emailobj = new EmailPacket();
				CopyEmailObj(emailobj,ipobj,emailparse);
				pfthread->PostThreadMessage(PROTOBUF_EMAIL_MESSAGE,0,(LPARAM)emailobj);
				emailobj = NULL;
			}
			delete emailparse;
		}
	}
	pfthread->PostThreadMessage(PROTOBUF_IP_MESSAGE, 0, (LPARAM)ipobj);

	
}


int CapturePacketThread::CheckIpPacket(IpPacket *ipobject,string localip)
{
	int port;
	int protocol;
	int pid;
	string processname;
	string processpath;
	int rc;
	if(localip == ipobject->sip())
		port = ipobject->sport();
	else
		port = ipobject->dport();
	protocol = ipobject->protocoltype();
	pid = ProcessMap::SharedInstance()->GetProcessPid(port,protocol);
	processname = ProcessMap::SharedInstance()->GetProcessName(pid,port,protocol);
	processpath = ProcessMap::SharedInstance()->GetProcessPath(pid,port,protocol);
//用于处理和判断
	if (pid!=-1 && processname!="" && processpath!="")
	{
			/*if(protocol == 0){	
				rc = Md5Map::SharedInstance()->CheckDict(port,pid,processpath,protocol);
				if(rc) return 1;
			}
			else 
			{
				rc = Md5Map::SharedInstance()->CheckDict(port,pid,processpath,protocol);
				if(rc) return 1;
			}*/
		rc = Md5Map::SharedInstance()->CheckDict(port,pid,processpath,protocol);
		if(rc) return 1;
	}
	string md5;
	md5 = Md5Map::SharedInstance()->GetMd5(processpath);
	ipobject->set_processname(processname);
	ipobject->set_processmd5(md5);
	return 0;
}

void CapturePacketThread::PacketHandler(u_char * user,const struct pcap_pkthdr *h,const u_char * p)
{
	//Releaseinfo("PacketHandler input");
    struct tm ltime;
    char timestr[20]={0};
    time_t local_tv_sec;
	char *ipc =(char *)user;
	string ipstr("");
	ipstr = ipc;
	local_tv_sec = h->ts.tv_sec;
    localtime_s(&ltime, &local_tv_sec);
    strftime( timestr, sizeof timestr, "%Y-%m-%d %H:%M:%S", &ltime);
	PROTOCOL_DEFINE::IP_HEADER *ip=(PROTOCOL_DEFINE::IP_HEADER *)(p+14);
	char srcipstr[16]={0};
    char desipstr[16]={0};
    sprintf(srcipstr,"%d.%d.%d.%d",ip->src_addr[0],ip->src_addr[1],ip->src_addr[2],ip->src_addr[3]);
    sprintf(desipstr,"%d.%d.%d.%d",ip->des_addr[0],ip->des_addr[1],ip->des_addr[2],ip->des_addr[3]);
	u_int ipheaderlen=PROTOCOL_DEFINE::GetIPHeaderLength(ip);
	IpPacket *ipobj = new IpPacket();
	string srcip_str = srcipstr;
	string desip_str = desipstr;
    ipobj->set_sip(srcipstr);
    ipobj->set_dip(desipstr);
    ipobj->set_datetime(timestr);
    ipobj->set_length(h->len);
	if(srcip_str == ipstr)
		ipobj->set_flow(0); //0表示上传
	if(desip_str == ipstr)
		ipobj->set_flow(1);//1表示下传
	switch(ip->protocol)
    {
        case TCP:
			{
				TcpPacketHandler(p+14+ipheaderlen,ipobj,h->len-14-ipheaderlen,ipstr);
				
			}
            break;
        case UDP:
			{
				UdpPacketHandler(p+14+ipheaderlen,ipobj,h->len-14-ipheaderlen,ipstr);
				
			}
            break;
		default:
            //Should't be here
			delete ipobj;
			return;
    }
}

