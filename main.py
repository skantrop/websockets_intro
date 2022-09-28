import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import websockets
import asyncio
import json
import time


xdata = []
ydata = []


fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()



def update_graph():
    ax.plot(xdata, ydata)

    fig.canvas.draw()
    plt.pause(0.05)
    

update_graph()

async def main():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client: # отправляем запросы но не закрываем соединение
        while True:
            data = json.loads(await client.recv())['data']
            time_ = time.localtime(data['E']// 1000)
            time_ = f"{time_.tm_hour}:{time_.tm_min}:{time_.tm_sec}"
            # print(time_, '->', data['c'])
            xdata.append(time_)
            ydata.append(int(float(data['c'])))
            update_graph()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())