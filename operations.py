import json
from book import Book
from logger import logger

def addbook(books):
    try:
        book_id = int(input("Enter your Book Id: "))
        for book in books:
            if book["Book_id"] == book_id:
                print("Book ID already exists.")
                logger.warning(f"Duplicate Book ID: {book_id}")
                return
    except ValueError:
        print("Invalid Book ID! Please enter numbers only....")
        logger.error("Invalid Book ID entered while adding book.")
        return

    try:
        title = input("Enter your Book Title: ")
        author = input("Enter your Book Author name: ")

    except ValueError:
        print("Invalid Book Details! Please enter Correct....")
        return
    
    B = Book(book_id,title,author)
    book_data = B.to_dict()

    books.append(book_data)
    save_file(books)
    print("\nBook Added successfully......")
    logger.info(f"Book added: ID={book_id}, Title={title}, Author={author}")
    print_book(book_data)
    print()

def view_all_book(books):
    if not books:
        print("\nNo books available.\n")
        return
    
    for book in books:
            print_book(book)
    print("\n")

def view_book(books):
    while True:
        print("1. Search by Book ID.\n2. Search by Book Name.\n3. Search by Book Auther.\n4. Exit")
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue 
                
        if choice == 1:
            try:
                book_id = int(input("Enter your Book Id: "))
            except ValueError:
                print("Invalid Book ID! Please enter numbers only")
                logger.error("Invalid Book ID entered while searching.")
                return
            for book in books:
                if book["Book_id"] == book_id:
                    print_book(book)
                    print()
                    logger.info(f"Book searched: ID={book_id}")
                    break
            else:
                print("Book not found")
                logger.warning(f"Search failed. Book ID {book_id} not found.")

        if choice == 2:
            try:
                book_name = (input("Enter your Book Name: "))
            except ValueError:
                print("Invalid Book Name! Please enter correct value...")
                logger.error("Invalid Book Name entered while searching.")
                return
            for book in books:
                if book["Title"].lower() == book_name.lower():
                    print_book(book)
                    print()
                    logger.info(f"Book searched: Name={book_name}")
                    break
            else:
                print("Book not found")
                logger.warning(f"Search failed. Book Name {book_name} not found.")

        if choice == 3:
            try:
                book_author = (input("Enter your Book Author: "))
            except ValueError:
                print("Invalid Book Author! Please enter correct value...")
                logger.error("Invalid Book Author entered while searching.")
                return
            for book in books:
                if book["Author"].lower() == book_author.lower():
                    print_book(book)
                    print()
                    logger.info(f"Book searched: Author={book_author}")
                    break
            else:
                print("Book not found")
                logger.warning(f"Search failed. Book Author {book_author} not found.")

        if choice == 4:
            return

def del_book(books):
    found = False
    try:
        print("\nEnter Book Id you want to delete Book.....")
        book_id = int(input("\nEnter your Book Id: "))
    except ValueError:
        print("Invalid Book ID! Please enter numbers only")
        logger.error("Invalid Book ID entered while deleting.")
        return
    for book in books:
        if book["Book_id"] == book_id:
            books.remove(book)
            found = True
            logger.info(f"Book deleted: ID={book_id}")
            break
    if found:
        print("Deleted Successfully........")
    else: 
        print("Book not found")
        logger.warning(f"Delete failed. Book ID {book_id} not found.")
    
    save_file(books)

def issue_book(books):
    try:
        print("\nEnter Book Id you want to issue Book....")
        book_id = int(input("\nEnter your Book Id: "))
    except ValueError:
        print("Invalid Book ID! Please enter numbers only")
        logger.error("Invalid Book ID entered while issuing.")
        return
    found = False
    for book in books:
        if book["Book_id"] == book_id:
            if not book["Issued"]:
                book["Issued"] = True
                found = True
                print("Book Issued Successfully")
                logger.info(f"Book issued: ID={book_id}")
                print_book(book)
                print()
            else:
              found = True
              print("Already Issued")
              logger.warning(f"Issue failed. Book ID {book_id} already issued.")
            break
    
    if not found:
        print("\nBook not found")
        logger.warning(f"Issue failed. Book ID {book_id} not found.")

    save_file(books)

