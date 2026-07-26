import json
from book import Book
from logger import logger
from datetime import datetime, timedelta
from auth import *
import csv
import os
import shutil

def addbook(books):
    try:
        book_id = int(input("Enter your Book Id: "))
        if book_id <= 0:
            print("Book ID must be greater than 0.")
            return
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
        title = input("Enter your Book Title: ").strip()
        if not title:
            print("Book Title cannot be empty.")
            return

        author = input("Enter your Book Author name: ").strip()
        if not author:
            print("Author name cannot be empty.")
            return
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
    logger.info("Viewed all books")
    if not books:
        print("\nNo books available.\n")
        return
    
    for book in books:
            print_book(book)
    print("\n")

def view_book(books):
    while True:
        print("1. Search by Book ID.\n2. Search by Book Name.\n3. Search by Book Author.\n4. Exit")
        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue 
                
        if choice == 1:
            try:
                book_id = int(input("Enter your Book Id: "))
                if book_id <= 0:
                    print("Book ID must be greater than 0.")
                    return
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

        elif choice == 2:
            found = False
            try:
                book_name = (input("Enter your Book Name: ")).strip()
                if not book_name:
                    print("Book name cannot be empty")
                    return
            except ValueError:
                print("Invalid Book Name! Please enter correct value...")
                logger.error("Invalid Book Name entered while searching.")
                return
            for book in books:
                if book_name.lower() in book["Title"].lower():
                    print_book(book)
                    print()
                    logger.info(f"Book searched: Name={book_name}")
                    found = True
            if not found:
                print("Book not found")
                logger.warning(f"Search failed. Book Name {book_name} not found.")

        elif choice == 3:
            found = False
            try:
                book_author = (input("Enter your Book Author: ")).strip()
                if not book_author:
                    print("Book Author cannot be empty")
                    return
            except ValueError:
                print("Invalid Book Author! Please enter correct value...")
                logger.error("Invalid Book Author entered while searching.")
                return
            for book in books:
                if book_author.lower() in book["Author"].lower():
                    print_book(book)
                    print()
                    logger.info(f"Book searched: Author={book_author}")
                    found = True
            if not found:
                print("Book not found")
                logger.warning(f"Search failed. Book Author {book_author} not found.")

        elif choice == 4:
            return

        else:
           print("Invalid Choice")

def del_book(books):
    found = False
    try:
        print("\nEnter Book Id you want to delete Book.....")
        book_id = int(input("\nEnter your Book Id: "))
        if book_id <= 0:
            print("Book ID must be greater than 0.")
            return
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

def issue_book(books,username):
    try:
        print("\nEnter Book Id you want to issue Book....")
        book_id = int(input("\nEnter your Book Id: "))
        if book_id <= 0:
            print("Book ID must be greater than 0.")
            return
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
                today = (datetime.today()).date()
                due_date = (today + timedelta(days = 7))
                book["Issue_date"] = str(today)
                book["Due_date"] = str(due_date)
                print(f"Due Date : {due_date}")
                logger.info(f"Book issued: ID={book_id}")
                history = load_history()
                history_data = {
                    "Username" : username,
                    "Book_id": book["Book_id"],
                    "Title": book["Title"],
                    "Author": book["Author"],
                    "Issued": book["Issued"],
                    "Issue_date" : str(today),
                    "Due_date": str(due_date),
                    "return_date" : ""
                }
                history.append(history_data)
                save_history(history)
                print("Book Issued Successfully")
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

