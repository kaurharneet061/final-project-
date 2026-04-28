from flower_database import Flower, Inventory, Order

def main():
    inv = Inventory()

    while True:
        print("\n--- Flower Shop Menu ---")
        print("1. Add Flower")
        print("2. View Inventory")
        print("3. Create Order")
        print("4. Exit")

        choice = input("Choose an option")

        if choice == "1":
            name = input("Enter flower name: ")
            price = float(input("Enter price: "))
            qty = int(input("Enter quantity: "))
            inv.add_flower(Flower(name, price, qty))
            print("Flower added!")

        elif choice == "2":
            print("\Inventory:")
            for row in inv.show_inventory():
                print(row)

        elif choice == "3":
            order = Order(inv)

            while True:
                name = input("Enter flower name (or 'done): ")
                if name.lower() == "done":
                    break

                qty = int(input("Enter quantity: "))
                order.add_items(name, qty)

            total = order.checkout()
            print("Order total:", total)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()