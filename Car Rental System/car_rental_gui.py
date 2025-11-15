import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from database import Database
import sys

class CarRentalGUI:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.setup_gui()
        
    def setup_gui(self):
        self.root.title("🚗 Car Rental System ")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f8ff')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_cars_tab()
        self.create_customers_tab()
        self.create_rentals_tab()
        self.create_reports_tab()
        
    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Header
        header_label = tk.Label(dashboard_frame, text="🚗 Car Rental System", 
                               font=('Arial', 24, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        header_label.pack(pady=20)
        
        sub_label = tk.Label(dashboard_frame, text="With Muslim Name Examples", 
                            font=('Arial', 14), bg='#f0f8ff', fg='#7f8c8d')
        sub_label.pack(pady=5)
        
        # Stats frame
        stats_frame = tk.Frame(dashboard_frame, bg='#f0f8ff')
        stats_frame.pack(pady=20)
        
        # Get statistics
        stats = self.get_statistics()
        
        # Create stat cards
        stat_cards = [
            ("💰 Total Revenue", f"${stats['total_revenue']:.2f}", "#27ae60"),
            ("🚗 Available Cars", stats['available_cars'], "#2980b9"),
            ("🔑 Active Rentals", stats['active_rentals'], "#e74c3c"),
            ("👥 Total Customers", stats['total_customers'], "#8e44ad")
        ]
        
        for i, (title, value, color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            card.grid(row=0, column=i, padx=10, pady=10, ipadx=20, ipady=20)
            
            title_label = tk.Label(card, text=title, bg=color, fg='white', 
                                 font=('Arial', 12, 'bold'))
            title_label.pack()
            
            value_label = tk.Label(card, text=value, bg=color, fg='white', 
                                 font=('Arial', 18, 'bold'))
            value_label.pack()
        
        # Quick actions frame
        actions_frame = tk.Frame(dashboard_frame, bg='#f0f8ff')
        actions_frame.pack(pady=30)
        
        action_buttons = [
            ("📝 Register Customer", self.register_customer_dialog),
            ("🚘 Rent Car", self.rent_car_dialog),
            ("🔄 Return Car", self.return_car_dialog),
            ("📊 View Reports", lambda: self.notebook.select(4))
        ]
        
        for i, (text, command) in enumerate(action_buttons):
            btn = tk.Button(actions_frame, text=text, command=command,
                          font=('Arial', 12), bg='#3498db', fg='white',
                          padx=20, pady=10, width=15)
            btn.grid(row=0, column=i, padx=10)
        
        # Recent activity
        recent_frame = tk.Frame(dashboard_frame, bg='#f0f8ff')
        recent_frame.pack(pady=20, fill='x', padx=50)
        
        recent_label = tk.Label(recent_frame, text="Recent Activity", 
                              font=('Arial', 16, 'bold'), bg='#f0f8ff')
        recent_label.pack()
        
        self.recent_tree = ttk.Treeview(recent_frame, columns=('ID', 'Customer', 'Car', 'Date', 'Amount'), 
                                      show='headings', height=8)
        self.recent_tree.heading('ID', text='Rental ID')
        self.recent_tree.heading('Customer', text='Customer')
        self.recent_tree.heading('Car', text='Car')
        self.recent_tree.heading('Date', text='Date')
        self.recent_tree.heading('Amount', text='Amount')
        
        self.recent_tree.column('ID', width=80)
        self.recent_tree.column('Customer', width=150)
        self.recent_tree.column('Car', width=120)
        self.recent_tree.column('Date', width=100)
        self.recent_tree.column('Amount', width=100)
        
        self.recent_tree.pack(fill='x', pady=10)
        self.load_recent_activity()
    
    def create_cars_tab(self):
        cars_frame = ttk.Frame(self.notebook)
        self.notebook.add(cars_frame, text="🚗 Cars")
        
        # Controls frame
        controls_frame = tk.Frame(cars_frame, bg='#f0f8ff')
        controls_frame.pack(fill='x', pady=10)
        
        tk.Button(controls_frame, text="Refresh", command=self.load_cars,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="Add Car", command=self.add_car_dialog,
                 font=('Arial', 10), bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(cars_frame, bg='#f0f8ff')
        filter_frame.pack(fill='x', pady=5)
        
        tk.Label(filter_frame, text="Status Filter:", bg='#f0f8ff').pack(side='left', padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'Available', 'Rented', 'Maintenance'])
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_cars())
        
        # Cars treeview
        self.cars_tree = ttk.Treeview(cars_frame, columns=('ID', 'Make', 'Model', 'Year', 'Color', 'License', 'Rate', 'Status', 'Fuel'), 
                                    show='headings', height=15)
        
        columns = [
            ('ID', 50), ('Make', 100), ('Model', 100), ('Year', 60), 
            ('Color', 80), ('License', 100), ('Rate', 80), ('Status', 100), ('Fuel', 80)
        ]
        
        for col, width in columns:
            self.cars_tree.heading(col, text=col)
            self.cars_tree.column(col, width=width)
        
        self.cars_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load initial data
        self.load_cars()
    
    def create_customers_tab(self):
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="👥 Customers")
        
        # Controls frame
        controls_frame = tk.Frame(customers_frame, bg='#f0f8ff')
        controls_frame.pack(fill='x', pady=10)
        
        tk.Button(controls_frame, text="Refresh", command=self.load_customers,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="Add Customer", command=self.register_customer_dialog,
                 font=('Arial', 10), bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        # Customers treeview
        self.customers_tree = ttk.Treeview(customers_frame, 
                                         columns=('ID', 'First Name', 'Last Name', 'Email', 'Phone', 'License'),
                                         show='headings', height=15)
        
        columns = [
            ('ID', 50), ('First Name', 120), ('Last Name', 120), 
            ('Email', 200), ('Phone', 120), ('License', 150)
        ]
        
        for col, width in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=width)
        
        self.customers_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.load_customers()
    
    def create_rentals_tab(self):
        rentals_frame = ttk.Frame(self.notebook)
        self.notebook.add(rentals_frame, text="🔑 Rentals")
        
        # Controls frame
        controls_frame = tk.Frame(rentals_frame, bg='#f0f8ff')
        controls_frame.pack(fill='x', pady=10)
        
        tk.Button(controls_frame, text="Refresh", command=self.load_rentals,
                 font=('Arial', 10), bg='#3498db', fg='white').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="New Rental", command=self.rent_car_dialog,
                 font=('Arial', 10), bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="Return Car", command=self.return_car_dialog,
                 font=('Arial', 10), bg='#e74c3c', fg='white').pack(side='left', padx=5)
        
        # Rentals treeview
        self.rentals_tree = ttk.Treeview(rentals_frame, 
                                       columns=('ID', 'Customer', 'Car', 'Rental Date', 'Return Date', 'Status', 'Amount'),
                                       show='headings', height=15)
        
        columns = [
            ('ID', 80), ('Customer', 150), ('Car', 120), 
            ('Rental Date', 100), ('Return Date', 100), ('Status', 100), ('Amount', 100)
        ]
        
        for col, width in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=width)
        
        self.rentals_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.load_rentals()
    
    def create_reports_tab(self):
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Revenue report
        revenue_frame = tk.Frame(reports_frame, bg='#f0f8ff')
        revenue_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(revenue_frame, text="Financial Reports", font=('Arial', 16, 'bold'), 
                bg='#f0f8ff').pack(anchor='w')
        
        self.report_text = tk.Text(reports_frame, height=15, width=80)
        self.report_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Button(reports_frame, text="Generate Report", command=self.generate_report,
                 font=('Arial', 12), bg='#3498db', fg='white').pack(pady=10)
    
    # Data loading methods
    def get_statistics(self):
        try:
            total_revenue = self.db.fetch_one("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status = 'Completed'")[0]
            available_cars = self.db.fetch_one("SELECT COUNT(*) FROM cars WHERE status = 'Available'")[0]
            active_rentals = self.db.fetch_one("SELECT COUNT(*) FROM rentals WHERE status = 'Active'")[0]
            total_customers = self.db.fetch_one("SELECT COUNT(*) FROM customers")[0]
            
            return {
                'total_revenue': float(total_revenue),
                'available_cars': available_cars,
                'active_rentals': active_rentals,
                'total_customers': total_customers
            }
        except:
            return {'total_revenue': 0, 'available_cars': 0, 'active_rentals': 0, 'total_customers': 0}
    
    def load_recent_activity(self):
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        query = """
        SELECT r.rental_id, c.first_name, c.last_name, car.make, car.model, 
               r.rental_date, r.total_cost 
        FROM rentals r 
        JOIN customers c ON r.customer_id = c.customer_id 
        JOIN cars car ON r.car_id = car.car_id 
        ORDER BY r.rental_id DESC LIMIT 10
        """
        
        rentals = self.db.fetch_all(query)
        for rental in rentals:
            customer_name = f"{rental[1]} {rental[2]}"
            car_name = f"{rental[3]} {rental[4]}"
            self.recent_tree.insert('', 'end', values=(
                rental[0], customer_name, car_name, rental[5], f"${rental[6]:.2f}"
            ))
    
    def load_cars(self):
        for item in self.cars_tree.get_children():
            self.cars_tree.delete(item)
        
        status_filter = self.status_filter.get()
        if status_filter == 'All':
            query = "SELECT * FROM cars ORDER BY car_id"
            cars = self.db.fetch_all(query)
        else:
            query = "SELECT * FROM cars WHERE status = %s ORDER BY car_id"
            cars = self.db.fetch_all(query, (status_filter,))
        
        for car in cars:
            self.cars_tree.insert('', 'end', values=car)
    
    def load_customers(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        query = "SELECT customer_id, first_name, last_name, email, phone, driver_license FROM customers ORDER BY customer_id"
        customers = self.db.fetch_all(query)
        
        for customer in customers:
            self.customers_tree.insert('', 'end', values=customer)
    
    def load_rentals(self):
        for item in self.rentals_tree.get_children():
            self.rentals_tree.delete(item)
        
        query = """
        SELECT r.rental_id, c.first_name || ' ' || c.last_name, car.make || ' ' || car.model,
               r.rental_date, r.return_date, r.status, r.total_cost
        FROM rentals r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN cars car ON r.car_id = car.car_id
        ORDER BY r.rental_id DESC
        """
        
        rentals = self.db.fetch_all(query)
        for rental in rentals:
            return_date = rental[4] if rental[4] else "Not Returned"
            self.rentals_tree.insert('', 'end', values=(
                rental[0], rental[1], rental[2], rental[3], return_date, rental[5], f"${rental[6]:.2f}"
            ))
    
    def generate_report(self):
        stats = self.get_statistics()
        
        report = f"""
CAR RENTAL SYSTEM - FINANCIAL REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

FINANCIAL SUMMARY:
• Total Revenue: ${stats['total_revenue']:.2f}
• Available Cars: {stats['available_cars']}
• Active Rentals: {stats['active_rentals']}
• Total Customers: {stats['total_customers']}

RECENT TRANSACTIONS:
"""
        
        # Add recent transactions
        query = """
        SELECT r.rental_id, c.first_name, c.last_name, car.make, car.model,
               r.rental_date, r.total_cost, r.status
        FROM rentals r
        JOIN customers c ON r.customer_id = c.customer_id
        JOIN cars car ON r.car_id = car.car_id
        ORDER BY r.rental_id DESC LIMIT 15
        """
        
        transactions = self.db.fetch_all(query)
        for trans in transactions:
            status_icon = "✅" if trans[6] == 'Completed' else "🔴" if trans[6] == 'Active' else "❌"
            report += f"• {status_icon} {trans[1]} {trans[2]} - {trans[3]} {trans[4]} - ${trans[5]:.2f} - {trans[6]}\n"
        
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report)
    
    # Dialog methods
    def register_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Register New Customer")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="First Name:").pack(pady=5)
        first_name_entry = tk.Entry(dialog, width=30)
        first_name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Last Name:").pack(pady=5)
        last_name_entry = tk.Entry(dialog, width=30)
        last_name_entry.pack(pady=5)
        
        tk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = tk.Entry(dialog, width=30)
        email_entry.pack(pady=5)
        
        tk.Label(dialog, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.pack(pady=5)
        
        tk.Label(dialog, text="Driver License:").pack(pady=5)
        license_entry = tk.Entry(dialog, width=30)
        license_entry.pack(pady=5)
        
        def save_customer():
            query = """
            INSERT INTO customers (first_name, last_name, email, phone, driver_license) 
            VALUES (%s, %s, %s, %s, %s)
            """
            if self.db.execute_query(query, (
                first_name_entry.get(), last_name_entry.get(), email_entry.get(),
                phone_entry.get(), license_entry.get()
            )):
                messagebox.showinfo("Success", "Customer registered successfully!")
                dialog.destroy()
                self.load_customers()
                self.load_recent_activity()
            else:
                messagebox.showerror("Error", "Failed to register customer!")
        
        tk.Button(dialog, text="Register", command=save_customer, 
                 bg='#27ae60', fg='white').pack(pady=20)
    
    def rent_car_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Rent a Car")
        dialog.geometry("500x400")
        
        # Customer selection
        tk.Label(dialog, text="Select Customer:").pack(pady=5)
        customer_var = tk.StringVar()
        customers = self.db.fetch_all("SELECT customer_id, first_name, last_name FROM customers ORDER BY first_name")
        customer_combo = ttk.Combobox(dialog, textvariable=customer_var, width=40)
        customer_combo['values'] = [f"{cid}: {fname} {lname}" for cid, fname, lname in customers]
        customer_combo.pack(pady=5)
        
        # Car selection
        tk.Label(dialog, text="Select Available Car:").pack(pady=5)
        car_var = tk.StringVar()
        cars = self.db.fetch_all("SELECT car_id, make, model, daily_rate FROM cars WHERE status = 'Available'")
        car_combo = ttk.Combobox(dialog, textvariable=car_var, width=40)
        car_combo['values'] = [f"{cid}: {make} {model} - ${rate}/day" for cid, make, model, rate in cars]
        car_combo.pack(pady=5)
        
        # Rental days
        tk.Label(dialog, text="Rental Days:").pack(pady=5)
        days_entry = tk.Entry(dialog, width=10)
        days_entry.insert(0, "1")
        days_entry.pack(pady=5)
        
        # Cost display
        cost_label = tk.Label(dialog, text="Total Cost: $0.00", font=('Arial', 12, 'bold'))
        cost_label.pack(pady=10)
        
        def calculate_cost():
            try:
                days = int(days_entry.get())
                car_text = car_var.get()
                if car_text:
                    daily_rate = float(car_text.split('$')[-1].split('/')[0])
                    total = days * daily_rate
                    cost_label.config(text=f"Total Cost: ${total:.2f}")
            except:
                pass
        
        days_entry.bind('<KeyRelease>', lambda e: calculate_cost())
        car_combo.bind('<<ComboboxSelected>>', lambda e: calculate_cost())
        
        def process_rental():
            try:
                customer_id = int(customer_var.get().split(':')[0])
                car_id = int(car_var.get().split(':')[0])
                days = int(days_entry.get())
                
                rental_date = datetime.now().date()
                expected_return = rental_date + timedelta(days=days)
                
                # Get daily rate
                car = self.db.fetch_one("SELECT daily_rate FROM cars WHERE car_id = %s", (car_id,))
                total_cost = days * car[0]
                
                # Create rental
                rental_query = """
                INSERT INTO rentals (customer_id, car_id, rental_date, expected_return_date, total_cost) 
                VALUES (%s, %s, %s, %s, %s)
                """
                
                # Update car status
                update_car_query = "UPDATE cars SET status = 'Rented' WHERE car_id = %s"
                
                if (self.db.execute_query(rental_query, (customer_id, car_id, rental_date, expected_return, total_cost)) and
                    self.db.execute_query(update_car_query, (car_id,))):
                    
                    # Create payment
                    payment_query = """
                    INSERT INTO payments (rental_id, amount, payment_method) 
                    VALUES ((SELECT rental_id FROM rentals ORDER BY rental_id DESC LIMIT 1), %s, 'Credit Card')
                    """
                    self.db.execute_query(payment_query, (total_cost,))
                    
                    messagebox.showinfo("Success", "Car rented successfully!")
                    dialog.destroy()
                    self.load_cars()
                    self.load_rentals()
                    self.load_recent_activity()
                else:
                    messagebox.showerror("Error", "Failed to rent car!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Please check all fields!\n{str(e)}")
        
        tk.Button(dialog, text="Rent Car", command=process_rental,
                 bg='#3498db', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def return_car_dialog(self):
        rental_id = simpledialog.askinteger("Return Car", "Enter Rental ID:")
        if rental_id:
            # Get rental details
            query = """
            SELECT r.rental_id, r.car_id, c.first_name, c.last_name, car.make, car.model 
            FROM rentals r 
            JOIN customers c ON r.customer_id = c.customer_id 
            JOIN cars car ON r.car_id = car.car_id 
            WHERE r.rental_id = %s AND r.status = 'Active'
            """
            rental = self.db.fetch_one(query, (rental_id,))
            
            if rental:
                if messagebox.askyesno("Confirm Return", 
                                      f"Return car for {rental[2]} {rental[3]}?\nCar: {rental[4]} {rental[5]}"):
                    return_query = "UPDATE rentals SET return_date = CURRENT_DATE, status = 'Completed' WHERE rental_id = %s"
                    update_car_query = "UPDATE cars SET status = 'Available' WHERE car_id = %s"
                    
                    if (self.db.execute_query(return_query, (rental_id,)) and 
                        self.db.execute_query(update_car_query, (rental[1],))):
                        messagebox.showinfo("Success", "Car returned successfully!")
                        self.load_cars()
                        self.load_rentals()
                        self.load_recent_activity()
                    else:
                        messagebox.showerror("Error", "Failed to return car!")
            else:
                messagebox.showerror("Error", "Rental not found or already returned!")
    
    def add_car_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Car")
        dialog.geometry("300x400")
        
        fields = [
            ("Make", "Toyota"),
            ("Model", "Corolla"),
            ("Year", "2023"),
            ("Color", "White"),
            ("License Plate", "ABC-123"),
            ("Daily Rate", "45.00"),
            ("Fuel Type", "Gasoline"),
            ("Mileage", "0")
        ]
        
        entries = {}
        for label, default in fields:
            tk.Label(dialog, text=label + ":").pack(pady=2)
            entry = tk.Entry(dialog, width=30)
            entry.insert(0, default)
            entry.pack(pady=2)
            entries[label] = entry
        
        def save_car():
            query = """
            INSERT INTO cars (make, model, year, color, license_plate, daily_rate, fuel_type, mileage) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            if self.db.execute_query(query, (
                entries['Make'].get(), entries['Model'].get(), int(entries['Year'].get()),
                entries['Color'].get(), entries['License Plate'].get(), 
                float(entries['Daily Rate'].get()), entries['Fuel Type'].get(),
                int(entries['Mileage'].get())
            )):
                messagebox.showinfo("Success", "Car added successfully!")
                dialog.destroy()
                self.load_cars()
            else:
                messagebox.showerror("Error", "Failed to add car!")
        
        tk.Button(dialog, text="Add Car", command=save_car,
                 bg='#27ae60', fg='white').pack(pady=20)

def main():
    root = tk.Tk()
    app = CarRentalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    