def return_book(books,username):
    try:
        print("\nEnter Book Id you want to return Book....")
        book_id = int(input("\nEnter your Book Id: "))
        if book_id <= 0:
            print("Book ID must be greater than 0.")
            return
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
                history = load_history()
                today = (datetime.today()).date()
                due_date = datetime.strptime(book["Due_date"], "%Y-%m-%d").date()
                if due_date < today:
                    late_days = (today - due_date).days
                    fine = late_days * 50
                    print(f"Late by {late_days} day(s)")
                    print(f"Fine = ₹{fine}")
                    book["Fine"] = fine
                else:
                    fine = 0
                book["Issue_date"] = ""
                book["Due_date"] = ""
                print(f"Return Date : {today}")
                book["Return_date"] = str(today)
                for record in history:
                    if (record["Username"] == username and record["Book_id"] == book_id and record["return_date"] == ""):
                        record["return_date"] = str(today)
                        if due_date < today:
                            record["Fine"] = fine
                        else:
                            record["Fine"] = 0
                        break
                    
                save_history(history)
                print("Book Returned Successfully")
                logger.info(f"Book returned: ID={book_id}")
                print_book(book)
                if book.get("Reserved_By", "") != "":
                    print(f"\nBook is reserved by {book['Reserved_By']}")
                    logger.info(f"Reserved book available for {book['Reserved_By']}")
                print()
            else:
              found = True
              print("Already Returned Book")
              logger.warning(f"Return failed. Book ID {book_id} already returned.")
            break
    
    if not found:
        print("\nBook not found")
        logger.warning(f"Return failed. Book ID {book_id} not found.")
        print("\nAvailable Books:")
        available_books(books)

    save_file(books)

def update_book(books):
    try:
        print("\nEnter Book Id you want to update Book....")
        book_id = int(input("\nEnter your Book Id: "))
        if book_id <= 0:
            print("Book ID must be greater than 0.")
            return
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
                        upd_title = input("\nEnter new Book Title: ").strip()
                        if not upd_title:
                           print("Author name cannot be empty.")
                           continue
                        book["Title"] = upd_title
                        print("Book Title successfully updeted....")
                        logger.info(f"Book title updated for ID {book['Book_id']}")
                    except ValueError:
                        print("Invalid Book Title! Please enter Correct....")
                        continue

                elif choice == 3:
                    try:
                        upd_author = input("\nEnter new Book Author: ").strip()
                        if not upd_author:
                            print("Author name cannot be empty.")
                            continue
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
    logger.info("Viewed library statistics")
    total = len(books)
    available = 0
    issued = 0

    for book in books:
        if book["Issued"]:
            issued += 1
        else:
            available += 1

    print(f"""
Total Books     : {total}
Available Books : {available}
Issued Books    : {issued}
""")

def load_books():
    try:
       with open("book.json","r") as file:
        Books = json.load(file)
        return Books
    except (FileNotFoundError , json.JSONDecodeError):
        return []

def save_file(books):
    with open("book.json", "w") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)

def print_book(book):
    print("-" * 15, "Book Detail", "-" * 15)
    print("-" * 30)
    print(f"Book ID    : {book['Book_id']}")
    print(f"Title      : {book['Title']}")
    print(f"Author     : {book['Author']}")
    print(f"Issued     : {book['Issued']}")
    print(f"Issue Date : {book.get('Issue_date','-')}")
    print(f"Due Date   : {book.get('Due_date','-')}")
    print("-" * 30)

def available_books(books):
    logger.info("Viewed available books")
    print("\nAvailable Books\n")
    found = False

    for book in books:
        if not book["Issued"]:
            print_book(book)
            found = True

    if not found:
        print("No available books.")

def issued_books(books):
    logger.info("Viewed issued books")
    print("\nIssued Books\n")
    found = False

    for book in books:
        if book["Issued"]:
            print_book(book)
            found = True

    if not found:
        print("No issued books.")

