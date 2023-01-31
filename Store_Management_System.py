import sys
import csv
import keyboard
from tabulate import tabulate


class Store:
    all = []

    def __init__(self, products, product_available, customers, quantity):
        self.products = products
        self.product_available = product_available
        self.customers = customers
        self.quantity = quantity
        Store.all.append(self)

    @classmethod
    def available_product(cls):
        type3 = ''
        try:
            type3 = int(input("We have two types of products available :\n\t"
                              "1. Phones\n\t"
                              "2. Accessories\n\t"
                              "3. Main Menu\n\t"
                              "4. Exit\n"
                              "Enter your choice: "))
        except ValueError:
            print("Invalid input. Only Numeric value is allowed.")
            cls.available_product()
        rows = []
        if type3 == 1:
            with open('user_input.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Use filter function to filter rows with age 21
            phone_filter = list(filter(lambda x: x["Category"] == "phone", rows))
            print(tabulate(phone_filter, headers='keys', tablefmt="fancy_grid", colalign=("left",)))
            while True:
                event = keyboard.read_event()
                if event.event_type == 'down' and event.name == 'esc':
                    cls.available_product()
        elif type3 == 2:
            with open('user_input.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Use filter function
            accessories_filter = list(filter(lambda x: x["Category"] == "accessories", rows))
            print(tabulate(accessories_filter, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        elif type3 == 3:
            Buyer.owner()
        elif type3 == 4:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.available_product()

    @classmethod
    def add_product(cls):
        print("\n******** We have following Products are available in our Store ********")
        rows = []
        with open('user_input.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(tabulate(rows, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        header = ["Productid", "Name", "Price", "Quantity", "Category"]
        rows = []
        product = True
        while product:
            try:
                productid = int(input("Enter the productid: "))
                Store.check_product_id(productid)
            # except:
            #     print("Invalid input...")


                name = input("Enter a name: ")
                price = int(input("Enter the price: "))
                quantity = int(input("Enter the quantity: "))
                category = input("Enter a category: ")

                rows.append(
                    {"Name": name, "Price": price, "Quantity": quantity, "Category": category, "Productid": productid})
            except ValueError:
                print("invalid input")
                cls.add_product()
            with open("user_input.csv", "a", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=header)
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerows(rows)
                rows = []
            want = input("\nDo you want add more Products Y/N ? ")
            if want == "n" or want == "N":
                break
            else:
                cls.add_product()
        cls.another()

    @classmethod
    def check_product_id(cls, idd):
        with open('user_input.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(idd):
                    print("Product ID already exists.Try new ID")
                    return Store.add_product()

    @classmethod
    def update_product_quantity(cls):
        rows = []
        with open('user_input.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(tabulate(rows, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        product_id = input("Enter Product ID: ")
        with open('user_input.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(product_id):
                    try:
                        new_quantity = int(input("Enter Quantity to add: "))
                    except:
                        print("Invalid input....!")
                        cls.update_product_quantity()
                    break
            if row[0] != str(product_id):
                print("Product ID not found.Please try existing ID")
                cls.update_product_quantity()

        # reading csv file
        with open('user_input.csv', "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        # update the quantity of the product
        for row in rows:
            if row["Productid"] == product_id:
                quantity = row["Quantity"]
                quantity = int(quantity)
                quantity += new_quantity
                row["Quantity"] = quantity

        # write the updated data to the CSV file
        with open('user_input.csv', "w", newline="") as file:
            fieldnames = ["Productid", "Name", "Price", "Quantity", "Category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        cls.another()

    @classmethod
    def remove_product_quantity(cls):
        rows = []
        with open('user_input.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(tabulate(rows, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        product_id = input("Enter Product ID: ")
        with open('user_input.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(product_id):
                    try:
                        new_quantity = int(input("Enter Quantity to remove: "))
                    except:
                        print("Invalid input....!")
                        cls.remove_product_quantity()
                    break
            if row[0] != str(product_id):
                print("Product ID not found.Please try existing ID")
                cls.remove_product_quantity()
        # reading csv file
        with open('user_input.csv', "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        # update the quantity of the product
        for row in rows:
            if row["Productid"] == product_id:
                quantity = row["Quantity"]
                quantity = int(quantity)
                quantity -= new_quantity
                row["Quantity"] = quantity

        # write the updated data to the CSV file
        with open('user_input.csv', "w", newline="") as file:
            fieldnames = ["Productid", "Name", "Price", "Quantity", "Category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        cls.another()

    @classmethod
    def update_product_price(cls):
        rows = []
        with open('user_input.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(tabulate(rows, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        product_id = input("Enter Product ID: ")
        with open('user_input.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(product_id):
                    try:
                        new_price = int(input("Enter New Price: "))
                    except:
                        print("Invalid input")
                        cls.update_product_price()
                    break
            if row[0] != str(product_id):
                print("Product ID not found.Please try existing ID")
                cls.update_product_price()
            # elif type(new_price) == int:
            #     cls.update_product_price()
        # reading csv file
        with open('user_input.csv', "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        # update the quantity of the product
        for row in rows:
            if row["Productid"] == product_id:
                price = row["Price"]
                price = int(price)
                price = new_price
                row["Price"] = price

        # write the updated data to the CSV file
        with open('user_input.csv', "w", newline="") as file:
            fieldnames = ["Productid", "Name", "Price", "Quantity", "Category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        cls.another()

    @classmethod
    def delete_product(cls):
        rows = []
        with open('user_input.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(tabulate(rows, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

        product_id = input("Enter Product ID: ")
        with open('user_input.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(product_id):
                    break
            if row[0] != str(product_id):
                print("Product ID not found.Please try existing ID")
                cls.delete_product()
        with open('user_input.csv', "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        for row in rows:
            if row["Productid"] == product_id:
                rows.remove(row)
        with open('user_input.csv', "w", newline="") as file:
            fieldnames = ["Productid", "Name", "Price", "Quantity", "Category"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        cls.another()

    @classmethod
    def another(cls):
        transaction = True
        while transaction:
            want = input("Do you want any other transaction???\n"
                         "Enter Y/y for yes "
                         "or any other key to break\n"
                         "Enter: ")
            if want == "y" or want == "Y":
                Buyer.owner()
            else:
                sys.exit()


class Buyer(Store):
    def __init__(self, name):
        self.name = name

    @classmethod
    def buy(cls):
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
            cls.buy()

        if user_input == 1:
            return Customer.choice()
        elif user_input == 2:
            return Buyer.owner()
        else:
            # Handle invalid input
            print("Invalid input. Please enter '1' for 'buyer' or '2' for 'owner'.")
            cls.buy()

    @classmethod
    def owner(cls):
        # Code to run for owner
        print("Welcome owner!")
        type2 = ''
        try:
            type2 = int(input("What do you want do? \n\t"
                              "1. Available Products\n\t"
                              "2. Add  New Products\n\t"
                              "3. Update Product Quantity\n\t"
                              "4. Remove Product Quantity\n\t"
                              "5. Update Product Price\n\t"
                              "6. Delete Product \n\t"
                              "7. Exit\n"
                              "Enter your choice: "))
        except:
            print("Invalid input. Only Numeric value is allowed.")
            cls.owner()

        if type2 == 1:
            Store.available_product()
        elif type2 == 2:
            Store.add_product()
            print("\nNew Product Added")
        elif type2 == 3:
            Store.update_product_quantity()
            print("\nProduct Quantity updated")
            Store.another()
        elif type2 == 4:
            Store.remove_product_quantity()
            print("\nProduct Quantity updated")
        elif type2 == 5:
            Store.update_product_price()
            print("\nPrice updated")
        elif type2 == 6:
            Store.delete_product()
            print("\nProduct Deleted")
        elif type2 == 7:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.owner()


class Customer(Store):
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    @classmethod
    def choice(cls):
        type1 = ''
        try:
            type1 = int(input(
                "We have a following Products Categories\n"
                "In which category you are interested?\n\t"
                "1. Phone\n\t"
                "2. Accessories\n\t"
                "3. Main Menu\n\t"
                "4. Exit\n"
                "Please Enter your choice: "))
        except ValueError:
            print("\nonly Integer value is allowed \n")
            cls.choice()
        rows = []
        if type1 == 1:
            print("\n******** We have following Products are available in our Store ********")
            with open('user_input.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Use filter function
            phone_filter = list(filter(lambda x: x["Category"] == "phone", rows))

            print(tabulate(phone_filter, headers='keys', tablefmt="fancy_grid", colalign=("left",)))
            return Customer.sell_product()

        elif type1 == 2:
            print("\n******** We have following Products are available in our Store ********")
            with open('user_input.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(row)

            # Use filter function
            accessories_filter = list(filter(lambda x: x["Category"] == "accessories", rows))

            print(tabulate(accessories_filter, headers='keys', tablefmt="fancy_grid", colalign=("left",)))
            return Customer.sell_product()

        elif type1 == 3:
            Buyer.buy()
        elif type1 == 4:
            sys.exit()
        else:
            print("\nInvalid input. Please enter the above mentioned number...!\n")
            cls.choice()

    @classmethod
    def sell_product(cls):
        # product_quantity = ''
        product_name = input("Enter the Product name: ")
        # reading csv file
        with open('user_input.csv', 'r') as csvfile:
            # creating a csv dict reader object
            reader = csv.DictReader(csvfile)

            # extracting field names through first row
            fields = reader.fieldnames

            # data rows of csv file
            data = []

            found = False

            # extracting each data row one by one
            for row in reader:
                if row['Name'] == product_name:
                    found = True
                    while True:
                        try:
                            product_quantity = int(input("Enter the Product quantity: "))
                            if int(row['Quantity']) >= product_quantity:
                                row['Quantity'] = int(row['Quantity']) - product_quantity
                                data.append(row)
                            else:
                                print(f"{product_name} has only {row['Quantity']} left")
                        except ValueError:
                            print("Invalid Value. Please Enter only numeric value")
                            continue
                        break
                else:

                    data.append(row)

            if not found:
                while not found:
                    rows = []
                    print("Product not found.We have only these Product in our Store.\n")
                    with open('user_input.csv', 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            rows.append(row)

                    # Use filter function
                    phone_filter = list(filter(lambda x: x["Category"] == "phone", rows))

                    print(tabulate(phone_filter, headers='keys', tablefmt="fancy_grid", colalign=("left",)))

                    print("Press Esc key to go back ")

                    while True:
                        try:
                            if keyboard.is_pressed('Esc'):
                                Customer.choice()
                            if keyboard.is_pressed('ENTER'):
                                break
                        except:
                            break
                    sys.exit()

                else:
                    print("Invalid input")
                    found = True
                    print("\nEnter the Product again....!\n")

        # writing to csv file
        with open('user_input.csv', 'w', newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)

            # writing headers (field names)
            writer.writeheader()

            # writing data rows
            writer.writerows(data)

        transaction = True
        while transaction:
            want = input("Do you want any other transaction???\n"
                         "Enter Y/y for yes "
                         "or any other key to break\n"
                         "Enter: ")
            if want == "y" or want == "Y":
                Customer.choice()
            else:
                sys.exit()


def main():
    buyer = Buyer(name='')
    buyer.buy()


main()
