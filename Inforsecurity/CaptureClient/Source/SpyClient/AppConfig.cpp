//AppConfig.cpp  Author: Zelong Yin

#include "StdAfx.h"
#include "AppConfig.h"
#include "Utils.h"
#include "LogMod.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

AppConfig* AppConfig::_instance = NULL;

//静态AppConfig类句柄的动态申请
AppConfig*  AppConfig::SharedInstance()
{	if (_instance == NULL)
	{
		_instance = new AppConfig;
	}
	return _instance;
}


//AppConfig的初始化函数
AppConfig::AppConfig(void)
{
	//对m_host,m_bkurl,m_version,m_pcid,m_userid,m_Port动态申请空间
	m_host=(char*)malloc(sizeof(char)*20);//IP格式XXX.XXX.XXX.XXX所需空间在20个字符之内
	memset(m_host,0,20);
	m_bkurl=(char*)malloc(sizeof(char)*100);
	memset(m_bkurl,0,100);
	m_version=(char*)malloc(sizeof(char)*20);
	memset(m_version,0,20);
	m_pcid=(char*)malloc(sizeof(char)*25);//pcid是24位字符，因此需要申请25位
	memset(m_pcid,0,25);
	m_userid=(char*)malloc(sizeof(char)*25);//userid是24位字符，因此需要申请25位
	memset(m_userid,0,25);
	m_Port=0;
	pConnection=NULL;
	session=NULL;
}

//AppConfig的析构函数
AppConfig::~AppConfig(void)
{
	//用于释放m_host,m_bkurl,m_version,m_pcid,m_userid所占的空间
	free(m_host);
	free(m_bkurl);
	free(m_version);
	free(m_pcid);
	free(m_userid);
	delete _instance;
}

//AppConfig的功能开始函数
int AppConfig::Init()
{
	//执行InitRegEdit 和InitPcIDAndUserID函数，执行成功返回为0，失败返回为1
    if(InitRegEdit() && InitPcIDAndUserID() && InitWhiteList())
		return TRUE;
	return FALSE;
}

	//AppConfig的初始化PcID和Userid函数
int AppConfig::InitPcIDAndUserID()
{
	int Reg_Error;
	ULONG u_RegStrSize=100;
	string mac_str("");
	TCHAR RegStrBuff[100]={0};

	LPCTSTR lpRegPath=_T("Software\\MoniClient");
	//分为_DEBUG形式和_Release形式
#ifndef _DEBUG
	//在DEBUG模式下，打开注册表"HKEY_CLASSES_ROOT\Software\MoniClient"
	if(regkeyobj.Open(HKEY_CLASSES_ROOT,lpRegPath,KEY_ALL_ACCESS)!=ERROR_SUCCESS)
	{
		cout<<"find the reg fails"<<endl;
		Releaseinfo("find the reg fails");
		return FALSE;
	}
#else
	//在Release模式下，打开注册表"HKEY_CURRENT_USER\Software\MoniClient"
	if(regkeyobj.Open(HKEY_CURRENT_USER,lpRegPath,KEY_ALL_ACCESS)!=ERROR_SUCCESS)
	{
		cout<<"find the reg fails"<<endl;
		Releaseinfo("find the reg fails");
		return FALSE;
	}
#endif
	//查看注册表里面是否存在UserID。若不存在，则返回FALSE;若存在，则将UserID值赋给m_userid
	if(regkeyobj.QueryStringValue(_T("UserID"),RegStrBuff,&u_RegStrSize)!=ERROR_SUCCESS)
	{
		Releaseinfo("find UserID fails");
		regkeyobj.Close();
		return FALSE;
	}
	else
	{
		Releaseinfo("find UserID success");
		Releaseinfo(RegStrBuff);
		sprintf(m_userid,"%s",RegStrBuff);
	}

    u_RegStrSize = 100; //由于u_RegStrSize在上一个函数中会返回一个值，因此必须将u_RegStrSize还原成以前的值

	//查看注册表里面是否存在PcID，若不存在，则向服务器申请；如果存在，则直接赋值给m_pcid。
	if((Reg_Error=regkeyobj.QueryStringValue(_T("PcID"),RegStrBuff,&u_RegStrSize))!=ERROR_SUCCESS)
	{
#ifdef UNICODE  
		MultiByteToWideChar(CP_ACP, 0, GetEthernetMacAddr().c_str(), -1, MacStrBuff, 100);  
#else
		//strcpy(MacStrBuff, GetEthernetMacAddr().c_str()); 
		//将MAC地址赋值给mac_str
		mac_str = GetEthernetMacAddr();
#endif
		cout<<"Error code:"<<Reg_Error<<endl;
		Releaseinfo("Error code");
		strcpy(RegStrBuff,PostUserIdAndMac(m_userid,mac_str).c_str()); //将获取的Pcid赋值给RegStrbuf
		Releaseinfo("PostUserIdAndMac");
		Releaseinfo(RegStrBuff);
		regkeyobj.SetStringValue(_T("PcID"),RegStrBuff,REG_SZ); //设置注册表的PcID
		sprintf(m_pcid,"%s",RegStrBuff);//赋值给m_pcid
	}
	else
	{
		//如果注册表里面存在PcID，则将其赋给m_pcid
		Releaseinfo("find PcID success");
		Releaseinfo(RegStrBuff);
		sprintf(m_pcid,"%s",RegStrBuff);
		Releaseinfo(m_pcid);
	}

	string pcid_str = m_pcid;
	string userid_str = m_userid;

	//如果userid为空或者其长度不是24个字节，则重新从注册表中获取userid
	if(userid_str.empty() ||userid_str.length()!=24)
	{
		Releaseinfo("userid_str is empty");
		//GetPrivateProfileString(_T("userinfo"),_T("UserID") ,_T(""),RegStrBuff,sizeof(RegStrBuff),_T(".\\config.ini"));
		GetPrivateProfileString(_T("userinfo"),_T("UserID") ,_T(""),RegStrBuff,sizeof(RegStrBuff),m_installpath.c_str());
		regkeyobj.SetStringValue(_T("UserID"),RegStrBuff,REG_SZ);
		sprintf(m_userid,"%s",RegStrBuff);
		Releaseinfo(m_userid);
	}

	//如果pcid为空或者其长度不是24个字节，则重新从注册表中获取pcid
	if(pcid_str.empty() || pcid_str.length()!=24)
	{
		Releaseinfo("pcid_str is empty");
		mac_str = GetEthernetMacAddr();
		strcpy(RegStrBuff,PostUserIdAndMac(m_userid,mac_str).c_str());
		regkeyobj.SetStringValue(_T("PcID"),RegStrBuff,REG_SZ);
		sprintf(m_pcid,"%s",RegStrBuff);
		Releaseinfo(m_pcid);
		//string pcid_str = m_pcid;
	}
	regkeyobj.Close();
	return -1;
}


