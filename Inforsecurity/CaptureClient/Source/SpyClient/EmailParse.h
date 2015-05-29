#pragma once
#define JUDGEFIND(found) 	if(std::string::npos==found) return FALSE;

#include <vector>
#include <ext_string.h>
#include "LogMod.h"
using namespace std;

class EmailParse
{
public:
	EmailParse(void);
	~EmailParse(void);
	void SetEmailProvider(int emailprovider);
	int RunParse(std::ext_string emaildata_extstr);
	int Parse163mail(std::ext_string emaildata_extstr);
	int ParseQqmail(std::ext_string emaildata_extstr);
	int ParseYahoomail(std::ext_string emaildata_extstr);
	int ParseSinamail(std::ext_string emaildata_extstr);
	int ParseSohumail(std::ext_string emaildata_extstr);
	int Parse139mail(std::ext_string emaildata_extstr);
	int ParseOutlook(std::ext_string emaildata_extstr);
	int ParseFoxmail(std::ext_string emaildata_extstr);
	int ParseSmtp(std::ext_string emaildata_exstr);
	ext_string GetSendMailObj(){return sendmailobj;};
	ext_string GetToMailObj(){return tomailobj;};
	ext_string GetCcMailObj(){return ccmailobj;};
	ext_string GetBccMailObj(){return bccmailobj;};
	ext_string GetSubJectObj(){return subjectobj;};
	ext_string GetContentObj(){return contentobj;};
	int Getemailtype(){return emailprovider;};
    ext_string ConvertUChar(ext_string inputstr);
	ext_string ParseMailAddress(ext_string mailstr);
private:	
	int emailprovider;
	ext_string sendmailobj;
	ext_string tomailobj;
	ext_string ccmailobj;
	ext_string bccmailobj;
	ext_string subjectobj;
	ext_string contentobj;
};