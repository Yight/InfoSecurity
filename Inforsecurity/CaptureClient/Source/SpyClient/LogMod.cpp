#include "stdafx.h"
#include "LogMod.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif
using namespace std;

CLogMod* CLogMod::_instance = NULL;

CLogMod*  CLogMod::SharedInstance()
{	if (_instance == NULL)
	{
		_instance = new CLogMod;
	}
	return _instance;
}

void CLogMod::Init(void)
{
	string m_installpath;
	CRegKey regkeyobj;
	LPCTSTR lpRegPath=_T("Software\\MoniClient");
#ifndef _DEBUG
	LONG IResult=regkeyobj.Open(HKEY_CLASSES_ROOT,lpRegPath,KEY_ALL_ACCESS);
#else
	LONG IResult=regkeyobj.Open(HKEY_CURRENT_USER,lpRegPath,KEY_ALL_ACCESS);
#endif
	if(ERROR_SUCCESS==IResult)
	{
		ULONG u_RegStrSize=100;
		char RegStrBuff[100]={0};
		if(regkeyobj.QueryStringValue(_T("InstallPath"),RegStrBuff,&u_RegStrSize)!=ERROR_SUCCESS)
		{
			Releaseinfo("Get InstallPath fails");
			regkeyobj.Close();
			return ;
		}
		m_installpath=RegStrBuff;
		m_installpath+="\\SpyClient.log";
		regkeyobj.Close();
	}

    helpers::LogLog::getLogLog()->setInternalDebugging(true);
	SharedAppenderPtr append_1(
		new RollingFileAppender(LOG4CPLUS_TEXT(m_installpath.c_str()), 20, 5));
	append_1->setName(LOG4CPLUS_TEXT("Main"));

    log4cplus::tstring pattern = LOG4CPLUS_TEXT("[%D] [%t] %-5p %c{2} - %m%n");
    append_1->setLayout( std::auto_ptr<Layout>(new PatternLayout(pattern)) );

    Logger::getRoot().addAppender(append_1);

    loginstance = Logger::getInstance(LOG4CPLUS_TEXT("SpyClient"));
	Test();
}

void CLogMod::AddLog(void)
{

}

void CLogMod::Test(void)
{
	// for(int i=0; i<LOOP_COUNT; ++i) {
 //        NDCContextCreator _context(LOG4CPLUS_TEXT("loop"));
 //        LOG4CPLUS_DEBUG(loginstance, "Entering loop #" << i);
 //    }
}

void CLogMod::LogDebug(std::string debuginfo)
{
    LOG4CPLUS_DEBUG(loginstance, debuginfo.c_str());
}

void CLogMod::LogWarn(std::string warninfo)
{
    LOG4CPLUS_WARN(loginstance, warninfo.c_str());
}

void CLogMod::LogInfo(std::string infostr)
{
    LOG4CPLUS_INFO(loginstance, infostr.c_str());
}

void CLogMod::LogError(std::string errorinfo)
{
    LOG4CPLUS_ERROR(loginstance, errorinfo.c_str());
}

void CLogMod::LogFatal(std::string fatalfo)
{
    LOG4CPLUS_FATAL(loginstance, fatalfo.c_str());
}

void CLogMod::LogDebug(const char* debuginfo)
{
    LOG4CPLUS_DEBUG(loginstance, debuginfo);
}

void CLogMod::LogWarn(const char* warninfo)
{
    LOG4CPLUS_WARN(loginstance, warninfo);
}

void CLogMod::LogInfo(const char* infostr)
{
    LOG4CPLUS_INFO(loginstance, infostr);
}

void CLogMod::LogError(const char* errorinfo)
{
    LOG4CPLUS_ERROR(loginstance, errorinfo);
}

void CLogMod::LogFatal(const char* fatalinfo)
{
    LOG4CPLUS_FATAL(loginstance, fatalinfo);
}

void Releaseinfo(char *infostr)
{
	if(SWITCH)
	{
		FILE *fp;
		fp = fopen("D:\\SpyClient123.log","a+");
		if(fp == NULL)
		{
			cout<<"file open fail"<<endl;
		}

		fprintf(fp,"%s\n",infostr);
		fclose(fp);
	}
}