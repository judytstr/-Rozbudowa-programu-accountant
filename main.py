class FileReader:
    def __init__(self):
        self.warehouse = {}
        self.actions = []
        self.balance = 0

    def save_data(self):
        with open("data.txt", "a") as file:
            file.write("Saldo konta: " + str(self.balance) + "\n")
            file.write("Stan magazynu:\n")
            for product, details in self.warehouse.items():
                file.write(f"Produkt: {product}, Cena: {details['price']}, Ilość: {details['quantity']}\n")
            file.write("Historia operacji:\n")
            for action in self.actions:
                file.write(str(action) + "\n")

    def load_data(self):
        self.warehouse = {}
        self.actions = []

        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                self.balance = float(lines[0].split(":")[1].strip())

                for line in lines[1:]:
                    if line.startswith("Produkt"):
                        parts = line.strip().split(", ")
                        name = parts[0].split(": ")[1]
                        price = float(parts[1].split(": ")[1])
                        quantity = int(parts[2].split(": ")[1])
                        self.warehouse[name] = {'price': price, 'quantity': quantity}
                    elif line.startswith("("):
                        action = eval(line.strip())  # Using eval() to convert string representation of tuple to actual tuple
                        self.actions.append(action)
        except FileNotFoundError:
            print("Plik danych nie istnieje. Tworzenie nowego pliku.")

    def modify(self, changes_list):
        for change in changes_list:
            x, y, value = map(str.strip, change.split(','))
            x, y = int(x), int(y)
            self.warehouse[y][x] = value

    def display(self):
        if not self.warehouse:
            print("Brak danych do wyświetlenia")
            return
        for row in self.warehouse:
            print(','.join(map(str, row)))

    def save(self):
        with open("data.txt", "w") as file:
            file.write("Saldo konta: " + str(self.balance) + "\n")
            file.write("Stan magazynu:\n")
            for product, details in self.warehouse.items():
                file.write(f"Produkt: {product}, Cena: {details['price']}, Ilość: {details['quantity']}\n")
            file.write("Historia operacji:\n")
            for action in self.actions:
                file.write(str(action) + "\n")

class Manager:
    def __init__(self):
        self.reader = FileReader()

    def assign(self, command):
        if command.startswith('saldo'):
            amount = float(input("Podaj kwotę do dodania lub odjęcia z konta: "))
            self.reader.balance += amount
            self.reader.actions.append(('saldo', amount))
        elif command.startswith('sprzedaż'):
            name = input("Podaj nazwę produktu: ")
            if name not in self.reader.warehouse:
                print("Produkt nie istnieje w magazynie!")
                return

            price = float(input("Podaj cenę produktu: "))
            quantity = int(input("Podaj liczbę sztuk: "))
            product = self.reader.warehouse[name]
            if product['quantity'] < quantity:
                print("Brak wystarczającej liczby sztuk w magazynie!")
                return

            total_price = price * quantity
            product['quantity'] -= quantity
            self.reader.balance += total_price
            self.reader.actions.append(('sprzedaż', name, price, quantity))
        elif command.startswith('zakup'):
            name = input("Podaj nazwę produktu: ")
            price = float(input("Podaj cenę produktu: "))
            quantity = int(input("Podaj liczbę sztuk: "))

            if name in self.reader.warehouse:
                self.reader.warehouse[name]['quantity'] += quantity
            else:
                self.reader.warehouse[name] = {'price': price, 'quantity': quantity}

            total_price = price * quantity
            self.reader.balance -= total_price
            self.reader.actions.append(('zakup', name, price, quantity))
        elif command.startswith('konto'):
            print("Stan konta: ", self.reader.balance)
        elif command.startswith('lista'):
            self.reader.display()
        elif command.startswith('magazyn'):
            name = input("Podaj nazwę produktu: ")
            product = self.reader.warehouse.get(name)
            if product:
                print(f"Stan magazynu dla produktu {name}: Cena: {product['price']}, Ilość: {product['quantity']}")
            else:
                print("Produkt nie istnieje w magazynie!")
        elif command.startswith('przegląd'):
            start = input("Podaj indeks początkowy (od 0) lub zostaw puste dla początku: ")
            end = input(f"Podaj indeks końcowy (max {len(self.reader.actions)-1}) lub zostaw puste dla końca: ")

            try:
                if start == '':
                    start = 0
                else:
                    start = int(start)
                if end == '':
                    end = len(self.reader.actions) - 1
                else:
                    end = int(end)

                if start < 0 or end >= len(self.reader.actions):
                    print(f"Podano nieprawidłowy zakres, dostępne indeksy od 0 do {len(self.reader.actions)-1}")
                    return

                print("Historia operacji:")
                for i in range(start, end + 1):
                    print(self.reader.actions[i])
            except ValueError:
                print("Podano nieprawidłowy zakres!")
        else:
            print("Nieprawidłowa komenda!")

    def execute(self):
        while True:
            print("\nDostępne komendy: saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")
            command = input("Podaj komendę: ").lower()

            if command.startswith('koniec'):
                print("Koniec działania programu.")
                break

            self.assign(command)
            self.reader.save()

if __name__ == "__main__":
    manager = Manager()
    manager.execute()
