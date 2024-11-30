import pytest
from main import BooksCollector


# Фикстура для создания объекта BooksCollector
@pytest.fixture
def collector():
    return BooksCollector()


# Тестирование метода add_new_book
# Проверка добавления книги с корректным именем
def test_add_new_book_valid_name(collector):
    collector.add_new_book("Book 1")
    assert "Book 1" in collector.books_genre


# Проверка, что жанр книги по умолчанию пустой
def test_add_new_book_default_genre(collector):
    collector.add_new_book("Book 1")
    assert collector.books_genre["Book 1"] == ''


# Проверка, что книга с именем больше 40 символов не добавляется
def test_add_new_book_invalid_name_length(collector):
    collector.add_new_book("A" * 41)
    assert "A" * 41 not in collector.books_genre


# Проверка, что одна и та же книга не добавляется дважды
def test_add_new_book_duplicate(collector):
    collector.add_new_book("Book 1")
    collector.add_new_book("Book 1")
    assert list(collector.books_genre.keys()).count("Book 1") == 1


# Тестирование метода set_book_genre
# Проверка установки жанра книги
def test_set_book_genre_valid(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.get_book_genre("Book 1") == "Фантастика"


# Проверка, что жанр, который не существует в списке, не устанавливается
def test_set_book_genre_invalid(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Роман")
    assert collector.get_book_genre("Book 1") == ''


# Тестирование метода get_book_genre
# Проверка получения жанра книги
def test_get_book_genre(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.get_book_genre("Book 1") == "Фантастика"


# Проверка, что для книги, у которой не установлен жанр, возвращается пустое значение
def test_get_book_genre_no_genre(collector):
    collector.add_new_book("Book 2")
    assert collector.get_book_genre("Book 2") == ''


# Тестирование метода get_books_with_specific_genre
# Проверка получения списка книг с определённым жанром
def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Фантастика")

    assert collector.get_books_with_specific_genre("Фантастика") == ["Book 1", "Book 3"]
    assert collector.get_books_with_specific_genre("Ужасы") == ["Book 2"]
    assert collector.get_books_with_specific_genre("Комедии") == []


# Тестирование метода get_books_genre
# Проверка возврата словаря всех книг с жанрами
def test_get_books_genre(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")

    expected = {
        "Book 1": "Фантастика",
        "Book 2": "Ужасы"
    }
    assert collector.get_books_genre() == expected


# Тестирование метода get_books_for_children
# Проверка фильтрации книг, подходящих детям
def test_get_books_for_children(collector):
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


# Тестирование метода add_book_in_favorites
# Проверка добавления книги в избранное
def test_add_book_in_favorites(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    assert "Book 1" in collector.favorites


# Проверка, что книга не добавляется в избранное повторно
def test_add_book_in_favorites_duplicate(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 1")
    assert collector.favorites.count("Book 1") == 1


# Тестирование метода delete_book_from_favorites
# Проверка удаления книги из избранного
def test_delete_book_from_favorites(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    collector.delete_book_from_favorites("Book 1")
    assert "Book 1" not in collector.favorites


# Проверка удаления несуществующей книги из избранного
def test_delete_book_from_favorites_not_in_list(collector):
    collector.add_new_book("Book 1")
    collector.delete_book_from_favorites("Book 2")  # Книга нет в избранном
    assert len(collector.favorites) == 0


# Тестирование метода get_list_of_favorites_books
# Проверка получения списка избранных книг
def test_get_list_of_favorites_books(collector):
    collector.add_new_book("Book 1")
    collector.add_new_book("Book 2")
    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 2")

    assert collector.get_list_of_favorites_books() == ["Book 1", "Book 2"]

    collector.delete_book_from_favorites("Book 1")
    assert collector.get_list_of_favorites_books() == ["Book 2"]
