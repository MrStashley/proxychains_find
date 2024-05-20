# usage proxychains_find.py -c <chain type> 
# options: 
# --find : find proxies
#   -t / --types json list of some combination of { HTTP, HTTPS, SOCKS4, SOCKS5 }
#   -l / --limit limit for find command
#   -r / --response-time cap on response time
# --tor use tor
# -c / --chain-type <chain type>, either dynamic, strict or random
#   --len chain-len if random chain is specified
# -p --proxy-dns <bool> whether or not to proxy dns, true by default
# -q --quiet-mode <bool> whether or not to use quiet mode, false by default 

import sys
from find_proxies import ProxyFinder

RANDOM_CHAIN = 0
DYNAMIC_CHAIN = 1
STRICT_CHAIN = 2

def write_to_conf(chain_type, chain_len = 0, quiet_mode = False, proxy_dns = True, use_tor = False, proxy_list = []):
    dyn_chain_line = "#dynamic_chain";
    strict_chain_line = "#strict_chain";
    random_chain_line = "#random_chain";
    chain_len_line = "#chain_len = 2";
    quiet_mode_line = "#quiet_mode"
    proxy_dns_line = "#proxy_dns";
    use_tor_line = "#socks4 127.0.0.1 9050 ";
    proxy_list_line = "";

    if(chain_type == RANDOM_CHAIN):
        random_chain_line = "random_chain";
        chain_len_line = "chain_len = " + chain_len;
    elif (chain_type == STRICT_CHAIN):
        strict_chain_line = "strict_chain";
    elif (chain_type == DYNAMIC_CHAIN):
        dyn_chain_line = "dynamic_chain";

    if(quiet_mode):
        quiet_mode_line = "quiet_mode";
    
    if(proxy_dns):
        proxy_dns_line = "proxy_dns";

    if(use_tor):
        use_tor_line = "socks4 127.0.0.1 9050 ";

    for proxy in proxy_list:
        proxy_list_line += proxy + "\n";

    
    conf_string = "# proxychains.conf  VER 3.1 " + "\n" + \
    "# " + "\n" + \
    "#        HTTP, SOCKS4, SOCKS5 tunneling proxifier with DNS. " + "\n" + \
    "# " + "\n" + \
    "\n" + \
    "# The option below identifies how the ProxyList is treated. " + "\n" + \
    "# only one option should be uncommented at time, " + "\n" + \
    "# otherwise the last appearing option will be accepted " + "\n" + \
    "# " + "\n" + \
    dyn_chain_line + "\n" + \
    "# " + "\n" + \
    "# Dynamic - Each connection will be done via chained proxies " + "\n" + \
    "# all proxies chained in the order as they appear in the list " + "\n" + \
    "# at least one proxy must be online to play in chain " + "\n" + \
    "# (dead proxies are skipped) " + "\n" + \
    "# otherwise EINTR is returned to the app " + "\n" + \
    "# " + "\n" + \
    strict_chain_line + "\n" + \
    "# " + "\n" + \
    "# Strict - Each connection will be done via chained proxies " + "\n" + \
    "# all proxies chained in the order as they appear in the list " + "\n" + \
    "# all proxies must be online to play in chain " + "\n" + \
    "# otherwise EINTR is returned to the app " + "\n" + \
    "# " + "\n" + \
    random_chain_line + "\n" + \
    "# " + "\n" + \
    "# Random - Each connection will be done via random proxy " + "\n" + \
    "# (or proxy chain, see  chain_len) from the list. " + "\n" + \
    "# this option is good to test your IDS :) " + "\n" + \
    "\n" + \
    "# Make sense only if random_chain " + "\n" + \
    chain_len_line + "\n" + \
    "\n" + \
    "# Quiet mode (no output from library) " + "\n" + \
    quiet_mode_line + "\n" + \
    "\n" + \
    "# Proxy DNS requests - no leak for DNS data " + "\n" + \
    proxy_dns_line + "\n" + \
    "\n" + \
    "# Some timeouts in milliseconds " + "\n" + \
    "tcp_read_time_out 15000 " + "\n" + \
    "tcp_connect_time_out 8000 " + "\n" + \
    "\n" + \
    "# ProxyList format " + "\n" + \
    "#       type  host  port [user pass] " + "\n" + \
    "#       (values separated by 'tab' or 'blank') " + "\n" + \
    "# " + "\n" + \
    "# " + "\n" + \
    "#        Examples: " + "\n" + \
    "# " + "\n" + \
    "#               socks5  192.168.67.78   1080    lamer   secret " + "\n" + \
    "#               http    192.168.89.3    8080    justu   hidden " + "\n" + \
    "#               socks4  192.168.1.49    1080 " + "\n" + \
    "#               http    192.168.39.93   8080 " + "\n" + \
    "# " + "\n" + \
    "# " + "\n" + \
    "#       proxy types: http, socks4, socks5 " + "\n" + \
    "#        ( auth types supported: \"basic\"-http  \"user/pass\"-socks ) " + "\n" + \
    "# " + "\n" + \
    "[ProxyList] " + "\n" + \
    "# add proxy here ... " + "\n" + \
    "# meanwile " + "\n" + \
    proxy_list_line + "\n" + \
    "# defaults set to \"tor\" " + "\n" + \
    use_tor_line;

    print(conf_string);

    with open("/etc/proxychains.conf", "w") as file:
        print("file: ", file);
        print(file.write(conf_string));

def get_params():
    find = False;
    types = [];
    limit = 0;
    resp_cap = 0;
    use_tor = False;
    chain_type = DYNAMIC_CHAIN;
    chain_len = 1;
    proxy_dns = True;
    quiet_mode = False;

    for arg in sys.argv:
        if("--chain-len=" in arg):
            chain_len = int(arg.lstrip("--chain-len="))
            
    return ({
        "chain_len": chain_len
    })

            
        
    
    

if __name__ == "__main__":
    pfinder = ProxyFinder();

    pfinder.find_proxies(['SOCKS5'], 10);

    proxy_list = pfinder.get_proxies();

    proxy_string_list = [];
    
    params_dict = get_params()

    for proxy in proxy_list: 
        if not proxy.is_working: 
            continue;

        proxy_string = "socks5 " + proxy.host + " " + str(proxy.port);
        proxy_string_list.append(proxy_string);       

    write_to_conf(DYNAMIC_CHAIN, chain_len=params_dict["chain_len"], proxy_list=proxy_string_list);
    
