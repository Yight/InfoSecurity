// MonCtrl.h: interface for the CMonCtrl class.
//
//////////////////////////////////////////////////////////////////////

#ifndef MON_CTRL_H
#define MON_CTRL_H

#include "stdafx.h"
#include <string>
using namespace std;
void Releaseinfo(char *infostr);

class CMonCtrl  
{
public:
	CMonCtrl();
	virtual ~CMonCtrl();
public:


	static CMonCtrl *Instance();
	
	BOOL DW_Init();
	BOOL DW_Destory();
	string InstallPath;
	bool Shouhu();

	string GetInstallPath();
private:
	
	
    static CMonCtrl *_instance;

};

#endif 