//初始化注册表函数
int AppConfig::InitRegEdit()
{
	LPCTSTR lpRegPath=_T("Software\\MoniClient");
//若在DEBUG模式下，打开HKEY_CURRENT_USER;若在Release模式下，打开HKEY_CLASSES_ROOT
#ifndef _DEBUG
	LONG IResult=regkeyobj.Open(HKEY_CLASSES_ROOT,lpRegPath,KEY_ALL_ACCESS);
#else 
	LONG IResult=regkeyobj.Open(HKEY_CURRENT_USER,lpRegPath,KEY_ALL_ACCESS);
#endif
	//如果注册表打开失败，则返回FALSE；成功则继续。
	if(ERROR_SUCCESS==IResult)
	{
		ULONG u_RegStrSize=100;
		TCHAR RegStrBuff[100]={0};
		TCHAR ProfileStrBuff[100]={0};
		int Reg_Error;
		//查找注册表中是否存在InstallPath Key名；如果不存在，则返回FALSE
		if(regkeyobj.QueryStringValue(_T("InstallPath"),RegStrBuff,&u_RegStrSize)!=ERROR_SUCCESS)
		{
			Releaseinfo("Get InstallPath fails");
			regkeyobj.Close();
			return FALSE;
		}
		m_installpath=RegStrBuff;
		m_installpath+=_T("\\config.ini"); //获取配置文件config.ini赋值给m_installpath
		m_whitelistpath=RegStrBuff;
		m_whitelistpath+=_T("\\whitelist");
		Releaseinfo(RegStrBuff);
		u_RegStrSize = 100;
		//查看注册表中是否存在版本号。如果不存在，则认为配置文件没有写进，将配置文件内容写进注册表，返回TRUE
		if(regkeyobj.QueryStringValue(_T("Version"),RegStrBuff,&u_RegStrSize)!=ERROR_SUCCESS)
		{
			Releaseinfo("Get Version fails");
			std::cout<<"Got Version fail"<<std::endl;
			SetReg(_T("server"),_T("Host"),STRINGTYPE); //将配置文件[Server] host写入注册表；
			SetReg(_T("server"),_T("Port"),DWORDTYPE); //将配置文件[Server] Port写入注册表
			SetReg(_T("transfer"),_T("Bkurl"),STRINGTYPE); //将配置文件[transfer] Bkurl写入注册表
			SetReg(_T("soft"),_T("Version"),STRINGTYPE); //将配置文件[soft] Version写入注册表
			regkeyobj.Close();
			return TRUE;
		}
		//如果注册表中存在Version，则从配置文件中取出[soft],Version赋值给ProfileStrBuff。
		Reg_Error=GetPrivateProfileString(_T("soft"),_T("Version"),_T(""),ProfileStrBuff,sizeof(ProfileStrBuff),m_installpath.c_str());
		//如果获取失败，则返回FALSE
		if(Reg_Error==sizeof(ProfileStrBuff)-1 || Reg_Error==sizeof(ProfileStrBuff)-2)
		{
			Releaseinfo("get config.ini fails");
			std::cout<<"Get soft fail"<<std::endl;
			regkeyobj.Close();
			return FALSE;
		}
		//如果配置文件中的版本号（Version)大于注册表中版本号，则覆盖注册表；否则，从注册表中获取Port,Version,Bkurl,Host赋值给类的变量
		if(_tcscmp(ProfileStrBuff,RegStrBuff)>0)
		{	
			SetReg(_T("server"),_T("Host"),STRINGTYPE);
			SetReg(_T("server"),_T("Port"),DWORDTYPE);
			SetReg(_T("transfer"),_T("Bkurl"),STRINGTYPE);
			SetReg(_T("soft"),_T("Version"),STRINGTYPE);	
		}
		else
		{
			DWORD d_Port=0;
			ULONG u_HostSize=20;
			ULONG u_BkUrlSize=100;
			ULONG u_VersionSize=20;
			regkeyobj.QueryDWORDValue(_T("Port"),d_Port);
			m_Port=d_Port;
			regkeyobj.QueryStringValue(_T("Version"),m_version,&u_VersionSize);
			regkeyobj.QueryStringValue(_T("Bkurl"),m_bkurl,&u_BkUrlSize);
			regkeyobj.QueryStringValue(_T("Host"),m_host,&u_HostSize);
		}
		regkeyobj.Close();
	}
	else
	{
		return FALSE;
	}
	return TRUE;

}

