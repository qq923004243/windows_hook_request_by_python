import struct
import ctypes
from ctypes import *
import os

current_directory = os.getcwd()
print(current_directory)
# 判断你的python环境是64位还是32位
__RuntimeEnvironment = struct.calcsize("P") * 8 == 64

try:
    if __RuntimeEnvironment:
        # 如果是64位加载64位DLL
        lib = CDLL(current_directory + "\Sunny64.dll")
        # Go语言回调函数声明
        TcpCallback = CFUNCTYPE(None, c_int64, c_char_p, c_char_p, c_int64, c_int64, c_int64, c_int64, c_int64, c_int64)
        HttpCallback = CFUNCTYPE(None, c_int64, c_int64, c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_int64)
        WsCallback = CFUNCTYPE(None, c_int64, c_int64, c_int64, c_int64, c_char_p, c_char_p, c_int64, c_int64)
        UDPCallback = CFUNCTYPE(None, c_int64, c_char_p, c_char_p, c_int64, c_int64, c_int64, c_int64)
    else:
        # 如果不是64位加载32位DLL
        lib = CDLL(current_directory + "\Sunny.dll")
        # Go语言回调函数声明
        TcpCallback = CFUNCTYPE(None, c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int)
        HttpCallback = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, c_int)
        WsCallback = CFUNCTYPE(None, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_int, c_int)
        UDPCallback = CFUNCTYPE(None, c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int)
except:
    print("载入DLL失败,请检测DLL文件")
    exit(1)


# 这个类 是动态加载DLL时 设置返回值为指针
class LibSunny:
    def __getattr__(self, name):
        func = getattr(lib, name)
        func.restype = ctypes.POINTER(ctypes.c_int)
        return func


DLLSunny = LibSunny()


# 指针到字节数组 ptr=指针 skip=偏移数 num=取出几个字节
def PtrToByte(ptr, skip, num):
    result_as_int = ctypes.cast(ptr, ctypes.c_void_p).value
    if result_as_int == None:
        return bytearray()
    result_as_int += skip
    new_result_ptr = ctypes.cast(result_as_int, ctypes.POINTER(ctypes.c_int))
    buffer = ctypes.create_string_buffer(num)
    ctypes.memmove(buffer, new_result_ptr, num)
    return buffer.raw


# 指针到整数
def PtrToInt(ptr):
    return ctypes.cast(ptr, ctypes.c_void_p).value


# 指针到字符串
def PointerToText(ptr):
    if ptr == 0:
        return ""
    buff = b''
    i = 0
    while True:
        bs = PtrToByte(ptr, i, 1)
        i += 1
        if len(bs) == 0:
            break
        if bs[0] == 0:
            break
        buff = buff + bs

    DLLSunny.Free(ptr) # 释放Sunny的指针,只要是Sunny返回的bytes 或 string 都需要释放指针
    try:
        return buff.decode('utf-8')
    except:
        return buff.decode('gbk')


# 指针到字节数组 (DLL协商的前8个字节是长度)
def PointerToBytes(ptr):
    if ptr == 0:
        return bytearray()
    lp = PtrToByte(ptr, 0, 8)
    if len(lp) != 8:
        return lp
    Lxp = PtrToInt(DLLSunny.BytesToInt(create_string_buffer(lp), 8))
    m = PtrToByte(ptr, 8, Lxp)
    DLLSunny.Free(ptr) # 释放Sunny的指针,只要是Sunny返回的bytes 或 string 都需要释放指针
    return  m

