# FuzzBlitz

Это мощный и быстрый инструмент для фаззинга веб-приложений. 

Он предназначен для поиска скрытых путей, endpoints и уязвимостей на веб-серверах. 

Инструмент поддерживает многопоточность, что позволяет значительно ускорить процесс сканирования.

FuzzBlitz идеально подходит для пентестеров, разработчиков и security-исследователей.

Основные возможности:

    Многопоточность: Использует несколько потоков для одновременного выполнения запросов.

    Поддержка различных HTTP-методов: GET, POST, PUT, DELETE.

    Гибкая настройка запросов: Возможность добавления заголовков и данных.

    Расширения: Поддержка добавления расширений (например, .php, .html) к словарю.

    Сохранение результатов: Результаты сканирования можно сохранить в JSON-файл.

    Простота использования: Легко настраивается и запускается из командной строки.

-----

Как пользоваться инструментом

Установка:

    Убедитесь, что у вас установлен Python 3.x.

    Установите необходимые зависимости: pip install requests

    
Запуск инструмента:

Инструмент запускается из командной строки. Основные параметры:

    -u или --url: Базовый URL для фаззинга (обязательный параметр).

    -w или --wordlist: Путь к файлу со словарем (обязательный параметр).

    -t или --threads: Количество потоков (по умолчанию 10).

    -e или --extensions: Расширения для добавления к словарю (например, .php, .html).

    -X или --method: HTTP-метод (GET, POST, PUT, DELETE). По умолчанию GET.

    -H или --headers: Пользовательские заголовки (например, Authorization: Bearer token).

    -d или --data: Данные для отправки с POST/PUT запросами.Примеры использования

-----

    Базовый фаззинг:python fuzzblitz.py -u http://example.com/ -w wordlist.txt
    

    Фаззинг с расширениями: python fuzzblitz.py -u http://example.com/ -w wordlist.txt -e .php .html
    

    Фаззинг с использованием 20 потоков: python fuzzblitz.py -u http://example.com/ -w wordlist.txt -t 20
    

    Фаззинг с POST-запросами и данными: python fuzzblitz.py -u http://example.com/ -w wordlist.txt -X POST -d "param1=value1&param2=value2"
    

    Фаззинг с пользовательскими заголовками: python fuzzblitz.py -u http://example.com/ -w wordlist.txt -H "Authorization: Bearer token" "Content-Type: application/json"Пример словаря (wordlist.txt)

 
 -----

Создайте текстовый файл wordlist.txt с путями для фаззинга, например:


admin
login
test
backup
api
user

-----

Пример вывода

После запуска инструмента вы увидите вывод в консоли:

[*] Starting FuzzBlitz on http://example.com/ with 10 threads...
[+] Found: http://example.com/admin (Status: 200)
[+] Found: http://example.com/login (Status: 200)
[-] Not found: http://example.com/test (Status: 404)
[-] Not found: http://example.com/backup (Status: 404)

[+] FuzzBlitz completed!
[*] Total time: 12.34 seconds
[+] Valid paths found:
URL: http://example.com/admin, Status: 200, Length: 1234
URL: http://example.com/login, Status: 200, Length: 5678
[+] Results saved to results.json

-----

Сохранение результатов

Если указан параметр -o, результаты будут сохранены в JSON-файл. Пример содержимого файла results.json:


[
    {
        "url": "http://example.com/admin",
        "status": 200,
        "length": 1234
    },
    {
        "url": "http://example.com/login",
        "status": 200,
        "length": 5678
    }
]

-----
 
 
Сохранение результатов в файл: python fuzzblitz.py -u http://example.com/ -w wordlist.txt -o results.json -o или --output: Файл для сохранения результатов в формате JSON.


-----

Используйте его только в законных целях!

    

    
    
    
