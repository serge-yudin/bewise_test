# bewise_test
Тестовое задание

Установка на linux (debian family)

<code>sudo apt install -y docker docker-compose</code>

<code>git clone https://github.com/serge-yudin/bewise_test && cd bewise_test</code>

<h3>Первый запуск</h3>
1. docker-compose build  # docker собирает image из Dockerfile (Python + Flask) и скачивате image Postgres если такой не имеется на хост машине
2. docker-compose up -d  # поднимает БД Postgres и зависящее от бд Flask приложение
3. docker-compose exec bewise_flask python init_db.py  # создает таблицы в бд из Models
<br/>
Результатом выполнения команды docker ps должны быть два контейнера bewise_flask_test и mypostgres
также на хост машине будут открыты порты 80 и 5432 (nmap localhost), если порты, на момент запуска, были использованы другими сервисами, то возникнет ошибка

<h3>Второй и последующие запуски</h3> 
<h3>docker-compose up -d</code>

<h3>Останов контейнеров(сервисов)</h3>
<code>docker-compose down</code>

Тест работы приложения
В текущей папке (клон репозитория) запустить команду 
python test_json.py
Первый запуск выведет на STDOUT 200 (код http ответа) и {} пустой объект JSON. Последующие запуски выводят последний введенный в бд вопрос полученный из api викторин.
В случае ошибки вида (открыт ли порт 5432, невозможно найти бд или убедитесь, что бд принимает tcp/ip подключения) запустить Bash скрипт ./get_ip.sh (в случае ошибки дать права исполнения chmod +x get_ip.sh) скопировать и вставить полученный ip адрес вместо localhost в строку 11 в main.py



