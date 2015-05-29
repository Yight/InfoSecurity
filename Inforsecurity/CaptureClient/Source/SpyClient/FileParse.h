#pragma once
#include "ProtoMessage.pb.h"
#include "pcap.h"
#include "string.h"
using namespace std;
using namespace SpyClient;
class FileParse
{
public:
	FileParse(void);
	~FileParse(void);
	void RunParse(const char *tcpdata,IpPacket *ipobj,u_int tcpdatalen);
	void FtpFileParse(const char * tcpdata, IpPacket *ipobj, u_int tcpdatalen);
	
};