#pragma once
#include <string>
#include <log4cplus/logger.h>
#include <log4cplus/fileappender.h>
#include <log4cplus/layout.h>
#include <log4cplus/ndc.h>
#include <log4cplus/helpers/loglog.h>
#include <log4cplus/loggingmacros.h>
#include <ext_string.h>


#define SWITCH 1
using namespace log4cplus;

// const int LOOP_COUNT = 20000;

class CLogMod
{
public:
	CLogMod(){};
	~CLogMod(){delete _instance;};
	void Init();
	void AddLog();

	static CLogMod *SharedInstance();
	
	void LogDebug(std::string debuginfo);
	void LogWarn(std::string warninfo);
	void LogInfo(std::string infostr);
	void LogError(std::string errorinfo);
	void LogFatal(std::string fatalfo);

	void LogDebug(const char* debuginfo);
	void LogWarn(const char* warninfo);
	void LogInfo(const char* infostr);
	void LogError(const char* errorinfo);
	void LogFatal(const char* fatalinfo);

private:
	static CLogMod *_instance;
	Logger loginstance;
	void Test(void);
};

void Releaseinfo(char *infostr);