//初始化白名单
int AppConfig::InitWhiteList()
{
	//打开进程白名单，获取最后的addtime
	int rc;
	sqlite3 *db;
	char *errs;
	_bstr_t t = m_whitelistpath.c_str();
	char* pwhitelistpath = (char *)t;
	rc = sqlite3_open(pwhitelistpath,&db);
	//将addtime发送给服务端
	if(rc)
	{
		Releaseinfo("db open fails\n");
		return 0;
	}

	string maxdatetime;
	rc = sqlite3_exec(db,"select max(addtime) from whitetable",SQLCallback,(string *)&maxdatetime,&errs);
	if(rc)
	{
		Releaseinfo("select fails");
		return 0;
	}

	string extendwhitelist = PostMaxAddTime(maxdatetime);
	//获取新增加的list,放入whitelist
	string tmpstr = extendwhitelist;
	int foundpos;
	while ((foundpos=tmpstr.find("!!!"))!=string::npos)
	{
		string sqlcommand = "insert into whitetable(processname,version,md5,addtime) values('";
		WhiteProcess whitepacket;
		string extendnode= tmpstr.substr(0,foundpos);
		whitepacket.ParseFromString(extendnode);
		sqlcommand= sqlcommand+whitepacket.processname()+"','"+whitepacket.version()+"','"+whitepacket.processmd5()+"','"+whitepacket.addtime()+"')";
		rc = sqlite3_exec(db,sqlcommand.c_str(),0,0,&errs);
		if(rc)
		{
			return 0;
		}

		tmpstr=tmpstr.substr(foundpos+3,tmpstr.length()-foundpos-3);
	}
	sqlite3_close(db);



	return 1;
}

int SQLCallback(void *para,int ncount,char **pvalue,char **pname)
{
	string *timestr = (string *)para;
	for(int i=0;i<ncount;i++)
	{
		*timestr+=pvalue[i];
	}
	return 0;
}

