import pytest
from main import BooksCollector

# Тестирование метода add_new_book.
# Проверяем добавление книги с корректной длиной имени и отсутствие добавления с длиной более 40 символов
def test_add_new_book():
    collector = BooksCollector()

    collector.add_new_book("Book 1")
    assert "Book 1" in collector.books_genre  # Проверка добавления
    assert collector.books_genre["Book 1"] == ''  # Проверка пустого жанра

    collector.add_new_book("Book 2")
    assert "Book 2" in collector.books_genre  # Проверка добавления второй книги

    collector.add_new_book("Book 1")  # Повторная попытка добавления
    assert list(collector.books_genre.keys()).count("Book 1") == 1  # Книга не должна добавляться дважды

    collector.add_new_book("A" * 41)  # Проверка книги с длинным именем
    assert "A" * 41 not in collector.books_genre  # Книга с таким именем не должна быть добавлена


# Тестирование метода set_book_genre.
# Проверяем установку жанра для книги
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


# Тестирование метода set_book_genre с некорректным жанром.
def test_set_book_genre_invalid_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 4")
    collector.set_book_genre("Book 4", "Роман")  # Некорректный жанр
    assert collector.get_book_genre("Book 4") == ''  # Жанр должен остаться пустым


# Тестирование метода get_book_genre.
# Проверяем правильность получения жанра
def test_get_book_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.get_book_genre("Book 1") == "Фантастика"  # Проверка установленного жанра

    collector.add_new_book("Book 2")
    assert collector.get_book_genre("Book 2") == ''  # Книга без жанра должна вернуть пустое значение


# Тестирование метода get_books_with_specific_genre.
# Проверяем, что книги с определённым жанром правильно фильтруются
def test_get_books_with_specific_genre():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Фантастика")

    # Проверка жанра "Фантастика"
    books = collector.get_books_with_specific_genre("Фантастика")
    assert books == ["Book 1", "Book 3"]

    # Проверка жанра "Ужасы"
    books = collector.get_books_with_specific_genre("Ужасы")
    assert books == ["Book 2"]

    # Проверка отсутствия книг с жанром "Комедии"
    books = collector.get_books_with_specific_genre("Комедии")
    assert books == []


# Тестирование метода get_books_genre.
# Проверяем, что метод возвращает правильный словарь жанров для всех книг
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
# Проверяем, что метод возвращает книги, подходящие для детей
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
    assert "Book 1" in books_for_children  # Фантастика подходит для детей
    assert "Book 4" in books_for_children  # Мультфильмы тоже подходят
    assert "Book 2" not in books_for_children  # Ужасы не подходят для детей
    assert "Book 3" not in books_for_children  # Детективы тоже не для детей


# Тестирование метода add_book_in_favorites.
# Проверяем добавление книги в избранное
def test_add_book_in_favorites():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")

    collector.add_book_in_favorites("Book 1")
    assert "Book 1" in collector.favorites  # Книга должна быть в избранном
    collector.add_book_in_favorites("Book 1")  # Повторное добавление не должно изменять список
    assert collector.favorites.count("Book 1") == 1  # Должна быть только одна книга


# Тестирование метода delete_book_from_favorites.
# Проверяем удаление книги, которая не в избранном
def test_delete_book_from_favorites():
    collector = BooksCollector()

    # Удаление книги, которая нет в избранном
    collector.delete_book_from_favorites("Book 1")  # Книги нет в избранном
    assert len(collector.favorites) == 0  # В избранном ничего нет


# Тестирование метода get_list_of_favorites_books.
# Проверяем получение списка избранных книг
def test_get_list_of_favorites_books():
    collector = BooksCollector()
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")

    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 2")

    assert collector.get_list_of_favorites_books() == ["Book 1", "Book 2"]  # Проверка избранного

    collector.delete_book_from_favorites("Book 1")
    assert collector.get_list_of_favorites_books() == ["Book 2"]  # После удаления книга должна исчезнуть
