from auth import *
from operations import *
from logger import logger

def admin_menu(username, role):
    while True:
        print("""
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
5. Issue Book
6. Return Book
7. Update Book
8. Library Statistics
9. Available Books
10. Issued Books
11. View All History
12. Export Books CSV
13. Export History CSV
14. Change Password
15. Reset Password
16. Delete User
17. View Profile
18. Update Profile
19. Dashboard
20. View All Users
21. Change User Role
22. Book Reservation
23. Review Admin Requests
24. Logout
""")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        books = load_books()

        if choice == 1:
            addbook(books)

        elif choice == 2:
            view_all_book(books)

        elif choice == 3:
            view_book(books)

        elif choice == 4:
            del_book(books)

        elif choice == 5:
            issue_book(books, username)

        elif choice == 6:
            return_book(books, username)

        elif choice == 7:
            update_book(books)

        elif choice == 8:
            total_books(books)

        elif choice == 9:
            available_books(books)

        elif choice == 10:
            issued_books(books)

        elif choice == 11:
            view_all_history()

        elif choice == 12:
            export_books_csv(role)

        elif choice == 13:
            export_history_csv(role)

        elif choice == 14:
            change_password(username)

        elif choice == 15:
            reset_password()

        elif choice == 16:
            delete_user(username, role)

        elif choice == 17:
            view_profile(username)

        elif choice == 18:
            update_profile(username)

        elif choice == 19:
            dashboard(role)

        elif choice == 20:
            view_all_users(role)

        elif choice == 21:
            change_user_role(username, role)

        elif choice == 22:
            reserve_book(books, username)

        elif choice == 24:
            review_admin_requests(username, role)

        elif choice == 23:
            logger.info(f"{username} logged out.")
            break

        else:
            print("Invalid choice.")

def user_menu(username):
    while True:
        print("""
1. View All Books
2. Search Book
3. Available Books
4. Issue Book
5. Return Book
6. View History
7. Issued Books
8. Change Password
9. Reset Password
10. View Profile
11. Update Profile
12. Book Reservation
13. Library Statistics
14. Request Admin Access
15. Logout
""")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        books = load_books()

        if choice == 1:
            view_all_book(books)

        elif choice == 2:
            view_book(books)

        elif choice == 3:
            available_books(books)

        elif choice == 4:
            issue_book(books, username)

        elif choice == 5:
            return_book(books, username)

        elif choice == 6:
            view_history(username)

        elif choice == 7:
            issued_books(books)

        elif choice == 8:
            change_password(username)

        elif choice == 9:
            reset_password()

        elif choice == 10:
            view_profile(username)

        elif choice == 11:
            update_profile(username)

        elif choice == 12:
            reserve_book(books, username)

        elif choice == 13:
            total_books(books)

        elif choice == 14:
            request_admin_access(username)

        elif choice == 15:
            logger.info(f"{username} logged out.")
            break

        else:
            print("Invalid choice.")

while True:
    print("\n1. Register\n2. Login\n3. Exit")

    try:
        choice = int(input("Enter your choice(1-3): "))
    except ValueError:
        print("Please enter correct value....")
        continue

    if choice == 1:
        register()

    elif choice == 2:
        result = login()

        if result:
            username, role = result

            if role == "admin":
                print("Welcome Admin")
                admin_menu(username, role)

            elif role == "user":
               print("Welcome User")
               user_menu(username)

            else:
                print("Role not exits")

    elif choice == 3:
        print("Thank you for using Library Management System.")
        logger.info("Application closed.")
        break

    else:
        print("Invalid choice")