#include "StdAfx.h"
#include "EmailParse.h"
#include "base64.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif
char* G2U(const char* gb2312)
{
	int len = MultiByteToWideChar(CP_ACP, 0, gb2312, -1, NULL, 0);
	wchar_t* wstr = new wchar_t[len+1];
	memset(wstr, 0, len+1);
	MultiByteToWideChar(CP_ACP, 0, gb2312, -1, wstr, len);
	len = WideCharToMultiByte(CP_UTF8, 0, wstr, -1, NULL, 0, NULL, NULL);
	char* str = new char[len+1];
	memset(str, 0, len+1);
	WideCharToMultiByte(CP_UTF8, 0, wstr, -1, str, len, NULL, NULL);
	if(wstr) delete[] wstr;
	return str;
}
char* U2G(const char* utf8)
{
	int len = MultiByteToWideChar(CP_UTF8, 0, utf8, -1, NULL, 0);
	wchar_t* wstr = new wchar_t[len+1];
	memset(wstr, 0, len+1);
	MultiByteToWideChar(CP_UTF8, 0, utf8, -1, wstr, len);
	len = WideCharToMultiByte(CP_ACP, 0, wstr, -1, NULL, 0, NULL, NULL);
	char* str = new char[len+1];
	memset(str, 0, len+1);
	WideCharToMultiByte(CP_ACP, 0, wstr, -1, str, len, NULL, NULL);
	if(wstr) delete[] wstr;
	return str;
}
EmailParse::EmailParse(void)
{
}


EmailParse::~EmailParse(void)
{
}

void EmailParse::SetEmailProvider(int emailprovider)
{
	this->emailprovider = emailprovider;
}

int EmailParse::RunParse(std::ext_string emaildata_extstr)
{
	size_t found;
	switch(emailprovider)
	{
	case PROVIDER_163_126_YEAH:
		found=emaildata_extstr.find("account");
		JUDGEFIND(found)
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		Parse163mail(emaildata_extstr);
		break;
	case PROVIDER_QQ:
		found=emaildata_extstr.find("from_s=cnew&");
		JUDGEFIND(found)
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		ParseQqmail(emaildata_extstr);
		break;
	case PROVIDER_YAHOO:
		found=emaildata_extstr.find("SendMessage");
		JUDGEFIND(found);
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		ParseYahoomail(emaildata_extstr);
		break;
	case PROVIDER_SINA:
		found=emaildata_extstr.find("name=\"from\"\r\n");
		JUDGEFIND(found);
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		ParseSinamail(emaildata_extstr);
		break;
	case PROVIDER_SOHU:
		found=emaildata_extstr.find("subject=");
		JUDGEFIND(found)
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		ParseSohumail(emaildata_extstr);
		break;
	case PROVIDER_139:
		found=emaildata_extstr.find("<string name=\"account\">");
		JUDGEFIND(found)
		emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		Parse139mail(emaildata_extstr);
		break;
	case PROVIDER_FOXMAIL:
		found=emaildata_extstr.find("From:");
		JUDGEFIND(found)
	    emaildata_extstr=emaildata_extstr.substr(found,emaildata_extstr.length()-found);
		ParseFoxmail(emaildata_extstr);
		break;
	case PROVIDER_SMTP:
		ParseSmtp(emaildata_extstr);
		break;
	default:
		break;

	}
	sendmailobj = ParseMailAddress(sendmailobj);
	tomailobj = ParseMailAddress(tomailobj);
	ccmailobj = ParseMailAddress(ccmailobj);
	bccmailobj = ParseMailAddress(bccmailobj);
	return TRUE;
}

