#include "StdAfx.h"
#include "PacketStruct.h"
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

namespace PROTOCOL_DEFINE
{
	int GetIPHeaderLength(IP_HEADER * ip)
	{
		return (ip->ver_len&15)*32/8;
	}

	int GetTCPHeaderLength(TCP_HEADER * tcp)
	{
		return  ((tcp->offset_reser_con)>>4)*4;;
	}


}