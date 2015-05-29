#include "stdafx.h"
#include "ProcessMap.h"

ProcessMap *ProcessMap::_instance= NULL;
Md5Map *Md5Map::_md5instance= NULL;
//静态AppConfig类句柄的动态申请
ProcessMap *ProcessMap::SharedInstance()
{	
	if (_instance == NULL)
	{
		_instance = new ProcessMap;
	}
	return _instance;
}


ProcessMap::ProcessMap()
{
	//初始化processmatrix
}

ProcessMap::~ProcessMap()
{
	//释放进程矩阵中数据
	ClearTcpProcessDict();
	ClearUdpProcessDict();
	portdict.clear();
	unkowntcpportdict.clear();
	unkownudpportdict.clear();
	delete _instance;

}

//初始化函数
int ProcessMap::Init()
{
	BuildTcpProcDict();
	BuildUdpProcDict();
	HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	PROCESSENTRY32 p;
	p.dwSize = sizeof(PROCESSENTRY32);
	// Traverse Process List
	/*for(BOOL ret = Process32First(hSnapShot, &p); ret != 0; ret = Process32Next(hSnapShot, &p))
	{
		// Get pid and file name
		int pid = p.th32ProcessID;
		
		// Get full path (if possible)
		HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
		if (hProcess != 0)
		{
			TCHAR fullPath[MAX_PATH];
			if (GetModuleFileNameEx(hProcess, 0, fullPath, MAX_PATH) > 0)// Success
			{
				FILE *fp;
				fp = fopen("D:\\SpyClient123.log","a+");
				if(fp == NULL)
				{
					cout<<"file open fail"<<endl;
				}

				fprintf(fp,"%s\n",TCHARTochar(fullPath));
				fprintf(fp,"%s\n",TCHARTochar(p.szExeFile));
				fclose(fp);
			}
				CloseHandle(hProcess);
		}
		else
		{
			FILE *fp;
			fp = fopen("D:\\SpyClient123.log","a+");
			if(fp == NULL)
			{
				cout<<"file open fail"<<endl;
			}
			fprintf(fp,"%s\n",TCHARTochar(p.szExeFile));
			fclose(fp);
		}
	}
	CloseHandle(hSnapShot);
	*/
	return 0;
}

//构建TCP进程字典
int ProcessMap::BuildTcpProcDict()
{
	//清空processtcpdict
	ClearTcpProcessDict();
	portdict.clear();
	//构建tcpportdict
	MIB_TCPTABLE_OWNER_PID tcptable;
	tcptable.dwNumEntries = sizeof(tcptable)/sizeof(tcptable.table[0]);
	DWORD tcptablesize = sizeof(tcptable);
	//if(GetExtendedTcpTable((void *)&tcptable, &tcptablesize, FALSE, AF_INET, TCP_TABLE_OWNER_PID_ALL, 0) == NO_ERROR)
	int tcptableerror = GetExtendedTcpTable((void *)&tcptable, &tcptablesize, FALSE, AF_INET, TCP_TABLE_OWNER_PID_ALL, 0);
	if(tcptableerror == NO_ERROR)
	{
		for(unsigned int i =0 ; i< tcptable.dwNumEntries; i++)
		{
			int port = ntohs((unsigned short)tcptable.table[i].dwLocalPort);
			int pid = tcptable.table[i].dwOwningPid;
			portdict.insert(pair<int ,int>(port,pid));
		}
	}
	// Take a snapshot
	HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	PROCESSENTRY32 p;
	p.dwSize = sizeof(PROCESSENTRY32);
	// Traverse Process List
	for(BOOL ret = Process32First(hSnapShot, &p); ret != 0; ret = Process32Next(hSnapShot, &p))
	{
		// Get pid and file name
		int pid = p.th32ProcessID;
		for(portdictit = portdict.begin();portdictit!=portdict.end();portdictit++)
		{
			if(portdictit->second == pid)
			{
				ProcessNode *processnode = new ProcessNode;
				processnode->pid = pid;
				processnode->processname = TCHARTochar(p.szExeFile);
				// Get full path (if possible)
				HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
				if (hProcess == 0)
				{
					processnode->processpath = NULL;
				}
				else
				{
					TCHAR fullPath[MAX_PATH];
					if (GetModuleFileNameEx(hProcess, 0, fullPath, MAX_PATH) > 0)// Success
					{
						processnode->processpath = TCHARTochar(fullPath);
					}
					else
						processnode->processpath = NULL;
				}
				CloseHandle(hProcess);
				tcpprocessdict.insert(pair<int,ProcessNode*>(portdictit->first,processnode));
			}
		}
		
	}
	CloseHandle(hSnapShot);

	UpdateUnknowTcpportdict();
	return 0;
}

