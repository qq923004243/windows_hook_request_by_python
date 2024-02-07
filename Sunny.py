import ctypes
import time
from ctypes import *
import SunnyDLL


def Base64ToHexDump(B):
    """ 传入字节数组 或 字符串 """
    v = B
    if isinstance(B, bytes):
        pass
    else:
        if isinstance(B, str):
            v = B.encode('utf-8')
        else:
            print("您传入的参数不是 字节数组 或 字符串")
            exit(1)
    return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.HexDump(v, len(v)))


def GetSunnyVersion():
    """ 获取SunnyNet DLL版本 """
    return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.GetSunnyVersion())


def tcp_modify_message(MessageId, message_class, new_message):
    """
    消息类型   【1=发送  2=接受  1=发送的消息  2=接收的消息 根据回调函数中的参数填写】
    """
    if not isinstance(MessageId, int):
        return
    if not isinstance(message_class, int):
        return
    if not isinstance(new_message, bytes):
        return
    SunnyDLL.DLLSunny.SetTcpBody(MessageId, message_class, create_string_buffer(new_message), len(new_message))


def tcp_set_agent(MessageId, agent):
    """
    给TCP请求设置S5代理。仅在TCP 即将连接时有效
    代理   【仅支持S5代理 例如 socket5://admin:123456@127.0.0.1:8888】
    """
    if not isinstance(MessageId, int):
        return
    if not isinstance(agent, str):
        return
    SunnyDLL.DLLSunny.SetTcpAgent(MessageId, create_string_buffer(agent))


def tcp_redict_connect(MessageId, new_address):
    """
    仅在TCP 即将连接时有效
    新地址   【例如“127.0.0.1:80”带上端口号】
    """
    if not isinstance(MessageId, int):
        return
    if not isinstance(new_address, str):
        return
    SunnyDLL.DLLSunny.SetTcpConnectionIP(MessageId, create_string_buffer(new_address))


def tcp_send_message(唯一id, objs, msg):
    """
    指定的TCP连接 向[服务器\客户端]主动发送数据
    发送方向      [0=向 服务器 主动发送数据 其他值 向 户端 主动发送数据 ]
    msg         [字节数组]
    返回发送成功的字节数
    """
    if not isinstance(唯一id, int):
        return 0
    if not isinstance(objs, int):
        return 0
    if not isinstance(msg, bytes):
        return 0
    if objs == 0:
        return SunnyDLL.PtrToInt(SunnyDLL.DLLSunny.TcpSendMsg(唯一id, create_string_buffer(msg), len(msg)))
    return SunnyDLL.PtrToInt(SunnyDLL.DLLSunny.TcpSendMsgClient(唯一id, create_string_buffer(msg), len(msg)))


def tcp_close_connect(tcp_id):
    """
    断开指定连接
    """
    if not isinstance(tcp_id, int):
        return False
    Ptr = SunnyDLL.DLLSunny.TcpCloseClient(tcp_id)
    return bool(Ptr)


def tcp_get_msg(data_ptr, data_len):
    """
    数据指针    [回调中的 参数]
    数据长度    [回调中的 参数]
    """
    if not isinstance(data_ptr, int):
        return bytearray()
    if not isinstance(data_len, int):
        return bytearray()
    return SunnyDLL.PtrToByte(data_ptr, 0, data_len)


def udp_get_msg(MessageId):
    """ UDP 取 接收/发送 的消息 返回字节数组 """
    if not isinstance(MessageId, int):
        return bytearray()
    Ptr = SunnyDLL.DLLSunny.GetUdpData(MessageId)
    return SunnyDLL.PointerToBytes(Ptr)


def udp_modify_msg(MessageId, 欲修改的Body):
    """ UDP 修改 接收/发送 的消息 """
    if not isinstance(MessageId, int):
        return False
    if not isinstance(欲修改的Body, bytes):
        return False
    Ptr = SunnyDLL.DLLSunny.SetUdpData(MessageId, create_string_buffer(欲修改的Body), len(欲修改的Body))
    return bool(Ptr)


def udp_send_server_msg(udp_id, msg):
    """ 指定的UDP连接 模拟客户端向服务器端主动发送数据 """
    if not isinstance(udp_id, int):
        return False
    if not isinstance(msg, bytes):
        return False
    Ptr = SunnyDLL.DLLSunny.UdpSendToServer(udp_id, create_string_buffer(msg), len(msg))
    return bool(Ptr)


