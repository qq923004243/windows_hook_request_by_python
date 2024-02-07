import aiohttp
import asyncio

async def send_request(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.text()

async def main():
    url = 'http://192.168.250.180:9230/uploadfile/'  # 你的FastAPI应用的URL和端口
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(16):
            with open(f'2.jpg', 'rb') as f:  # 假设你有16个名为'image_0.jpg'到'image_15.jpg'的图片文件
                data = f.read()
            tasks.append(send_request(session, url, {'file':data}))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

# 运行主函数
asyncio.run(main())