int EmailParse::ParseFoxmail(std::ext_string emaildata_extstr)
{
	//找发送方
	size_t found_send;
    ext_string send_mail_extstr;
	found_send = emaildata_extstr.find("From");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr = emaildata_extstr.substr(found_send+5,emaildata_extstr.length()-found_send-5);
		found_send = send_mail_extstr.find(">\r\n");
		JUDGEFIND(found_send);
		send_mail_extstr = send_mail_extstr.substr(0,found_send+1);
		send_mail_extstr.replace(" ","");
		send_mail_extstr.replace(",\r\n\t",";");
		send_mail_extstr+=";";
		sendmailobj = send_mail_extstr;
	}
	//找收件方
	size_t found_to;
	ext_string to_mail_extstr;
	found_to = emaildata_extstr.find("To");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr = emaildata_extstr.substr(found_to+3,emaildata_extstr.length()-found_to-3);
		found_to = to_mail_extstr.find(">\r\n");
		JUDGEFIND(found_to);
		to_mail_extstr = to_mail_extstr.substr(0,found_to+1);
		to_mail_extstr.replace(" ","");
		to_mail_extstr.replace(",\r\n\t",";");
		to_mail_extstr+=";";
		tomailobj = to_mail_extstr;
	}
	//找抄送方
	size_t found_cc;
	ext_string cc_mail_extstr;
	found_cc = emaildata_extstr.find("Cc");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr = emaildata_extstr.substr(found_cc+3,emaildata_extstr.length()-found_cc-3);
		found_cc = cc_mail_extstr.find(">\r\n");
		JUDGEFIND(found_cc);
		cc_mail_extstr = cc_mail_extstr.substr(0,found_cc+1);
		cc_mail_extstr.replace(" ","");
		cc_mail_extstr.replace(",\r\n\t",";");
		cc_mail_extstr+=";";
		ccmailobj = cc_mail_extstr;
	}

	//找密送方
	//找主题
	unsigned int ret;
	size_t found_subject;
	ext_string subject_mail_extstr;
	found_subject = emaildata_extstr.find("Subject");
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr = emaildata_extstr.substr(found_subject+9,emaildata_extstr.length()-found_subject-9);
		found_subject = subject_mail_extstr.find("\r\n");
		JUDGEFIND(found_subject);
		subject_mail_extstr = subject_mail_extstr.substr(11,found_subject-13);
		subject_mail_extstr = (char *)base64Decode(subject_mail_extstr.c_str(),ret);
		subject_mail_extstr = G2U(subject_mail_extstr.c_str());
		subjectobj = subject_mail_extstr;
	}
	return TRUE;
}

int EmailParse::ParseSmtp(std::ext_string emaildata_extstr)
{
	//找发送方
	size_t found_send;
	ext_string send_mail_extstr;
	found_send = emaildata_extstr.find("From");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr = emaildata_extstr.substr(found_send+5,emaildata_extstr.length()-found_send-5);
		found_send = send_mail_extstr.find("\r\n");
		JUDGEFIND(found_send);
		send_mail_extstr = send_mail_extstr.substr(0,found_send+1);
		send_mail_extstr.replace(" ","");
		send_mail_extstr+=";";
		sendmailobj = send_mail_extstr;
	}
	//找收件方
	size_t found_to;
	ext_string to_mail_extstr;
	found_to = emaildata_extstr.find("To");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr = emaildata_extstr.substr(found_to+3,emaildata_extstr.length()-found_to-3);
		found_to = to_mail_extstr.find("\r\n");
		JUDGEFIND(found_to);
		to_mail_extstr = to_mail_extstr.substr(0,found_to+1);
		to_mail_extstr.replace(" ","");
		to_mail_extstr+=";";
		tomailobj = to_mail_extstr;
	}
	//找抄送方
	size_t found_cc;
	ext_string cc_mail_extstr;
	found_cc = emaildata_extstr.find("CC");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr = emaildata_extstr.substr(found_cc+3,emaildata_extstr.length()-found_cc-3);
		found_cc = cc_mail_extstr.find("\r\n");
		JUDGEFIND(found_cc);
		cc_mail_extstr = cc_mail_extstr.substr(0,found_cc+1);
		cc_mail_extstr.replace(" ","");
		cc_mail_extstr+=";";
		ccmailobj = cc_mail_extstr;
	}

	//找密送方
	size_t found_bcc;
	ext_string bcc_mail_extstr;
	found_bcc = emaildata_extstr.find("Bcc");
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr = emaildata_extstr.substr(found_bcc+4,emaildata_extstr.length()-found_bcc-4);
		found_bcc = bcc_mail_extstr.find("\r\n");
		JUDGEFIND(found_bcc);
		bcc_mail_extstr = bcc_mail_extstr.substr(0,found_bcc+1);
		bcc_mail_extstr.replace(" ","");
		bcc_mail_extstr+=";";
		bccmailobj = bcc_mail_extstr;
	}
	//找主题
	unsigned int ret;
	size_t found_subject;
	ext_string subject_mail_extstr;
	found_subject = emaildata_extstr.find("Subject");
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr = emaildata_extstr.substr(found_subject+9,emaildata_extstr.length()-found_subject-9);
		found_subject = subject_mail_extstr.find("\r\n");
		JUDGEFIND(found_subject);
		subject_mail_extstr = subject_mail_extstr.substr(11,found_subject-13);
		subject_mail_extstr = (char *)base64Decode(subject_mail_extstr.c_str(),ret);
		subject_mail_extstr = G2U(subject_mail_extstr.c_str());
		subjectobj = subject_mail_extstr;
	}
	return TRUE;
}

