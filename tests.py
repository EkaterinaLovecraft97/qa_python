import pytest
from main import BooksCollector


# Фикстура для создания объекта BooksCollector
@pytest.fixture
def collector():
    return BooksCollector()


# Тестирование метода add_new_book
def test_add_new_book_valid_name(collector):
    collector.add_new_book("Book 1")
    assert "Book 1" in collector.books_genre


def test_add_new_book_empty_genre_by_default(collector):
    collector.add_new_book("Book 1")
    assert collector.books_genre["Book 1"] == ''


def test_add_new_book_name_length_40(collector):
    name = "A" * 40
    collector.add_new_book(name)
    assert name in collector.books_genre


def test_add_new_book_invalid_name_length(collector):
    collector.add_new_book("A" * 41)
    assert len(collector.books_genre) == 0


def test_add_new_book_duplicate(collector):
    collector.add_new_book("Book 1")
    collector.add_new_book("Book 1")
    assert len(collector.books_genre) == 1


# Тестирование метода set_book_genre
def test_set_book_genre_valid(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.books_genre["Book 1"] == "Фантастика"


def test_set_book_genre_invalid(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Роман")
    assert collector.books_genre["Book 1"] == ''


# Тестирование метода get_book_genre
def test_get_book_genre_returns_correct_value(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    assert collector.get_book_genre("Book 1") == "Фантастика"


# Тестирование метода get_books_with_specific_genre
def test_get_books_with_specific_genre_fantasy(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Фантастика")

    assert collector.get_books_with_specific_genre("Фантастика") == ["Book 1", "Book 3"]


def test_get_books_with_specific_genre_no_matches(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Ужасы")
    assert collector.get_books_with_specific_genre("Фантастика") == []


# Тестирование метода get_books_genre
def test_get_books_genre_empty(collector):
    assert collector.get_books_genre() == {}


def test_get_books_genre_with_books(collector):
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
def test_get_books_for_children_empty(collector):
    assert collector.get_books_for_children() == []


def test_get_books_for_children_with_books(collector):
    collector.add_new_book("Book 1")
    collector.set_book_genre("Book 1", "Фантастика")
    collector.add_new_book("Book 2")
    collector.set_book_genre("Book 2", "Ужасы")
    collector.add_new_book("Book 3")
    collector.set_book_genre("Book 3", "Детективы")
    collector.add_new_book("Book 4")
    collector.set_book_genre("Book 4", "Мультфильмы")

    assert collector.get_books_for_children() == ["Book 1", "Book 4"]


# Тестирование метода add_book_in_favorites
def test_add_book_in_favorites(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    assert "Book 1" in collector.favorites


def test_add_book_in_favorites_duplicate(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 1")
    assert collector.favorites.count("Book 1") == 1


# Тестирование метода delete_book_from_favorites
def test_delete_book_from_favorites_existing(collector):
    collector.add_new_book("Book 1")
    collector.add_book_in_favorites("Book 1")
    collector.delete_book_from_favorites("Book 1")
    assert "Book 1" not in collector.favorites


def test_delete_book_from_favorites_non_existing(collector):
    collector.delete_book_from_favorites("Book 1")
    assert len(collector.favorites) == 0


# Тестирование метода get_list_of_favorites_books
def test_get_list_of_favorites_books(collector):
    collector.add_new_book("Book 1")
    collector.add_new_book("Book 2")
    collector.add_book_in_favorites("Book 1")
    collector.add_book_in_favorites("Book 2")

    assert collector.get_list_of_favorites_books() == ["Book 1", "Book 2"]
