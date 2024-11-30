import json
import os


# წიგნის კლასი, რომელიც წარმოადგენს  წიგნს.
class Book:
    def __init__(self, title, author, year):
        # ინიციალიზაცია: წიგნის სათაური, ავტორი და გამოცემის წელი.
        self.title = title.strip()
        self.author = author.strip()
        self.year = year

    # წიგნის ობიექტის კონვერტაცია დიქტ ფორმატში (JSON ფაილში შესანახად).
    def to_dict(self):
        return {"title": self.title, "author": self.author, "year": self.year}

    # სტრიქონული წარმოდგენა წიგნის შესახებ (ბეჭდვისთვის).
    def __str__(self):
        return f"სათაური: {self.title}, ავტორი: {self.author}, გამოცემის წელი: {self.year}"


# წიგნების მართვის კლასი (სიის მართვა, ჩაწერა/ამოღება).
class BookManager:
    def __init__(self, file_path="books.json"):
        # JSON ფაილის მისამართის და სიის ინიციალიზაცია.
        self.file_path = file_path
        self.books = self.load_books()  # სიის ჩატვირთვა ფაილიდან.

    # წიგნების სიის ჩატვირთვა JSON ფაილიდან.
    def load_books(self):
        if not os.path.exists(self.file_path):
            return []  # ფაილი არ არსებობს -> ცარიელი სია.
        with open(self.file_path, "r", encoding="utf-8") as file:
            return [Book(**book_data) for book_data in json.load(file)]

    # სიის ჩაწერა JSON ფაილში.
    def save_books(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    # ახალი წიგნის დამატება სიისთვის.
    def add_book(self, title, author, year):
        
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return False, "ასეთი წიგნი უკვე არსებობს!"
        # ახალი წიგნის შექმნა და სიისთვის დამატება.
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()  # განახლებული სიის შენახვა ფაილში.
        return True, f"წიგნი '{title}' წარმატებით დაემატა!"

    # ყველა წიგნის სიის მიღება.
    def list_books(self):
        if not self.books:
            return "წიგნების სია ცარიელია.", False  
        return "\n".join(f"{i + 1}. {book}" for i, book in enumerate(self.books)), True

    # წიგნის ძიება სათაურის მიხედვით.
    def search_by_title(self, title):
        title = title.strip().lower()
        # ყველა წიგნის მოძიება, რომელიც შეიცავს მოთხოვნილ სათაურს.
        found_books = [book for book in self.books if title in book.title.lower()]
        if not found_books:
            return "ასეთი სათაურის მქონე წიგნი ვერ მოიძებნა.", False
        return "\n".join(str(book) for book in found_books), True

    # წიგნის წაშლა ინდექსის მიხედვით.
    def delete_book(self, index):
        if 0 <= index < len(self.books):  # ინდექსის ვალიდაციის შემოწმება.
            removed_book = self.books.pop(index)
            self.save_books()  # სიის განახლების შენახვა.
            return f"წიგნი '{removed_book.title}' წარმატებით წაიშალა!"
        else:
            return "მოცემული ინდექსით წიგნი ვერ მოიძებნა."


# მომხმარებლის ინტერფეისის კლასი (მენიუ და ოპერაციები).
class BookApp:
    def __init__(self):
        self.manager = BookManager()  # წიგნების მართვის ობიექტი.
        self.options = {
            "1": self.add_book,        # ახალი წიგნის დამატება.
            "2": self.view_books,      # ყველა წიგნის ნახვა.
            "3": self.search_book,     # წიგნის ძებნა.
            "4": self.delete_book,     # წიგნის წაშლა.
            "5": self.exit_app         # გამოსვლა.
        }

    # აპლიკაციის მთავარი ციკლი.
    def run(self):
        while True:
            self.show_menu()  # მენიუს ჩვენება.
            choice = input("აირჩიეთ მოქმედება (1-5): ").strip()
            action = self.options.get(choice)
            if action:
                action()  # არჩეული მოქმედების შესრულება.
            else:
                print("გთხოვთ, აირჩიოთ შესაბამისი მოქმედება.")

    @staticmethod
    def show_menu():
        # მენიუს გამოხატვა.
        print("\n წიგნების მართვის სისტემა ")
        print("1. ახალი წიგნის დამატება")
        print("2. ყველა წიგნის ნახვა")
        print("3. წიგნის ძებნა სათაურის მიხედვით")
        print("4. წიგნის წაშლა")
        print("5. გამოსვლა")

    # ახალი წიგნის დამატების ფუნქცია.
    def add_book(self):
        title = input("შეიყვანეთ წიგნის სათაური: ").strip()
        author = input("შეიყვანეთ ავტორის სახელი: ").strip()
        year = self.get_valid_year("შეიყვანეთ გამოცემის წელი: ")
        success, message = self.manager.add_book(title, author, year)
        print(message)
        if not success:
            input("დააჭირეთ Enter მენიუში დასაბრუნებლად.")

    # სიის ჩვენება.
    def view_books(self):
        print("\n ყველა წიგნი ")
        books, success = self.manager.list_books()
        print(books)
        if not success:
            input("დააჭირეთ Enter მენიუში დასაბრუნებლად.")

    # წიგნის ძებნა.
    def search_book(self):
        title = input("შეიყვანეთ წიგნის სათაური: ").strip()
        print("\n ძიების შედეგი:")
        results, success = self.manager.search_by_title(title)
        print(results)
        if not success:
            input("დააჭირეთ Enter მენიუში დასაბრუნებლად.")

    # წიგნის წაშლა.
    def delete_book(self):
        self.view_books()  # სიის ჩვენება წაშლამდე.
        try:
            index = int(input("\nშეიყვანეთ წასაშლელი წიგნის ნომერი: ")) - 1
            print(self.manager.delete_book(index))
        except ValueError:
            print("გთხოვთ, შეიყვანოთ ვალიდური ნომერი.")

    # ვალიდური წლის შეყვანის მოთხოვნა.
    @staticmethod
    def get_valid_year(prompt):
        while True:
            try:
                year = int(input(prompt).strip())
                return year
            except ValueError:
                print("გთხოვთ, შეიყვანოთ ვალიდური წელი.")

    # აპლიკაციიდან გამოსვლა.
    @staticmethod
    def exit_app():
        print("დროებით ნახვამდის!")
        exit()


# აპლიკაციის გაშვება
if __name__ == "__main__":
    BookApp().run()
