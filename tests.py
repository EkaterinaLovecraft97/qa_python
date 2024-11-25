import pytest
from main import BooksCollector  # Импортируем класс, предполагаем, что он в файле main.py


# Тестирование метода add_new_book.
# Проверяем добавление книги в books_genre с корректными условиями (имя книги не более 40 символов)
def test_add_new_book():
    collector = BooksCollector()

    collector.add_new_book("Book 1")
    assert "Book 1" in collector.books_genre
    assert collector.books_genre["Book 1"] == ''

    collector.add_new_book("Book 2")
    assert "Book 2" in collector.books_genre

    collector.add_new_book("Book 1")  # Повторно не добавляется
    assert list(collector.books_genre.keys()).count("Book 1") == 1

    collector.add_new_book("A" * 41)  # Имя больше 40 символов
    assert "A" * 41 not in collector.books_genre


# Тестирование метода set_book_genre.
# Проверяем правильность назначения жанра, а также случаи, когда жанр отсутствует в списке
@pytest.mark.parametrize("book_name, genre, expected_genre", [
    ("Book 1", "Фантастика", "Фантастика"),
    ("Book 2", "Ужасы", "Ужасы"),
    ("Book 3", "Комедии", "Комедии")
])
def test_set_book_genre(book_name, genre, expected_genre):
    collector = BooksCollector()
    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)
    assert collector.get_book_genre(book_name) == expected_genre


def test_set_book_genre_invalid_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 4")
    collector.set_book_genre("Book 4", "Роман")  # Жанр не из списка
    assert collector.get_book_genre("Book 4") == ''


# Тестирование метода get_book_genre.
# Проверяем получение жанра для уже установленной книги и для книги, жанр которой ещё не установлен.
def test_get_book_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.get_book_genre("Book 1") == "Фантастика"

    collector.add_new_book("Book 2")
    assert collector.get_book_genre("Book 2") == ''  # Жанр ещё не установлен


# Тестирование метода get_books_with_specific_genre.
# Проверяем правильность вывода книг с определённым жанром.
def test_get_books_with_specific_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Фантастика")

    assert collector.get_books_with_specific_genre("Фантастика") == ["Book 1", "Book 3"]
    assert collector.get_books_with_specific_genre("Ужасы") == ["Book 2"]
    assert collector.get_books_with_specific_genre("Комедии") == []


# Тестирование метода get_books_genre.
# Проверяем, что метод возвращает правильный словарь жанров для всех книг.
def test_get_books_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")

    expected = {
        "Book 1": "Фантастика",
        "Book 2": "Ужасы"
    }
    assert collector.get_books_genre() == expected


# Тестирование метода get_books_for_children.
# Проверяем, что метод возвращает только те книги, которые не имеют возрастной маркировки.
def test_get_books_for_children():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Детективы")
    collector.add_new_book("Book 4")
    collector.set_book_genre("Book 4", "Мультфильмы")

    books_for_children = collector.get_books_for_children()
    assert "Book 1" in books_for_children
    assert "Book 4" in books_for_children
    assert "Book 2" not in books_for_children
    assert "Book 3" not in books_for_children


# Тестирование метода add_book_in_favorites.
# Проверяем добавление книги в избранное и отсутствие дублирования.
def test_add_book_in_favorites():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")

    collector.add_book_in_favorites("Book 1")
    assert "Book 1" in collector.favorites
    collector.add_book_in_favorites("Book 1")  # Повторно не добавляется
    assert collector.favorites.count("Book 1") == 1


# Тестирование метода delete_book_from_favorites.
# Проверяем удаление книги из избранного и обработку случаев, когда книги нет в избранном.
def test_delete_book_from_favorites():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_book_in_favorites("Book 1")

    collector.delete_book_from_favorites("Book 1")
    assert "Book 1" not in collector.favorites

    collector.delete_book_from_favorites("Book 2")  # Книга нет в избранном
    assert len(collector.favorites) == 0


# Тестирование метода get_list_of_favorites_books.
# Проверяем корректность получения списка избранных книг.
def test_get_list_of_favorites_books():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")

    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 2")

    assert collector.get_list_of_favorites_books() == ["Book 1", "Book 2"]

    collector.delete_book_from_favorites("Book 1")
    assert collector.get_list_of_favorites_books() == ["Book 2"]

