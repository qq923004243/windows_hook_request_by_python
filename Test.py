import requests


def SunnyNetCreateRequest1():
    """
    [ /activity/report ]
    本函数由SunnyNet网络中间件生成
    """
    url = "https://mp-activity.csdn.net/activity/report"
    payload = "{\"pageUrl\":\"https://blog.csdn.net/weixin_43935474/article/details/121402550\",\"action\":\"pageView\",\"platform\":\"pc\"}"
    headers = {
        'sec-ch-ua-mobile': "?0",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        'Connection': "Keep-Alive",
        'Host': "mp-activity.csdn.net",
        'Referer': "https://blog.csdn.net/weixin_43935474/article/details/121402550",
        'Origin': "https://blog.csdn.net",
        'Sec-Fetch-Dest': "empty",
        'sec-ch-ua': "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        'Accept-Encoding': "gzip, deflate, br",
        'Sec-Fetch-Mode': "cors",
        'Cache-Control': "no-cache",
        'Pragma': "no-cache",
        'Content-Type': "application/json; charset=UTF-8",
        'Sec-Fetch-Site': "same-site",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'sec-ch-ua-platform': "\"Windows\"",
        'Cookie': "uuid_tt_dd=10_19878917860-1680037919178-757560; UN=qqq564998512; _ga_K2GWXDJ6YJ=GS1.1.1686925554.1.1.1686925564.50.0.0; _ga_WMYH9GC2T9=GS1.1.1690923537.1.0.1690923540.57.0.0; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19878917860-1680037919178-757560!5744*1*qqq564998512; p_uid=U010000; ssxmod_itna=GqUx0ii=eiqQwqBPqeTm4jxmw4wxRircQecCx05abeGzDAxn40iDtPPuQ7eZOlp0ixWxpDewxa4Tt4uDWenlx3PW7bWSTeDHxY=DUgiLXYD4fKGwD0eG+DD4DWfx03DoxGASpx0+kSBcu=nDAQDQ4GyDitDKkixxG3D0R=3FR6MS32xHeDSCBtrCqDMD7tD/3xT=0=DGMnW=AXM/WeDbxPntliDtqD9CjUXFeDH+MXl3L9z7DpN7Y4z/AmeW2x3KiqKQ0xQzIhieu8KYA54Drk=Q0Gv6G5yxD34mG53eD===; ssxmod_itna2=GqUx0ii=eiqQwqBPqeTm4jxmw4wxRircQecDn9EBvxDs+W8DLirT294n4hlvjIt3QmhhKhGl3IoAXeKcgnyAGRQlQH=LtAQD8a8on=BMbjlCCc20hTyaTg2C83SjjA20qfFKkQxTGK86oRiln9D43psg0GaWB7Cv1pNtSyQgYBDQl487oaHtpu7We9ii9+N4SvTc1nwRYALjbwsyiuT41MWtagdsxrdFhpQqBR0Fcc0qdmtW4ItIzPXHP1OTyFc21Z+OLTrvIuynSPBH5Hcd+IwoL/BQb9++yFrdstlmvKO2ppMlNA//RrQYQX87hDahb35ox/B1TODw2hcRD4w=U+41R+X7eRiWwqw4TeBRF7oNNfKgGPsW7/GxvDDwg4DjKDeuD4D=; c_segment=8; ins_first_time=1698670855027; x_inscode_token=; SESSION=4896b8b8-6a66-4c93-a8e0-c6ae1ab71bc6; UserName=qqq564998512; UserInfo=34163bcbabb54222a692a9114691e768; UserToken=34163bcbabb54222a692a9114691e768; UserNick=qqq564998512; AU=BF5; BT=1698737652536; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22qqq564998512%22%2C%22scope%22%3A1%7D%7D; __gpi=UID=00000c737cf8c6d5:T=1698242611:RT=1699254581:S=ALNI_MbjmKWHaKCwzvJgWfufHVT8IlLXmw; log_Id_pv=609; log_Id_view=2883; log_Id_click=368; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1701263808; dc_sid=d83036b4bfc4c725c59ef4fe265eb0ca; c_pref=https%3A//www.baidu.com/link; is_advert=1; firstDie=1; SidecHatdocDescBoxNum=true; c_ref=https%3A//www.google.com/; c_first_ref=www.google.com; c_first_page=https%3A//blog.csdn.net/weixin_43935474/article/details/121402550; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1702048817; _ga=GA1.2.485460145.1680037919; _gid=GA1.2.1879601995.1702048818; __gads=ID=3259962bbb136e73-22c1b9bca9e400fd:T=1698242611:RT=1702048816:S=ALNI_MZNNDj0FF24ntUAO7nZnkvlGCt1Ig; FCNEC=%5B%5B%22AKsRol-836JIsd-he73-HG3Z7ejR2qjPNL__oEAX0vNVmYYnSXJ-g2ivL_FIMC4IYFxXexFOauFG5njLCdW4Yg433XxhTGFpaJpu0wZaKml-gn5sApmYTbNQs12S0b34Ei1pBTj68SwQoUYygFN60XRBJqhzuHXG2A%3D%3D%22%5D%5D; dc_session_id=10_1702051691878.615545; _ga_7W1N0GEY1P=GS1.1.1702051693.83.0.1702051693.60.0.0; c_dsid=11_1702051694929.712954; c_page_id=default; dc_tos=s5cvhq; creativeSetApiNew=%7B%22toolbarImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20231011044944.png%22%2C%22publishSuccessImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20231011045003.png%22%2C%22articleNum%22%3A0%2C%22type%22%3A0%2C%22oldUser%22%3Afalse%2C%22useSeven%22%3Atrue%2C%22oldFullVersion%22%3Afalse%2C%22userName%22%3A%22qqq564998512%22%7D",

    }
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)





SunnyNetCreateRequest1()