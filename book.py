class Book:
    def __init__(self,book_id,title,author,issued = False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
         return {
            "Book_id": self.book_id,
            "Title": self.title,
            "Author": self.author,
            "Issued": self.issued
        }