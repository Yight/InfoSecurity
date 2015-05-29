#pragma once
#include "StdAfx.h"
#include <string>
#include <afxtempl.h>
#include "ProtoMessage.pb.h"
#include "afxmt.h"
#include <ctime>

using namespace SpyClient;
using namespace std;


class ProtobufThread : public CWinThread
{
	DECLARE_DYNCREATE(ProtobufThread)

protected:
   // UINT m_nTimerID1;
   //UINT m_nTimerID2;
   //afx_msg void OnTimer(WPARAM wParam, LPARAM lParam); // added by hand
   DECLARE_MESSAGE_MAP()

    ProtobufThread(){}        // protected constructor used by dynamic creation
    virtual ~ProtobufThread(){}
    virtual BOOL InitInstance();
    virtual int ExitInstance();
    afx_msg void OnIPMessage(WPARAM wParam, LPARAM lParam);
    afx_msg void OnHTTPMessage(WPARAM wParam, LPARAM lParam);
	afx_msg void OnEmailMessage(WPARAM wParam,LPARAM lParam);
    afx_msg void OnQuit(WPARAM wParam, LPARAM lParam);
public:
	void SetSdThread(CWinThread* sdthread);
private:
	CWinThread *sdthread;
	vector<EmailPacket> *email_vector;
	vector<HttpPacket>  *http_vector;
	vector<IpPacket> *ippacket_vector;
	CTime  timeobj;
//	CMutex mutex_map;
//	CMutex mutex_email;
//	CMutex mutex_http;
//	CMutex mutex_ippacket;

};