string AppConfig::PostMaxAddTime(string maxdatetime)
{
	string sendbuff("");
	string sendpath("");
	string getwhitelist("");
	sendbuff+="time=";
	sendbuff+=maxdatetime;
	//如果pConnection为空，则试图去连接服务器
	if(!pConnection)
		ConnectToServer();

	Releaseinfo("ConnectToServer Success");
	sendpath="/get/pc/addtime/";
	//打开httpfile文件，传送数据的方式是POST，文件路径是/get/pc/addtime/
	CHttpFile* pFile = pConnection->OpenRequest( CHttpConnection::HTTP_VERB_POST,
		sendpath.c_str(),
		NULL,
		1,
		NULL,
		"HTTP/1.1",
		INTERNET_FLAG_RELOAD);
	//如果pConnection是空，重新连接服务器。如果连接失败，则返回空的pcid_str.
	if(pConnection==NULL)
	{
		Releaseinfo("pConnection==NULL");
		if(!ConnectToServer())
			return getwhitelist;
	}
	//需要提交的数据
	CString szHeaders   = "Content-Type: application/x-www-form-urlencoded;";
	//下面这段编码，则是可以让服务器正常处理
	//CHAR* strFormData = "username=WaterLin&password=TestPost";
	//发送数据到服务器。如果返回的数据是0，则发送失败。如果出现异常，则重新发送
	try
	{
		if(pFile->SendRequest( szHeaders,
			szHeaders.GetLength(),
			(LPVOID)sendbuff.c_str(),
			sendbuff.length())==0)
		{
			Releaseinfo("SendRequest fails");
			cout<<"calling fails"<<endl;
			return getwhitelist;
		}
		cout<<"send ok"<<endl;
	}
	catch (CInternetException* e)
	{
		if(!ConnectToServer())
			return getwhitelist;
		PostMaxAddTime(maxdatetime);
	}

	//获取来自服务端的回复，获取来自服务端的pcid
	DWORD dwRet;
	pFile->QueryInfoStatusCode(dwRet);

	if(dwRet != HTTP_STATUS_OK)
	{
		CString errText;
		errText.Format("POST出错，错误码：%d", dwRet);
	}
	else
	{
		int len = pFile->GetLength();
		char *buf = new char[len+1];
		memset(buf,0,len+1);

		int numread;
		while ((numread = pFile->Read(buf,sizeof(buf)-1))> 0)
		{
			buf[numread]='\0';
			getwhitelist+=buf;

		}
		delete buf;

	}
	return getwhitelist;
}



//连接服务器函数
int AppConfig::ConnectToServer()
{
	Releaseinfo("ConnectToServer");
	static int stick = 0;
	string host_ip("");
	try
	{
		Releaseinfo("try connect");
		//连接前，先清空并关闭session 和 pConnection
		if(session)
		{
			session->Close();
			delete session;
		}
		if(pConnection)
		{

			pConnection->Close();
			delete pConnection;
		}

		//动态申请session，并设置各属性
		session = new CInternetSession;
		session->SetOption(INTERNET_OPTION_CONNECT_TIMEOUT, 1000 * 20);
		session->SetOption(INTERNET_OPTION_CONNECT_BACKOFF, 1000);
		session->SetOption(INTERNET_OPTION_CONNECT_RETRIES, 1);

		host_ip = m_host;
		Releaseinfo("host_ip = m_host;");
		Releaseinfo(m_host);
		//用http协议连接host_ip,m_port
		pConnection = session->GetHttpConnection( host_ip.c_str(),INTERNET_FLAG_EXISTING_CONNECT,(INTERNET_PORT)m_Port);
		Releaseinfo("GetHttpConnection");
		stick = 0;
		return TRUE;
	}

	//如果连接出现异常，尝试进行4次连接
	catch (CInternetException* e)
	{
		Releaseinfo("catch connect");
		char errorcount[10]={0};
		e->GetErrorMessage(errorcount,10);
	    Releaseinfo(errorcount);
		if(stick<4)
		{
			stick++;
			return ConnectToServer();
		}
		else
		{
			Releaseinfo("Connect Error");
			stick = 0;
			return FALSE;
		}
		Releaseinfo("catch connect end");
	}
	Releaseinfo("connect server end ");
}