int ProcessMap::BuildUdpProcDict()
{
	//清空processtcpdict
	ClearUdpProcessDict();
	portdict.clear();
	//构建tcpportdict
	MIB_UDPTABLE_OWNER_PID udptable;
	udptable.dwNumEntries = sizeof(udptable)/sizeof(udptable.table[0]);
	DWORD udptablesize = sizeof(udptable);
	if(GetExtendedUdpTable((void *)&udptable, &udptablesize, FALSE, AF_INET, UDP_TABLE_OWNER_PID, 0) == NO_ERROR)
	{
		for(unsigned int i =0 ; i< udptable.dwNumEntries; i++)
		{
			int port = ntohs((unsigned short)udptable.table[i].dwLocalPort);
			int pid = udptable.table[i].dwOwningPid;
			portdict.insert(pair<int ,int>(port,pid));
		}
	}
	//构建UdpProcessDict
	// Take a snapshot
	HANDLE hSnapShot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	PROCESSENTRY32 p;
	p.dwSize = sizeof(PROCESSENTRY32);
	// Traverse Process List
	for(BOOL ret = Process32First(hSnapShot, &p); ret != 0; ret = Process32Next(hSnapShot, &p))
	{
		// Get pid and file name
		int pid = p.th32ProcessID;
		for(portdictit=portdict.begin();portdictit!=portdict.end();portdictit++)
		{
			if(portdictit->second == pid)
			{
				ProcessNode *processnode = new ProcessNode;
				processnode->pid = pid;
				processnode->processname = TCHARTochar(p.szExeFile);
				// Get full path (if possible)
				HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
				if (hProcess == 0)
				{
					processnode->processpath = NULL;
				}
				else
				{
					TCHAR fullPath[MAX_PATH];
					if (GetModuleFileNameEx(hProcess, 0, fullPath, MAX_PATH) > 0) // Success
					{
						processnode->processpath = TCHARTochar(fullPath);
					}
					else
						processnode->processpath = NULL;
				}
				CloseHandle(hProcess);
				udpprocessdict.insert(pair<int,ProcessNode*>(portdictit->first,processnode));
			}
		}
	}
	CloseHandle(hSnapShot);
	UpdateUnknowUdpportdict();
	return 0;
}

void ProcessMap::UpdateUnknowTcpportdict()
{
	portdictit = unkowntcpportdict.begin();
	while(portdictit!=unkowntcpportdict.end())
	{
		processdictit = tcpprocessdict.find(portdictit->first);
		if(processdictit!=tcpprocessdict.end())
		{
			int port = portdictit->first;
			portdictit++;
		    unkowntcpportdict.erase(port);
		}
		else
			portdictit++;
	};
}

void ProcessMap::UpdateUnknowUdpportdict()
{
	portdictit = unkownudpportdict.begin();
	while(portdictit!=unkownudpportdict.end())
	{
		processdictit = udpprocessdict.find(portdictit->first);
		if(processdictit!=udpprocessdict.end())
		{
			int port = portdictit->first;
			portdictit++;
			unkownudpportdict.erase(port);
		}
		else
			portdictit++;
	};
}

int ProcessMap::GetProcessPid(int port,int protocoltype)
{
	switch(protocoltype)
	{
	case 0:{
		//判断其端口是否属于未知端口字典
		portdictit = unkowntcpportdict.find(port);
		if(portdictit!=unkowntcpportdict.end())
			return -1;
		processdictit =tcpprocessdict.find(port);
		if(processdictit==tcpprocessdict.end())
		{
			BuildTcpProcDict();
			processdictit = tcpprocessdict.find(port);
			if(processdictit == tcpprocessdict.end())
			{
				portdictit = unkowntcpportdict.find(port);
				if(portdictit==unkowntcpportdict.end())
					unkowntcpportdict.insert(pair<int,int>(port,0));
				return -1;
			}
			else
				return processdictit->second->pid;
		}
		else
			return processdictit->second->pid;
		   }break;
	case 1:{
		portdictit = unkownudpportdict.find(port);
		if(portdictit!=unkownudpportdict.end())
			return -1;
		processdictit =udpprocessdict.find(port);
		if(processdictit==udpprocessdict.end())
		{
			BuildUdpProcDict();
			processdictit = udpprocessdict.find(port);
			if(processdictit == udpprocessdict.end())
			{
				portdictit = unkownudpportdict.find(port);
				if(portdictit==unkownudpportdict.end())
					unkownudpportdict.insert(pair<int,int>(port,0));
				return -1;
			}
			else
				return processdictit->second->pid;
		}
		else
			return processdictit->second->pid;

		   }break;
	default:;
	}
	return -1;
}