def udp_send_client_msg(udp_id, msg):
    """ 指定的UDP连接 模拟客户端向服务器端主动发送数据 """
    if not isinstance(udp_id, int):
        return False
    if not isinstance(msg, bytes):
        return False
    Ptr = SunnyDLL.DLLSunny.UdpSendToClient(udp_id, create_string_buffer(msg), len(msg))
    return bool(Ptr)


def get_ws_body_length(message_id):
    """ ws、wss 取 接收/发送 的消息长度 """
    if not isinstance(message_id, int):
        return 0
    return SunnyDLL.PtrToInt(SunnyDLL.DLLSunny.GetWebsocketBodyLen(message_id))

def get_ws_body(message_id):
    #ws、wss 取 接收/发送 的消息 返回字节数组
    if not isinstance(message_id, int):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.GetWebsocketBody(message_id)
    m_result = SunnyDLL.PtrToByte(ptr, 0, get_ws_body_length(message_id))
    SunnyDLL.DLLSunny.Free(ptr)  # 释放指针
    return m_result


def modify_ws_body(message_id, new_body):
    """ ws、wss 修改 接收/发送 的消息 """
    if not isinstance(message_id, int):
        return False
    if not isinstance(new_body, bytes):
        return False
    ptr = SunnyDLL.DLLSunny.SetWebsocketBody(message_id, create_string_buffer(new_body), len(new_body))
    return bool(ptr)


def send_ws_body(unique_id, direction, message_type, body_to_send):
    """
      ws、wss主动发送消息
      发送方向    [   0=向服务器发送 其他值向客户端发送 ]
      消息类型    [   ws/wss 发送或接收的消息类型 请使用[ Sunny_WsMessage_ ] ]
      """
    if not isinstance(unique_id, int):
        return False
    if not isinstance(direction, int):
        return False
    if not isinstance(message_type, int):
        return False
    if not isinstance(body_to_send, bytes):
        return False
    if direction == 0:
        return bool(
            SunnyDLL.DLLSunny.SendWebsocketBody(unique_id, message_type, create_string_buffer(body_to_send),
                                                len(body_to_send)))
    return bool(
        SunnyDLL.DLLSunny.SendWebsocketClientBody(unique_id, message_type, create_string_buffer(body_to_send),
                                                  len(body_to_send)))

def disconnect_ws(unique_id):
    """
    断开指定连接
    """
    if not isinstance(unique_id, int):
        return False
    ptr = SunnyDLL.DLLSunny.CloseWebsocket(unique_id)
    return bool(ptr)


def add_certificate_rule(host, certificate, usage_rule):
    """
    添加证书，双向认证时使用
    Host            [如果之前设置过相同Host将会覆盖]
    使用规则          [1=发送请求时使用 2=发送及解析时使用 3=解析时使用]
    """
    if not isinstance(host, str):
        return
    if not isinstance(certificate, SunnyCertificateManager):
        return
    if not isinstance(usage_rule, int):
        return
    SunnyDLL.DLLSunny.AddHttpCertificate(create_string_buffer(bytes(host, 'utf-8')), certificate.get_certificate_context(), usage_rule)

def delete_certificate_rule(host):
    if not isinstance(host, str):
        return False
    ptr = SunnyDLL.DLLSunny.DelHttpCertificate(create_string_buffer(host))
    return bool(ptr)

def br_compress(bin):
    """ brotli Br压缩 """
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.BrCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def br_decompress(bin):
    """ brotli 解压缩 """
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.BrUnCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)

def deflate_compress(bin):
    """ (可能等同于zlib压缩) """
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.DeflateCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def deflate_decompress(bin):
    """ (可能等同于zlib解压缩) """
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.DeflateUnCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)

def gzip_compress(bin):
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.GzipCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def gzip_decompress(bin):
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.GzipUnCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def zlib_compress(bin):
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.ZlibCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def zlib_decompress(bin):
    if not isinstance(bin, bytes):
        return bytearray()
    ptr = SunnyDLL.DLLSunny.ZlibUnCompress(create_string_buffer(bin), len(bin))
    return SunnyDLL.PointerToBytes(ptr)


def pb_to_pb_json(pb_byte_array_data):
    if not isinstance(pb_byte_array_data, bytes):
        return ""
    return SunnyDLL.DLLSunny.PbToJson(create_string_buffer(pb_byte_array_data), len(pb_byte_array_data))


