import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Cafe Billing System")
        self.root.geometry("980x720")
        self.root.minsize(940, 680)
        self.root.configure(bg="#f6f1e8")

        self.item_prices = {
            "Tea": 20.0,
            "Coffee": 35.0,
            "Sandwich": 80.0,
            "Burger": 120.0,
            "Fries": 60.0,
            "Juice": 50.0,
        }

        self.item_suggestions = {
            "Tea": "Suggested add-on: Biscuit",
            "Coffee": "Suggested add-on: Muffin",
            "Sandwich": "Suggested add-on: Cold Drink",
            "Burger": "Suggested add-on: Fries",
            "Fries": "Suggested add-on: Ketchup",
            "Juice": "Suggested add-on: Sandwich",
        }

        self.combo_recommendations = {
            "Tea": "If the customer buys 3 or more Tea items, suggest a biscuit combo.",
            "Coffee": "If the order is large, suggest a coffee + muffin combo.",
            "Sandwich": "If quantity is 2 or more, suggest adding a cold drink.",
            "Burger": "If quantity is 2 or more, suggest Fries as a combo add-on.",
            "Fries": "If Fries are selected, suggest ketchup as a low-cost add-on.",
            "Juice": "If the subtotal is low, suggest adding a sandwich for a meal combo.",
        }

        # Session-scoped purchase history to enable simple personalization/loyalty rules
        # Structure: { contact_number: { 'count': int, 'total': float, 'items': {item_name: qty} } }
        self.purchase_history = {}

        # Loyalty tiers (based on number of previous purchases)
        # These are simple rule-based tiers for demonstration
        self.loyalty_tiers = [
            (10, 12.0, "Platinum"),
            (5, 8.0, "Gold"),
            (2, 5.0, "Silver"),
        ]

        self.customer_name_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.item_var = tk.StringVar(value="Tea")
        self.price_var = tk.StringVar(value=f"{self.item_prices['Tea']:.2f}")
        self.quantity_var = tk.StringVar(value="1")
        self.discount_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(value="Select an item to auto-fill the price and suggestion.")

        self._build_ui()
        self._update_item_info()

    def _build_ui(self):
        header_frame = tk.Frame(self.root, bg="#3c2f2f", padx=15, pady=15)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Mini Cafe Billing System",
            font=("Helvetica", 24, "bold"),
            bg="#3c2f2f",
            fg="#ffffff",
        ).pack()
        tk.Label(
            header_frame,
            text="Tkinter Widgets Lab - Real-Time Billing Case Study",
            font=("Helvetica", 11),
            bg="#3c2f2f",
            fg="#f2d2b6",
        ).pack(pady=(4, 0))

        body_frame = tk.Frame(self.root, bg="#f6f1e8", padx=15, pady=15)
        body_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(body_frame, bg="#fffdf9", bd=2, relief="groove", padx=15, pady=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(body_frame, bg="#fffdf9", bd=2, relief="groove", padx=15, pady=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        form_title = tk.Label(
            left_frame,
            text="Customer & Item Details",
            font=("Helvetica", 16, "bold"),
            bg="#fffdf9",
            fg="#3c2f2f",
        )
        form_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        labels = [
            "Customer Name",
            "Contact Number",
            "Cafe Item",
            "Item Price",
            "Quantity",
            "Discount (%)",
        ]

        for index, label_text in enumerate(labels, start=1):
            tk.Label(
                left_frame,
                text=label_text,
                font=("Helvetica", 11, "bold"),
                bg="#fffdf9",
                fg="#4c3b31",
            ).grid(row=index, column=0, sticky="w", pady=8, padx=(0, 12))

        self.customer_entry = tk.Entry(left_frame, textvariable=self.customer_name_var, font=("Helvetica", 11), width=28)
        self.customer_entry.grid(row=1, column=1, sticky="ew", pady=8)

        self.contact_entry = tk.Entry(left_frame, textvariable=self.contact_var, font=("Helvetica", 11), width=28)
        self.contact_entry.grid(row=2, column=1, sticky="ew", pady=8)

        self.item_combo = ttk.Combobox(
            left_frame,
            textvariable=self.item_var,
            values=list(self.item_prices.keys()),
            state="readonly",
            font=("Helvetica", 11),
            width=26,
        )
        self.item_combo.grid(row=3, column=1, sticky="ew", pady=8)
        self.item_combo.bind("<<ComboboxSelected>>", lambda event: self._update_item_info())

        self.price_entry = tk.Entry(left_frame, textvariable=self.price_var, font=("Helvetica", 11), width=28)
        self.price_entry.grid(row=4, column=1, sticky="ew", pady=8)

        self.quantity_entry = tk.Entry(left_frame, textvariable=self.quantity_var, font=("Helvetica", 11), width=28)
        self.quantity_entry.grid(row=5, column=1, sticky="ew", pady=8)

        self.discount_entry = tk.Entry(left_frame, textvariable=self.discount_var, font=("Helvetica", 11), width=28)
        self.discount_entry.grid(row=6, column=1, sticky="ew", pady=8)

        left_frame.grid_columnconfigure(1, weight=1)

        suggestion_box = tk.LabelFrame(
            left_frame,
            text="Smart Billing Hint",
            font=("Helvetica", 10, "bold"),
            bg="#fffdf9",
            fg="#3c2f2f",
            padx=10,
            pady=10,
        )
        suggestion_box.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(15, 10))
        tk.Label(
            suggestion_box,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            bg="#fffdf9",
            fg="#6a4f3b",
            wraplength=350,
            justify="left",
        ).pack(anchor="w")

        button_frame = tk.Frame(left_frame, bg="#fffdf9")
        button_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        tk.Button(
            button_frame,
            text="Generate Receipt",
            font=("Helvetica", 11, "bold"),
            bg="#4a7c59",
            fg="white",
            activebackground="#3d6548",
            activeforeground="white",
            relief="flat",
            command=self.generate_receipt,
            padx=12,
            pady=8,
        ).pack(side="left", padx=(0, 8), fill="x", expand=True)

        tk.Button(
            button_frame,
            text="Clear",
            font=("Helvetica", 11, "bold"),
            bg="#d4a373",
            fg="white",
            activebackground="#ba8a5d",
            activeforeground="white",
            relief="flat",
            command=self.clear_form,
            padx=12,
            pady=8,
        ).pack(side="left", padx=8, fill="x", expand=True)

        tk.Button(
            button_frame,
            text="Save Receipt",
            font=("Helvetica", 11, "bold"),
            bg="#3a5a40",
            fg="white",
            activebackground="#304b35",
            activeforeground="white",
            relief="flat",
            command=self.save_receipt,
            padx=12,
            pady=8,
        ).pack(side="left", padx=8, fill="x", expand=True)

        tk.Button(
            button_frame,
            text="Apply AI Suggestion",
            font=("Helvetica", 11, "bold"),
            bg="#5b7c8a",
            fg="white",
            activebackground="#47616a",
            activeforeground="white",
            relief="flat",
            command=self.apply_ai_suggestion,
            padx=12,
            pady=8,
        ).pack(side="left", padx=8, fill="x", expand=True)

        tk.Button(
            button_frame,
            text="Exit",
            font=("Helvetica", 11, "bold"),
            bg="#8d3b3b",
            fg="white",
            activebackground="#742f2f",
            activeforeground="white",
            relief="flat",
            command=self.exit_app,
            padx=12,
            pady=8,
        ).pack(side="left", padx=(8, 0), fill="x", expand=True)

        receipt_title = tk.Label(
            right_frame,
            text="Receipt Preview",
            font=("Helvetica", 16, "bold"),
            bg="#fffdf9",
            fg="#3c2f2f",
        )
        receipt_title.pack(anchor="w", pady=(0, 10))

        receipt_container = tk.Frame(right_frame, bg="#fffdf9")
        receipt_container.pack(fill="both", expand=True)

        self.receipt_text = tk.Text(
            receipt_container,
            wrap="word",
            font=("Courier New", 11),
            bg="#fffaf4",
            fg="#2d2d2d",
            relief="sunken",
            bd=2,
            padx=10,
            pady=10,
            height=24,
        )
        self.receipt_text.pack(side="left", fill="both", expand=True)

        receipt_scrollbar = ttk.Scrollbar(receipt_container, orient="vertical", command=self.receipt_text.yview)
        receipt_scrollbar.pack(side="right", fill="y")
        self.receipt_text.configure(yscrollcommand=receipt_scrollbar.set)

        self._insert_receipt_placeholder()

    def _insert_receipt_placeholder(self):
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(
            tk.END,
            "Receipt will appear here after clicking Generate Receipt.\n\n"
            "The system will validate inputs, apply any eligible rule-based discount,\n"
            "and then show a formatted bill summary."
        )

    def _update_item_info(self):
        selected_item = self.item_var.get()
        suggested_price = self.item_prices.get(selected_item, 0.0)
        self.price_var.set(f"{suggested_price:.2f}")
        self.status_var.set(self.item_suggestions.get(selected_item, "No suggestion available for the selected item."))

    def _get_ai_recommendation(self, contact, item_name, quantity, subtotal):
        # Start with a generic recommendation for the item
        recommendation = self.combo_recommendations.get(item_name, "No AI recommendation available for this item.")

        # Personalization: if this contact has previous history, recommend items they often buy
        history = self.purchase_history.get(contact)
        if history:
            fav_item = None
            max_qty = 0
            for it, qty in history.get('items', {}).items():
                if qty > max_qty:
                    fav_item = it
                    max_qty = qty
            if fav_item and fav_item != item_name:
                recommendation = f"Personalized suggestion: customers who bought {item_name} often also buy {fav_item}."

        # Compose an AI rule message describing why the suggestion was made
        if subtotal >= 1000:
            return recommendation, "AI decision: high-value order detected, bulk discount recommended."
        if quantity >= 10:
            return recommendation, "AI decision: very large quantity, apply top-tier bulk discount."
        if quantity >= 5:
            return recommendation, "AI decision: quantity threshold reached, mid-size discount recommended."
        if quantity >= 2:
            return recommendation, "AI decision: suggest a related combo item to increase value."
        return recommendation, "AI decision: standard order, no extra rule triggered."

    def _get_loyalty_discount(self, contact):
        # Return loyalty discount percent and a message
        info = self.purchase_history.get(contact)
        count = info.get('count', 0) if info else 0
        for threshold, percent, name in self.loyalty_tiers:
            if count >= threshold:
                return percent, f"Loyalty tier: {name} ({percent:.0f}% discount)"
        return 0.0, "No loyalty discount"

    def _record_purchase(self, contact, item, qty, amount):
        # Update the in-memory purchase history for the session
        if contact not in self.purchase_history:
            self.purchase_history[contact] = {'count': 0, 'total': 0.0, 'items': {}}
        rec = self.purchase_history[contact]
        rec['count'] += 1
        rec['total'] += float(amount)
        rec['items'][item] = rec['items'].get(item, 0) + int(qty)

    def _validate_inputs(self):
        customer_name = self.customer_name_var.get().strip()
        contact_number = self.contact_var.get().strip()
        item_name = self.item_var.get().strip()
        price_text = self.price_var.get().strip()
        quantity_text = self.quantity_var.get().strip()
        discount_text = self.discount_var.get().strip()

        if not customer_name:
            messagebox.showerror("Validation Error", "Customer name cannot be empty.")
            self.customer_entry.focus_set()
            return None

        if not contact_number or not contact_number.isdigit() or len(contact_number) < 7 or len(contact_number) > 15:
            messagebox.showerror("Validation Error", "Enter a valid contact number with 7 to 15 digits.")
            self.contact_entry.focus_set()
            return None

        if item_name not in self.item_prices:
            messagebox.showerror("Validation Error", "Please select a valid cafe item.")
            self.item_combo.focus_set()
            return None

        try:
            item_price = float(price_text)
            if item_price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Item price must be a positive numeric value.")
            self.price_entry.focus_set()
            return None

        try:
            quantity = int(quantity_text)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity must be a positive whole number.")
            self.quantity_entry.focus_set()
            return None

        try:
            discount_percent = float(discount_text) if discount_text else 0.0
            if discount_percent < 0 or discount_percent > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Discount must be a number from 0 to 100.")
            self.discount_entry.focus_set()
            return None

        return customer_name, contact_number, item_name, item_price, quantity, discount_percent

    def _calculate_rule_discount(self, subtotal, quantity):
        if subtotal >= 1000 or quantity >= 10:
            return 12.0, "Automatic promotion applied: 12% bulk discount"
        if subtotal >= 500 or quantity >= 5:
            return 8.0, "Automatic promotion applied: 8% mid-size order discount"
        return 0.0, "No automatic promotion applied"

    def generate_receipt(self):
        validated = self._validate_inputs()
        if not validated:
            return

        customer_name, contact_number, item_name, item_price, quantity, manual_discount = validated
        subtotal = item_price * quantity
        recommendation_text, ai_rule_text = self._get_ai_recommendation(contact_number, item_name, quantity, subtotal)
        rule_discount, rule_message = self._calculate_rule_discount(subtotal, quantity)
        loyalty_discount, loyalty_message = self._get_loyalty_discount(contact_number)

        # Choose the best discount among manual, rule-based, and loyalty
        applied_discount = max(manual_discount, rule_discount, loyalty_discount)

        # Determine reason text for the discount applied
        if applied_discount == loyalty_discount and loyalty_discount > 0:
            discount_reason = loyalty_message
        elif applied_discount == rule_discount and rule_discount > 0:
            discount_reason = rule_message
        elif manual_discount > 0 and applied_discount == manual_discount:
            discount_reason = f"Manual discount applied: {manual_discount:.2f}%"
        else:
            discount_reason = "No discount applied"

        discount_amount = subtotal * (applied_discount / 100)
        final_total = subtotal - discount_amount

        current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        receipt_lines = [
            "=" * 48,
            "               The Cozy Corner Cafe               ",
            "=" * 48,
            f"Date/Time   : {current_time}",
            f"Customer    : {customer_name}",
            f"Contact No. : {contact_number}",
            "-" * 48,
            f"Item        : {item_name}",
            f"Price       : Rs. {item_price:.2f}",
            f"Quantity    : {quantity}",
            f"Subtotal    : Rs. {subtotal:.2f}",
            f"Discount    : {applied_discount:.2f}%",
            f"Discount Rs.: Rs. {discount_amount:.2f}",
            f"Payable     : Rs. {final_total:.2f}",
            "-" * 48,
            "AI Decision Rules",
            f"Recommendation: {recommendation_text}",
            f"Rule Status   : {ai_rule_text}",
            f"Billing Note  : {discount_reason}",
            "-" * 48,
            self.status_var.get(),
            "Thank you for visiting The Cozy Corner Cafe!",
            "=" * 48,
        ]

        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert(tk.END, "\n".join(receipt_lines))

        # Record purchase in session history for future personalization
        try:
            self._record_purchase(contact_number, item_name, quantity, final_total)
        except Exception:
            pass

    def apply_ai_suggestion(self):
        validated = self._validate_inputs()
        if not validated:
            return

        customer_name, contact_number, item_name, item_price, quantity, manual_discount = validated
        subtotal = item_price * quantity
        rec_text, ai_text = self._get_ai_recommendation(contact_number, item_name, quantity, subtotal)
        loyalty_discount, loyalty_msg = self._get_loyalty_discount(contact_number)
        rule_discount, rule_msg = self._calculate_rule_discount(subtotal, quantity)
        suggested = max(manual_discount, rule_discount, loyalty_discount)

        msg = (
            f"Recommendation:\n{rec_text}\n\n"
            f"AI Note: {ai_text}\n"
            f"Loyalty: {loyalty_msg}\n"
            f"Suggested discount: {suggested:.2f}%\n\n"
            "Apply suggested discount to the current form?"
        )

        if messagebox.askyesno("Apply AI Suggestion", msg):
            self.discount_var.set(f"{suggested:.2f}")
            self.status_var.set(f"AI suggestion applied: {ai_text}")
            messagebox.showinfo("AI Suggestion", "Suggested discount applied to the form.")
        else:
            self.status_var.set("AI suggestion was not applied.")

    def clear_form(self):
        self.customer_name_var.set("")
        self.contact_var.set("")
        self.item_var.set("Tea")
        self.price_var.set(f"{self.item_prices['Tea']:.2f}")
        self.quantity_var.set("1")
        self.discount_var.set("0")
        self._update_item_info()
        self._insert_receipt_placeholder()
        self.customer_entry.focus_set()

    def save_receipt(self):
        receipt_content = self.receipt_text.get("1.0", tk.END).strip()
        if not receipt_content or "Receipt will appear here" in receipt_content:
            messagebox.showwarning("Save Receipt", "Generate a receipt before saving it.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Receipt",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialfile="cafe_receipt.txt",
        )

        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(receipt_content)

        messagebox.showinfo("Save Receipt", f"Receipt saved successfully at:\n{file_path}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Do you want to close the billing system?"):
            self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    CafeBillingSystem(app_root)
    app_root.mainloop()