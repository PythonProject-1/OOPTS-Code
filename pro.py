import json
import uuid
import matplotlib.pyplot as plt

# ---------------- ORDER CLASS ----------------
class Order:
    def __init__(self, customer_name, items):
        self.order_id = str(uuid.uuid4())[:8]   # Short unique ID
        self.customer_name = customer_name
        self.items = items
        self.status = "Placed"

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "items": self.items,
            "status": self.status
        }

# ---------------- ORDER SYSTEM ----------------
class OrderSystem:
    def __init__(self, file_name="orders.json"):
        self.file_name = file_name
        self.orders = self.load_orders()

    # Load existing orders
    def load_orders(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except:
            return []

    # Save orders to file
    def save_orders(self):
        with open(self.file_name, "w") as file:
            json.dump(self.orders, file, indent=4)

    # Create new order
    def create_order(self):
        name = input("Enter customer name: ")
        items = input("Enter items (comma separated): ").split(",")

        order = Order(name, items)
        self.orders.append(order.to_dict())
        self.save_orders()

        print(f"\n Order created successfully!")
        print(f" Order ID: {order.order_id}")

    # View all orders
    def view_orders(self):
        if not self.orders:
            print("\n No orders found.")
            return

        print("\n All Orders:")
        for order in self.orders:
            print("-" * 30)
            print(f"Order ID   : {order['order_id']}")
            print(f"Customer   : {order['customer_name']}")
            print(f"Items      : {', '.join(order['items'])}")
            print(f"Status     : {order['status']}")

    # Update order status
    def update_status(self):
        order_id = input("Enter Order ID: ")

        for order in self.orders:
            if order["order_id"] == order_id:
                print("\n1. Processing")
                print("2. Shipped")
                print("3. Delivered")

                choice = input("Select new status: ")

                status_map = {
                    "1": "Processing",
                    "2": "Shipped",
                    "3": "Delivered"
                }

                order["status"] = status_map.get(choice, order["status"])
                self.save_orders()

                print("\nStatus updated successfully!")
                return

        print("\nOrder not found!")

    # Track specific order
    def track_order(self):
        order_id = input("Enter Order ID: ")

        for order in self.orders:
            if order["order_id"] == order_id:
                print("\nOrder Details:")
                print("-" * 30)
                print(f"Order ID   : {order['order_id']}")
                print(f"Customer   : {order['customer_name']}")
                print(f"Items      : {', '.join(order['items'])}")
                print(f"Status     : {order['status']}")
                return

        print("\nOrder not found!")

    # Show charts of order statuses
    def show_order_chart(self):
        if not self.orders:
            print("\nNo orders to display in chart.")
            return

        statuses = [order["status"] for order in self.orders]
        status_count = {s: statuses.count(s) for s in set(statuses)}

        # Bar chart
        plt.bar(status_count.keys(), status_count.values(), color=['blue','orange','green'])
        plt.title("Order Status Distribution")
        plt.xlabel("Status")
        plt.ylabel("Number of Orders")
        plt.show()

        # Pie chart
        plt.pie(status_count.values(), labels=status_count.keys(), autopct='%1.1f%%')
        plt.title("Order Status Share")
        plt.show()

# ---------------- MAIN FUNCTION ----------------
def main():
    system = OrderSystem()

    while True:
        print("\n========== ORDER MANAGEMENT SYSTEM ==========")
        print("1. Create Order")
        print("2. View All Orders")
        print("3. Update Order Status")
        print("4. Track Order")
        print("5. Exit")
        print("6. Show Order Charts")

        choice = input("Enter your choice: ")

        if choice == "1":
            system.create_order()
        elif choice == "2":
            system.view_orders()
        elif choice == "3":
            system.update_status()
        elif choice == "4":
            system.track_order()
        elif choice == "6":
            system.show_order_chart()
        elif choice == "5":
            print("\nExiting... Thank you!")
            break
        else:
            print("\nInvalid choice! Try again.")

# ---------------- RUN PROGRAM ----------------
if __name__ == "__main__":
    main()