def pb_json_to_pb(pb_json_string):
    if not isinstance(pb_json_string, str):
        return bytearray()
    try:
        d = pb_json_string.encode("gbk")
    except:
        d = pb_json_string.encode("utf-8")
    return SunnyDLL.PointerToBytes(SunnyDLL.DLLSunny.JsonToPB(create_string_buffer(d), len(d)))

class Queue:
    """ Sunny 队列 """

    def __init__(self, unique_id=""):
        self._id = ""
        if isinstance(unique_id, str):
            self.create_queue(unique_id)

    def is_empty(self):
        if self._id == "":
            return True
        return bool(SunnyDLL.DLLSunny.QueueIsEmpty(create_string_buffer(self._id.encode("utf-8"))))

    def destroy(self):
        if self._id == "":
            return
        SunnyDLL.DLLSunny.QueueRelease(create_string_buffer(self._id.encode("utf-8")))

    def create_queue(self, unique_id):
        if not isinstance(unique_id, str):
            return
        self._id = unique_id
        SunnyDLL.DLLSunny.CreateQueue(create_string_buffer(self._id.encode("utf-8")))

    def set_unique_id(self, unique_id):
        if not isinstance(unique_id, str):
            return
        self._id = unique_id

    def clear(self):
        if self._id == "":
            return
        self.destroy()
        self.create_queue(self._id)

    def get_queue_length(self):
        if self._id == "":
            return
        return SunnyDLL.PtrToInt(SunnyDLL.DLLSunny.QueueLength(create_string_buffer(self._id.encode("utf-8"))))

    def push(self, data):
        """ Data 可以是字节数组 也可以字符串 """
        if self._id == "":
            return
        if isinstance(data, bytes):
            SunnyDLL.DLLSunny.QueuePush(create_string_buffer(self._id.encode("utf-8")), create_string_buffer(data),
                                        len(data))
            return
        if isinstance(data, str):
            d = data.encode("utf-8")
            SunnyDLL.DLLSunny.QueuePush(create_string_buffer(self._id.encode("utf-8")), create_string_buffer(d), len(d))
            return

    def pop_byte_array(self):
        if self._id == "":
            return bytearray()
        p = SunnyDLL.DLLSunny.QueuePull(create_string_buffer(self._id.encode("utf-8")))
        return SunnyDLL.PointerToBytes(p)

    def pop_string(self):
        sb = self.pop_byte_array()
        try:
            return sb.decode("utf-8")
        except:
            return sb.decode("gbk")


