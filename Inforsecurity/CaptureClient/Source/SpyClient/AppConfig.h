//AppConfig.h 配置文件的头文件  author:Zelong Yin

#pragma once
#include <ext_string.h>
#include "sqlite3.h"
#include <comdef.h>
#include "ProtoMessage.pb.h"
typedef std::basic_string<TCHAR,std::char_traits<TCHAR>> wtstring;
#define DWORDTYPE 0
#define STRINGTYPE 1

using namespace std;
using namespace SpyClient;

class AppConfig
{
public:
	AppConfig(void);
	~AppConfig();
	int Init();
	int InitRegEdit(); //初始化注册表函数 包括Host、Port、bkurl、Version
	int InitPcIDAndUserID(); //初始化PcID 和 UserID
	int InitWhiteList();//初始化白名单
	string PostMaxAddTime(string maxdatetime);//传递最大添加时间
	int SetReg(LPCTSTR SectionName,LPCTSTR KeyName,int ValueType); //设置注册表 参数分别是字段、key值、类型
	int GetPrivateValue(LPCTSTR KeyName,TCHAR *RegStrBuff=NULL,int port=0);//获取私有对象，将TCHAR转化为char
	const char* GetHostIp(){return m_host;}; //获取服务器IP
	int GetPort(){return m_Port;}; //获取服务器端口地址
	wtstring GetWhitelistPath(){return m_whitelistpath;};
	const char* GetBkUrl(){return m_bkurl;}; //获取URL
	const char* GetVersion(){return m_version;}; //获取版本号
	const char* GetPcID(){return m_pcid;}; //获取PC ID
	const char* GetUserID(){return m_userid;};//获取User ID
	string PostUserIdAndMac(string userid_str,string mac_str); //将Userid 和 MAC 地址传送给服务器，返回Pcid
	int ConnectToServer(); //连接服务器函数
	static AppConfig *SharedInstance();
private:
	static AppConfig *_instance;
	CRegKey regkeyobj; //注册表类对象
	char *m_host; //用于存储服务器IP
	int m_Port;//用于存储服务器开放端口
	char *m_bkurl;//用于存储URL
	char *m_version;//用于存储版本号
	char *m_pcid;//用于存储pcid
	char *m_userid;//用于存储userid
	wtstring m_installpath; //配置文件用双字节来存储安装路径
	wtstring m_whitelistpath;//白名单的存储用双字节来存储安装路径
	CInternetSession* session; //Internet会话句柄
	CHttpConnection* pConnection; //Http连接句柄
};

//sqlite的回调函数
int SQLCallback(void *para,int ncount,char **pvalue,char **pname); 