import time

import Sunny as SyNet


def BytesToStr(b):
    """ 将字节数组转为字符串 """
    try:
        return b.decode('utf-8')
    except:
        return b.decode('gbk')


def replace_bytes(byte_array, old_bytes, new_bytes):
    """ 字节数组替换 """
    start_pos = byte_array.find(old_bytes)
    if start_pos == -1:
        # 如果需要替换的字节数组不存在，返回原始字节数组
        return byte_array
    end_pos = start_pos + len(old_bytes)
    new_byte_array = bytearray(byte_array)
    new_byte_array[start_pos:end_pos] = new_bytes
    return new_byte_array


# ↓↓↓↓ 这里是回调函数 ↓↓↓↓
class Callback:
    Http_消息类型_发起请求 = 1
    Http_消息类型_请求完成 = 2
    Http_消息类型_请求失败 = 3

    def Http(SunnyContext, 请求唯一ID, MessageId, 消息类型, 请求方式, 请求地址, 错误信息, pid):
        """ HTTP / HTTPS 回调地址 """
        """ 
        SunnyContext      [Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的]  [ int 类型]
        请求唯一ID         [同一个请求 的发送和响应 唯一ID一致]                      [ int 类型]
        MessageId         [同一个请求 的发送和响应 MessageId不一致]                 [ int 类型]
        消息类型           [参考 Http_消息类型_* ]                                [ int 类型]
        请求方式           [请求方式 例如POST GET PUT ]                           [ 字节数组 类型]   自己转换为str 类型
        请求地址           [请求的URL]                                           [ 字节数组 类型]   自己转换为str 类型
        错误信息           [如果消息类型 =  请求失败 错误信息=请求错误的原因]           [ 字节数组 类型]   自己转换为str 类型
        pid              [进程PID 若等于0 表示通过代理远程请求 无进程PID]               [ int 类型]
        """

        # 获取到SunnyHTTP请求对象
        SyHTTP = SyNet.MessageIdToSunny(MessageId)
        请求来源 = SyHTTP.请求来源IP
        # ↓↓↓↓ 以下是简单示例 ↓↓↓↓
        if 消息类型 == Callback.Http_消息类型_发起请求:
            # 避免返回数据是压缩的，有时候尽管你这里删除了压缩标记，返回数据依旧是压缩的,就需要你自己根据返回协议头中的压缩方式，自己手动解压数据
            SyHTTP.请求.删除压缩标记()
            print("请求来源=" + 请求来源 + " 收到 " + BytesToStr(请求方式) + " 请求：URL是：" + BytesToStr(请求地址))
            if 请求方式 == b"POST":
                # 获取到POST提交的数据
                POST数据 = SyHTTP.请求.取POST数据_字符串()
                print("POST数据是：" + POST数据)
                # 按照字符串形式替换POST提交数据
                """ 
                POST数据 = SyHTTP.请求.取POST数据_字符串() 
                # 替换数据中的123456替换为654321
                POST数据 = POST数据.replace("123456", "654321")
                SyHTTP.请求.修改Body_字符串(POST数据)
                """
                # 按照字节数组形式替换POST提交数据
                """ 
                POST数据 = SyHTTP.请求.取POST数据_字节数组()
                # 替换数据中的123456替换为654321
                POST数据 = replace_bytes(POST数据, b"123456", b"654321")
                SyHTTP.请求.修改Body_字节数组(POST数据)
                """
            # 修改请求地址
            """ SyHTTP.请求.修改Url("https://baidu.com") """
            # 其他操作
            """ SyHTTP.请求. """
            pass
        elif 消息类型 == Callback.Http_消息类型_请求完成:
            """ 获取响应数据 """
            # 先检查数据是不是压缩的，如果是压缩的先解压
            Encoding = SyHTTP.响应.取协议头("Content-Encoding").lower()
            if Encoding == "gzip":
                SyHTTP.响应.删除协议头_单条("Content-Encoding")
                Body = SyHTTP.响应.取响应Body()
                Body = SyNet.Gzip解压缩(Body)
                if len(Body) > 0:
                    SyHTTP.响应.修改响应内容_字节数组(Body)
            elif Encoding == "br":
                SyHTTP.响应.删除协议头_单条("Content-Encoding")
                Body = SyHTTP.响应.取响应Body()
                Body = SyNet.Br解压缩(Body)
                if len(Body) > 0:
                    SyHTTP.响应.修改响应内容_字节数组(Body)
            elif Encoding == "deflate":
                SyHTTP.响应.删除协议头_单条("Content-Encoding")
                Body = SyHTTP.响应.取响应Body()
                Body = SyNet.Deflate解压缩(Body)
                if len(Body) > 0:
                    SyHTTP.响应.修改响应内容_字节数组(Body)
            # 然后再获取数据 操作
            # SyHTTP.响应.取响应文本()
            # SyHTTP.响应.取响应Body()
            """ 要修改响应数据请参考 修改提交的POST数据 """
            # 其他操作
            """ SyHTTP.响应. """
        elif 消息类型 == Callback.Http_消息类型_请求失败:
            err = BytesToStr(错误信息)
            print(BytesToStr(请求地址) + " : 请求错误 :" + err)
            pass

    TCP_消息类型_连接成功 = 0
    TCP_消息类型_发送数据 = 1
    TCP_消息类型_收到数据 = 2
    TCP_消息类型_断开连接 = 3
    TCP_消息类型_即将连接 = 4

    def Tcp(SunnyContext, 来源地址, 远程地址, 消息类型, MessageId, 数据指针, 数据长度, 唯一ID, pid):
        """ Tcp 回调地址 """
        """ 
        SunnyContext      [Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的]      [ int 类型]
        来源地址           [由哪个地址发起的请求，例如 127.0.0.1:1234]                   [ 字节数组 类型]自己转换为str 类型
        远程地址           [远程地址，例如 8.8.8.8:1234 或 baidu.com:443]              [ 字节数组 类型]自己转换为str 类型
        消息类型           [参考 TCP_消息类型_* ]                                     [ int 类型]
        MessageId         [同一个请求 的连接/发送/响应/断开/即将连接 MessageId不一致]     [ int 类型]
        数据指针           [发送或接收的数据指针]                                       [ int 类型]  
        数据长度           [发送或接收的数据长度]                                       [ int 类型]  
        唯一ID            [同一个请求 的连接/发送/响应/断开/即将连接 唯一ID一致]            [ int 类型]
        pid              [进程PID 若等于0 表示通过代理远程请求 无进程PID]                   [ int 类型]
        """
        # 取出数据
        """ print(SyNet.Tcp_取数据(数据指针,数据长度))  """
        # 其他操作
        """ SyNet.Tcp_* """
        pass

    Sunny_UDP_消息类型_关闭 = 1
    Sunny_UDP_消息类型_发送 = 2
    Sunny_UDP_消息类型_接收 = 3

    def UDP(SunnyContext, 来源地址, 远程地址, 事件类型, MessageId, 唯一ID, pid):
        """ Tcp 回调地址 """
        """ 
        SunnyContext      [Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的]      [ int 类型]
        来源地址           [由哪个地址发起的请求，例如 127.0.0.1:1234]                   [ 字节数组 类型]自己转换为str 类型
        远程地址           [远程地址，例如 8.8.8.8:1234 或 baidu.com:443]              [ 字节数组 类型]自己转换为str 类型
        事件类型           [参考 Sunny_UDP_消息类型_* ]                               [ int 类型]
        MessageId         [同一个请求 的连接/发送/响应/断开/即将连接 MessageId不一致]     [ int 类型]
        唯一ID            [同一个请求 的连接/发送/响应/断开/即将连接 唯一ID一致]           [ int 类型]
        pid              [进程PID 若等于0 表示通过代理远程请求 无进程PID]                   [ int 类型]
        """
        if 事件类型 == Callback.Sunny_UDP_消息类型_发送:
            # 取出数据
            data = SyNet.UDP_取Body(MessageId)
            print("发送UDP", 唯一ID, data)
        elif 事件类型 == Callback.Sunny_UDP_消息类型_接收:
            # 取出数据
            data = SyNet.UDP_取Body(MessageId)
            print("接收UDP", 唯一ID, data)
        elif 事件类型 == Callback.Sunny_UDP_消息类型_关闭:
            print(" UDP 关闭", 唯一ID)
            pass

        # 其他操作
        # SyNet.UDP_取Body()
        # SyNet.UDP_修改Body()
        # SyNet.UDP_向客户端发送消息()
        # SyNet.UDP_向服务器发送消息()
        pass

    Websocket_消息类型_连接成功 = 1
    Websocket_消息类型_发送数据 = 2
    Websocket_消息类型_收到数据 = 3
    Websocket_消息类型_断开连接 = 4

    WsMessage_Text = 1
    WsMessage_Binary = 2
    WsMessage_Close = 8
    WsMessage_Ping = 9
    WsMessage_Pong = 10
    WsMessage_Invalid = -1

    def Ws(SunnyContext, 请求唯一ID, MessageId, 消息类型, 请求方式, 请求地址, pid, ws消息类型):
        """ ws / wss 回调地址 """
        """ 
        SunnyContext      [Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的]  [ int 类型]
        请求唯一ID         [同一个请求 的发送和响应 唯一ID一致]                      [ int 类型]
        MessageId         [同一个请求 的发送和响应 MessageId不一致]                 [ int 类型]
        消息类型           [参考 Websocket_消息类型_* ]                            [ int 类型]
        请求方式           [请求方式 例如POST GET PUT ]                           [ 字节数组 类型]   自己转换为str 类型
        请求地址           [请求的URL]                                           [ 字节数组 类型]   自己转换为str 类型
        pid              [进程PID 若等于0 表示通过代理远程请求 无进程PID]               [ int 类型]
        ws消息类型        [ws/wss 发送或接收的消息类型 参考   WsMessage_ ]          [ int 类型]
        """
        # 取出消息Body
        """ SyNet.ws_取Body(MessageId) """
        # 其他操作
        """ SyNet.ws_ """
        pass


