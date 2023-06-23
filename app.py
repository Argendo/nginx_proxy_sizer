from prettytable import PrettyTable
import http.client, math, sys, requests


def round_up_to_power(number):
    if number <= 0:
        return 0
    power = math.ceil(math.log2(number))
    return int(math.pow(2, power))

if "-sh" in sys.argv:
    known_header = sys.argv[2]
    rounded_header = math.ceil(round(int(known_header)/1024))
    if rounded_header==0:
        rounded_header+=1
    remainder_header = rounded_header % 4
    if remainder_header != 0:
        rounded_header += 4 - remainder_header
    print(f'Минимально допустимое значение proxy_buffer_size: {str(rounded_header)} KB')
    rounded_header = round_up_to_power((int(known_header)/1024)*1.5)
    if rounded_header==0:
        rounded_header+=1
    remainder_header = rounded_header % 4
    if remainder_header != 0:
        rounded_header += 4 - remainder_header
    print(f'Оптимальное значение proxy_buffer_size: {str(rounded_header)} KB')
    
    print(f'\nВаша конфигурация:\nproxy_buffer_size {rounded_header}k;')
    print(f'\nПомните, что данные значения носят исключительно рекомендательный характер.\nЗначение proxy_buffer_size должно быть не меньше максимально возможного размера заголовков HTTP ответа.\nПроизведение полученное из количества буфферов и их размера в директиве proxy_buffers должно быть не менее максимально возможного размера тела HTTP ответа.\nЗначение proxy_busy_buffers_size должно быть не меньше значения proxy_buffer_size, но не должно превышать результат выражения (proxy_buffers-buffer_size), где buffer_size - размер одного буфера')
elif "-sb" in sys.argv:
    known_body = sys.argv[2]
    rounded_body = round_up_to_power((int(known_body)/1024)*1.5)
    if rounded_body==0:
        rounded_body+=1
    remainder_body = rounded_body % 4
    if remainder_body != 0:
        rounded_body += 4 - remainder_body
    print(f'Оптимальное значание proxy_buffers: {"8 "+str(int(rounded_body/8))} KB')
    print(f'Оптимальное значение proxy_busy_buffers_size: {str(int(rounded_body/8)*6)} KB')
    
    print(f'\nВаша конфигурация:\nproxy_buffers {"8 "+str(int(rounded_body/8))}k;\nproxy_busy_buffers_size {str(int(rounded_body/8)*6)}k;')
    print(f'\nПомните, что данные значения носят исключительно рекомендательный характер.\nЗначение proxy_buffer_size должно быть не меньше максимально возможного размера заголовков HTTP ответа.\nПроизведение полученное из количества буфферов и их размера в директиве proxy_buffers должно быть не менее максимально возможного размера тела HTTP ответа.\nЗначение proxy_busy_buffers_size должно быть не меньше значения proxy_buffer_size, но не должно превышать результат выражения (proxy_buffers-buffer_size), где buffer_size - размер одного буфера')
elif "-s" in sys.argv:
    known_header = sys.argv[2]
    known_body = sys.argv[3]
    rounded_header = math.ceil(round(int(known_header)/1024))
    if rounded_header==0:
        rounded_header+=1
    remainder_header = rounded_header % 4
    if remainder_header != 0:
        rounded_header += 4 - remainder_header
    print(f'Минимально допустимое значение proxy_buffer_size: {str(rounded_header)} KB')
    rounded_header = round_up_to_power((int(known_header)/1024)*1.5)
    if rounded_header==0:
        rounded_header+=1
    remainder_header = rounded_header % 4
    if remainder_header != 0:
        rounded_header += 4 - remainder_header
    print(f'Оптимальное значение proxy_buffer_size: {str(rounded_header)} KB')
    rounded_body = round_up_to_power((int(known_body)/1024)*1.5)
    if rounded_body==0:
        rounded_body+=1
    remainder_body = rounded_body % 4
    if remainder_body != 0:
        rounded_body += 4 - remainder_body
    print(f'Оптимальное значание proxy_buffers: {"8 "+str(int(rounded_body/8))} KB')
    print(f'Оптимальное значение proxy_busy_buffers_size: {str(int(rounded_body/8)*6)} KB')

    print(f'\nВаша конфигурация:\nproxy_buffer_size {rounded_header}k;\nproxy_buffers {"8 "+str(int(rounded_body/8))}k;\nproxy_busy_buffers_size {str(int(rounded_body/8)*6)}k;')

    print(f'\nПомните, что данные значения носят исключительно рекомендательный характер.\nЗначение proxy_buffer_size должно быть не меньше максимально возможного размера заголовков HTTP ответа.\nПроизведение полученное из количества буфферов и их размера в директиве proxy_buffers должно быть не менее максимально возможного размера тела HTTP ответа.\nЗначение proxy_busy_buffers_size должно быть не меньше значения proxy_buffer_size, но не должно превышать результат выражения (proxy_buffers-buffer_size), где buffer_size - размер одного буфера')
else:
    url=str(sys.argv[1])

    hs_stats = []
    h_stats = []

    th=['HTTPS headers', 'HTTP headers', 'HTTPS body', 'HTTP body']
    table=PrettyTable(th)
    table.title = f'Размеры ответов в байтах для сайта "{url}"'
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
    bs_size=len(requests.get("https://"+url).content)
    b_size=len(requests.get("http://"+url).content)
    td = [hs_size, h_size, bs_size, bs_size]
    table.add_row(td)
    print(table)
    t_headers = [hs_size, h_size]
    t_body = [bs_size, b_size]
    rounded = math.ceil(round(int(max(t_headers))/1024))
    if rounded==0:
        rounded+=1
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print(f'\nМинимально допустимое значение proxy_buffer_size: {str(rounded)} KB')
    rounded = round_up_to_power((int(max(t_headers))/1024)*1.5)
    if rounded==0:
        rounded+=1
    remainder = rounded % 4
    if remainder != 0:
        rounded += 4 - remainder
    print(f'Оптимальное значение proxy_buffer_size: {str(rounded)} KB')
    rounded_body = round_up_to_power((int(max(t_body))/1024)*1.5)
    if rounded_body==0:
        rounded_body+=1
    remainder_body = rounded_body % 4
    if remainder_body != 0:
        rounded_body += 4 - remainder_body
    print(f'Оптимальное значание proxy_buffers: {"8 "+str(int(rounded_body/8))} KB')
    print(f'Оптимальное значение proxy_busy_buffers_size: {str(int(rounded_body/8)*6)} KB')

    print(f'\nВаша конфигурация:\nproxy_buffer_size {rounded}k;\nproxy_buffers {"8 "+str(int(rounded_body/8))}k;\nproxy_busy_buffers_size {str(int(rounded_body/8)*6)}k;')
    print(f'\nПомните, что данные значения носят исключительно рекомендательный характер.\nЗначение proxy_buffer_size должно быть не меньше максимально возможного размера заголовков HTTP ответа.\nПроизведение полученное из количества буфферов и их размера в директиве proxy_buffers должно быть не менее максимально возможного размера тела HTTP ответа.\nЗначение proxy_busy_buffers_size должно быть не меньше значения proxy_buffer_size, но не должно превышать результат выражения (proxy_buffers-buffer_size), где buffer_size - размер одного буфера')

