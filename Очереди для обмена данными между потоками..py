import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()

    def customer_arrival(self):
        while True:
            time.sleep(1)
            customer = Customer(self)
            customer.start()
            print(f"Посетитель номер {customer.number} прибыл")

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                customer.table = table
                print(f"Посетитель номер {customer.number} сел за стол {table.number}")
                return
        self.queue.put(customer)
        print(f"Посетитель номер {customer.number} ожидает свободный стол")

class Customer(threading.Thread):
    def __init__(self, cafe):
        super().__init__()
        self.cafe = cafe
        self.number = self.cafe.queue.qsize() + 1

    def run(self):
        self.cafe.serve_customer(self)

# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()