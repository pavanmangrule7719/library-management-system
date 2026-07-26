import json
import hashlib
import random
import smtplib
import os
import time
from email.message import EmailMessage
from logger import logger

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_file():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_file(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def generate_otp():
    return random.randint(100000, 999999)

def send_otp(receiver_email, subject):

    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    APP_PASSWORD = os.getenv("APP_PASSWORD")

    otp = generate_otp()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

Your OTP is: {otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Thank You.
""")

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(SENDER_EMAIL,APP_PASSWORD)
            server.send_message(msg)

        logger.info(f"OTP sent successfully to {receiver_email}")
        return otp

    except Exception as e:
        logger.error(f"Failed to send OTP : {e}")
        print("Failed to send OTP.")
        return None

def verify_otp(email, subject, username):

    otp = send_otp(email, subject)

    if otp is None:
        return False

    otp_time = time.time()

    otp_expiry = 300
    max_attempts = 3
    max_resends = 3

    attempts = 0
    resend_count = 0

    while True:

        current_time = time.time()

        if current_time - otp_time < otp_expiry:

            try:
                user_otp = int(input("Enter OTP : "))
            except ValueError:
                attempts += 1

                print("OTP must contain digits only.")
                print(f"Remaining Attempts : {max_attempts-attempts}")

                if attempts >= max_attempts:
                    logger.warning(f"{username} exceeded OTP attempts.")
                    return False

                continue

            if user_otp == otp:
                logger.info(f"OTP verified for {username}")
                return True

            attempts += 1

            if attempts >= max_attempts:
                print("Too many invalid attempts.")
                logger.warning(f"{username} entered invalid OTP 3 times.")
                return False

            print(f"Remaining Attempts : {max_attempts-attempts}")

        else:

            logger.warning(f"OTP expired for {username}")

            print("""
OTP Expired

1. Resend OTP
2. Cancel
""")

            choice = input("Enter choice : ").strip()

            if choice == "1":

                if resend_count >= max_resends:
                    print("Resend limit exceeded.")
                    logger.warning(f"{username} exceeded resend limit.")
                    return False

                resend_count += 1

                otp = send_otp(email, subject)

                if otp is None:
                    return False

                otp_time = time.time()
                attempts = 0

                print("New OTP sent successfully.")
                print(f"Remaining Resends : {max_resends-resend_count}")

            elif choice == "2":
                logger.info(f"{username} cancelled OTP verification.")
                return False

            else:
                print("Invalid Choice.")

def register():
    users = load_file()

    username = input("Enter Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        logger.warning("Registration failed: Empty username.")
        return

    if len(username) < 3:
        print("Username must be at least 3 characters.")
        logger.warning("Registration failed: Username too short.")
        return

    for user in users:
        if user["Username"].lower() == username.lower():
            print("Username already exists.")
            logger.warning(f"Registration failed: Username '{username}' already exists.")
            return

    password = input("Enter Password: ").strip()

    if not password:
        print("Password cannot be empty.")
        logger.warning(f"{username}: Empty password.")
        return

    if len(password) < 6:
        print("Password must be at least 6 characters.")
        logger.warning(f"{username}: Password too short.")
        return

    confirm_password = input("Confirm Password: ").strip()

    if password != confirm_password:
        print("Passwords do not match.")
        logger.warning(f"{username}: Password confirmation failed.")
        return

    hashed_password = hash_password(password)

    email = input("Enter Email: ").strip()

    if not email:
        print("Email cannot be empty.")
        logger.warning(f"{username}: Empty email.")
        return

    if "@" not in email or "." not in email:
        print("Invalid Email.")
        logger.warning(f"{username}: Invalid email format.")
        return

    for user in users:
        if user["Email"].lower() == email.lower():
            print("Email already registered.")
            logger.warning(f"{username}: Email already exists.")
            return

    if not verify_otp(email, "Email Verification OTP", username):
        return

    while True:
        role = input("Enter Role (admin/user): ").strip().lower()

        if role in ("admin", "user"):
            break

        print("Invalid Role.")
        logger.warning(f"{username}: Invalid role entered.")

    users.append({
        "Username": username,
        "Email": email,
        "Password": hashed_password,
        "Role": role
    })

    save_file(users)

    logger.info(f"New user registered: {username} ({role})")

    print("\nRegistration Successful.\n")

def login():
    users = load_file()

    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    if not username or not password:
        print("Username and Password are required.")
        logger.warning("Login failed: Empty credentials.")
        return None, None

    hashed = hash_password(password)

    for user in users:

        if user["Username"] == username:

            if user["Password"] == hashed:

                logger.info(f"{username} logged in successfully.")
                print("\nLogin Successful.\n")

                return user["Username"], user["Role"]

            logger.warning(f"Wrong password entered by {username}")
            print("Invalid Password.")
            return None, None

    logger.warning(f"Username not found: {username}")
    print("Invalid Username.")

    return None, None

def change_password(username):
    users = load_file()

    for user in users:
        if user["Username"] == username:

            old_password = input("Enter Old Password: ").strip()

            if hash_password(old_password) != user["Password"]:
                print("Old password is incorrect.")
                logger.warning(f"{username} entered wrong old password.")
                return

            new_password = input("Enter New Password: ").strip()

            if not new_password:
                print("Password cannot be empty.")
                return

            if len(new_password) < 6:
                print("Password must be at least 6 characters.")
                return

            confirm = input("Confirm New Password: ").strip()

            if confirm != new_password:
                print("Passwords do not match.")
                return

            hashed = hash_password(new_password)

            if hashed == user["Password"]:
                print("New password cannot be same as old password.")
                logger.warning(f"{username} tried to reuse old password.")
                return

            user["Password"] = hashed

            save_file(users)

            logger.info(f"{username} changed password successfully.")

            print("Password changed successfully.")

            return

    logger.warning(f"Password change failed. User '{username}' not found.")

def reset_password():

    users = load_file()

    username = input("Enter Username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    for user in users:

        if user["Username"] == username:

            if not verify_otp(user["Email"], "Password Reset OTP", username):
                return

            while True:

                password = input("Enter New Password: ").strip()

                if not password:
                    print("Password cannot be empty.")
                    continue

                if len(password) < 6:
                    print("Password must be at least 6 characters.")
                    continue

                confirm = input("Confirm Password: ").strip()

                if confirm != password:
                    print("Passwords do not match.")
                    continue

                hashed = hash_password(password)

                if hashed == user["Password"]:
                    print("New password cannot be same as old password.")
                    continue

                user["Password"] = hashed

                save_file(users)

                logger.info(f"Password reset successfully for {username}")

                print("Password reset successfully.")

                return

    print("Username not found.")
    logger.warning(f"Password reset failed. Username '{username}' not found.")

def view_profile(username):
    users = load_file()

    for user in users:
        if user["Username"] == username:

            print("\n========== MY PROFILE ==========")
            print(f"Username : {user['Username']}")
            print(f"Email    : {user['Email']}")
            print(f"Role     : {user['Role']}")
            print("================================")

            logger.info(f"{username} viewed profile.")
            return

    print("User not found.")
    logger.warning(f"Profile not found for {username}")

def update_profile(username):

    users = load_file()

    while True:

        print("""
========== UPDATE PROFILE ==========
1. Change Username
2. Change Email
3. Back
====================================
""")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            for user in users:

                if user["Username"] == username:

                    new_username = input("Enter New Username: ").strip()

                    if not new_username:
                        print("Username cannot be empty.")
                        break

                    if len(new_username) < 3:
                        print("Username must be at least 3 characters.")
                        break

                    exists = any(
                        u["Username"].lower() == new_username.lower()
                        for u in users
                    )

                    if exists:
                        print("Username already exists.")
                        logger.warning(f"{username} tried existing username.")
                        break

                    user["Username"] = new_username

                    save_file(users)

                    logger.info(f"{username} changed username to {new_username}")

                    print("Username updated successfully.")

                    username = new_username

                    break

        elif choice == "2":

            for user in users:

                if user["Username"] == username:

                    new_email = input("Enter New Email: ").strip()

                    if not new_email:
                        print("Email cannot be empty.")
                        break

                    if "@" not in new_email or "." not in new_email:
                        print("Invalid Email.")
                        break

                    exists = any(
                        u["Email"].lower() == new_email.lower()
                        for u in users
                    )

                    if exists:
                        print("Email already registered.")
                        logger.warning(f"{username} tried existing email.")
                        break

                    if not verify_otp(
                        new_email,
                        "Email Change OTP",
                        username
                    ):
                        break

                    user["Email"] = new_email

                    save_file(users)

                    logger.info(f"{username} changed email.")

                    print("Email updated successfully.")

                    break

        elif choice == "3":
            return

        else:
            print("Invalid choice.")

def delete_user(current_user, current_role):

    if current_role != "admin":
        print("Access Denied!")
        logger.warning(f"{current_user} tried to delete user.")
        return

    users = load_file()

    username = input("Enter Username to Delete: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    if username == current_user:
        print("You cannot delete your own account.")
        logger.warning(f"{current_user} tried deleting own account.")
        return

    for user in users:

        if user["Username"] == username:

            if user["Role"] == "admin":

                admin_count = sum(
                    1
                    for u in users
                    if u["Role"] == "admin"
                )

                if admin_count == 1:
                    print("Cannot delete the last admin.")
                    logger.warning("Attempt to delete last admin.")
                    return

            confirm = input(
                f"Delete '{username}' ? (yes/no): "
            ).strip().lower()

            if confirm != "yes":
                print("Delete cancelled.")
                logger.info(f"{current_user} cancelled deletion.")
                return

            users.remove(user)

            save_file(users)

            logger.info(
                f"{current_user} deleted user '{username}'."
            )

            print("User deleted successfully.")

            return

    print("User not found.")

    logger.warning(f"Delete failed. '{username}' not found.")

def view_all_users(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can view all users.")
        logger.warning("Unauthorized access to view all users.")
        return

    users = load_file()

    if not users:
        print("No users found.")
        logger.info("No users available.")
        return

    print("\n==================== ALL USERS ====================")
    print(f"{'Username':<20}{'Role':<10}{'Email'}")
    print("-" * 55)

    for user in users:
        print(f"{user['Username']:<20}{user['Role']:<10}{user['Email']}")

    print("=" * 55)

    logger.info("Admin viewed all users.")

def search_user(current_role):
    if current_role != "admin":
        print("Access Denied! Only admin can search users.")
        logger.warning("Unauthorized user search attempt.")
        return

    users = load_file()

    username = input("Enter Username to Search: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    for user in users:
        if user["Username"].lower() == username.lower():

            print("\n========== USER DETAILS ==========")
            print(f"Username : {user['Username']}")
            print(f"Email    : {user['Email']}")
            print(f"Role     : {user['Role']}")
            print("==================================")

            logger.info(f"Admin searched user: {username}")
            return

    print("User not found.")
    logger.warning(f"Search failed. User '{username}' not found.")

