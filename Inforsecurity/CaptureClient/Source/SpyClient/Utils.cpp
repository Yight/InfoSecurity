#include "Stdafx.h"
#include "Utils.h"
#include <WinSock2.h>
#include <Iphlpapi.h>
#include <iostream>
#ifdef _DEBUG
#define new DEBUG_NEW
#endif

/*ext_string format(const char *fmt, ) 
{ 
	ext_string strResult="";
	if (NULL != fmt)
	{
		va_list marker = NULL;            
		va_start(marker, fmt);                            //初始化变量参数 
		size_t nLength = _vscprintf(fmt, marker) + 1;    //获取格式化字符串长度
		std::vector<char> vBuffer(nLength, '\0');        //创建用于存储格式化字符串的字符数组
		int nWritten = _vsnprintf_s(&vBuffer[0], vBuffer.size(), nLength, fmt, marker);
		if (nWritten>0)
		{
		    strResult = &vBuffer[0];
		}
		va_end(marker);                                    //重置变量参数
	}
	return strResult; 
}

std::wstring format(const wchar_t *fmt, ) 
{ 
    std::wstring strResult=L"";
    if (NULL != fmt)
    {
        va_list marker = NULL;            
        va_start(marker, fmt);                            //初始化变量参数
        size_t nLength = _vscwprintf(fmt, marker) + 1;    //获取格式化字符串长度
        std::vector<wchar_t> vBuffer(nLength, L'\0');    //创建用于存储格式化字符串的字符数组
        int nWritten = _vsnwprintf_s(&vBuffer[0], vBuffer.size(), nLength, fmt, marker); 
        if (nWritten > 0)
        {
            strResult = &vBuffer[0];
        }
        va_end(marker);                                    //重置变量参数
    }
    return strResult; 
} */

std::string GetEthernetMacAddr()
{
	ULONG BufferLength = 0;
	BYTE* pBuffer = 0;
	if( ERROR_BUFFER_OVERFLOW == GetAdaptersInfo( 0, &BufferLength ))
	{
		pBuffer = new BYTE[ BufferLength ];
	}
	else
		return NOTFOUNDETHERNET;

	PIP_ADAPTER_INFO pAdapterInfo = reinterpret_cast<PIP_ADAPTER_INFO>(pBuffer);
	GetAdaptersInfo( pAdapterInfo, &BufferLength );

	while( pAdapterInfo )
	{
		if(MIB_IF_TYPE_ETHERNET ==pAdapterInfo->Type)
		{
			CString csMacAddress;
			csMacAddress.Format(_T("%02X%02X%02X%02X%02X%02X"),
							pAdapterInfo->Address[0],
							pAdapterInfo->Address[1],
							pAdapterInfo->Address[2],
							pAdapterInfo->Address[3],
							pAdapterInfo->Address[4],
							pAdapterInfo->Address[5]);
			delete[] pBuffer;
			return csMacAddress.GetBuffer();
		}
		pAdapterInfo = pAdapterInfo->Next;
	}

	delete[] pBuffer;
	return NOTFOUNDETHERNET;
}

char* ConvertLPWSTRToLPSTR (LPWSTR lpwszStrIn)
{
	LPSTR pszOut = NULL;
	if (lpwszStrIn != NULL)
	{
		int nInputStrLen = wcslen (lpwszStrIn);

		// Double NULL Termination
		int nOutputStrLen = WideCharToMultiByte (CP_ACP, 0, lpwszStrIn, nInputStrLen, NULL, 0, 0, 0) + 2;
		pszOut = new char [nOutputStrLen];

		if (pszOut)
		{
			memset (pszOut, 0x00, nOutputStrLen);
			WideCharToMultiByte(CP_ACP, 0, lpwszStrIn, nInputStrLen, pszOut, nOutputStrLen, 0, 0);
		}
	}
	return pszOut;
}