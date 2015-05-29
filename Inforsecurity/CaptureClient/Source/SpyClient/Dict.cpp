#include "stdafx.h"
#include "Dict.h"

Dict* Dict::_instance = NULL;

Dict* Dict::SharedInstance()
{
	if(_instance==NULL)
	{
		_instance=new Dict;
	}
	return _instance;
}


Dict::Dict(void)
{
	dictindex=(byte *)malloc(sizeof(byte)*13);
}

Dict::~Dict(void)

{
	free(dictindex);
}

int Dict::SetFiveTupleMap(string sip,string dip,u_short sport,u_short dport,byte prototype)
{
	//string s_dictindex;
	FiveTupleConvertIndex(sip,dip,sport,dport,prototype);
	//s_dictindex=dictindex;
	//cout<<s_dictindex.length()<<endl;
   // fivetupleit=fivetuplemap.find(s_dictindex);
	return TRUE;
}

void Dict::FiveTupleConvertIndex(string sip,string dip,u_short sport,u_short dport,byte prototype)
{
	u_int u_sip=3;
	u_int u_dip=0;
	u_sip=inet_addr(sip.c_str());
	u_dip=inet_addr(dip.c_str());
	dictindex[0]=(byte)(u_sip>>24);
	dictindex[1]=(byte)(u_sip>>16);
	dictindex[2]=(byte)(u_sip>>8);
	dictindex[3]=(byte)(u_sip);
	dictindex[4]=(byte)(u_dip>>24);
	dictindex[5]=(byte)(u_dip>>16);
	dictindex[6]=(byte)(u_dip>>8);
	dictindex[7]=(byte)(u_dip);
	dictindex[8]=(byte)(sport>>8);
	dictindex[9]=(byte)(sport);
	dictindex[10]=(byte)(dport>>8);
	dictindex[11]=(byte)(dport);
	dictindex[12]=prototype;

}