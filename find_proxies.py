import asyncio
from proxybroker import Broker, Proxy

class ProxyFinder:

    def __init__(self):
        self.proxy_list = [];
    

    async def add_to_list(self,proxies):
        while True:
            proxy = await proxies.get();
            if proxy is None: break;
            self.proxy_list.append(proxy);

    def get_proxies(self):
        return self.proxy_list;

    def find_proxies(self,types, limit):
        proxies = asyncio.Queue();
        broker = Broker(proxies, verify_ssl=True);
        tasks = asyncio.gather(
                broker.find(types=types, limit=limit),
                self.add_to_list(proxies));

        loop = asyncio.get_event_loop();
        loop.run_until_complete(tasks);


def print_proxy(proxy):
    print("proxy: ", proxy);
    print("geo: ", proxy.geo);
    print("avg_resp_time: ", proxy.avg_resp_time);
    print("error rate: ", proxy.error_rate);
    print("is_working: ", proxy.is_working);
    print("host: ", proxy.host);
    print("port: ", proxy.port);
    print();

if __name__ == "__main__": 
    pfinder = ProxyFinder();

    pfinder.find_proxies(['SOCKS5'],10);
    
    proxy_list = pfinder.get_proxies();

    for proxy in proxy_list:
        print_proxy(proxy);




