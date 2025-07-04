# =============================================================
# Online Shopping Cart System - GUI Version (Physical Products Only)
# =============================================================
# Developed using Python OOP and Tkinter GUI
# Demonstrates all four pillars of OOP:
# 1. Encapsulation
# 2. Abstraction
# 3. Inheritance
# 4. Polymorphism
# Includes Decorators (@property) and a menu-driven GUI interface.
# =============================================================

import tkinter as tk  # GUI framework used to build window-based apps
from tkinter import messagebox, simpledialog  # Message and input dialogs

# ------------------------
# Product Class (OOP Encapsulation + Abstraction)
# ------------------------
class Product:
    """
    Represents a physical product.
    Demonstrates Encapsulation (private variables) and uses @property decorators
    to control access to attributes.
    """
    def __init__(self, pid, name, price, quantity):
        self._product_id = pid
        self._name = name
        self._price = price
        self._quantity_available = quantity

    # --- Decorators (@property) used here ---
    # Provide read-only or controlled access to private variables
    @property
    def product_id(self): return self._product_id

    @property
    def name(self): return self._name

    @property
    def price(self): return self._price

    @property
    def quantity_available(self): return self._quantity_available

    @quantity_available.setter
    def quantity_available(self, value):
        if value >= 0:
            self._quantity_available = value

    def decrease_quantity(self, amount):
        """Decreases stock if available"""
        if 0 < amount <= self._quantity_available:
            self._quantity_available -= amount
            return True
        return False

    def increase_quantity(self, amount):
        """Restocks the product"""
        self._quantity_available += amount

    def display(self):
        """Returns string representation of product details"""
        return f"{self._product_id}: {self._name} - ₹{self._price} (Stock: {self._quantity_available})"

# ------------------------
# CartItem Class
# ------------------------
class CartItem:
    """Stores a product and its selected quantity in the cart"""
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def subtotal(self):
        """Returns subtotal for that item (price x quantity)"""
        return self.product.price * self.quantity

# ------------------------
# ShoppingCart Class (Encapsulation + Abstraction)
# ------------------------
class ShoppingCart:
    def __init__(self):
        self.catalog = {}  # Dictionary of product_id: Product
        self.cart = {}     # Dictionary of product_id: CartItem
        self._next_id = 1  # Used for generating unique product IDs

    def generate_product_id(self):
        """Generates unique product IDs like PID001"""
        pid = f"PID{self._next_id:03d}"
        self._next_id += 1
        return pid

    def add_product(self, name, price, qty):
        """Adds a new product to the catalog"""
        pid = self.generate_product_id()
        self.catalog[pid] = Product(pid, name, price, qty)
        return pid

    def add_to_cart(self, pid, qty):
        """Adds a product to the cart if stock is sufficient"""
        if pid in self.catalog:
            product = self.catalog[pid]
            if product.decrease_quantity(qty):
                if pid in self.cart:
                    self.cart[pid].quantity += qty
                else:
                    self.cart[pid] = CartItem(product, qty)
                return True
        return False

    def update_cart_quantity(self, pid, new_qty):
        """Modifies quantity of an existing item in the cart"""
        if pid in self.cart:
            item = self.cart[pid]
            current_qty = item.quantity
            available_qty = item.product.quantity_available
            diff = new_qty - current_qty

            if diff == 0:
                return True
            elif diff > 0:
                if diff <= available_qty:
                    item.product.decrease_quantity(diff)
                    item.quantity = new_qty
                    return True
                else:
                    return False
            else:
                item.product.increase_quantity(-diff)
                item.quantity = new_qty
                return True
        return False

    def remove_from_cart(self, pid):
        """Removes an item from the cart and restores quantity"""
        if pid in self.cart:
            self.catalog[pid].increase_quantity(self.cart[pid].quantity)
            del self.cart[pid]
            return True
        return False

    def get_cart_total(self):
        """Returns total amount of all items in the cart"""
        return sum(item.subtotal() for item in self.cart.values())

    def clear_cart(self):
        """Empties the cart after successful checkout"""
        self.cart.clear()

