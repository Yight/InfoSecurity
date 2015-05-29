// ServiceCtrl.h: interface for the ServiceCtrl class.
//
//////////////////////////////////////////////////////////////////////

#ifndef SERVICECTRL_H
#define SERVICECTRL_H


#define BUFFER_SIZE 1024

#include "stdafx.h"

/* �ڿͻ��������ʻ�ɾ������ʱΪ�ر����е�Cmd���̶����������ݽṹ */
typedef struct tagPROCESSDATA  
{								
	HANDLE			hProcess;	// ����Cmd����ʱ��õĽ��̾��
	DWORD			dwProcessId;// ����Cmd����ʱ��õĽ��̱�ʶ��
	tagPROCESSDATA	*next;		// ָ����һ�����ݽṹ��ָ��
} PROCESSDATA, *LPPROCESSDATA;

typedef struct tagSESSIONDATA	// �ض���Cmd��׼����/���ʱʹ�õ����ݽṹ
{
	HANDLE hPipe;				// Ϊʵ�ֽ��̼�ͨ�Ŷ�ʹ�õĹܵ�
	SOCKET sClient;				// ��ͻ��˽���ͨ��ʱ�Ŀͻ����׽���		
} SESSIONDATA, *PSESSIONDATA;

void  WINAPI CmdStart(DWORD, LPTSTR*);	/* ��������е�"ServiceMain"��
										 * ע�������ƾ���������������߳�.*/
void  WINAPI CmdControl(DWORD);			/* ��������е�"CtrlHandler"��
										 * ������յ��Ŀ������ɾ���Ѵ�����Cmd����.*/
DWORD WINAPI CmdService(LPVOID);		/* �������̣߳�������������˿ڣ�
										 * �ڽ��ܿͻ�����ʱ�������ض���Cmd��׼����/����߳�.*/
DWORD WINAPI CmdShell(LPVOID);			/* �����ܵ���Cmd���̣���Cmd������/����߳�.*/
DWORD WINAPI ReadShell(LPVOID);			/* �ض���Cmd���������ȡ��Ϣ���͵��ͻ���.*/
DWORD WINAPI WriteShell(LPVOID);		/* �ض���Cmd�����룬���տͻ��˵���Ϣ���뵽Cmd����.*/
												// ���ѡ��Զ��ģʽ��������Զ�������������ӣ�
//BOOL  ConnectRemote(BOOL, char*, char*, char*); // ע���ṩ����ԱȨ�޵��û��������룬
												// ����Ϊ��ʱ��"NULL"����.
//void  InstallCmdService(char*);		// ���ƴ����ļ����򿪷�����ƹ�������������򿪷������.
//void  RemoveCmdService(char*);		// ɾ���ļ���ֹͣ�����ж�ط������.

#endif

