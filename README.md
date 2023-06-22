# HTTP-response-headers-size
Данный скрипт поможет Вам определить размер заголовков HTTP и HTTPS ответов, а также расчитает оптимальные значения `proxy_buffer_size` для nginx конфига исходя из полученных данных.

## Установка
`
python3 -m venv venv_nginx_proxy_sizer &&
source venv_nginx_proxy_sizer/bin/activate &&
pip install -r requirements.txt
`

## Пример использования
`python3 app.py example.com 5`, где `example.com` - домен, для которого производятся вычисления, а `5` - число запросов.
Если необходимо вычислить оптимальные значения для уже имеющихся данных, то можно использовать следующую комманду
`python3 app.py -s 1921`, где `1921` - максимальный размер заголовков HTTP ответа.