# http 请求操作类
class SunnyRequest:
    def __init__(self, _MessageId):
        self.MessageId = _MessageId

    def delete_gzipflag(self):
        """ 请求协议头中去除Gzip 若不删除压缩标记，返回数据可能是压缩后的 """
        DLLSunny.DelRequestHeader(self.MessageId, create_string_buffer("Accept-Encoding".encode("utf-8")))

    def set_agent(self, agent1):
        """
         对这个请求使用指定代理请求请求
         仅支持Socket5和http 例如 socket5://admin:123456@127.0.0.1:8888 或 http://admin:123456@127.0.0.1:8888
        """
        if not isinstance(agent1, str):
            return
        return bool(DLLSunny.SetRequestProxy(self.MessageId, create_string_buffer(agent1.encode("utf-8"))))

    def set_request_outtime(self, outtime):
        """
        仅限在发起请求时候使用,单位【毫秒】
        """
        if not isinstance(outtime, int):
            return
        DLLSunny.SetRequestOutTime(self.MessageId, outtime)

    def modify_url(self, new_url):
        """
        可以转向  1->2   网址A->网址B
        """
        if not isinstance(new_url, str):
            return
        DLLSunny.SetRequestUrl(self.MessageId, create_string_buffer(new_url.encode("utf-8")))

    def modify_requestbody_bytes(self, requestbody_bytes):
        """
        成功返回 True
        """
        if not isinstance(requestbody_bytes, bytes):
            return False
        return PtrToInt(
            DLLSunny.SetRequestData(self.MessageId, create_string_buffer(requestbody_bytes),
                                    len(requestbody_bytes))) == 1

    def modify_requestbody_str(self, requestbody):
        """
        成功返回 True
        """
        if not isinstance(requestbody, str):
            return False
        try:
            return self.modify_requestbody_bytes(requestbody.encode("gbk"))
        except:
            return self.modify_requestbody_bytes(requestbody.encode("utf-8"))

    def update_header_params(self, header_param):
        """
        若本身无指定的协议头，即为新增，若有则为修改
        可多条 一行一个 例如 Accept: image/gif
        """
        if not isinstance(header_param, str):
            return
        my_list = header_param.split("\r\n")
        for item in my_list:
            my_list2 = item.split(":")
            if len(my_list2) >= 1:
                name = my_list2[0]
                value = item.replace(name + ":").strip()
                DLLSunny.SetRequestHeader(self.MessageId, create_string_buffer(name.encode("utf-8")),
                                          create_string_buffer(value.encode("utf-8")))

    def close_connection(self):
        """
        使用本命令后,这个请求将不会被发送出去
        """
        DLLSunny.SetResponseHeader(self.MessageId, create_string_buffer("Connection".encode("utf-8")),
                                   create_string_buffer("Close".encode("utf-8")))

    def update_header_param(self, key, value):
        """
        若本身无指定的协议头，即为新增，若有则为修改
        """
        if not isinstance(key, str):
            return
        if not isinstance(value, str):
            return
        DLLSunny.SetRequestHeader(self.MessageId, create_string_buffer(key.encode("utf-8")),
                                  create_string_buffer(value.encode("utf-8")))

    def get_request_all_header(self):
        return PointerToText(DLLSunny.GetRequestAllHeader(self.MessageId))

    def get_request_header(self, key):
        if not isinstance(key, str):
            return ""
        return PointerToText(
            DLLSunny.GetRequestHeader(self.MessageId, create_string_buffer(key.encode("utf-8"))))

    def delete_request_header(self, key):
        if not isinstance(key, str):
            return
        DLLSunny.DelRequestHeader(self.MessageId, create_string_buffer(key.encode("utf-8")))

    def delete_request_all_header(self):
        h = self.get_request_all_header()
        a = h.split("\r\n")
        for item in a:
            my_list2 = item.split(":")
            if len(my_list2) >= 1:
                name = my_list2[0]
                DLLSunny.DelRequestHeader(self.MessageId, create_string_buffer(name.encode("utf-8")))

    def update_request_all_cookie(self, value):
        """ 设置请求全部Cookies 例如 a=1;b=2;c=3 """
        if not isinstance(value, str):
            return
        DLLSunny.SetRequestAllCookie(self.MessageId, create_string_buffer(value.encode("utf-8")))

    def modify_request_cookie(self, key, value):
        """
        若本身无指定的协议头，即为新增，若有则为修改
        """
        if not isinstance(key, str):
            return
        if not isinstance(value, str):
            return
        DLLSunny.SetRequestCookie(self.MessageId, create_string_buffer(key.encode("utf-8")),
                                  create_string_buffer(value.encode("utf-8")))

    def get_request_all_cookie(self):
        return PointerToText(DLLSunny.GetRequestALLCookie(self.MessageId))

    def get_request_cookie(self, key):
        if not isinstance(key, str):
            return ""
        ptr = DLLSunny.GetRequestCookie(self.MessageId, create_string_buffer(key.encode("utf-8")))
        m = PointerToText(ptr)
        return m

    def get_cookie_not_contain_key(self, key):
        if not isinstance(key, str):
            return ""
        ptr = DLLSunny.GetRequestCookie(self.MessageId, create_string_buffer(key.encode("utf-8")))
        a = PointerToText(ptr)
        return a.replace(key + "=", "").replace(";", "").strip()

    def get_requestbody_len(self):
        return PtrToInt(DLLSunny.GetRequestBodyLen(self.MessageId))

    def get_postform_str(self):
        try:
            return self.get_postform_bytes().decode("gbk")
        except:
            return self.get_postform_bytes().decode("utf-8")

    def get_postform_bytes(self):
        ptr = DLLSunny.GetRequestBody(self.MessageId)
        m = PtrToByte(ptr, 0, self. get_requestbody_len())
        DLLSunny.Free(ptr) # 释放Sunny的指针,只要是Sunny返回的bytes 或 string 都需要释放指针
        return m