char *ProcessMap::GetProcessPath(int pid,int port,int protocoltype)
{
	if(pid == -1)
		return "";
	switch(protocoltype)
	{
	case 0:{
		processdictit = tcpprocessdict.find(port);
		if(processdictit->second->processpath)
			return processdictit->second->processpath;
		else
			return "";
		   }break;
	case 1:{
		processdictit = udpprocessdict.find(port);
		if(processdictit->second->processpath)
			return processdictit->second->processpath;
		else
			return "";
		   }break;
	default:;
	}
	return "";
}

char *ProcessMap::GetProcessName(int pid,int port,int protocoltype)
{
	if(pid == -1)
		return "";
	switch(protocoltype)
	{
	case 0:{
		processdictit = tcpprocessdict.find(port);
		if(processdictit->second->processname)
			return processdictit->second->processname;
		else
			return "";
		   }break;
	case 1:{
		processdictit = udpprocessdict.find(port);
		if(processdictit->second->processname)
			return processdictit->second->processname;
		else
			return "";
		   }break;
	default:;
	}
	return "";
}
int ProcessMap::ClearTcpProcessDict()
{
	for(processdictit = tcpprocessdict.begin();processdictit!=tcpprocessdict.end();processdictit++)
	{
		delete processdictit->second->processname;
		delete processdictit->second->processpath;
		processdictit->second->pid = 0;
		delete processdictit->second;
	}
	tcpprocessdict.clear();
	return 0;
}

int ProcessMap::ClearUdpProcessDict()
{
	for(processdictit = udpprocessdict.begin();processdictit!=udpprocessdict.end();processdictit++)
	{
		delete processdictit->second->processname;
		delete processdictit->second->processpath;
		processdictit->second->pid = 0;
		delete processdictit->second;
	}
	udpprocessdict.clear();
	return 0;
}

char *ProcessMap::TCHARTochar(TCHAR *tchstr)
{
	char swappol[MAX_PATH+1]={0};
	char *chstr;
	sprintf(swappol,"%s",tchstr);
	chstr = new char[strlen(swappol)+1];
	memset(chstr,0,strlen(swappol)+1);
	strcpy(chstr,swappol);
	return chstr;
}

Md5Map *Md5Map::SharedInstance()
{	
	if (_md5instance == NULL)
	{
		_md5instance = new Md5Map;
	}
	return _md5instance;
}


Md5Map::Md5Map()
{
	
}

Md5Map::~Md5Map()
{
	ClearUdpPDict();
	ClearTcpPDict();
	delete _md5instance;
}

string Md5Map::GetMd5(string processpath){	
	if (processpath!=""){
			string strmd5 = MD5(ifstream(processpath, ios::binary)).toString();
			if (strmd5.length()==0)
				return "";
			return strmd5;
	}
	return "";
}


