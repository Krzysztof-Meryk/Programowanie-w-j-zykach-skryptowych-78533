import datetime
import json

books = []
students = {}

def load_data():
    global books, students
    try:
        with open("books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except FileNotFoundError:
        pass

    try:
        with open("students.json", "r") as f:
            students = json.load(f)
    except FileNotFoundError:
        pass

def save_data():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    with open("students.json", "w") as f:
        json.dump(students, f)

def add_book():
    book = {
        "author": input("Autor: "),
        "title": input("Tytuł: "),
        "year": input("Rok wydania: "),
        "pages": int(input("Liczba stron: ")),
        "count": int(input("Liczba egzemplarzy: "))
    }
    books.append(book)
    save_data()

def edit_book():
    print("\n--- Edytuj książkę ---")

    if not books:
        print("Brak książek do edycji.")
        return

    print("Lista książek:")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['title']} (autor: {book['author']}, rok: {book['year']})")

    try:
        choice = int(input("Wybierz numer książki do edycji: "))
        if not 1 <= choice <= len(books):
            print("Nieprawidłowy numer.")
            return
        book = books[choice - 1]
    except ValueError:
        print("Nieprawidłowy wybór.")
        return

    print(f"\nWybrano książkę: {book['title']}")

    while True:
        print("\nCo chcesz edytować?")
        print("1. Autor")
        print("2. Tytuł")
        print("3. Rok wydania")
        print("4. Liczba stron")
        print("5. Liczba egzemplarzy")
        print("0. Zakończ edycję")
        option = input("Wybierz opcję: ")

        if option == "1":
            book["author"] = input("Nowy autor: ")
        elif option == "2":
            book["title"] = input("Nowy tytuł: ")
        elif option == "3":
            book["year"] = input("Nowy rok wydania: ")
        elif option == "4":
            try:
                book["pages"] = int(input("Nowa liczba stron: "))
            except ValueError:
                print("Podano nieprawidłową liczbę.")
        elif option == "5":
            try:
                book["count"] = int(input("Nowa liczba egzemplarzy: "))
            except ValueError:
                print("Podano nieprawidłową liczbę.")
        elif option == "0":
            break
        else:
            print("Nieprawidłowy wybór.")

    save_data()
    print("Zapisano zmiany.")

def remove_book():
    print("\n--- Usuń książkę ---")

    if not books:
        print("Brak książek do usunięcia.")
        return

    print("Lista książek:")
    for i, book in enumerate(books, start=1):
        print(f"{i}. {book['title']} (autor: {book['author']}, rok: {book['year']})")

    try:
        choice = int(input("Wybierz numer książki do usunięcia: "))
        if 1 <= choice <= len(books):
            removed_book = books.pop(choice - 1)
            save_data()
            print(f"Książka '{removed_book['title']}' została usunięta.")
        else:
            print("Nieprawidłowy numer.")
    except ValueError:
        print("Nieprawidłowy wybór.")

def list_books():
    print("\n--- Lista książek ---")
    if not books:
        print("Brak książek w systemie.")
        return
    for book in books:
        print(f"Autor: {book['author']}")
        print(f"Tytuł: {book['title']}")
        print(f"Rok wydania: {book['year']}")
        print(f"Liczba stron: {book['pages']}")
        print(f"Liczba egzemplarzy: {book['count']}")
        print("-" * 40)

def add_student():
    if len(students) >= 15:
        print("Osiągnięto limit studentów.")
        return
    name = input("Imię i nazwisko studenta: ")
    students[name] = []
    save_data()

def borrow_book():
    print("\n--- Wypożycz książkę ---")

    if not students:
        print("Brak studentów w systemie.")
        return

    print("Lista studentów:")
    student_list = list(students.keys())
    for i, name in enumerate(student_list, start=1):
        print(f"{i}. {name}")

    try:
        student_choice = int(input("Wybierz numer studenta: "))
        if 1 <= student_choice <= len(student_list):
            name = student_list[student_choice - 1]
        else:
            print("Nieprawidłowy numer.")
            return
    except ValueError:
        print("Nieprawidłowy wybór.")
        return

    if len(students[name]) >= 5:
        print("Ten student wypożyczył już 5 książek.")
        return

    available_books = [book for book in books if book["count"] > 0]

    if not available_books:
        print("Brak dostępnych książek do wypożyczenia.")
        return

    print("\nDostępne książki:")
    for i, book in enumerate(available_books, start=1):
        print(f"{i}. {book['title']} (autor: {book['author']}, dostępne: {book['count']})")

    try:
        book_choice = int(input("Wybierz numer książki: "))
        if 1 <= book_choice <= len(available_books):
            selected_book = available_books[book_choice - 1]
        else:
            print("Nieprawidłowy numer.")
            return
    except ValueError:
        print("Nieprawidłowy wybór.")
        return

    students[name].append({"title": selected_book["title"], "date": str(datetime.date.today())})
    selected_book["count"] -= 1
    save_data()
    print(f"Książka '{selected_book['title']}' została wypożyczona studentowi {name}.")

def reminder_report():
    print("\n--- Raport przypomnienia ---")
    for student, borrowed in students.items():
        if not borrowed:
            continue
        print(f"\nStudent: {student}")
        for item in borrowed:
            borrow_date = datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
            return_date = borrow_date + datetime.timedelta(days=7)
            print(f"  - Tytuł: {item['title']}")
            print(f"    Wypożyczono: {borrow_date}")
            print(f"    Termin zwrotu: {return_date}")

def return_book():
    print("\n--- Zwrot książki ---")

    students_with_books = {name: items for name, items in students.items() if items}

    if not students_with_books:
        print("Brak studentów z wypożyczonymi książkami.")
        return

    print("Studenci z wypożyczonymi książkami:")
    student_list = list(students_with_books.keys())
    for i, name in enumerate(student_list, start=1):
        print(f"{i}. {name}")

    try:
        student_choice = int(input("Wybierz numer studenta: "))
        if 1 <= student_choice <= len(student_list):
            name = student_list[student_choice - 1]
        else:
            print("Nieprawidłowy numer.")
            return
    except ValueError:
        print("Nieprawidłowy wybór.")
        return

    borrowed_books = students[name]

    print(f"\n{name} wypożyczył(a):")
    for i, item in enumerate(borrowed_books, start=1):
        print(f"{i}. {item['title']} (wypożyczono {item['date']})")

    try:
        book_choice = int(input("Podaj numer książki do zwrotu: "))
        if 1 <= book_choice <= len(borrowed_books):
            returned = borrowed_books.pop(book_choice - 1)

            for book in books:
                if book["title"] == returned["title"]:
                    book["count"] += 1
                    break
            save_data()
            print(f"Książka '{returned['title']}' została zwrócona przez {name}.")
        else:
            print("Nieprawidłowy numer.")
    except ValueError:
        print("Nieprawidłowy wybór.")



def menu():
    while True:
        print(
            "\n1. Dodaj książkę\n2. Edytuj książkę\n3. Usuń książkę\n4. Lista książek\n5. Dodaj studenta\n6. Wypożycz książkę\n7. Zwrot książki\n8. Lista wypożyczonych książek\n0. Wyjście")
        choice = input("Wybierz opcję: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_book()
        elif choice == "3":
            remove_book()
        elif choice == "4":
            list_books()
        elif choice == "5":
            add_student()
        elif choice == "6":
            borrow_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            reminder_report()
        elif choice == "0":
            break
        else:
            print("Nieprawidłowy wybór.")

load_data()
menu()