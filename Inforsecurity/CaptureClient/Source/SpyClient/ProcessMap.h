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
    int Init(); //��ʼ������
	int BuildTcpProcDict(); //����TCP�����ֵ�
	int BuildUdpProcDict(); //����UDP�����ֵ�
	static ProcessMap *SharedInstance();
	int ClearTcpProcessDict();//���TCP processdict
	int ClearUdpProcessDict();//���UDP processdict
	char *TCHARTochar(TCHAR *tchstr);//��TCHARת��Ϊchar
	char *GetProcessName(int pid,int port,int protocoltype);//��ȡ��������
	char *GetProcessPath(int pid,int port,int protocoltype);//��ȡ����·��
	int GetProcessPid(int port,int protocoltype);//��ȡ���̵�PID
	void UpdateUnknowUdpportdict();//����δ֪udp�˿��ֵ�
	void UpdateUnknowTcpportdict();//����δ֪tcp�˿��ֵ�
private:
	static ProcessMap *_instance;
	map<int,ProcessNode*> tcpprocessdict;
	map<int,ProcessNode*> udpprocessdict;
	map<int,ProcessNode*>::iterator processdictit;
	map<int,int> portdict;//���ڻ���port��pid�Ķ�Ӧ
	map<int,int>::iterator portdictit;

	map<int,int> unkowntcpportdict; //δ֪tcp�˿��ֵ�
	map<int,int> unkownudpportdict; //δ֪udp�˿��ֵ�
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