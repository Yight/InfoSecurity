#pragma once

class CMainCtrl
{
public:
	CMainCtrl(void){};
	~CMainCtrl(void);
	int Init();
	void StopService();
	void TestPostData();
	bool RunCapturePacket(CWinThread* pfthread);

	static CMainCtrl *SharedInstance();
	
private:
	static CMainCtrl *_instance;

};

