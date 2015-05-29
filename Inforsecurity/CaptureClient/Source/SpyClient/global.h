﻿#pragma once

#define        PROTOBUF_IP_MESSAGE           WM_USER + 1
#define        PROTOBUF_HTTP_MESSAGE         WM_USER + 2
#define        PROTOBUF_EMAIL_MESSAGE        WM_USER + 3
#define        WM_RUN        WM_USER + 4
#define        SENDDATA_REC_IPMESSAGE WM_USER+5
#define        SENDDATA_REC_HTTPMESSAGE WM_USER+6
#define        SENDDATA_REC_EMAILMESSAGE WM_USER+7

#define	NOTFOUNDETHERNET ""
#define MAXSIZEDATA 500

enum EMAILPROVIDER {
	PROVIDER_163_126_YEAH=0,
	PROVIDER_QQ=1,
	PROVIDER_YAHOO=2,
	PROVIDER_SINA=3,
	PROVIDER_SOHU=4,
	PROVIDER_139=5,
	PROVIDER_FOXMAIL=6,
	PROVIDER_SMTP=7
};