class SunnyCertificateManager:
    SSL_ClientAuth_NoClientCert = 0
    """ 表示在握手过程中不应该请求客户端证书，并且如果发送了任何证书，它们将不会被验证。 """
    SSL_ClientAuth_RequestClientCert = 1
    """     表示应该在握手过程中请求客户端证书，但不要求客户端发送任何证书。     """
    SSL_ClientAuth_RequireAnyClientCert = 2
    """     表示在握手过程中应该请求客户端证书，并且客户端至少需要发送一个证书，但该证书不需要有效。 """
    SSL_ClientAuth_VerifyClientCertIfGiven = 3
    """     表示应该在握手过程中请求客户端证书，但不要求客户端发送证书。如果客户端发送了一个证书，它就需要是有效的。 """
    SSL_ClientAuth_RequireAndVerifyClientCert = 4
    """     表示握手时需要请求客户端证书，客户端至少需要发送一个有效的证书。 """

    def __init__(self):
        self.CertificateContext = SunnyDLL.DLLSunny.CreateCertificate()
        self.skip_host_verification(True)

    def __del__(self):
        SunnyDLL.DLLSunny.RemoveCertificate(self.CertificateContext)


    def skip_host_verification(self, skip):
        """ 请先载入证书 默认真 """
        SunnyDLL.DLLSunny.SetInsecureSkipVerify(self.CertificateContext, skip)

    def recreate(self):
        if self.CertificateContext > 0:
            SunnyDLL.DLLSunny.RemoveCertificate(self.CertificateContext)
        self.CertificateContext = SunnyDLL.DLLSunny.CreateCertificate()
        self.skip_host_verification(True)

    def load_p12_certificate(self, p12_certificate_path, p12_certificate_password):

        SunnyDLL.DLLSunny.LoadP12Certificate(self.CertificateContext,
                                             create_string_buffer(p12_certificate_path.encode("utf-8")),
                                             create_string_buffer(p12_certificate_password.encode("utf-8")))
    def _load_x509_key_pair(self, cert_file_path, key_file_path):
         """ 从一对文件读取和解析一个公钥/私钥对。
         文件必须包含PEM编码的数据。证书文件可以在叶证书之后包含中间证书，形成证书链。
          默认 跳过主机验证 """
         SunnyDLL.DLLSunny.LoadX509KeyPair(self.CertificateContext, create_string_buffer(cert_file_path.encode("utf-8")),
                                          create_string_buffer(key_file_path.encode("utf-8")))

    def _load_x509_certificate(self, host, cer_file_content, key_file_content):
        """ 默认 跳过主机验证 """
        SunnyDLL.DLLSunny.LoadX509Certificate(self.CertificateContext, create_string_buffer(host.encode("utf-8")),
                                              create_string_buffer(cer_file_content.encode("utf-8")),
                                              create_string_buffer(key_file_content.encode("utf-8")))


    def set_server_name(self, name):
         #请先载入证书 设置的证书上的主机名
        SunnyDLL.DLLSunny.SetServerName(self.CertificateContext, create_string_buffer(name.encode("utf-8")))

    def get_server_name(self):
        """ 请先载入证书 返回的证书上的主机名 """
        return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.GetServerName(self.CertificateContext))

    def get_certificate_context(self):
        return self.CertificateContext

    def add_client_trusted_certificate_file(self, file_path):
        SunnyDLL.DLLSunny.AddCertPoolPath(self.CertificateContext, create_string_buffer(file_path.encode("utf-8")))

    def add_client_trusted_certificate_text(self, trusted_certificate_file_content):
        SunnyDLL.DLLSunny.AddCertPoolText(self.CertificateContext,
                                          create_string_buffer(trusted_certificate_file_content.encode("utf-8")))


    def set_client_authentication_mode(self, mode=0):
        """  0-4 使用  SSL_ClientAuth_ """
        SunnyDLL.DLLSunny.AddClientAuth(self.CertificateContext, mode)

    def create_certificate(self, certificate_domain, certificate_country="CN", certificate_company_name="Sunny",
                           certificate_department_name="Sunny",
                           certificate_issuing_organization_province="BeiJing",
                           certificate_issuing_organization_city="BeiJing", expiration_time=3650):
        """
               证书所属的国家              默认      CN
               证书存放的公司名称           默认      Sunny
               证书所属的部门名称           默认      Sunny
               证书签发机构所在省           默认      BeiJing
               证书签发机构所在市           默认      BeiJing
               到期时间                   默认      3650天
               """
        r = SunnyDLL.DLLSunny.CreateCA(self.CertificateContext,
                                       create_string_buffer(certificate_country.encode("utf-8")),
                                       create_string_buffer(certificate_company_name.encode("utf-8")),
                                       create_string_buffer(certificate_department_name.encode("utf-8")),
                                       create_string_buffer(certificate_issuing_organization_province.encode("utf-8")),
                                       create_string_buffer(certificate_domain.encode("utf-8")),
                                       create_string_buffer(certificate_issuing_organization_city.encode("utf-8")),
                                       2048, expiration_time)
        return bool(r)


    def _Replace(self, str):
        return str.replace("\r", "").replace("\n", "\r\n")

    def export_public_key(self):
        return self._Replace(SunnyDLL.PointerToText(SunnyDLL.DLLSunny.ExportPub(self.CertificateContext)))

    def export_private_key(self):
        return self._Replace(SunnyDLL.PointerToText(SunnyDLL.DLLSunny.ExportKEY(self.CertificateContext)))

    def export_ca_certificate(self):
        return self._Replace(SunnyDLL.PointerToText(SunnyDLL.DLLSunny.ExportCA(self.CertificateContext)))

    def get_common_name(self):
        return self._Replace(SunnyDLL.PointerToText(SunnyDLL.DLLSunny.GetCommonName(self.CertificateContext)))

    def export_p12_file(self, save_path, p12_password):
        r = SunnyDLL.DLLSunny.ExportP12(self.CertificateContext, create_string_buffer(
            save_path.encode("utf-8")), create_string_buffer(p12_password.encode("utf-8")))
        return bool(r)


