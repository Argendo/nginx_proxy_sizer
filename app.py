from prettytable import PrettyTable
import http.client, math, sys

if "-s" in sys.argv:
    known = sys.argv[2]
    rounded = math.ceil(round(int(known)/1024))
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print(f'Оптимальное значение proxy_buffer_size: {str(rounded)} KB')
    rounded = math.ceil(round(int(known)/1024)*1.5)
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print("Значение с запасом: "+str(rounded)+" KB")
else:
    url=str(sys.argv[1])
    c = int(sys.argv[2])

    hs_stats = []
    h_stats = []

    th=['HTTPS', 'HTTP']
    table=PrettyTable(th)
    table.title = "Response headers size in bytes"
    conn_hs = http.client.HTTPSConnection(url)
    conn_hs.request("GET", "/")
    hs_resp = conn_hs.getresponse()
    hs_headers = hs_resp.getheaders()
    hs_str  = "\n".join([f"{name}: {value}" for name, value in hs_headers])
    hs_size = len(hs_str.encode("utf-8"))
    conn_hs.close()
    conn_h = http.client.HTTPConnection(url)
    conn_h.request("GET", "/")
    h_resp = conn_h.getresponse()
    h_headers = h_resp.getheaders()
    h_str  = "\n".join([f"{name}: {value}" for name, value in h_headers])
    h_size = len(h_str.encode("utf-8"))
    conn_h.close()
    td = [hs_size, h_size]
    hs_stats.append(int(hs_size))
    h_stats.append(int(h_size))
    table.add_row(td)
    print(table)
    for i in range (c-1):
        conn_hs = http.client.HTTPSConnection(url)
        conn_hs.request("GET", "/")
        hs_resp = conn_hs.getresponse()
        hs_headers = hs_resp.getheaders()
        hs_str  = "\n".join([f"{name}: {value}" for name, value in hs_headers])
        hs_size = len(hs_str.encode("utf-8"))
        conn_hs.close()
        conn_h = http.client.HTTPConnection(url)
        conn_h.request("GET", "/")
        h_resp = conn_h.getresponse()
        h_headers = h_resp.getheaders()
        h_str  = "\n".join([f"{name}: {value}" for name, value in h_headers])
        h_size = len(h_str.encode("utf-8"))
        conn_h.close()
        td = [hs_size, h_size]
        hs_stats.append(int(hs_size))
        h_stats.append(int(h_size))
        table.add_row(td)
        print( "\n".join(table.get_string().splitlines()[-2:]) )
    t = [max(hs_stats), max(h_stats)]
    print(f"Максимальный размер заголовков из {c} запросов составил {str(max(t))} B")
    rounded = math.ceil(round(int(max(t))/1024))
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print(f'Оптимальное значение proxy_buffer_size для сайта "{url}": {str(rounded)} KB')
    rounded = math.ceil(round(int(max(t))/1024)*1.5)
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print("Значение с запасом: "+str(rounded)+" KB")