int EmailParse::ParseSohumail(std::ext_string emaildata_extstr)
{
	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaildata_extstr.find("subject=");
    if(found_subject!=std::string::npos)
	{
		subject_mail_extstr=emaildata_extstr.substr(found_subject+8,emaildata_extstr.length()-found_subject-8);
		found_subject=subject_mail_extstr.find("&");
		JUDGEFIND(found_subject)
		subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
		subject_mail_extstr.replace("%40","@");
		subject_mail_extstr.replace("%22","\"");
		subjectobj=subject_mail_extstr;
		subjectobj=ConvertUChar(subjectobj);
		std::cout<<subjectobj<<std::endl;
		CLogMod::SharedInstance()->LogInfo(subjectobj);
	}

	//发送方
	size_t found_send;
	std::ext_string send_mail_extstr;
	found_send=emaildata_extstr.find("from=");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr=emaildata_extstr.substr(found_send+5,emaildata_extstr.length()-found_send-5);
		found_send=send_mail_extstr.find("&");
		JUDGEFIND(found_send)
		send_mail_extstr=send_mail_extstr.substr(0,found_send);
		send_mail_extstr.replace("%40","@");
		send_mail_extstr.replace("%22","");
		send_mail_extstr.replace("%3C","<");
		send_mail_extstr.replace("%3E",">");
		sendmailobj=send_mail_extstr;
		std::cout<<sendmailobj<<std::endl;
	}

	//接受方
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaildata_extstr.find("to=");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr=emaildata_extstr.substr(found_to+3,emaildata_extstr.length()-found_to-3);
		found_to=to_mail_extstr.find("&");
		JUDGEFIND(found_to);
		to_mail_extstr=to_mail_extstr.substr(0,found_to);
		to_mail_extstr.replace("%40","@");
		to_mail_extstr.replace("%22","");
		to_mail_extstr.replace("%3C","<");
		to_mail_extstr.replace("%3E",">");
		to_mail_extstr.replace("%2C%20",";");
		tomailobj=to_mail_extstr;
		std::cout<<tomailobj<<std::endl;
	}

	//抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaildata_extstr.find("cc=");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr=emaildata_extstr.substr(found_cc+3,emaildata_extstr.length()-found_cc-3);
		found_cc=cc_mail_extstr.find("&");
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
		cc_mail_extstr.replace("%40","@");
		cc_mail_extstr.replace("%22","");
		cc_mail_extstr.replace("%3C","<");
		cc_mail_extstr.replace("%3E",">");
		cc_mail_extstr.replace("%2C%20",";");
		ccmailobj=cc_mail_extstr;
		std::cout<<ccmailobj<<std::endl;
	}

	//密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaildata_extstr.find("bcc=");
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr=emaildata_extstr.substr(found_bcc+4,emaildata_extstr.length()-found_bcc-4);
		found_bcc=bcc_mail_extstr.find("&");
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
		bcc_mail_extstr.replace("%40","@");
		bcc_mail_extstr.replace("%22","");
		bcc_mail_extstr.replace("%3C","<");
		bcc_mail_extstr.replace("%3E",">");
		bcc_mail_extstr.replace("%2C%20",";");
		bccmailobj=bcc_mail_extstr;
		std::cout<<bccmailobj<<std::endl;
	}

	//发送内容
	/*
	size_t found_content;
	std::ext_string content_mail_extstr;
	found_content=emaildata_extstr.find("text=");
	if(found_content!=std::string::npos)
	{
		content_mail_extstr=emaildata_extstr.substr(found_content+5,emaildata_extstr.length()-found_content-5);
		found_content=content_mail_extstr.find("&");
		JUDGEFIND(found_content)
		content_mail_extstr=content_mail_extstr.substr(0,found_content);
		content_mail_extstr.replace("%40","@");
		content_mail_extstr.replace("%22","\"");
		content_mail_extstr.replace("%3C","<");
		content_mail_extstr.replace("%3E",">");
		content_mail_extstr.replace("%2C%20",";");
		contentobj=content_mail_extstr;
		std::cout<<contentobj<<std::endl;
	}
	*/
	return TRUE;
}