class SunnyNet:
    def __init__(self):
        """ 创建Sunny中间件对象,可创建多个 """
        self.WsCallback = None
        self.TcpCallback = None
        self.HttpCallback = None
        self.Context = SunnyDLL.DLLSunny.CreateSunnyNet()

    def __del__(self):
        """ 释放SunnyNet """
        SunnyDLL.DLLSunny.ReleaseSunnyNet(self.Context)


    def get_sunny_net_context(self):
        """ Sunny中间件可创建多个 由这个参数判断是哪个Sunny回调过来的 """
        return self.Context

    def export_certificate(self):
        """ 导出已经设置的证书 """
        return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.ExportCert(self.Context))

    def force_client_to_use_tcp(self, open):
        """ 开启后SunnyNet不再对数据进行解密直接使用TCP发送，HTTPS的数据无法解码 """
        if isinstance(open, bool):
            SunnyDLL.DLLSunny.SunnyNetMustTcp(self.Context, open)

    def enable_identity_verification_mode(self, open):
        """ 开启后客户端只能使用S5代理，并且输入设置的账号密码"""
        if isinstance(open, bool):
            SunnyDLL.DLLSunny.SunnyNetVerifyUser(self.Context, open)

    def identity_verification_mode_add_user(self, m_user, m_pass):
        """ 开启 身份验证模式 后 添加用户名 """
        if isinstance(m_user, str) and isinstance(m_pass, str):
            print(bool(SunnyDLL.DLLSunny.SunnyNetSocket5AddUser(self.Context, create_string_buffer(m_user.encode("utf-8")), create_string_buffer(m_pass.encode("utf-8")))))

    def identity_verification_mode_delete_user(self, m_user):
        """ 开启 身份验证模式 后 删除用户名 """
        if isinstance(m_user, str):
            SunnyDLL.DLLSunny.SunnyNetSocket5DelUser(self.Context, m_user)

    def identity_verification_mode_get_authorized_identity(self, unique_request_id):
      #开启身份验证模式后 获取授权的S5账号,注意UDP请求无法获取到授权的s5账号 """
        if isinstance(unique_request_id, int):
            return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.SunnyNetGetSocket5User(unique_request_id))

    def bind_port(self, port):
       #在启动之前调用 """
        if isinstance(port, int):
            SunnyDLL.DLLSunny.SunnyNetSetPort(self.Context, port)

    def start(self):
        """ 启动前先绑定端口 """
        return bool(SunnyDLL.DLLSunny.SunnyNetStart(self.Context))

    def close_ie_proxy(self):
        """ 取消已经设置的IE代理 """
        SunnyDLL.DLLSunny.SetIeProxy(self.Context, True)

    def stop_proxy(self):
        """ 停止中间件【停止的同时将会自动关闭IE代理】 """
        self.关闭IE代理()
        SunnyDLL.DLLSunny.SunnyNetClose(self.Context)

    def bind_callback_address(self, HTTP_callback_address, TCP_callback_address, ws_callback_address,
                              UDP_callback_address):
        """ 开启 身份验证模式 后 删除用户名  """
        self.HttpCallback = 0
        self.TcpCallback = 0
        self.WsCallback = 0
        self.UDPCallback = 0
        if callable(HTTP_callback_address):
            self.HttpCallback = SunnyDLL.HttpCallback(HTTP_callback_address)
        if callable(TCP_callback_address):
            self.TcpCallback = SunnyDLL.TcpCallback(TCP_callback_address)
        if callable(ws_callback_address):
            self.WsCallback = SunnyDLL.WsCallback(ws_callback_address)
        if callable(UDP_callback_address):
            self.UDPCallback = SunnyDLL.UDPCallback(UDP_callback_address)
        SunnyDLL.DLLSunny.SunnyNetSetCallback(self.Context, self.HttpCallback, self.TcpCallback, self.WsCallback,
                                              self.UDPCallback)

    def set_custom_ca_certificate(self, certificate_manager):
        """ 导入自己的证书 """
        if isinstance(certificate_manager, SunnyCertificateManager):
            r = SunnyDLL.DLLSunny.SunnyNetSetCert(self.Context, certificate_manager.get_certificate_context())
            return bool(r)
        else:
            print("设置自定义CA证书 传入参数错误")
            exit(0)
    def install_certificate(self):
        """ 启动后调用,将中间件的证书安装到系统内 返回安装结果文本，若失败需要手动安装 """
        err = SunnyDLL.PointerToText(SunnyDLL.DLLSunny.SunnyNetInstallCert(self.Context))
        if "添加到存储" in err:
            return True
        if "已经在存储中" in err:
            return True
        return False

    def get_error(self):
        """ 获取中间件启动时的错误信息 """
        return SunnyDLL.PointerToText(SunnyDLL.DLLSunny.SunnyNetError(self.Context))

    def set_upstream_proxy(self, proxy):
        """
        设置上游代理 仅支持S5代理 或 http代理
        仅支持Socket5和http 例如 socket5://admin:123456@127.0.0.1:8888 或 http://admin:123456@127.0.0.1:8888
        """
        if not isinstance(proxy, str):
            return False
        return bool(SunnyDLL.DLLSunny.SetGlobalProxy(self.Context, create_string_buffer(proxy.encode("utf-8"))))

    def set_upstream_proxy_usage_rule(self, rule):
        """
        默认全部使用上游代理(只要设置了上游代理)
        输入Host不带端口号;在此规则内的不使用上游代理 多个用";"分号或换行分割 例如"127.0.0.1;192.168.*.*"地址不使用上游代理
        """
        if not isinstance(rule, str):
            return False
        return bool(SunnyDLL.DLLSunny.CompileProxyRegexp(self.Context, create_string_buffer(rule.encode("utf-8"))))

    def set_force_tcp_rule(self, rule):
        """
        设置强制走TCP规则,如果 打开了全部强制走TCP状态,本功能则无效
        输入Host不带端口号;在此规则内 多个用";"分号或换行分割 例如"127.0.0.1;192.168.*.*"强制使用TCP
        """
        if not isinstance(rule, str):
            return False
        return bool(SunnyDLL.DLLSunny.SetMustTcpRegexp(self.Context, create_string_buffer(rule.encode("utf-8"))))

    def set_ie_proxy(self):
        """
        设置当前绑定的端口号为当前IE代理 设置前请先绑定端口
        """
        SunnyDLL.DLLSunny.SetIeProxy(self.Context, False)

    def process_proxy_load_driver(self):
        """
        只允许一个中间件服务 加载驱动,使用前，请先启动Sunny中间件
        """
        return bool(SunnyDLL.DLLSunny.StartProcess(self.Context))

    def process_proxy_add_process_name(self, name):
        """
        添加指定的进程名进行捕获[需调用 启动进程代理 后生效]
        name = 进程名 例如 e.exe
		会强制断开此进程已经连接的TCP连接
        """
        if not isinstance(name, str):
            return
        SunnyDLL.DLLSunny.ProcessAddName(self.Context, create_string_buffer(name.encode("utf-8")))

    def process_proxy_delete_process_name(self, name):
        """
        删除指定的进程名 停止捕获[需调用 启动进程代理 后生效]
        name = 进程名 例如 e.exe
		会强制断开此进程已经连接的TCP连接
        """
        if not isinstance(name, str):
            return
        SunnyDLL.DLLSunny.ProcessDelName(self.Context, create_string_buffer(name.encode("utf-8")))

    def rocess_proxy_add_pid(self, pid):
        """
        添加指定的进程PID进行捕获[需调用 启动进程代理 后生效]
        pid = 进程PID 例如 11223
		会强制断开此进程已经连接的TCP连接
        """
        if not isinstance(pid, int):
            return
        SunnyDLL.DLLSunny.ProcessAddPid(self.Context, pid)

    def process_proxy_delete_pid(self, pid):
        """
        删除指定的进程PID 停止捕获[需调用 启动进程代理 后生效]
        pid = 进程PID 例如 11223
		会强制断开此进程已经连接的TCP连接
        """
        if not isinstance(pid, int):
            return
        SunnyDLL.DLLSunny.ProcessDelPid(self.Context, pid)

    def process_proxy_set_capture_any_process(self, open):
        """
        开启后 所有进程将会被捕获[需调用 启动进程代理 后生效]
        无论开启还是关闭 都会将之前添加的进程名或PID清空
		会强制断开所有进程已经连接的TCP连接
        """
        if not isinstance(open, bool):
            return
        SunnyDLL.DLLSunny.ProcessALLName(self.Context, open)

    def process_proxy_delete_all(self):
        """
        删除已设置的所有PID,进程名 [需调用 启动进程代理 后生效]
		会强制断开所有进程已经连接的TCP连接
        """
        SunnyDLL.DLLSunny.ProcessCancelAll(self.Context)


def MessageIdToSunny(MessageId):
    if not isinstance(MessageId, int):
        print("MessageIdToSunny 传入参数错误")
        exit(0)
    return SunnyDLL.Sunny(MessageId)