print("SunnyNet DLL版本：" + SyNet.GetSunnyVersion());

# ↓↓↓↓ 使用Sunny中间件 ↓↓↓↓
Sunny = SyNet.SunnyNet()
Sunny.绑定端口(2024)
Sunny.安装证书()
# Sunny.强制客户端走TCP(True)
# Sunny.设置上游代理("http://:@127.0.0.1:2022")
# 具体操作 请查看 Callback.Http, Callback.Tcp, Callback.Ws
Sunny.绑定回调地址(Callback.Http, Callback.Tcp, Callback.Ws, Callback.UDP)
if not Sunny.启动():
    print("启动失败")
    print(Sunny.取错误())
    exit(0)
else:
    print("正在运行 0.0.0.0:2024")
    if not Sunny.进程代理_加载驱动():
        print("加载驱动失败，进程代理不可用(注意，需要管理员权限（请检查），win7请安装 KB3033929 补丁)")
    else:
        # 添加、删除 进程名、PID 会让目标进程断网一次
        Sunny.进程代理_添加进程名("sunny1.exe")

while True:
    time.sleep(1)

# ↓↓↓↓ 使用Sunny队列 ↓↓↓↓
"""
nm = SyNet.Queue("5556666")
nm.压入("123456")
nm.压入("1234560")
nm.压入("9999999999999999")
nm.压入("888888888888888888")
print(nm.弹出_字符串())
print(nm.弹出_字节数组())
nv = SyNet.Queue()
nv.置唯一标识("5556666")
print(nv.弹出_字符串())
print(nv.弹出_字节数组())
exit(0)
"""

# ↓↓↓↓ 使用Sunny证书管理器 ↓↓↓↓
"""
cer = SyNet.Sunny证书管理器()
cer.创建证书("baidu.com")
print(cer.导出公钥())
print(cer.导出私钥())
print(cer.导出CA证书())
exit(0)
"""
