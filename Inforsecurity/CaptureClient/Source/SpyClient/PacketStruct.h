#pragma once

#include "stdafx.h"


using namespace std;


namespace PROTOCOL_DEFINE
{
	//下面的定义参见RFC 1700
#define IP		"0x0800"
	
#define TCP		6		//传输控制协议
#define	UDP		17		//用户数据报协议

	struct IP_HEADER
	{
		byte ver_len;		//版本4位,头长度4位,报头长度以32位为一个单位
		byte type;			//类型8位
		byte length[2];		//总长度,16位,指出报文的以字节为单位的总长度，报文长度不能超过65536个字接，否则认为报文遭到破坏
		byte id[2];			//报文标示,用于多于一个报文16位
		byte flag_offset[2];//标志,3位	数据块偏移13位
		byte time;			//生存时间,8位
		byte protocol;		//协议,8位
		byte crc_val[2];	//头校验和，16位
		byte src_addr[4];	//源地址,32位
		byte des_addr[4];	//目标地址,32位
		byte options[4];	//选项和填充,32位
	};

	struct TCP_HEADER
	{
		u_short sport;
		u_short dport;
		u_int sequence_no;	//32位，标示消息端的数据位于全体数据块的某一字节的数字
		u_int ack_no;			//32位，确认号,标示接收端对于发送端接收到数据块数值
		u_char offset_reser_con;//数据偏移4位，预留6位，控制位6为
		u_char window;			//窗口16位
		u_short checksum;		//校验码,16位
		u_short urgen_pointer;	//16位，紧急数据指针
		//u_short options;		//选祥和填充,32位
	};



	struct UDP_HEADER
	{
	    u_short sport;          // Source port
	    u_short dport;          // Destination port
	    u_short len;            // Datagram length
	    u_short crc;            // Checksum
	};

	int GetIPHeaderLength(IP_HEADER * ip);
	int GetTCPHeaderLength(TCP_HEADER * tcp);

};