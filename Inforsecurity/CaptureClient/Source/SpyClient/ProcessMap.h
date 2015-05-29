#pragma once
#include "stdafx.h"
#include <ext_string.h>
#include <windows.h>
#include <iphlpapi.h>
#include <tlhelp32.h>
#include <psapi.h>
#include "pcap.h"
#include <stdlib.h>
#include <tchar.h>
#include "string.h"
#include <malloc.h>
#include <map>
#include "md5.h"
#include "sqlite3.h"
#include "AppConfig.h"
#define MAXPORT 65536
#define MAXPID 32768

using namespace std;
struct ProcessNode
{
	char *processname;
	char *processpath;
	int pid;
};

class ProcessMap
{
public:
	ProcessMap();
	~ProcessMap();
    int Init(); //初始化函数
	int BuildTcpProcDict(); //构建TCP进程字典
	int BuildUdpProcDict(); //构建UDP进程字典
	static ProcessMap *SharedInstance();
	int ClearTcpProcessDict();//清空TCP processdict
	int ClearUdpProcessDict();//清空UDP processdict
	char *TCHARTochar(TCHAR *tchstr);//将TCHAR转化为char
	char *GetProcessName(int pid,int port,int protocoltype);//获取进程名字
	char *GetProcessPath(int pid,int port,int protocoltype);//获取进程路径
	int GetProcessPid(int port,int protocoltype);//获取进程的PID
	void UpdateUnknowUdpportdict();//更新未知udp端口字典
	void UpdateUnknowTcpportdict();//更新未知tcp端口字典
private:
	static ProcessMap *_instance;
	map<int,ProcessNode*> tcpprocessdict;
	map<int,ProcessNode*> udpprocessdict;
	map<int,ProcessNode*>::iterator processdictit;
	map<int,int> portdict;//用于缓存port与pid的对应
	map<int,int>::iterator portdictit;

	map<int,int> unkowntcpportdict; //未知tcp端口字典
	map<int,int> unkownudpportdict; //未知udp端口字典
};

struct pNode
{
	int pid;
	bool isSafe;
};
class Md5Map
{
public:
	Md5Map();
	~Md5Map();
	static Md5Map *SharedInstance();
	int CheckDict(int port,int pid,string processpath,int protocoltype);
	int Md5Map::ClearTcpPDict();
	int Md5Map::ClearUdpPDict();
	string GetMd5(string processpath);
private:
	static Md5Map *_md5instance;
	map<int,pNode*>::iterator pdictit;
	map<int,pNode*> udppdict;
	map<int,pNode*> tcppdict;
	sqlite3 *db;
};