//PostUserIdAndMac的函数功能是将userid和mac地址传送给服务器，返回值是服务器返回的pcid
string AppConfig::PostUserIdAndMac(string userid_str,string mac_str)
{
	string sendbuff("");
	string sendpath("");
	string pcid_str("");
	sendbuff+="userid=";
	sendbuff+=userid_str;
	sendbuff+="&";
	sendbuff+="mac=";
	sendbuff+=mac_str;
	//如果pConnection为空，则试图去连接服务器
	if(!pConnection)
		ConnectToServer();

	Releaseinfo("ConnectToServer Success");
	sendpath="/get/pc/pcid/";
	//打开httpfile文件，传送数据的方式是POST，文件路径是/get/pc/pcid/
	CHttpFile* pFile = pConnection->OpenRequest( CHttpConnection::HTTP_VERB_POST,
		sendpath.c_str(),
		NULL,
		1,
		NULL,
		"HTTP/1.1",
		INTERNET_FLAG_RELOAD);
	//如果pConnection是空，重新连接服务器。如果连接失败，则返回空的pcid_str.
	if(pConnection==NULL)
	{
		Releaseinfo("pConnection==NULL");
		if(!ConnectToServer())
			return pcid_str;
	}
	//需要提交的数据
	CString szHeaders   = "Content-Type: application/x-www-form-urlencoded;";
	//下面这段编码，则是可以让服务器正常处理
	//CHAR* strFormData = "username=WaterLin&password=TestPost";
	//发送数据到服务器。如果返回的数据是0，则发送失败。如果出现异常，则重新发送
	try
	{
		if(pFile->SendRequest( szHeaders,
			szHeaders.GetLength(),
			(LPVOID)sendbuff.c_str(),
			sendbuff.length())==0)
		{
			Releaseinfo("SendRequest fails");
			cout<<"calling fails"<<endl;
			return pcid_str;
		}
	}
	catch (CInternetException* e)
	{
		if(!ConnectToServer())
			return pcid_str;
		PostUserIdAndMac(userid_str,mac_str);
	}

	//获取来自服务端的回复，获取来自服务端的pcid
	DWORD dwRet;
	pFile->QueryInfoStatusCode(dwRet);

	if(dwRet != HTTP_STATUS_OK)
	{
		CString errText;
		errText.Format("POST出错，错误码：%d", dwRet);
	}
	else
	{
		int len = pFile->GetLength();
		char buf[50];
		int numread;
		while ((numread = pFile->Read(buf,sizeof(buf)-1)) > 0)
		{
			buf[numread] = '\0';
		}
		pcid_str = buf;

	}
	cout<<pcid_str<<endl;
	return pcid_str;
}

//根据keyname值将双字节RegStrBuff或者port赋值给相应的私有对象
int AppConfig::GetPrivateValue(LPCTSTR KeyName,TCHAR *RegStrBuff,int port)
{
	//将keyname同“Host”进行比较，如果相同的话，就将RegStrBuff赋值给m_host 
	if(_tcscmp(KeyName,_T("Host"))==0)
	{
		sprintf(m_host,"%s",RegStrBuff);
		// std::cout<<m_host<<std::endl;
		return TRUE;
	}
	else if (_tcscmp(KeyName,_T("Port"))==0)
	{
		m_Port=port;
		// std::cout<<m_Port<<std::endl;
		return TRUE;
	}
	else if(_tcscmp(KeyName,_T("Bkurl"))==0)
	{
		sprintf(m_bkurl,"%s",RegStrBuff);
		// std::cout<<m_bkurl<<std::endl;
		return TRUE;
	}
	else if(_tcscmp(KeyName,_T("Version"))==0)
	{
		sprintf(m_version,"%s",RegStrBuff);
		// std::cout<<m_version<<std::endl;
		return TRUE;
	}
	else
	{
		return FALSE;
	}
	return FALSE;
}



//设置注册表。根据选项字段名、key名还有值的类型来设置注册表
int AppConfig::SetReg(LPCTSTR SectionName,LPCTSTR KeyName,int ValueType)
{
	int RegError;
	int Port;
	TCHAR RegStrBuff[50]={0};
	//根据ValueType进行选择
	switch(ValueType)
	{
		case DWORDTYPE:
			{
				Port=GetPrivateProfileInt(SectionName,KeyName,-1,m_installpath.c_str());
				if(Port==-1)
				{
					regkeyobj.Close();
					return FALSE;
				}
				regkeyobj.SetDWORDValue(KeyName,Port);
				GetPrivateValue(KeyName,NULL,Port);
				return TRUE;
			}break;
		case STRINGTYPE:
			{
				RegError=GetPrivateProfileString(SectionName,KeyName,_T(""),RegStrBuff,sizeof(RegStrBuff),m_installpath.c_str());
				if(RegError==sizeof(RegStrBuff)-1 || RegError==sizeof(RegStrBuff)-2)
				{

					regkeyobj.Close();
					return FALSE;
				}
				Releaseinfo("config.ini");
				Releaseinfo(RegStrBuff);
				regkeyobj.SetStringValue(KeyName,RegStrBuff,REG_SZ);
				GetPrivateValue(KeyName,RegStrBuff,0);
				return TRUE;
			}break;
		default:
			return FALSE; break;
	}
}