int Md5Map::CheckDict(int port,int pid,string processpath,int protocoltype)
{
	int rc,nrows,ncols;
	string md5;
	char *errmsg = NULL;
	char **result;
	pNode *pnode = new pNode;
	bool ismd5exist = 0;
	switch(protocoltype)
	{
	case 0:
		{
		pdictit = tcppdict.find(port);
		if(pdictit != tcppdict.end())
		{
			if (pdictit->second->pid==pid)
			{
				if(pdictit->second->isSafe==1)
					return 1;
				else
					return 0;
			}
			else
			{
				delete pdictit->second;
				tcppdict.erase(pdictit);
				md5 = Md5Map::SharedInstance()->GetMd5(processpath);					
				const char *charmd5;
				charmd5=md5.c_str();
				_bstr_t t = AppConfig::SharedInstance()->GetWhitelistPath().c_str();
				char* pwhitelistpath = (char *)t;
				rc = sqlite3_open(pwhitelistpath,&db);
				if(rc!=SQLITE_OK)
					return 0;
				sqlite3_get_table(db,"select md5 from whitetable;",&result,&nrows,&ncols,&errmsg);
				for(int i=0;i<nrows+1;i++)
				{
					if (memcmp(result[i],charmd5,strlen(charmd5))==0)
					{
						ismd5exist=1;
						break;
					}
				}
				sqlite3_close(db);
				if (ismd5exist)
				{
					pnode->pid = pid;
					pnode->isSafe = 1;
					tcppdict.insert(pair<int ,pNode*>(port,pnode));
					delete (char *) charmd5;
					return 1;
				}
				else
				{
					pnode->pid = pid;
					pnode->isSafe = 0;
					tcppdict.insert(pair<int, pNode*>(port,pnode));
					delete (char *) charmd5;
					return 0;
				}
			}
		}
		else 
		{
			md5 = Md5Map::SharedInstance()->GetMd5(processpath);
			const char *charmd5;
			charmd5=md5.c_str();
			_bstr_t t = AppConfig::SharedInstance()->GetWhitelistPath().c_str();
			char* pwhitelistpath = (char *)t;
			rc = sqlite3_open(pwhitelistpath,&db);
			if(rc!=SQLITE_OK)
				return 0;
			sqlite3_get_table(db,"select md5 from whitetable;",&result,&nrows,&ncols,&errmsg);
			for(int i=0;i<nrows+1;i++)
			{
				if (memcmp(result[i],charmd5,strlen(charmd5))==0)
				{
					ismd5exist=1;
					break;
				}
			}
			sqlite3_close(db);
			//delete charmd5;
			//charmd5=NULL;
			if (ismd5exist)
			{
				pnode->pid = pid;
				pnode->isSafe = 1;
				tcppdict.insert(pair<int ,pNode*>(port,pnode));
				return 1;
			}
			else
			{
				pnode->pid =pid;
				pnode->isSafe = 0;
				tcppdict.insert(pair<int,pNode*>(port,pnode));
				return 0;
			}
		}
	}break;
	case 1:{
		pdictit = udppdict.find(port);
		if(pdictit != udppdict.end())
		{
			if (pdictit->second->pid==pid)
			{
				if(pdictit->second->isSafe==1)
					return 1;
				else
					return 0;
			}
			else
			{
				delete pdictit->second;
				udppdict.erase(pdictit);
				md5 = Md5Map::SharedInstance()->GetMd5(processpath);
				const char *charmd5;
				charmd5=md5.c_str();
				_bstr_t t = AppConfig::SharedInstance()->GetWhitelistPath().c_str();
				char* pwhitelistpath = (char *)t;
				rc = sqlite3_open(pwhitelistpath,&db);
				if(rc!=SQLITE_OK)
				return 0;
				sqlite3_get_table(db,"select md5 from whitetable;",&result,&nrows,&ncols,&errmsg);
				for(int i=0;i<nrows+1;i++)
				{
					if (memcmp(result[i],charmd5,strlen(charmd5))==0)
					{
						ismd5exist=1;
						break;
					}
				}
				sqlite3_close(db);
				if (ismd5exist)
				{
					pnode->pid = pid;
					pnode->isSafe = 1;
					udppdict.insert(pair<int ,pNode*>(port,pnode));
					return 1;
				}
				else
				{
					pnode->pid = pid;
					pnode->isSafe = 0;
					udppdict.insert(pair<int, pNode*>(port,pnode));
					return 0;
				}
			}
		}
		else 
		{

			md5 = Md5Map::SharedInstance()->GetMd5(processpath);
			const char *charmd5;
			charmd5=md5.c_str();
			_bstr_t t = AppConfig::SharedInstance()->GetWhitelistPath().c_str();
			char* pwhitelistpath = (char *)t;
			rc = sqlite3_open(pwhitelistpath,&db);
			if(rc!=SQLITE_OK)
				return 0;
			sqlite3_get_table(db,"select md5 from whitetable;",&result,&nrows,&ncols,&errmsg);
			for(int i=0;i<nrows+1;i++)
			{
				if (memcmp(result[i],charmd5,strlen(charmd5))==0)
				{
					ismd5exist=1;
					break;
				}
			}
			sqlite3_close(db);
			//delete charmd5;
			//charmd5=NULL;
			if (ismd5exist)
			{
				pnode->pid = pid;
				pnode->isSafe = 1;
				udppdict.insert(pair<int ,pNode*>(port,pnode));
				return 1;
			}
			else
			{
				pnode->pid =pid;
				pnode->isSafe = 0;
				udppdict.insert(pair<int,pNode*>(port,pnode));
				return 0;
			}
		}
	}break;
	default:break;
	}
}
int Md5Map::ClearTcpPDict()
{
	for(pdictit = tcppdict.begin();pdictit!=tcppdict.end();pdictit++)
	{
		delete pdictit->second;
	}
	tcppdict.clear();
	return 0;
}
int Md5Map::ClearUdpPDict()
{
	for(pdictit = udppdict.begin();pdictit!=udppdict.end();pdictit++)
	{
		delete pdictit->second;
	}
	udppdict.clear();
	return 0;
}