int EmailParse::ParseSinamail(std::ext_string emaildata_extstr)
{
	//找发送方
	size_t found_send;
	std::ext_string send_mail_extstr;
	found_send=emaildata_extstr.find("name=\"from\"\r\n");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr=emaildata_extstr.substr(found_send+15,emaildata_extstr.length()-found_send-15);
		found_send=send_mail_extstr.find("\r\n");
		JUDGEFIND(found_send)
		send_mail_extstr=send_mail_extstr.substr(0,found_send);
		send_mail_extstr.replace("\"","");
		send_mail_extstr.replace(" ","");
		sendmailobj=send_mail_extstr;
		std::cout<<sendmailobj<<std::endl;
		CLogMod::SharedInstance()->LogInfo(subjectobj);
	}

	//找收件方
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaildata_extstr.find("name=\"to\"\r\n");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr=emaildata_extstr.substr(found_to+13,emaildata_extstr.length()-found_to-13);
		found_to=to_mail_extstr.find("\r\n");
		JUDGEFIND(found_to)
		to_mail_extstr=to_mail_extstr.substr(0,found_to);
		to_mail_extstr.replace("\"","");
		to_mail_extstr.replace(" ","");
		tomailobj=to_mail_extstr;
		std::cout<<tomailobj<<std::endl;
	}

	//找抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaildata_extstr.find("name=\"cc\"\r\n");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr=emaildata_extstr.substr(found_cc+13,emaildata_extstr.length()-found_cc-13);
		found_cc=cc_mail_extstr.find("\r\n");
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
		cc_mail_extstr.replace("\"","");
		cc_mail_extstr.replace(" ","");
		ccmailobj=cc_mail_extstr;
		std::cout<<ccmailobj<<std::endl;
	}

	//找密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaildata_extstr.find("name=\"bcc\"\r\n");
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr=emaildata_extstr.substr(found_bcc+14,emaildata_extstr.length()-found_bcc-14);
		found_bcc=bcc_mail_extstr.find("\r\n");
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
		bcc_mail_extstr.replace("\"","");
		bcc_mail_extstr.replace(" ","");
		bccmailobj=bcc_mail_extstr;
		std::cout<<bccmailobj<<std::endl;
	}

	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaildata_extstr.find("name=\"subj\"\r\n");
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr=emaildata_extstr.substr(found_subject+15,emaildata_extstr.length()-found_subject-15);
		found_subject=subject_mail_extstr.find("\r\n");
		JUDGEFIND(found_subject)
		subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
		subject_mail_extstr.replace("\"","");
		subjectobj=subject_mail_extstr;
		std::cout<<subjectobj<<std::endl;
		CLogMod::SharedInstance()->LogInfo(subjectobj.c_str());
	}
   //由于新浪的文本内容和一般不在一个TCP报文里面

	return TRUE;
}

int EmailParse::ParseOutlook(std::ext_string emaildata_extstr)
{

	return TRUE;
}

