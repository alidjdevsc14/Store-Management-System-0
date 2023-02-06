import sqlite3
import sys
from datetime import datetime

from tabulate import tabulate


class Store:

    @classmethod
    def available_product(cls, mail):
        type3 = ''
        try:
            type3 = int(input("We have two types of products available :\n\t"
                              "1. All Products\n\t"
                              "2. Phones\n\t"
                              "3. Accessories\n\t"
                              "4. Owner Menu\n\t"
                              "5. Exit\n"
                              "Enter your choice: "))
        except ValueError:
            print("Invalid input. Only Numeric value is allowed.")
            cls.available_product(mail)
        if type3 == 1:
            cls.show_data()
        elif type3 == 2:
            cls.search_by_mobile()
        elif type3 == 3:
            cls.search_by_accessories()
        elif type3 == 4:
            Buyer.owner(mail)
        elif type3 == 5:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.available_product(mail)
        cls.another(mail)

    @classmethod
    def add_data(cls, mail):
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect('Store.db')
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # Create the "users" table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                          (product_id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL, 
                          quantity INTEGER, category TEXT)''')
        try:
            cls.show_data()
        except:
            print("Currently we don't have any product in our store")
        product = True
        while product:
            try:
                product_id = int(input("Enter the product_id: "))
                if Store.chk_data(product_id):
                    print("Product ID already exists. Try with another id\n")
                    cls.add_data(mail)
                else:
                    pass
                name = input("Enter a name: ")
                while True:
                    price = input("Enter the price: ")
                    if price.isdigit() and int(price) > 0:
                        break
                    print("Invalid input. Please enter a positive integer.")
                while True:
                    quantity = input("Enter the quantity: ")
                    if quantity.isdigit() and int(quantity) > 0:
                        break
                    print("Invalid input. Please enter a positive integer.")
                category = input("Enter a category: ")
                # Insert the user data into the "products" table
                cursor.execute("INSERT INTO products (product_id, name, price, quantity, category) VALUES (?,?,?,?,?)",
                               (product_id, name, price, quantity, category))
                # Save the changes to the database
                conn.commit()
                conn.close()
            except ValueError:
                print("invalid input")
                cls.add_data(mail)
            want = input("\nDo you want to add more Products Y/N ? ")
            if want == "n" or want == "N":
                print("no")
                break
            else:
                cls.add_data(mail)
            product = False
        cls.another(mail)

    @classmethod
    def show_data(cls):
        # Connect to the database
        conn = sqlite3.connect('Store.db')
        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        # Select all data from the "products" table
        cursor.execute("SELECT * FROM products")

        # Fetch all the data from the cursor
        products = cursor.fetchall()

        # Add column names to the table
        column_names = [i[0] for i in cursor.description]

        # Print the table
        print(tabulate(products, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))

        # Close the connection
        conn.close()

    @classmethod
    def search_by_mobile(cls):

        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        column_names = [i[0] for i in cursor.description]
        data = conn.execute("SELECT * FROM products where category='phone'")
        row = []
        for n in data:
            row.append(n)
        try:
            print(tabulate(row, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        except:
            print("Not available......!")

    @classmethod
    def search_by_accessories(cls):

        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        column_names = [i[0] for i in cursor.description]
        data = conn.execute("SELECT * FROM products where category='accessories'")
        row = []
        for n in data:
            row.append(n)
        try:
            print(tabulate(row, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        except:
            print("Not available......!")

    @classmethod
    def del_data(cls):
        cls.show_data()

        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()

        # Create the SQL query
        query = "DELETE FROM products WHERE product_id = ?"
        product_id = input("Enter the product ID to delete an item: ")
        if Store.chk_data(product_id):
            pass
        else:
            print("Product ID not found. Try with existing ID......!\n")
            cls.del_data()

        # Execute the query
        cursor.execute(query, (product_id,))

        # Commit the changes
        conn.commit()
        cls.show_data()
        # Close the connection
        conn.close()

    @classmethod
    def update_name(cls):
        cls.show_data()

        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()

        # Create the SQL query
        query = "UPDATE products SET name = ? WHERE product_id = ?"
        product_id = input("Enter Product ID: ")
        if Store.chk_data(product_id):
            u = input("Enter New Updated Name: ")
            cursor.execute(query, (u, product_id))
        else:
            print("Product ID not found. Try with existing ID......!\n")
            cls.update_name()

        # Commit the changes
        conn.commit()
        cls.show_data()
        # Close the connection
        conn.close()

    @classmethod
    def update_price(cls):
        cls.show_data()
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        # Create the SQL query
        query = "UPDATE products SET price = ? WHERE product_id = ?"
        product_id = input("Enter Product ID: ")
        if Store.chk_data(product_id):
            while True:
                u = input("Enter the price: ")
                if u.isdigit() and int(u) > 0:
                    break
                print("Invalid input. Please enter a positive integer.")
            cursor.execute(query, (u, product_id))
        else:
            print("Product ID not found. Try with existing ID......!\n")
            cls.update_price()
        # Commit the changes
        conn.commit()
        cls.show_data()
        # Close the connection
        conn.close()

    @classmethod
    def update_category(cls):
        cls.show_data()
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        # Create the SQL query
        query = "UPDATE products SET category = ? WHERE product_id = ?"
        product_id = input("Enter Product ID: ")
        if Store.chk_data(product_id):
            u = input("Enter New Updated category: ")
            # Execute the query
            cursor.execute(query, (u, product_id))
        else:
            print("Product ID not found. Try with existing ID......!\n")
            cls.update_category()
        # Commit the change
        conn.commit()
        cls.show_data()
        # Close the connection
        conn.close()

    @classmethod
    def update_quantity(cls):
        cls.show_data()
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        # Create the SQL query
        query = "UPDATE products SET quantity = quantity + ? WHERE product_id = ?"
        product_id = input("Enter Product ID: ")
        if Store.chk_data(product_id):
            while True:
                u = input("Enter the quantity: ")
                if u.isdigit() and int(u) > 0:
                    break
                print("Invalid input. Please enter a positive integer.")
            # Execute the query
            cursor.execute(query, (u, product_id))
        else:
            print("Product ID not found. Try with existing ID......!\n")
            cls.update_quantity()
        # Commit the changes
        conn.commit()
        cls.show_data()
        # Close the connection
        conn.close()

    @classmethod
    def chk_data(cls, product_id):
        # Connect to the database
        conn = sqlite3.connect('Store.db')
        # Create a cursor object to execute SQL commands
        c = conn.cursor()
        # Execute a SELECT statement to check if the product ID already exists
        c.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
        result = c.fetchone()
        # Close the connection to the database
        conn.close()
        if result is None:
            return False
        else:
            return True

    @classmethod
    def another(cls, mail):
        transaction = True
        while transaction:
            want = input("Do you want any other transaction???\n"
                         "Enter Y/y for yes "
                         "or any other key to break\n"
                         "Enter: ")
            if want == "y" or want == "Y":
                Buyer.owner(mail)
            else:
                sys.exit()


class Buyer(Store):
    def __init__(self, name):
        self.name = name

    @classmethod
    def buy(cls, mail):
        user_input = ''
        try:
            user_input = int(input(
                "-----------Welcome to our Store------------ \n"
                "Are you a buyer or a owner? \n\t"
                "1. Buyer\n\t"
                "2. Owner\n"
                "Please enter:  "))
        except ValueError:
            print("\nonly Integer value is allowed \n")
            cls.buy(mail)
        if user_input == 1:
            return Customer.choice(mail)
        elif user_input == 2:
            return Buyer.owner(mail)
        else:
            # Handle invalid input
            print("Invalid input. Please enter '1' for 'buyer' or '2' for 'owner'.")
            cls.buy(mail)

    @classmethod
    def owner(cls, mail):
        print("Welcome owner!")
        type2 = ''
        try:
            type2 = int(input("What do you want do? \n\t"
                              "1. Available Products\n\t"
                              "2. Add  New Products\n\t"
                              "3. Update Product Name\n\t"
                              "4. Update Product Price\n\t"
                              "5. Update Product Quantity\n\t"
                              "6. Update Product Category\n\t"
                              "7. Delete Product \n\t"
                              "8. Main Menu\n\t"
                              "9. Exit\n"
                              "Enter your choice: "))
        except:
            print("Invalid input. Only Numeric value is allowed.")
            cls.owner(mail)
        if type2 == 1:
            Store.available_product(mail)
        elif type2 == 2:
            Store.add_data(mail)
            print("\nNew Product Added")
        elif type2 == 3:
            Store.update_name()
            print("\nProduct Name updated")
            Store.another(mail)
        elif type2 == 4:
            Store.update_price()
            print("\nProduct Price updated")
            Store.another(mail)
        elif type2 == 5:
            Store.update_quantity()
            print("\nProduct Quantity updated")
            Store.another(mail)
        elif type2 == 6:
            Store.update_category()
            print("\nProduct Category updated")
            Store.another(mail)
        elif type2 == 7:
            Store.del_data()
            print("\nProduct Deleted")
            Store.another(mail)
        elif type2 == 8:
            Buyer.buy(mail)
        elif type2 == 9:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.owner(mail)


class Customer(Store):
    def __init__(self, name, quantity, mail):
        self.name = name
        self.quantity = quantity
        self.mail = mail

    @classmethod
    def choice(cls, mail):
        type1 = ''
        try:
            type1 = int(input(
                "We have a following Products Categories\n"
                "In which category you are interested?\n\t"
                "1. All Products\n\t"
                "2. Phone\n\t"
                "3. Accessories\n\t"
                "4. Main Menu\n\t"
                "5. Exit\n"
                "Please Enter your choice: "))
        except ValueError:
            print("\nonly Integer value is allowed \n")
            cls.choice(mail)
        if type1 == 1:
            print("\n******** We have following Products are available in our Store ********")
            Store.show_data()
            return Customer.sell_product(mail)
        elif type1 == 2:
            print("\n******** We have following Products are available in our Store ********")
            Store.search_by_mobile()
            return Customer.sell_product(mail)
        elif type1 == 3:
            print("\n******** We have following Products are available in our Store ********")
            Store.search_by_accessories()
            return Customer.sell_product(mail)
        elif type1 == 4:
            Buyer.buy(mail)
        elif type1 == 5:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.choice(mail)

    @classmethod
    def sell_product(cls, mail):
        product_id = input("Enter the Product ID: ")
        if Store.chk_data(product_id):
            pass
        else:
            print("\nsorry.......!Product not Available\n")
            cls.another(mail)
        try:
            customer_req = int(input("Enter the Product quantity: "))
            if Customer.chk_quantity(product_id, customer_req, mail):
                print("if")
            else:
                cls.another(mail)
        except ValueError:
            print("Invalid Value. Please Enter only numeric value")
            cls.sell_product(mail)

    @classmethod
    def chk_quantity(cls, product_id, customer_req, mail):
        conn = sqlite3.connect('Store.db')
        # Create a cursor to execute SQL statements
        cur = conn.cursor()

        # Get the current product quantity
        cur.execute("SELECT quantity FROM products WHERE product_id=?", (product_id,))
        result = cur.fetchone()
        if result is None:
            return "Product not found."
        product_quantity = result[0]

        # Check if the product quantity is less than the customer requirement
        if product_quantity < customer_req:
            print("\nWe have available quantity: {}".format(product_quantity))
            print("Please Enter quantity less than or equal in our Store......!\n")
            return False
        else:
            cls.remove_data(customer_req, product_id, mail)

    @classmethod
    def remove_data(cls, customer_req, product_id, mail):

        conn = sqlite3.connect('Store.db')
        # create a cursor
        cur = conn.cursor()
        print("here", mail)
        print("updating.........")
        # update the quantity of the product
        cur.execute("UPDATE products SET quantity = quantity - ? WHERE product_id = ?",
                    (customer_req, product_id))
        cur.execute("SELECT price FROM products WHERE product_id=?", (product_id,))
        num = cur.fetchone()
        one = num[0]
        print(one)
        total_price = one * customer_req
        print(total_price)
        cur.execute("SELECT product_id, name FROM products WHERE product_id=?", (product_id,))
        data1 = cur.fetchone()
        product_id = data1[0]
        print(product_id)
        name = data1[1]
        print(name)
        print(data1)
        cur.execute("SELECT user_id, user_email FROM users WHERE user_email=?", (mail,))
        data2 = cur.fetchone()
        user_id = data2[0]
        print(user_id)
        user_email = data2[1]
        print(user_email)
        print(data2)
        product_quantity = customer_req
        date_time = datetime.now()
        # Create the "users" table if it doesn't exist
        cur.execute('''
                        CREATE TABLE IF NOT EXISTS records (
                        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id TEXT ,
                            name TEXT ,
                            user_id TEXT ,
                            user_email TEXT ,
                            product_quantity TEXT ,
                            total_price TEXT,
                            date_time TIMESTAMP
                        )
                    ''')
        cur.execute(
            "INSERT INTO records "
            "(product_id, name, user_id, user_email, product_quantity, total_price, date_time) "
            "VALUES (?,?,?,?,?,?,?)",
            (product_id, name, user_id, user_email, product_quantity, total_price, date_time))
        # commit the changes to the database
        conn.commit()
        cls.show_data()
        # close the connection
        conn.close()

    @classmethod
    def another(cls, mail):
        transaction = True
        while transaction:
            want = input("Do you want any other transaction???\n"
                         "Enter Y/y for yes "
                         "or any other key to break\n"
                         "Enter: ")
            if want == "y" or want == "Y":
                Customer.choice(mail)
            else:
                sys.exit()


class User:

    @classmethod
    def user_type(cls):
        import sqlite3
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()

        # Create the table to store user information
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_role TEXT NOT NULL,
                    user_email TEXT NOT NULL,
                    time_date TIMESTAMP
                )
            ''')
        user_email = input("Enter your email address: ")
        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_email=?", (user_email,))
        result = cursor.fetchone()
        if result is None:
            return cls.add_user(user_email)
        mail = result[2]
        if result:
            user_role = result[1]
            if user_role == "customer":
                print("Customer")
                return Customer.choice(mail)
            elif user_role == "owner":
                # print("Welcome Owner....!")
                return Buyer.owner(mail)
        else:
            print("Email not found.........!\nMention your role to add your email: ")
            user_role = input("Enter your Type (customer/owner): ")
            if user_role.lower() == "customer":
                cursor.execute("INSERT INTO users (user_email, user_role) VALUES (?, ?)", (user_email, "customer"))
                print("New Customer has been added....!")
            elif user_role.lower() == "owner":
                cursor.execute("INSERT INTO users (user_email, user_role) VALUES (?, ?)", (user_email, "owner"))
                print("New Owner has been added.......!")
            else:
                print("Invalid role.")
        conn.commit()
        conn.close()

    @classmethod
    def add_user(cls, user_email):
        time_date = datetime.now()

        conn = sqlite3.connect('Store.db')
        cursor = conn.cursor()
        print("Email not found.........!\nMention your role to add your email: ")
        user_role = input("Enter your Type (customer/owner): ")
        if user_role.lower() == "customer":
            cursor.execute("INSERT INTO users (user_email, user_role, time_date) VALUES (?, ?, ?)", (user_email, "customer", time_date))
            print("New Customer has been added....!")
        elif user_role.lower() == "owner":
            cursor.execute("INSERT INTO users (user_email, user_role, time_date) VALUES (?, ?, ?)", (user_email, "owner", time_date))
            print("New Owner has been added.......!")
        else:
            print("Invalid role.")
        conn.commit()
        conn.close()


def main():
    user = User()
    user.user_type()


main()
