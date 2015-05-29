// ServiceCtrl.h: interface for the ServiceCtrl class.
//
//////////////////////////////////////////////////////////////////////

#ifndef SERVICECTRL_H
#define SERVICECTRL_H


#define BUFFER_SIZE 1024

#include "stdafx.h"

/* 在客户结束访问或删除服务时为关闭所有的Cmd进程而创建的数据结构 */
typedef struct tagPROCESSDATA  
{								
	HANDLE			hProcess;	// 创建Cmd进程时获得的进程句柄
	DWORD			dwProcessId;// 创建Cmd进程时获得的进程标识符
	tagPROCESSDATA	*next;		// 指向下一个数据结构的指针
} PROCESSDATA, *LPPROCESSDATA;

typedef struct tagSESSIONDATA	// 重定向Cmd标准输入/输出时使用的数据结构
{
	HANDLE hPipe;				// 为实现进程间通信而使用的管道
	SOCKET sClient;				// 与客户端进行通信时的客户端套接字		
} SESSIONDATA, *PSESSIONDATA;

void  WINAPI CmdStart(DWORD, LPTSTR*);	/* 服务程序中的"ServiceMain"，
										 * 注册服务控制句柄，创建服务主线程.*/
void  WINAPI CmdControl(DWORD);			/* 服务程序中的"CtrlHandler"，
										 * 处理接收到的控制命令，删除已创建的Cmd进程.*/
DWORD WINAPI CmdService(LPVOID);		/* 服务主线程，创建服务监听端口，
										 * 在接受客户连接时，创建重定向Cmd标准输入/输出线程.*/
DWORD WINAPI CmdShell(LPVOID);			/* 创建管道与Cmd进程，及Cmd的输入/输出线程.*/
DWORD WINAPI ReadShell(LPVOID);			/* 重定向Cmd的输出，读取信息后发送到客户端.*/
DWORD WINAPI WriteShell(LPVOID);		/* 重定向Cmd的输入，接收客户端的信息输入到Cmd进程.*/
												// 如果选择远程模式，则须与远程主机建立连接，
//BOOL  ConnectRemote(BOOL, char*, char*, char*); // 注须提供管理员权限的用户名与密码，
												// 密码为空时用"NULL"代替.
//void  InstallCmdService(char*);		// 复制传送文件，打开服务控制管理器，创建或打开服务程序.
//void  RemoveCmdService(char*);		// 删除文件，停止服务后，卸载服务程序.

#endif