int EmailParse::Parse139mail(std::ext_string emaidata_extstr)
{
	//找发送方
	size_t found_send;
	std::ext_string send_mail_extstr;
	found_send=emaidata_extstr.find("<string name=\"account\">");
	JUDGEFIND(found_send);
	send_mail_extstr=emaidata_extstr.substr(found_send+23,emaidata_extstr.length()-found_send-23);
	found_send=send_mail_extstr.find("</string>");
	JUDGEFIND(found_send);
	send_mail_extstr=send_mail_extstr.substr(0,found_send);
	send_mail_extstr.replace("&quot;","");
	send_mail_extstr.replace("&lt;","<");
	send_mail_extstr.replace("&gt;",">");
	send_mail_extstr.replace(",",";");
    sendmailobj=send_mail_extstr;
	std::cout<<sendmailobj<<std::endl;

	//找收件方
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaidata_extstr.find("<string name=\"to\">");
	JUDGEFIND(found_to);
	to_mail_extstr=emaidata_extstr.substr(found_to+18,emaidata_extstr.length()-found_to-18);
	found_to=to_mail_extstr.find("</string>");
	JUDGEFIND(found_to);
	to_mail_extstr=to_mail_extstr.substr(0,found_to);
	to_mail_extstr.replace("&quot;","");
	to_mail_extstr.replace("&lt;","<");
	to_mail_extstr.replace("&gt;",">");
	to_mail_extstr.replace(",",";");
	tomailobj=to_mail_extstr;
	std::cout<<tomailobj<<std::endl;

	//找抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaidata_extstr.find("<string name=\"cc\">");
	JUDGEFIND(found_cc);
	cc_mail_extstr=emaidata_extstr.substr(found_cc+18,emaidata_extstr.length()-found_cc-18);
	found_cc=cc_mail_extstr.find("</string>");
	JUDGEFIND(found_cc);
	cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
	cc_mail_extstr.replace("&quot;","");
	cc_mail_extstr.replace("&lt;","<");
	cc_mail_extstr.replace("&gt;",">");
	ccmailobj=cc_mail_extstr;
	std::cout<<ccmailobj<<std::endl;


	//找密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaidata_extstr.find("<string name=\"bcc\">");
	JUDGEFIND(found_bcc);
	bcc_mail_extstr=emaidata_extstr.substr(found_bcc+19,emaidata_extstr.length()-found_bcc-19);
	found_bcc=bcc_mail_extstr.find("</string>");
	JUDGEFIND(found_bcc);
	bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
	bcc_mail_extstr.replace("&quot;","");
	bcc_mail_extstr.replace("&lt;","<");
	bcc_mail_extstr.replace("&gt;",">");
	bcc_mail_extstr.replace(",",";");
	bccmailobj=bcc_mail_extstr;
	std::cout<<bccmailobj<<std::endl;

	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaidata_extstr.find("<string name=\"subject\">");
	JUDGEFIND(found_subject);
	subject_mail_extstr=emaidata_extstr.substr(found_subject+23,emaidata_extstr.length()-found_subject-23);
	found_subject=subject_mail_extstr.find("</string>");
	JUDGEFIND(found_subject);
	subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
	subjectobj=subject_mail_extstr;
	std::cout<<subjectobj<<std::endl;
	CLogMod::SharedInstance()->LogInfo(subjectobj);
	//找内容
	size_t found_content;
	std::ext_string content_mail_extstr;
	found_content=emaidata_extstr.find("<string name=\"content\">");
	JUDGEFIND(found_content);
	content_mail_extstr=emaidata_extstr.substr(found_content+23,emaidata_extstr.length()-found_content-23);
	found_content=content_mail_extstr.find("</string>");
	JUDGEFIND(found_content);
	content_mail_extstr=content_mail_extstr.substr(0,found_content);
	contentobj=content_mail_extstr;
	std::cout<<contentobj<<std::endl;
    
	return TRUE;
}

int EmailParse::ParseYahoomail(std::ext_string emaildata_extstr)
{
	//std::cout<<"catch"<<std::endl;
	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaildata_extstr.find("\"subject\"");
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr=emaildata_extstr.substr(found_subject+11,emaildata_extstr.length()-found_subject-11);
		found_subject=subject_mail_extstr.find("\"");
		JUDGEFIND(found_subject)
		subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
		subjectobj=subject_mail_extstr;
		std::cout<<subjectobj<<std::endl;
	}

    //找发送方
	size_t found_send;
	std::ext_string send_mail_extstr;
	found_send=emaildata_extstr.find("\"from\"");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr=emaildata_extstr.substr(found_send+8,emaildata_extstr.length()-found_send-8);
		found_send=send_mail_extstr.find("}");
		//std::cout<<send_mail_extstr<<std::endl;
		JUDGEFIND(found_send)
		send_mail_extstr=send_mail_extstr.substr(0,found_send);
		send_mail_extstr.replace("\"email\":\"","<");
		send_mail_extstr.replace("\",\"name\":\"",">");
		send_mail_extstr.replace("\"","");
		sendmailobj=send_mail_extstr;
		std::cout<<sendmailobj<<std::endl;
	}

	//接受方
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaildata_extstr.find("\"to\":");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr=emaildata_extstr.substr(found_to+6,emaildata_extstr.length()-found_to-6);
		found_to=to_mail_extstr.find("]");
		JUDGEFIND(found_to)
		to_mail_extstr=to_mail_extstr.substr(0,found_to);
		to_mail_extstr.replace("true","false");
		to_mail_extstr.replace("\"fail\":false,\"email\":\"","<");
		to_mail_extstr.replace("\",\"name\":\"",">");
		to_mail_extstr.replace("}","");
		to_mail_extstr.replace("{","");
		to_mail_extstr.replace("\"","");
		to_mail_extstr.replace(",",";");
		tomailobj=to_mail_extstr;
		std::cout<<tomailobj<<std::endl;
	}

	//抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaildata_extstr.find("\"cc\":");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr=emaildata_extstr.substr(found_cc+6,emaildata_extstr.length()-found_cc-6);
		found_cc=cc_mail_extstr.find("]");
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
	    cc_mail_extstr.replace("true","false");
		cc_mail_extstr.replace("\"fail\":false,\"email\":\"","<");
		cc_mail_extstr.replace("\",\"name\":\"",">");
		cc_mail_extstr.replace("}","");
		cc_mail_extstr.replace("{","");
		cc_mail_extstr.replace("\"","");
		cc_mail_extstr.replace(",",";");
		ccmailobj=cc_mail_extstr;
		std::cout<<ccmailobj<<std::endl;
	}

	//密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaildata_extstr.find("\"bcc\":");
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr=emaildata_extstr.substr(found_bcc+7,emaildata_extstr.length()-found_bcc-7);
		found_bcc=bcc_mail_extstr.find("]");
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
		bcc_mail_extstr.replace("true","false");
		bcc_mail_extstr.replace("\"fail\":false,\"email\":\"","<");
		bcc_mail_extstr.replace("\",\"name\":\"",">");
		bcc_mail_extstr.replace("}","");
		bcc_mail_extstr.replace("{","");
		bcc_mail_extstr.replace("\"","");
		bcc_mail_extstr.replace(",",";");
		bccmailobj=bcc_mail_extstr;
		std::cout<<bccmailobj<<std::endl;
	}

	//正文
	size_t found_content;
	std::ext_string content_mail_extstr;
	found_content=emaildata_extstr.find("\"simplebody\"");
	if(found_content!=std::string::npos)
	{
		content_mail_extstr=emaildata_extstr.substr(found_content+14,emaildata_extstr.length()-found_content-14);
		found_content=content_mail_extstr.find("]}");
		JUDGEFIND(found_content)
		content_mail_extstr=content_mail_extstr.substr(0,found_content+1);
		contentobj=content_mail_extstr;
		std::cout<<contentobj<<std::endl;
	}
	return TRUE;
}

