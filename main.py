import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget

conn = sqlite3.connect('books.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        genre TEXT,
        year INTEGER
    )
''')
conn.commit()


def add_book():
    title = entry_title.text()
    author = entry_author.text()
    genre = entry_genre.text()
    year = entry_year.text()

    if title and author and genre and year:
        try:
            year = int(year)
            cursor.execute('''
                INSERT INTO Books (title, author, genre, year)
                VALUES (?, ?, ?, ?)
            ''', (title, author, genre, year))
            conn.commit()
            QMessageBox.information(window, "Успех", "Книга успешно добавлена!")
        except ValueError:
            QMessageBox.critical(window, "Ошибка", "Неверный формат года!")
    else:
        QMessageBox.critical(window, "Ошибка", "Пожалуйста, заполните все поля.")


def search_book_by_title():
    title = entry_search.text()
    cursor.execute('SELECT * FROM Books WHERE title LIKE ?', ('%' + title + '%',))
    books = cursor.fetchall()
    if books:
        book_info = ""
        for book in books:
            book_info += f"ID: {book[0]}\nНазвание: {book[1]}\nАвтор: {book[2]}\nЖанр: {book[3]}\nГод издания: {book[4]}\n\n"
        QMessageBox.information(window, "Результаты поиска", book_info)
    else:
        QMessageBox.information(window, "Результаты поиска", "Книга не найдена")


def view_books():
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    if books:
        book_info = ""
        for book in books:
            book_info += f"ID: {book[0]}\nНазвание: {book[1]}\nАвтор: {book[2]}\nЖанр: {book[3]}\nГод издания: {book[4]}\n\n"
        QMessageBox.information(window, "Список книг", book_info)
    else:
        QMessageBox.information(window, "Список книг", "Нет книг в базе данных")


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Справочная система о книгах')
central_widget = QWidget()
layout = QVBoxLayout()


label_title = QLabel("Название:")
layout.addWidget(label_title)
entry_title = QLineEdit()
layout.addWidget(entry_title)

label_author = QLabel("Автор:")
layout.addWidget(label_author)
entry_author = QLineEdit()
layout.addWidget(entry_author)

label_genre = QLabel("Жанр:")
layout.addWidget(label_genre)
entry_genre = QLineEdit()
layout.addWidget(entry_genre)

label_year = QLabel("Год издания:")
layout.addWidget(label_year)
entry_year = QLineEdit()
layout.addWidget(entry_year)

button_add = QPushButton("Добавить книгу")
button_add.clicked.connect(add_book)
layout.addWidget(button_add)

label_search = QLabel("Поиск по названию:")
layout.addWidget(label_search)
entry_search = QLineEdit()
layout.addWidget(entry_search)

button_search = QPushButton("Найти книгу")
button_search.clicked.connect(search_book_by_title)
layout.addWidget(button_search)

button_view = QPushButton("Просмотреть книги")
button_view.clicked.connect(view_books)
layout.addWidget(button_view)

central_widget.setLayout(layout)
window.setCentralWidget(central_widget)
window.show()

sys.exit(app.exec_())


conn.close()
