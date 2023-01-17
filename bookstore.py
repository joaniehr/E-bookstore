import sqlite3

RESET = '\33[0m'
BOLD = '\33[1m'
GREEN = '\33[32m'
PURPLE = '\33[35m'
UNDERLINE = '\33[4m'
RED = '\33[31m'

# creates new database
db = sqlite3.connect("C:\\Users\\joani\\Documents\\HyperionDev\\T48\\ebookstore.db")

# creates cursor object
cursor = db.cursor()

# creates table in database to hold book information
cursor.execute("""
CREATE TABLE books (
ID char(4) NOT NULL,
Title varchar(50) NOT NULL,
Author varchar(50) NOT NULL,
Quantity int NOT NULL,
PRIMARY KEY (ID)
)
""")

# initial book list to be added to table
initial_books = [("3001", "A Tale Of Two Cities", "Charles Dickens", 30),
                 ("3002", "Harry Potter And The Philosopher's Stone", "J.K. Rowling", 40),
                 ("3003", "The Lion, The Witch And The Wardrobe", "C.S. Lewis", 25),
                 ("3004", "The Lord Of The Rings", "J.R.R Tolkien", 37),
                 ("3005", "Alice In Wonderland", "Lewis Carroll", 12),
                 ("3006", "If We Were Villains", "M.L. Rio", 5),
                 ("3007", "A Good Girl's Guide To Murder", "Holly Jackson", 12),
                 ("3008", "Pet", "Akwaeke Emezi", 10),
                 ("3009", "Good Girl, Bad Blood", "Holly Jackson", 14),
                 ("3010", "Six Of Crows", "Leigh Bardugo", 32)]

# adds initial books to table
cursor.executemany("""
INSERT INTO books
VALUES (?,?,?,?)""", initial_books)

# commits db changes
db.commit()


# function to add a book to database
def add_book():
    print("You are now adding a book to the database.")

    # gets book_id, returns error if ID is not 4 chars long and loops until valid
    while True:
        book_id = input("Please enter the ID number of the book: ")
        if len(book_id) == 4:

            # checks if book ID already exists in database to avoid unique ID error
            cursor.execute("""
            SELECT * FROM books
            WHERE ID=?""", (book_id,))

            if cursor.fetchone():
                print("Book ID already exists in database.")
            else:
                break
        else:
            print(f"{RED}Invalid ID.{RESET}")

    # gets book title and author
    book_title = input("Please enter the title of the book: ").title()
    book_author = input("Please enter the author of the book: ").title()

    # gets book quantity, error if not integer, loops until valid
    while True:
        try:
            book_qty = int(input("Please enter the quantity of books in stock: "))
            break
        except ValueError:
            print(f"{RED}Quantity must be an integer.{RESET}")

    # creates tuple from user info
    new_entry = (book_id, book_title, book_author, book_qty)

    # adds new entry to database
    cursor.execute("""
    INSERT INTO books
    VALUES (?,?,?,?)""", new_entry)


# function to delete book from database
def delete_book():
    print("You are going to delete a book from the database.")

    while True:
        book_id = input("Please enter the ID of the book you wish to delete: ")

        # checks if user input is valid book id in database
        cursor.execute("""
        SELECT * FROM books
        WHERE ID=? """, (book_id,))

        # if book is in database, gets confirmation and deletes
        if cursor.fetchone():
            del_confirm = input("Are you sure you would like to delete this book? ").lower()

            if del_confirm == "yes" or del_confirm == "y":
                cursor.execute("""
                DELETE FROM books
                WHERE ID=? """, (book_id,))

                print(f"{GREEN}Book deleted.{RESET}")
                break

            # if confirmation is not yes, asks user if they would like to delete another book
            else:
                del_again = input("Would you like to delete another book? ").lower()

                # if user does not want to delete another book, returns to main menu
                if del_again == "no" or del_again == "n":
                    break

                # else loops to ask for new ID input
                elif del_again == "yes" or del_again == "y":
                    continue

        else:
            print("Invalid ID.")