int EmailParse::ParseQqmail(std::ext_string emaildata_extstr)
{
    //找收件人
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaildata_extstr.find("to=");
	if(found_to!=std::string::npos)
	{
		to_mail_extstr=emaildata_extstr.substr(found_to+3,emaildata_extstr.length()-found_to-3);
		found_to=to_mail_extstr.find("&");
		JUDGEFIND(found_to)
		to_mail_extstr=to_mail_extstr.substr(0,found_to);
		to_mail_extstr.replace("%22","");
		to_mail_extstr.replace("; ",";");
		tomailobj=to_mail_extstr;
		std::cout<<tomailobj<<std::endl;

	}
	//找抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaildata_extstr.find("cc=");
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr=emaildata_extstr.substr(found_cc+3,emaildata_extstr.length()-found_cc-3);
		found_cc=cc_mail_extstr.find("&");
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
		cc_mail_extstr.replace("%22","");
		cc_mail_extstr.replace("; ",";");
		ccmailobj=cc_mail_extstr;
		std::cout<<ccmailobj<<std::endl;
	}

	//找密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaildata_extstr.find("bcc=");
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr=emaildata_extstr.substr(found_bcc+4,emaildata_extstr.length()-found_bcc-4);
		found_bcc=bcc_mail_extstr.find("&");
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
		bcc_mail_extstr.replace("%22","");
		bcc_mail_extstr.replace("; ",";");
		bccmailobj=bcc_mail_extstr;
		std::cout<<bccmailobj<<std::endl;
	}

	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaildata_extstr.find("subject=");
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr=emaildata_extstr.substr(found_subject+8,emaildata_extstr.length()-found_subject-8);
		found_subject=subject_mail_extstr.find("&");
		JUDGEFIND(found_subject)
		subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
		subjectobj=subject_mail_extstr;
		std::cout<<subjectobj<<std::endl;
		CLogMod::SharedInstance()->LogInfo(subjectobj);
	}
	//找内容
	size_t found_content;
	std::ext_string content_mail_extstr;
	found_content=emaildata_extstr.find("content__html=");
	if(found_content!=std::string::npos)
	{
		content_mail_extstr=emaildata_extstr.substr(found_content+14,emaildata_extstr.length()-found_content-14);
		found_content=content_mail_extstr.find("&");
		JUDGEFIND(found_content)
		content_mail_extstr=content_mail_extstr.substr(0,found_content);
		contentobj=content_mail_extstr;
		std::cout<<contentobj<<std::endl;
	}

	//找发送者
	size_t found_send;
	std::ext_string send_mail_extstr;
	found_send=emaildata_extstr.find("sendmailname=");
	if(found_send!=std::string::npos)
	{
		send_mail_extstr=emaildata_extstr.substr(found_send+13,emaildata_extstr.length()-found_send-13);
		found_send=send_mail_extstr.find("&");
		JUDGEFIND(found_send)
		send_mail_extstr=send_mail_extstr.substr(0,found_send);
		send_mail_extstr.replace("%22","");
		send_mail_extstr.replace("; ",";");
		sendmailobj=send_mail_extstr;
		std::cout<<sendmailobj<<std::endl;
	}
	return TRUE;
}

