#include "stdafx.h"
#include "FileParse.h"

FileParse::FileParse(void)
{

}

FileParse::~FileParse(void)
{

}

void FileParse::RunParse(const char *tcpdata,IpPacket *ipobj,u_int tcpdatalen)
{
	if(ipobj->dport()==21)
	  FtpFileParse(tcpdata,ipobj,tcpdatalen);
}

void FileParse::FtpFileParse(const char * tcpdata, IpPacket *ipobj, u_int tcpdatalen)
{
	if((tcpdatalen-20)!=0)
	{
		string tcpdatastr((char*)(tcpdata+20),tcpdatalen-20);
		if(string::npos!=tcpdatastr.find("RETR"))
		{
			//FTP下载文件
		}
		else if(string::npos!=tcpdatastr.find("STOR"))
		{
			//FTP文件上传
		}
		else
		{

		}
	}
}