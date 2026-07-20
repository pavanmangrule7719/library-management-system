# 📚 Library Management System (Python)

A simple Command Line Library Management System built using Python.

## ✨ Features

- ➕ Add Book
- 📖 View All Books
- 🔍 Search Book by ID
- 🗑️ Delete Book
- 📕 Issue Book
- 📗 Return Book
- ✏️ Update Book Details
- 📊 Show Total Books
- 💾 Store data in JSON
- 📝 Logging using Python logging module

## 🛠️ Technologies Used

- Python 3
- JSON
- Logging Module

## 📂 Project Structure

```
Library_Management/
│── main.py
│── book.py
│── operations.py
│── logger.py
│── book.json
│── library.log
└── README.md
```

## ▶️ How to Run

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/library-management-system.git
```

2. Open the project folder

```bash
cd library-management-system
```

3. Run the project

```bash
python main.py
```

## 📋 Menu

```
1. Add Book
2. View All Books
3. Search Book
4. Delete Book
5. Issue Book
6. Return Book
7. Update Book
8. Total Books
9. Exit
```

## 📁 Data Storage

Book records are stored in `book.json`.

Example:

```json
[
    {
        "Book_id": 1,
        "Title": "Python",
        "Author": "Guido",
        "Issued": false
    }
]
```

## 📝 Logging

All important operations are stored in `library.log`.

Example:

```
Book Added
Book Deleted
Book Issued
Book Returned
Book Updated
Application Closed
```

## 🚀 Future Improvements

- Search by Book Name
- Search by Author
- Login System
- Due Date for Issued Books
- Fine Calculation
- Colored CLI Output

## 👨‍💻 Author

Pavan Mangrule