def return_book(books):
    try:
        print("\nEnter Book Id you want to return Book....")
        book_id = int(input("\nEnter your Book Id: "))
    except ValueError:
        print("Invalid Book ID! Please enter numbers only")
        logger.error("Invalid Book ID entered while returning.")
        return
    
    found = False
    for book in books:
        if book["Book_id"] == book_id:
            if book["Issued"]:
                book["Issued"] = False
                found = True
                print("Book Returned Successfully")
                logger.info(f"Book returned: ID={book_id}")
                print_book(book)
                print()
            else:
              found = True
              print("Already Returned Book")
              logger.warning(f"Return failed. Book ID {book_id} already returned.")
            break
    
    if not found:
        print("\nBook not found")
        logger.warning(f"Issue failed. Book ID {book_id} not found.")

    save_file(books)

def update_book(books):
    try:
        print("\nEnter Book Id you want to update Book....")
        book_id = int(input("\nEnter your Book Id: "))
    except ValueError:
        print("Invalid Book ID! Please enter numbers only")
        logger.error("Invalid Book ID entered while updating.")
        return
    
    found = False
    for book in books:
        if book["Book_id"] == book_id:
            found = True
            while True:
                print("1. Update Book ID\n2. Update Book Title\n3. Update Book Author\n4. Save Update and Exit\n5. Cancel")
                try:
                    choice = int(input("\nEnter your choice: "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue 
                
                if choice == 1:
                    try:
                        upd_id = int(input("\nEnter new Book Id: "))
                        for b in books:
                            if b["Book_id"] == upd_id and b["Book_id"] != book["Book_id"]:
                                print("Book ID already exists.")
                                logger.warning(f"Duplicate Book ID: {book_id}")
                                return
                        book["Book_id"] = upd_id
                        print("Book ID successfully updeted....")
                        logger.info(f"Book ID updated from {book_id} to {upd_id}")
                    except ValueError:
                        print("Invalid Book ID! Please enter numbers only")
                        continue
                
                elif choice == 2:
                    try:
                        upd_title = input("\nEnter new Book Title: ")
                        book["Title"] = upd_title
                        print("Book Title successfully updeted....")
                        logger.info(f"Book title updated for ID {book['Book_id']}")
                    except ValueError:
                        print("Invalid Book Title! Please enter Correct....")
                        continue

                elif choice == 3:
                    try:
                        upd_author = input("\nEnter new Book Author: ")
                        book["Author"] = upd_author
                        print("Book Author successfully updeted....")
                        logger.info(f"Book author updated for ID {book['Book_id']}")
                    except ValueError:
                        print("Invalid Book Author! Please enter Correct....")
                        continue

                elif choice == 4:
                    save_file(books)
                    print("Book updated successfully....")
                    logger.info(f"Book updated successfully: ID={book['Book_id']}")
                    print_book(book)
                    print()
                    return
                
                elif choice == 5:
                    logger.info(f"Update cancelled for Book ID {book_id}")
                    return
                
                else:
                    print("Invalid Choice.........\nPlease Enter Correct choice (1 - 4): ")
                    continue

    if not found:
        print("\nBook not found")
        logger.warning(f"Issue failed. Book ID {book_id} not found.")

def total_books(books):
    print(f"\nTotal Books in Library: {len(books)}\n")

def load_file():
    try:
       with open("book.json","r") as file:
        Books = json.load(file)
        return Books
    except (FileNotFoundError , json.JSONDecodeError):
        return []

def save_file(books):
    with open("book.json", "w") as file:
        json.dump(books, file, indent=4)

def print_book(book):
    print("\n----Book Detail----")
    print("-------------------")
    print(f"Book Id: {book['Book_id']}")
    print(f"Title: {book['Title']}")
    print(f"Author: {book['Author']}")
    print(f"Issued: {book['Issued']}")
