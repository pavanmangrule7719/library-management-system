from operations import *
from logger import logger

while True:
    print("""
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
5. Issue Book
6. Return Book
7. Update Book
8. Total Books
9. Exit
""")

    choice = int(input("Enter your choice: "))

    books = load_file()

    if choice == 1:
        addbook(books)

    elif choice == 2:
        view_all_book(books)

    elif choice == 3:
        view_book(books)

    elif choice == 4:
        del_book(books)

    elif choice == 5:
        issue_book(books)

    elif choice == 6:
        return_book(books)

    elif choice == 7:
        update_book(books)

    elif choice == 8:
        total_books(books)

    elif choice == 9:
        logger.info("Application closed.")
        break