int EmailParse::Parse163mail(std::ext_string emaildata_extstr)
{
	//找用户名
	size_t found_usename;
	found_usename=emaildata_extstr.find("account"); //
	if(found_usename!=std::string::npos)
	{
		std::ext_string usename_data_extstr=emaildata_extstr.substr(found_usename,emaildata_extstr.length()-found_usename);
		found_usename=usename_data_extstr.find("%3C%2Fstring%3E");
		JUDGEFIND(found_usename)
		usename_data_extstr=usename_data_extstr.substr(0,found_usename);
		found_usename=usename_data_extstr.find("%3E");
		JUDGEFIND(found_usename)
		usename_data_extstr=usename_data_extstr.substr(found_usename+3,usename_data_extstr.length()-found_usename-3);
		usename_data_extstr.replace("%22",""); // "
		usename_data_extstr.replace("%26lt%3B","<"); // &lt;
		usename_data_extstr.replace("%26gt%3B",">"); // &gt;
		usename_data_extstr.replace("%40","@"); //@
		sendmailobj=usename_data_extstr;
		std::cout<<sendmailobj<<std::endl;
	}

	//找收件方
	size_t found_to;
	std::ext_string to_mail_extstr;
	found_to=emaildata_extstr.find("%3Carray%20name%3D%22to%22%3E"); // <array name="to">
	if(found_to!=std::string::npos)
	{
		to_mail_extstr=emaildata_extstr.substr(found_to,emaildata_extstr.length()-found_to);
		found_to=to_mail_extstr.find("%3C%2Farray%3E");  // </array>
		JUDGEFIND(found_to)
		to_mail_extstr=to_mail_extstr.substr(0,found_to);
		found_to=to_mail_extstr.find("%3Cstring%3E");
		JUDGEFIND(found_to)
		to_mail_extstr=to_mail_extstr.substr(found_to,to_mail_extstr.length()-found_to);
		to_mail_extstr.replace("%26lt%3B","<");
		to_mail_extstr.replace("%26gt%3B",">");
		to_mail_extstr.replace("%22","");
		to_mail_extstr.replace("%3Cstring%3E","");
		to_mail_extstr.replace("%3C%2Fstring%3E",";");
		to_mail_extstr.replace("%40","@"); 
		tomailobj=to_mail_extstr;
		std::cout<<tomailobj<<std::endl;
		
	}
	
	//找抄送方
	size_t found_cc;
	std::ext_string cc_mail_extstr;
	found_cc=emaildata_extstr.find("%3Carray%20name%3D%22cc%22%3E"); // <array name="cc">
	if(found_cc!=std::string::npos)
	{
		cc_mail_extstr=emaildata_extstr.substr(found_cc,emaildata_extstr.length()-found_cc);
		found_cc=cc_mail_extstr.find("%3C%2Farray%3E");  // </array>
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(0,found_cc);
		found_cc=cc_mail_extstr.find("%3Cstring%3E");
		JUDGEFIND(found_cc)
		cc_mail_extstr=cc_mail_extstr.substr(found_cc,cc_mail_extstr.length()-found_cc);
		cc_mail_extstr.replace("%26lt%3B","<");
		cc_mail_extstr.replace("%26gt%3B",">");
		cc_mail_extstr.replace("%22","");
		cc_mail_extstr.replace("%3Cstring%3E","");
		cc_mail_extstr.replace("%3C%2Fstring%3E",";");
		cc_mail_extstr.replace("%40","@"); 
		ccmailobj=cc_mail_extstr;
		std::cout<<ccmailobj<<std::endl;
	}
	
	//找密送方
	size_t found_bcc;
	std::ext_string bcc_mail_extstr;
	found_bcc=emaildata_extstr.find("%3Carray%20name%3D%22bcc%22%3E"); // <array name="bcc">
	if(found_bcc!=std::string::npos)
	{
		bcc_mail_extstr=emaildata_extstr.substr(found_bcc,emaildata_extstr.length()-found_bcc);
		found_bcc=bcc_mail_extstr.find("%3C%2Farray%3E");  // </array>
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(0,found_bcc);
		found_bcc=bcc_mail_extstr.find("%3Cstring%3E");
		JUDGEFIND(found_bcc)
		bcc_mail_extstr=bcc_mail_extstr.substr(found_bcc,bcc_mail_extstr.length()-found_bcc);
		bcc_mail_extstr.replace("%26lt%3B","<");
		bcc_mail_extstr.replace("%26gt%3B",">");
		bcc_mail_extstr.replace("%22","");
		bcc_mail_extstr.replace("%3Cstring%3E","");
		bcc_mail_extstr.replace("%3C%2Fstring%3E",";");
		bcc_mail_extstr.replace("%40","@"); 
		bccmailobj=bcc_mail_extstr;
		std::cout<<bccmailobj<<std::endl;
	}
	
	//找主题
	size_t found_subject;
	std::ext_string subject_mail_extstr;
	found_subject=emaildata_extstr.find("%3Cstring%20name%3D%22subject%22%3E"); // <string name="subject">
	if(found_subject!=std::string::npos)
	{
		subject_mail_extstr=emaildata_extstr.substr(found_subject,emaildata_extstr.length()-found_subject);
		found_subject=subject_mail_extstr.find("%3C%2Fstring%3E");  // </string>
		JUDGEFIND(found_subject)
		subject_mail_extstr=subject_mail_extstr.substr(0,found_subject);
		subjectobj=subject_mail_extstr.substr(35,subject_mail_extstr.length()-35);
		subjectobj=ConvertUChar(subjectobj);
		std::cout<<subjectobj<<std::endl;
		CLogMod::SharedInstance()->LogInfo(subjectobj);
	}

	//找内容
	size_t found_content;
	std::ext_string content_mail_extstr;
	found_content=emaildata_extstr.find("%3Cstring%20name%3D%22content%22%3E"); // <string name="content">
	if(found_content!=std::string::npos)
	{
		content_mail_extstr=emaildata_extstr.substr(found_content,emaildata_extstr.length()-found_content);
		found_content=content_mail_extstr.find("%3C%2Fstring%3E");  // </string>
		JUDGEFIND(found_content)
		content_mail_extstr=content_mail_extstr.substr(0,found_content);
		contentobj=content_mail_extstr.substr(35,content_mail_extstr.length()-35);
		std::cout<<contentobj<<std::endl;
	}
	return TRUE;
}
ext_string EmailParse::ParseMailAddress(ext_string mailstr)
{
	ext_string extstr;
	ext_string mailnodestr;
	ext_string mailliststr;
	int found=0;
	extstr = mailstr;
    while(string::npos!=(found=extstr.find(";")))
	{
		mailnodestr = extstr.substr(0,found);
		extstr = extstr.substr(found+1,extstr.length()-found-1);
		if(string::npos!=(found=mailnodestr.find("<")))
		{
			mailnodestr = mailnodestr.substr(found+1,mailnodestr.length()-found-1);
			found = mailnodestr.find(">");
			mailnodestr = mailnodestr.substr(0,found);
			mailliststr+=mailnodestr;
			mailliststr+=";";
		}
		else
		{
			mailliststr+=mailnodestr;
			mailliststr+=";";
		}
	}
 	if(extstr.length()!=0)
  	{
		mailnodestr = extstr;
		if(string::npos!=(found=mailnodestr.find("<")))
		{
			mailnodestr = mailnodestr.substr(found+1,mailnodestr.length()-found-1);
			found = mailnodestr.find(">");
			mailnodestr = mailnodestr.substr(0,found);
			mailliststr+=mailnodestr;
			mailliststr+=";";
		}
		else
		{
			mailliststr+=mailnodestr;
			mailliststr+=";";
		}
	}
	return mailliststr;
}

ext_string EmailParse::ConvertUChar(ext_string inputstr)
{
	char p;
	ext_string restr;
	for(int i=0;i<inputstr.length();)
	{
		if(inputstr[i]=='%')
		{
			string tmp = inputstr.substr(i+1,2);
			if(48<=tmp[0]&&tmp[0]<=57)
				tmp[0]=tmp[0]-48;
			if(tmp[0]>=65)
				tmp[0]=tmp[0]-55;
			if(48<=tmp[1]&&tmp[1]<=57)
				tmp[1]=tmp[1]-48;
			if(tmp[1]>=65)
				tmp[1]=tmp[1]-55;
			tmp = tmp[0]*16+tmp[1];
			restr+=tmp;
			i+=3;		
		}
		else
		{
			string tmp;
			tmp = inputstr[i];
			restr+=tmp;
			i++;
		}
	}
	return restr;
}