import json
import time

import Sunny as SyNet
from urllib.parse import urlparse, parse_qs

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

def parse_post_data(post_data):
    lines = post_data.split('\n')
    formhead = lines[0]
    data_dict = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if 'name=' in line:
            key_temp = line.split('=')[1].replace('"', '').replace('\r', '')
            value_temp = lines[i+2].replace('\r', '')
            print(key_temp, value_temp)
            data_dict[key_temp] = value_temp
            i += 3
        else:
            i += 1
    return formhead, data_dict
# ↓↓↓↓ 这里是回调函数 ↓↓↓↓
class Callback:
    http_flag_start_request = 1
    http_flag_success_request = 2
    http_flag_fail_request = 3

    def Http(SunnyContext, session_id, message_id, message_class, request_class, request_url, error_info, pid):
        """ HTTP / HTTPS 回调地址 """
        """ 
        SunnyContext      [Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的]  [ int 类型]
        请求唯一ID    SessionId     [同一个请求 的发送和响应 唯一ID一致]                      [ int 类型]
        MessageId         [同一个请求 的发送和响应 MessageId不一致]                 [ int 类型]
        消息类型     message_class      [参考 Http_消息类型_* ]                                [ int 类型]
        请求方式     request_class      [请求方式 例如POST GET PUT ]                           [ 字节数组 类型]   自己转换为str 类型
        请求地址       request_url    [请求的URL]                                           [ 字节数组 类型]   自己转换为str 类型
        错误信息  error_info         [如果消息类型 =  请求失败 错误信息=请求错误的原因]           [ 字节数组 类型]   自己转换为str 类型
        pid              [进程PID 若等于0 表示通过代理远程请求 无进程PID]               [ int 类型]
        """

        # 获取到SunnyHTTP请求对象
        SyHTTP = SyNet.MessageIdToSunny(message_id)
        origin_request_ip = SyHTTP.origin_request_ip
        # ↓↓↓↓ 以下是简单示例 ↓↓↓↓
        if message_class == Callback.http_flag_start_request:
            # 避免返回数据是压缩的，有时候尽管你这里删除了压缩标记，返回数据依旧是压缩的,就需要你自己根据返回协议头中的压缩方式，自己手动解压数据
            SyHTTP.request_sunny.delete_gzipflag()
            print("请求来源=" + origin_request_ip + " 收到 " + BytesToStr(request_class) + " 请求：URL是：" + BytesToStr(request_url))
            if request_class == b"POST":
                # 获取到POST提交的数据# 按照字符串形式替换POST提交数据
                post_form = SyHTTP.request_sunny.get_postform_str()
                SyHTTP.request_sunny.get_requestbody_len()
                print("POST数据是：" + post_form)
                form_head, param_dict = parse_post_data(post_form)
                print("数据获取后")
                print(form_head)
                print(param_dict)
                #构造表单
                param_dict['name'] = 'Decade'
                modify_form = form_head + '\r\n'
                for key, value in param_dict.items():
                    modify_form += 'Content-Disposition: form-data; name="' + key + '"'+'\r\n' + value + '\r\n'
                    modify_form += form_head + '\r\n'
                modify_form = modify_form.replace('12345','98765')

                print("修改后的表单："+modify_form)

                SyHTTP.request_sunny.modify_requestbody_str(modify_form)

                # # 修改请求地址
                #SyHTTP.request_sunny.modify_url("https://baidu.com/s")
                #
                # 其他操作
                #SyHTTP.request_sunny.get_request_all_header()# 获取所有请求头
                #SyHTTP.request_sunny.get_request_header("User-Agent")# 获取请求头
                #SyHTTP.request_sunny.modify_request_header("User-Agent","Sunny")# 修改请求头
                #SyHTTP.request_sunny.delete_request_header("User-Agent")# 删除请求头
                #SyHTTP.request_sunny.get_request_cookie()# 获取请求cookie
                #SyHTTP.request_sunny.modify_request_cookie("cookie","123456")
                #SyHTTP.request_sunny.delete_request_cookie("cookie")
                #SyHTTP.request_sunny.delete_gzipflag()# 删除压缩标记
                #SyHTTP.request_sunny.set_request_outtime(2000)# 设置超时时间
                #SyHTTP.request_sunny.close_connection()# 关闭连接 拦截本次请求
            elif request_class == b"GET":
                # 获取到GET提交的数据
                get_url = BytesToStr(request_url)
                print("get数据是：" + get_url)
                parsed_url = urlparse(get_url)# 解析URL
                host = parsed_url.hostname
                path = parsed_url.path# 获取路径
                params = parse_qs(parsed_url.query) # 获取参数
                query = parsed_url.query# 获取参数
                print("host=" + host)#请求host
                print("path=" + path)#请求路径
                print("params=" + str(params))#params请求参数
                print("query=" + query)#query请求字符串
                modify_host = ["baidu.com", "www.baidu.com","192.168.250.180"]#要修改的host
                modify_path = ['/items']#要修改的请求路径
                if host in modify_host:
                    for ss in modify_path:
                        if ss in path:
                            get_url = get_url.replace("923004243","987654321")#替换923004243为这个
                            SyHTTP.request_sunny.modify_url(get_url)#修改请求地址
                # 按照字节数组形式替换POST提交数据
            # 修改请求地址
            """ SyHTTP.请求.修改Url("https://baidu.com") """
            # 其他操作
            """ SyHTTP.请求. """
            pass
        elif message_class == Callback.http_flag_success_request:
            """ 获取响应数据 """
            # 先检查数据是不是压缩的，如果是压缩的先解压
            Encoding = SyHTTP.response_sunny.get_response_header("Content-Encoding").lower()
            if Encoding == "gzip":
                SyHTTP.response_sunny.delete_response_header("Content-Encoding")
                Body = SyHTTP.response_sunny.get_responsebody()
                Body = SyNet.gzip_decompress(Body)
                if len(Body) > 0:
                    SyHTTP.response_sunny.modify_response_arrs(Body)
            elif Encoding == "br":
                SyHTTP.response_sunny.delete_response_header("Content-Encoding")
                Body = SyHTTP.response_sunny.get_responsebody()
                Body = SyNet.br_decompress(Body)
                if len(Body) > 0:
                    SyHTTP.response_sunny.modify_response_arrs(Body)
            elif Encoding == "deflate":
                SyHTTP.response_sunny.delete_response_header("Content-Encoding")
                Body = SyHTTP.response_sunny.get_responsebody()
                Body = SyNet.deflate_decompress(Body)
                if len(Body) > 0:
                    SyHTTP.response_sunny.modify_response_arrs(Body)
            print(SyHTTP.response_sunny.get_responsebody())
            print(SyHTTP.response_sunny.get_responsebody_text())
            print(SyHTTP.response_sunny.get_response_all_header())
            print(request_url)
            #可以根据请求地址进行修改
            response_dict = {"code": 200, "msg": "success","model":"tesla","price":1000000}
            SyHTTP.response_sunny.modify_response(json.dumps(response_dict))
            # 然后再获取数据 操作
            # SyHTTP.响应.取响应文本()
            # SyHTTP.响应.取响应Body()
            """ 要修改响应数据请参考 修改提交的POST数据 """
            # 其他操作
            """ SyHTTP.响应. """
        elif message_class == Callback.http_flag_fail_request:
            err = BytesToStr(error_info)
            print(BytesToStr(request_url) + " : 请求错误 :" + err)
            pass

    tcp_msg_connect_success = 0
    tcp_msg_start_send_data = 1
    tcp_msg_recv_data = 2
    tcp_msg_has_disconnect = 3
    tcp_msg_will_be_connect = 4

    def Tcp(SunnyContext, origin_host, dest_host, message_class, message_id, data_ptr, data_len, session_id, pid):
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

    udp_msg_close = 1
    udp_msg_send = 2
    udp_msg_recv = 3

    def UDP(SunnyContext, origin_host, dest_host, event_class, message_id, session_id, pid):
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
        if event_class == Callback.udp_msg_send :
            # 取出数据
            data = SyNet.udp_get_msg(message_id)
            print("发送UDP", session_id, data)
        elif event_class == Callback.udp_msg_recv:
            # 取出数据
            data = SyNet.udp_get_msg(message_id)
            print("接收UDP", session_id, data)
        elif event_class == Callback.udp_msg_close:
            print(" UDP 关闭", session_id)
            pass

        # 其他操作
        # SyNet.UDP_取Body()
        # SyNet.UDP_修改Body()
        # SyNet.UDP_向客户端发送消息()
        # SyNet.UDP_向服务器发送消息()
        pass

    websocket_connect_success = 1
    websocket_send_data = 2
    websocket_recv_data = 3
    websocket_disconnect = 4

    websocket_message_text = 1
    websocket_message_binary = 2
    websocket_message_close = 8
    websocket_message_ping = 9
    websocket_message_pong = 10
    websocket_message_invalid = -1

    def Ws(SunnyContext, session_id, message_id, message_class, requset_method, request_adrr, pid, websocket_message_class):
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
Sunny.bind_port(2024)
Sunny.install_certificate()
# Sunny.强制客户端走TCP(True)
# Sunny.设置上游代理("http://:@127.0.0.1:2022")
# 具体操作 请查看 Callback.Http, Callback.Tcp, Callback.Ws
Sunny.bind_callback_address(Callback.Http, Callback.Tcp, Callback.Ws, Callback.UDP)


if not Sunny.start():
    print("启动失败")
    print(Sunny.get_error())
    exit(0)
else:
    print("正在运行 0.0.0.0:2024")
    if not Sunny.process_proxy_load_driver():
        print("加载驱动失败，进程代理不可用(注意，需要管理员权限（请检查），win7请安装 KB3033929 补丁)")
    else:
        # 添加、删除 进程名、PID 会让目标进程断网一次
        Sunny.process_proxy_add_process_name("postman.exe")
        Sunny.process_proxy_add_process_name("qaxbrowser.exe")
        print("start postman.exe")

# ↓↓↓↓ 使用Sunny证书管理器 ↓↓↓↓

# cer = SyNet.SunnyCertificateManager()
# cer.create_ca_certificate()
# print(cer.export_public_key())
# print(cer.export_private_key())
# print(cer.export_ca_certificate())
# exit(0)
while True:
    time.sleep(1)