# ------------------------
# ShoppingCartApp Class (Tkinter GUI)
# ------------------------
class ShoppingCartApp:
    """
    Builds the GUI using Tkinter.
    Allows users to perform actions like adding products, adding to cart,
    updating cart, and checking out.
    Demonstrates Abstraction (UI hides internal logic).
    """
    def __init__(self, root):
        self.root = root
        self.cart = ShoppingCart()
        self.root.title("🛒 Online Shopping Cart System")
        self.root.geometry("750x600")

        # Main Frame and Text Display
        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.output = tk.Text(self.frame, width=90, height=20, bg="#f9f9f9")
        self.output.pack(pady=8)

        # Buttons to trigger actions
        button_frame = tk.Frame(self.frame)
        button_frame.pack(pady=5)

        buttons = [
            ("➕ Add Product", self.add_product_ui),
            ("📋 Show Catalog", self.show_catalog),
            ("🛒 Add to Cart", self.add_to_cart_ui),
            ("✏️ Update Cart Quantity", self.update_cart_quantity_ui),
            ("🧾 View Cart", self.view_cart),
            ("❌ Remove Item", self.remove_from_cart_ui),
            ("✅ Checkout", self.checkout)
        ]

        for label, command in buttons:
            tk.Button(button_frame, text=label, width=35, bg="#d1e7dd", command=command).pack(pady=4)

    # ------------------------
    # GUI Button Functionalities
    # ------------------------

    def add_product_ui(self):
        """UI to add a new product to the catalog"""
        name = simpledialog.askstring("Name", "Enter product name:")
        price = simpledialog.askfloat("Price", "Enter price:")
        qty = simpledialog.askinteger("Quantity", "Enter quantity:")
        pid = self.cart.add_product(name, price, qty)
        self.output.insert(tk.END, f"✅ Added: {pid} - {name}\n")

    def show_catalog(self):
        """Displays all products in the catalog"""
        self.output.insert(tk.END, "\n📦 --- Product Catalog ---\n")
        for prod in self.cart.catalog.values():
            self.output.insert(tk.END, prod.display() + "\n")

    def add_to_cart_ui(self):
        """UI to add a product to the shopping cart"""
        pid = simpledialog.askstring("Product ID", "Enter Product ID:")
        if pid not in self.cart.catalog:
            messagebox.showerror("Error", "Product ID not found.")
            return
        qty = simpledialog.askinteger("Quantity", "Enter quantity:")
        if self.cart.add_to_cart(pid, qty):
            self.output.insert(tk.END, f"🛒 Added {qty} of {pid} to cart.\n")
        else:
            messagebox.showerror("Error", "Not enough stock.")

    def update_cart_quantity_ui(self):
        """UI to update quantity of an item in the cart"""
        pid = simpledialog.askstring("Update Item", "Enter Product ID in cart:")
        if pid not in self.cart.cart:
            messagebox.showerror("Error", "Item not in cart.")
            return
        qty = simpledialog.askinteger("Quantity", "Enter new quantity:")
        if self.cart.update_cart_quantity(pid, qty):
            self.output.insert(tk.END, f"✏️ Updated {pid} to {qty}.\n")
        else:
            messagebox.showerror("Error", "Not enough stock to increase.")

    def view_cart(self):
        """Displays all items currently in the shopping cart"""
        self.output.insert(tk.END, "\n🧾 --- Your Cart ---\n")
        for pid, item in self.cart.cart.items():
            self.output.insert(tk.END, f"{pid}: {item.product.name} x {item.quantity} = ₹{item.subtotal()}\n")
        self.output.insert(tk.END, f"Total = ₹{self.cart.get_cart_total()}\n")

    def remove_from_cart_ui(self):
        """UI to remove an item from the cart"""
        pid = simpledialog.askstring("Remove Item", "Enter Product ID:")
        if self.cart.remove_from_cart(pid):
            self.output.insert(tk.END, f"❌ Removed {pid} from cart.\n")
        else:
            messagebox.showerror("Error", "Item not in cart.")

    def checkout(self):
        """Simulates checkout and payment flow"""
        total = self.cart.get_cart_total()
        if total == 0:
            messagebox.showinfo("Checkout", "Cart is empty.")
            return

        msg = f"💳 Select a payment method:\n1. UPI: shop@upi\n2. Card: ****1234\n3. COD\n\nTotal to Pay: ₹{total}"
        messagebox.showinfo("Payment", msg)
        self.cart.clear_cart()
        self.output.insert(tk.END, "\n✅ Order placed! Cart cleared.\n")


# ------------------------
# Main Entry Point
# ------------------------
if __name__ == '__main__':
    # Tkinter root window created and app launched
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