# function to update book in database
def update_book():
    while True:
        book_id = input("\nPlease enter the ID of the book you wish to update: ")

        # checks if user input is valid book id in database
        cursor.execute("""
        SELECT * FROM books
        WHERE ID=? """, (book_id,))

        # if book is in database, checks which category to update
        if cursor.fetchone():
            while True:
                data_change = input(f"""\nWhich piece of data would you like to change about book {book_id}?
1. Title
2. Author
3. Quantity
""").lower()

                if data_change == "1" or data_change == "title":
                    new_title = input(f"Please enter the new title for book {book_id}: ")
                    cursor.execute("""
                    UPDATE books
                    SET Title=?
                    WHERE ID=?""", (new_title, book_id))

                    print(f"{GREEN}Book {book_id} title updated to: {new_title}{RESET}")
                    break

                elif data_change == "2" or data_change == "author":
                    new_author = input(f"Please enter the new author for book {book_id}: ")
                    cursor.execute("""
                    UPDATE books
                    SET Author=?
                    WHERE ID=?""", (new_author, book_id))

                    print(f"{GREEN}Book {book_id} author updated to: {new_author}{RESET}")
                    break

                elif data_change == "3" or data_change == "quantity":
                    new_qty = input(f"Please enter the new quantity for book {book_id}: ")
                    cursor.execute("""
                    UPDATE books
                    SET Quantity=?
                    WHERE ID=?""", (new_qty, book_id))

                    print(f"{GREEN}Book {book_id} quantity updated to: {new_qty}{RESET}")
                    break

                else:
                    print("Invalid Selection.")

            update_again = input("\nWould you like to update another book? ").lower()

            if update_again == "yes" or update_again == "y":
                continue
            else:
                break

        else:
            print("Invalid Book ID.")


# function to search db by book id
def id_search():
    while True:
        book_id = input("Please enter the book ID: ")

        cursor.execute("""
        SELECT * FROM books
        WHERE ID=?""", (book_id,))

        selected = cursor.fetchone()

        if selected:
            print(f"""\n{GREEN}Book ID: {selected[0]}
Title: {selected[1]}
Author: {selected[2]}
Quantity: {selected[3]}{RESET}""")
            break

        else:
            print(f"{RED}Book not in database.{RESET}")


# function to search db by book title
def title_search():
    while True:
        book_title = input("Please enter the book title: ").title()

        cursor.execute("""
            SELECT * FROM books
            WHERE Title=?""", (book_title,))

        selected = cursor.fetchone()

        if selected:
            print(f"""{GREEN}Book ID: {selected[0]}
Title: {selected[1]}
Author: {selected[2]}
Quantity: {selected[3]}{RESET}""")
            break

        else:
            print(f"{RED}Book not in database.{RESET}")


# function to search db by author
def author_search():
    while True:
        book_author = input("Please enter the book author: ").title()

        cursor.execute("""
            SELECT * FROM books
            WHERE Author=?""", (book_author,))

        selected = cursor.fetchall()

        if selected:
            print("\nBooks by this author:")

            for item in selected:
                print(f"""\n{GREEN}Book ID: {item[0]}
Title: {item[1]}
Author: {item[2]}
Quantity: {item[3]}{RESET}""")

            break

        else:
            print("Author not in database.")


# main user menu
menu = f"""{PURPLE}
╔═══════════════════════════╗
║         {RESET}{BOLD}{UNDERLINE}Main Menu{RESET}{PURPLE}         ║
║   1. Add Book             ║
║   2. Update Book          ║
║   3. Delete Book          ║
║   4. Search Books         ║
║   0. Exit                 ║
╚═══════════════════════════╝
{RESET}"""

# search by menu
search_menu = f"""{PURPLE}
╔══════════════════════════╗
║         {RESET}{BOLD}{UNDERLINE}Search by:{RESET}{PURPLE}       ║
║  1. Book ID              ║
║  2. Title                ║
║  3. Author               ║
║  0. Return to Main Menu  ║
╚══════════════════════════╝
{RESET}"""

# creates while loop to continuously display menu and input after each choice until user manually exits
while True:
    print(menu)
    user_choice = input("Please select an option from the menu above: ").lower()

    if user_choice == "1" or user_choice == "add book":
        add_book()
        print(f"{GREEN}Book successfully added to database.{RESET}")

    elif user_choice == "2" or user_choice == "update book":
        update_book()

    elif user_choice == "3" or user_choice == "delete book":
        delete_book()

    elif user_choice == "4" or user_choice == "search books":
        # displays sub-menu for user to select from search options
        while True:
            print(search_menu)
            search_choice = input("Please select an option from the menu above: ").lower()

            if search_choice == "1" or search_choice == "book id":
                id_search()

            elif search_choice == "2" or search_choice == "title":
                title_search()

            elif search_choice == "3" or search_choice == "author":
                author_search()

            # returns to main menu
            elif search_choice == "0":
                break

            # displays error message, loops to search menu
            else:
                print("Invalid input. Please try again.")

    # if user selects 0 or exit, goodbye message printed and loop breaks, ending programme
    elif user_choice == "0" or user_choice == "exit":
        print(f"{PURPLE}Thank you. Goodbye!")
        break

    # if user input is invalid, print error message and loop back to main menu
    else:
        print(f"{RED}Invalid input. Please try again.{RESET}")

db.commit()
db.close()
