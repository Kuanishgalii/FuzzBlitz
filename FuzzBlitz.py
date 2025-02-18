import requests
import threading
import queue
import argparse
from urllib.parse import urljoin
import time
import json

# Глобальные переменные для хранения результатов
results = []
lock = threading.Lock()

class FuzzBlitz:
    def __init__(self, base_url, wordlist, threads=10, extensions=None, method="GET", headers=None, data=None, output=None):
        self.base_url = base_url
        self.wordlist = wordlist
        self.threads = threads
        self.extensions = extensions
        self.method = method.upper()
        self.headers = headers if headers else {}
        self.data = data
        self.output = output
        self.word_queue = queue.Queue()
        self.session = requests.Session()

    def load_wordlist(self):
        """Загружает словарь из файла."""
        try:
            with open(self.wordlist, "r") as f:
                words = f.read().splitlines()
            for word in words:
                self.word_queue.put(word)
        except FileNotFoundError:
            print(f"[-] Wordlist file not found: {self.wordlist}")
            exit(1)

    def fuzz_target(self, word):
        """Функция для фаззинга целевого URL."""
        try:
            # Добавляем расширения, если они указаны
            if self.extensions:
                for ext in self.extensions:
                    target_url = urljoin(self.base_url, word + ext)
                    self.make_request(target_url)
            else:
                target_url = urljoin(self.base_url, word)
                self.make_request(target_url)
        except Exception as e:
            with lock:
                print(f"[-] Error with {target_url}: {e}")

    def make_request(self, url):
        """Выполняет HTTP-запрос."""
        try:
            if self.method == "GET":
                response = self.session.get(url, headers=self.headers)
            elif self.method == "POST":
                response = self.session.post(url, headers=self.headers, data=self.data)
            elif self.method == "PUT":
                response = self.session.put(url, headers=self.headers, data=self.data)
            elif self.method == "DELETE":
                response = self.session.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")

            with lock:
                if response.status_code == 200:
                    print(f"[+] Found: {url} (Status: {response.status_code})")
                    results.append({"url": url, "status": response.status_code, "length": len(response.content)})
                else:
                    print(f"[-] Not found: {url} (Status: {response.status_code})")
        except requests.RequestException as e:
            with lock:
                print(f"[-] Error with {url}: {e}")

    def worker(self):
        """Рабочая функция для потоков."""
        while not self.word_queue.empty():
            word = self.word_queue.get()
            self.fuzz_target(word)
            self.word_queue.task_done()

    def run(self):
        """Запускает фаззинг."""
        print(f"[*] Starting FuzzBlitz on {self.base_url} with {self.threads} threads...")
        start_time = time.time()

        # Загрузка словаря
        self.load_wordlist()

        # Запуск потоков
        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        # Ожидание завершения всех потоков
        for thread in threads:
            thread.join()

        # Вывод результатов
        print("\n[+] FuzzBlitz completed!")
        print(f"[*] Total time: {time.time() - start_time:.2f} seconds")
        if results:
            print("[+] Valid paths found:")
            for result in results:
                print(f"URL: {result['url']}, Status: {result['status']}, Length: {result['length']}")
            if self.output:
                self.save_results()
        else:
            print("[-] No valid paths found.")

    def save_results(self):
        """Сохраняет результаты в файл."""
        with open(self.output, "w") as f:
            json.dump(results, f, indent=4)
        print(f"[+] Results saved to {self.output}")

def main():
    parser = argparse.ArgumentParser(description="FuzzBlitz - Powerful web fuzzer for finding hidden paths and endpoints.")
    parser.add_argument("-u", "--url", required=True, help="Base URL to fuzz.")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist.")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use.")
    parser.add_argument("-e", "--extensions", nargs="+", help="Extensions to append (e.g., .php, .html).")
    parser.add_argument("-X", "--method", default="GET", help="HTTP method to use (GET, POST, PUT, DELETE).")
    parser.add_argument("-H", "--headers", nargs="+", help="Custom headers (e.g., 'Header: Value').")
    parser.add_argument("-d", "--data", help="Data to send with POST/PUT requests.")
    parser.add_argument("-o", "--output", help="Output file to save results.")
    args = parser.parse_args()

    # Парсинг заголовков
    headers = {}
    if args.headers:
        for header in args.headers:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()

    # Инициализация FuzzBlitz
    fuzzer = FuzzBlitz(
        base_url=args.url,
        wordlist=args.wordlist,
        threads=args.threads,
        extensions=args.extensions,
        method=args.method,
        headers=headers,
        data=args.data,
        output=args.output
    )

    # Запуск FuzzBlitz
    fuzzer.run()

if __name__ == "__main__":
    main()