# http 响应操作类
class SunnyResponse:
    def __init__(self, _MessageId):
        self.MessageId = _MessageId

    def get_responsebody_text(self):
        return PointerToText(DLLSunny.GetResponseBody(self.MessageId))

    def get_response_header(self, header_key):
        if not isinstance(header_key, str):
            return ""
        m=create_string_buffer(header_key.encode("utf-8"))
        return PointerToText(DLLSunny.GetResponseHeader(self.MessageId, m))

    def get_response_all_header(self):
        return PointerToText(DLLSunny.GetResponseAllHeader(self.MessageId))

    def delete_response_all_header(self):
        h = self.get_response_all_header()
        a = h.split("\r\n")
        for inm in a:
            ar = inm.split(":")
            if len(ar) >= 1:
                self.delete_response_header(ar[0])

    def delete_response_header(self, header_key):
        if not isinstance(header_key, str):
            return
        DLLSunny.DelResponseHeader(self.MessageId, create_string_buffer(header_key.encode("utf-8")))

    def update_response_header(self, key, value):
        if not isinstance(key, str):
            return
        if not isinstance(value, str):
            return
        DLLSunny.SetResponseHeader(self.MessageId, create_string_buffer(key.encode("utf-8")),
                                   create_string_buffer(value.encode("utf-8")))

    def update_response_headers(self, new_headers):
        if not isinstance(new_headers, str):
            return
        DLLSunny.SetResponseAllHeader(self.MessageId, create_string_buffer(new_headers.encode("utf-8")))

    def update_response_status(self, Status):
        if not isinstance(Status, int):
            return
        if Status <= 0:
            DLLSunny.SetResponseStatus(self.MessageId, 200)
            return
        DLLSunny.SetResponseStatus(self.MessageId, Status)

    def get_response_status(self):
        return PtrToInt(DLLSunny.GetResponseStatusCode(self.MessageId))

    def get_response_status_for_text(self):
        res = PointerToText(DLLSunny.GetResponseStatus(self.MessageId))
        a = res.split(" ")
        print(res)
        if len(a) > 1:
            del a[0]
            return " ".join(a).strip()
        return ""

    def get_responsebody_len(self):
        ptr=DLLSunny.GetResponseBodyLen(self.MessageId)
        m = PtrToInt(ptr)
        return m

    def get_responsebody(self):
        ptr = DLLSunny.GetResponseBody(self.MessageId)
        m =  PtrToByte(ptr, 0, self.get_responsebody_len())
        DLLSunny.Free(ptr) # 释放Sunny的指针,只要是Sunny返回的bytes 或 string 都需要释放指针
        return  m

    def modify_response_arrs(self, new_response_arrs):
        if not isinstance(new_response_arrs, bytes):
            return
        DLLSunny.SetResponseData(self.MessageId, new_response_arrs, len(new_response_arrs))

    def modify_response(self, new_response):
        if not isinstance(new_response, str):
            return
        try:
            self.modify_response_arrs(new_response.encode("utf-8"))
        except:
            self.modify_response_arrs(new_response.encode("gbk"))


# http 操作类
class Sunny:
    request_sunny = None
    """ HTTP/HTTPS 请求操作对象 """
    response_sunny = None
    """ HTTP/HTTPS 响应操作对象 """
    origin_request_ip = ""
    """ HTTP/HTTPS 发起请求的客户端IP """

    def __init__(self, MessageId):
        self.request_sunny = SunnyRequest(MessageId)
        self.response_sunny = SunnyResponse(MessageId)
        self.origin_request_ip = PointerToText(DLLSunny.GetRequestClientIp(MessageId))