def load_history():
    try:
        with open("history.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open("history.json","w") as file:
        json.dump(history,file,indent=4)

def view_history(username):
    logger.info(f"History viewed by user: {username}")
    found = False
    history = load_history()
    for record in history:
        if record["Username"] == username:
            print("-" * 30)
            print(f"Book ID     : {record['Book_id']}")
            print(f"Title       : {record['Title']}")
            print(f"Author      : {record['Author']}")
            print(f"Issue Date  : {record['Issue_date']}")
            print(f"Return Date : {record['return_date']}")
            print(f"Fine        : ₹{record.get('Fine', 0)}")
            print("-" * 30)
            found = True

    if not found:
        logger.warning(f"No history found for user: {username}")
        print("No history found")

def view_all_history():
    logger.info("Admin viewed all history")
    history = load_history()

    if not history:
        logger.warning("Admin tried to view history but no history found.")
        print("No history found.")
        return

    for record in history:
        print("-" * 30)
        print(f"Username    : {record['Username']}")
        print(f"Book ID     : {record['Book_id']}")
        print(f"Title       : {record['Title']}")
        print(f"Author      : {record['Author']}")
        print(f"Issue Date  : {record['Issue_date']}")
        print(f"Return Date : {record['return_date']}")
        print(f"Fine        : ₹{record.get('Fine', 0)}")
        print("-" * 30)

def dashboard(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can view dashboard.")
        logger.warning("Unauthorized dashboard access.")
        return

    users = load_file()
    books = load_books()
    total_users = len(users)
    total_admins = sum(1 for user in users if user["Role"] == "admin")
    total_normal_users = total_users - total_admins

    total_books = len(books)
    issued_books = sum(1 for book in books if book["Issued"])
    available_books = total_books - issued_books

    print("\n========== DASHBOARD ==========")
    print(f"Total Users      : {total_users}")
    print(f"Admins           : {total_admins}")
    print(f"Users            : {total_normal_users}")
    print("--------------------------------")
    print(f"Total Books      : {total_books}")
    print(f"Issued Books     : {issued_books}")
    print(f"Available Books  : {available_books}")
    print("================================")

    logger.info("Admin viewed dashboard.")

def view_all_users(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can view all users.")
        logger.warning("Non-admin tried to view all users.")
        return

    users = load_file()

    if not users:
        print("No users found.")
        return

    print("\n========== ALL USERS ==========")

    for i, user in enumerate(users, start=1):
        print(f"\nUser {i}")
        print(f"Username : {user['Username']}")
        print(f"Email    : {user['Email']}")
        print(f"Role     : {user['Role']}")
        print("-" * 30)

    logger.info("Admin viewed all users.")

def change_user_role(current_user, current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can change user roles.")
        logger.warning(f"{current_user} tried to change user role.")
        return

    users = load_file()

    username = input("Enter username: ").strip()

    for user in users:
        if user["Username"] == username:

            if username == current_user:
                print("You cannot change your own role.")
                return

            print(f"\nCurrent Role : {user['Role']}")
            print("1. Admin")
            print("2. User")

            choice = input("Select new role: ").strip()

            if choice == "1":
                new_role = "admin"
            elif choice == "2":
                new_role = "user"
            else:
                print("Invalid choice.")
                return

            if user["Role"] == new_role:
                print("User already has this role.")
                return

            # Prevent removing the last admin
            if user["Role"] == "admin" and new_role == "user":
                admin_count = sum(1 for u in users if u["Role"] == "admin")
                if admin_count == 1:
                    print("Cannot change role of the last admin.")
                    logger.warning("Attempt to remove last admin role.")
                    return

            user["Role"] = new_role
            save_file(users)

            logger.info(f"{current_user} changed {username}'s role to {new_role}.")
            print("Role updated successfully.")
            return

    print("User not found.")
    logger.warning(f"Role change failed. User '{username}' not found.")

def search_user(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can search users.")
        logger.warning("Unauthorized search user attempt.")
        return

    users = load_file()

    username = input("Enter username to search: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    for user in users:
        if username.lower() == user["Username"].lower():
            print("\n===== USER DETAILS =====")
            print(f"Username : {user['Username']}")
            print(f"Email    : {user['Email']}")
            print(f"Role     : {user['Role']}")
            print("========================")

            logger.info(f"Admin searched user: {username}")
            return

    print("User not found.")
    logger.warning(f"Search failed. User '{username}' not found.")

def export_books_csv(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can export books.")
        logger.warning("Unauthorized export books attempt.")
        return

    books = load_books()

    if not books:
        print("No books available.")
        return

    try:
        with open("books.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Book ID",
                "Title",
                "Author",
                "Issued",
                "Issue Date",
                "Due Date"
            ])

            for book in books:
                writer.writerow([
                    book["Book_id"],
                    book["Title"],
                    book["Author"],
                    book["Issued"],
                    book.get("Issue_date", ""),
                    book.get("Due_date", "")
                ])

        print("Books exported successfully to books.csv")
        logger.info("Books exported to books.csv")

    except Exception as e:
        print("Export failed.")
        logger.error(f"Export Books CSV Error: {e}")

def export_history_csv(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can export history.")
        logger.warning("Unauthorized export history attempt.")
        return

    history = load_history()

    if not history:
        print("No history available.")
        logger.warning("Export failed. No history found.")
        return

    try:
        with open("history.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Username",
                "Book ID",
                "Title",
                "Author",
                "Issue Date",
                "Due Date",
                "Return Date",
                "Fine"
            ])

            for record in history:
                writer.writerow([
                    record["Username"],
                    record["Book_id"],
                    record["Title"],
                    record["Author"],
                    record["Issue_date"],
                    record["Due_date"],
                    record["return_date"],
                    record.get("Fine", 0)
                ])

        print("History exported successfully to history.csv")
        logger.info("History exported to history.csv")

    except Exception as e:
        print("Export failed.")
        logger.error(f"Export History CSV Error: {e}")

def backup_database(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can create backup.")
        logger.warning("Unauthorized backup attempt.")
        return

    backup_folder = "backup"

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    files = [
        "book.json",
        "users.json",
        "history.json"
    ]

    try:
        for file in files:
            if os.path.exists(file):
                filename = f"{timestamp}_{file}"
                destination = os.path.join(backup_folder, filename)
                shutil.copy(file, destination)

        print("Database backup created successfully.")
        logger.info("Database backup created.")

    except Exception as e:
        print("Backup failed.")
        logger.error(f"Backup Error: {e}")

def library_statistics(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can view library statistics.")
        logger.warning("Unauthorized library statistics access.")
        return

    books = load_books()
    history = load_history()

    total_books = len(books)
    issued_books = 0
    available_books = 0

    for book in books:
        if book["Issued"]:
            issued_books += 1
        else:
            available_books += 1

    total_issued = len(history)

    returned_books = 0
    pending_returns = 0
    total_fine = 0

    for record in history:
        if record["return_date"]:
            returned_books += 1
        else:
            pending_returns += 1

        total_fine += record.get("Fine", 0)

    print("\n========== LIBRARY STATISTICS ==========")
    print(f"Total Books        : {total_books}")
    print(f"Available Books    : {available_books}")
    print(f"Issued Books       : {issued_books}")
    print("----------------------------------------")
    print(f"Total Issues       : {total_issued}")
    print(f"Returned Books     : {returned_books}")
    print(f"Pending Returns    : {pending_returns}")
    print("----------------------------------------")
    print(f"Total Fine Collected : ₹{total_fine}")
    print("========================================")

    logger.info("Admin viewed library statistics.")

def reserve_book(books, username):

    try:
        book_id = int(input("Enter Book ID to reserve: "))
    except ValueError:
        print("Invalid Book ID.")
        return

    for book in books:

        if book["Book_id"] == book_id:

            if not book["Issued"]:
                print("Book is available. You can issue it directly.")
                return

            if book.get("Reserved_By", "") != "":
                print("Book is already reserved.")
                return

            book["Reserved_By"] = username
            save_file(books)

            logger.info(f"{username} reserved Book ID {book_id}")
            print("Book reserved successfully.")
            return

    print("Book not found.")
    