import random
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import mysql.connector
from datetime import date
import csv
import pickle
import os
from tkinter import messagebox



# ------------------ DB CONFIG ------------------
DB_HOST     = 'localhost'
DB_USER     = 'root'
DB_PASSWORD = 'password'
DB_NAME     = 'grocery_db'

# ------------------ SIMPLE DB CONNECT ------------------
def db_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,charset='utf8'
    )

# ------------------ INIT DB ------------------
def init_db():
    # create DB
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,charset='utf8')
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    cur.close()
    conn.close()

    # create tables
    conn = db_conn()
    cur = conn.cursor()          # app_users->customers ,doners
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_users (      
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE,
            password VARCHAR(80)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_ngos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE,
            password VARCHAR(80)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE,
            password VARCHAR(80)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_donations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            donor_id INT,
            category VARCHAR(100),
            item VARCHAR(100),
            quantity INT,
            donated_on DATE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_claims (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ngo_id INT,
            donation_id INT,
            claimed_qty INT,
            claimed_on DATE
        )
    """)
    # ensure default admin exists (insecure password for demo)
    try:
        cur.execute("INSERT INTO app_admins (username, password) VALUES (%s,%s)", ('admin','admin123'))
    except mysql.connector.IntegrityError:
        pass
    conn.commit()
    cur.close()
    conn.close()

# ------------------ CATEGORY DATA ------------------
def category_data():
    return {
        'Fruits': ['Apple','Banana','Mango','Orange'],
        'Vegetables': ['Carrot','Potato','Tomato','Onion'],
        'Snacks & Sweets': ['Choco Bar','Cookies','Brownie','Ice Cream'],
        'Beverages': ['Water','Orange Juice','Cola','Tea'],
    }

# ------------------ APP STATE ------------------
app = {                   # app is a global dictionary
    'root': None,
    'user_id': None,
    'role': None,
    'stage': 0,
    'store': None,
    'buy_cart': {},
    'donate_cart': {},
    'prices': {},
    'stock': {},
    'stores': [
        ('FreshMart', '123 Market St'),
        ('GreenGrocer', '45 Green Rd'),
        ('DailyNeeds', '78 Daily Ave')
    ],
    'ngo_data': {},
    'ngo_stage': 0,
    'claim_cart': {}
}

def generate_prices_and_stock():
    prices = {}
    stock = {}
    for cat_items in category_data().values():  #['Apple','Banana','Mango','Orange']-> cat_items
        for item in cat_items:
            prices[item] = random.randint(10, 100)
            stock[item] = random.randint(1, 50)
    app['prices'] = prices
    app['stock'] = stock

# ------------------ GUI HELPERS ------------------
def clear_content():
    for w in content_frame.winfo_children():
        w.destroy()

def msg_screen(message):
    clear_content()
    tk.Label(content_frame, text=message, font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=50)
    tk.Button(content_frame, text="Back to Home", command=home_screen,
              bg=btn_color, fg="white", width=18).pack()

def show_error(msg):
    """Simple popup for errors."""
    messagebox.showerror("Error", msg)
# ------------------ HOME SCREEN ------------------
def home_screen():           #Clears previous session data
    app['role'] = None
    app['user_id'] = None
    app['stage'] = 0
    app['store'] = None
    app['buy_cart'].clear()
    app['donate_cart'].clear()
    app['claim_cart'].clear()

    clear_content()
    tk.Label(content_frame, text="Welcome to Grocery & Donation",
             font=("Segoe UI", 18, "bold"), bg=card_bg).pack(pady=(10,10))
    tk.Label(content_frame, text="Choose your role to continue:",
             font=("Segoe UI", 12), bg=card_bg).pack(pady=(0,15))

    btn_frame = tk.Frame(content_frame, bg=card_bg)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Customer", command=lambda: login_register('customer'),
              bg=btn_color, fg="white", width=18).grid(row=0, column=0, padx=8, pady=8)
    tk.Button(btn_frame, text="Donor", command=lambda: login_register('donor'),
              bg=btn_color, fg="white", width=18).grid(row=0, column=1, padx=8, pady=8)
    tk.Button(btn_frame, text="NGO", command=lambda: login_register('ngo'),
              bg=btn_color, fg="white", width=18).grid(row=1, column=0, padx=8, pady=8)
    tk.Button(btn_frame, text="Admin", command=lambda: login_register('admin'),
              bg=btn_color, fg="white", width=18).grid(row=1, column=1, padx=8, pady=8)

# ------------------ LOGIN / REGISTER ------------------
def login_register(role): #--> called twice 1) home_screen()
    app['role'] = role    #                 2) auth_screen()- when back pressed
    clear_content()
    tk.Label(content_frame, text=f"{role.capitalize()} Portal",
             font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=(10,15))

    frm = tk.Frame(content_frame, bg=card_bg); frm.pack(pady=6)
    if role != 'admin':
        tk.Button(frm, text="Login", command=lambda: auth_screen('login'),
                  bg=btn_color, fg="white", width=14).grid(row=0, column=0, padx=12, pady=8)
        tk.Button(frm, text="Register", command=lambda: auth_screen('register'),
                  bg=btn_color, fg="white", width=14).grid(row=0, column=1, padx=12, pady=8)
    else:
        # admin only login (no register)
        tk.Button(frm, text="Login (Admin)", command=lambda: auth_screen('login'),
                  bg=btn_color, fg="white", width=14).grid(row=0, column=0, padx=12, pady=8)

    tk.Button(content_frame, text="Back", command=home_screen, width=12).pack(pady=10)

def auth_screen(action):
    clear_content()
    tk.Label(content_frame, text=f"{action.capitalize()} ({app['role']})",
             font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=(6,12))

    app['var_usr'] = tk.StringVar() #tk.StringVar() creates a variable that automatically stores what’s typed inside an Entry box.
    app['var_pwd'] = tk.StringVar()

    frm = tk.Frame(content_frame, bg=card_bg); frm.pack(pady=4)
    tk.Label(frm, text="Username:", bg=card_bg).grid(row=0, column=0, sticky='e', padx=6, pady=6) #sticky='e' means align the label to the east (right) side of the grid cell
    tk.Entry(frm, textvariable=app['var_usr'], width=28).grid(row=0, column=1, padx=6, pady=6)
    tk.Label(frm, text="Password:", bg=card_bg).grid(row=1, column=0, sticky='e', padx=6, pady=6)
    tk.Entry(frm, textvariable=app['var_pwd'], show='*', width=28).grid(row=1, column=1, padx=6, pady=6)

    info_label = tk.Label(content_frame, text="", bg=card_bg, fg="red")
    info_label.pack(pady=6)

    def submit(): #--->submit() is called (from the button’s command)
        name = app['var_usr'].get().strip()  #.get() → reads what the user typed
        pwd  = app['var_pwd'].get().strip()  #.strip() → removes any accidental extra spaces before/after the input.
        if not name or not pwd:
            info_label.config(text="Please fill both username and password", fg='red')
            return

        if app['role'] == 'admin':
            table = 'app_admins'
        elif app['role'] == 'ngo':
            table = 'app_ngos'
        else:
            table = 'app_users'

        conn = db_conn()
        cur = conn.cursor()
        if action == 'register':
            if app['role'] == 'admin':
                info_label.config(text="Admin self-register disabled", fg='red')
            else:
                try:
                    cur.execute(f"INSERT INTO {table} (username, password) VALUES (%s, %s)", (name, pwd))
                    conn.commit()
                    # Clear the entry boxes (not the DB)
                    app['var_usr'].set("")
                    app['var_pwd'].set("")

                    # Redirect to login page
                    auth_screen('login')
                except mysql.connector.IntegrityError:
                    info_label.config(text="That username is taken.", fg='red')
        else:  # login
            cur.execute(f"SELECT id FROM {table} WHERE username=%s AND password=%s", (name, pwd))
            row = cur.fetchone()
            if row:
                app['user_id'] = row[0]
                if app['role'] == 'customer':
                    app['username'] = name  # Store username for receipts
                    pick_store(donating=False)
                elif app['role'] == 'donor':
                    pick_store(donating=True) # used in pick store func below
                elif app['role'] == 'ngo':
                    ngo_portal()
                else:
                    admin_portal()
            else:
                info_label.config(text="Wrong username/password", fg='red')
        cur.close()
        conn.close()

    tk.Button(content_frame, text="Submit", command=submit,  # submit func called
              bg=btn_color, fg="white", width=14).pack(pady=8)
    tk.Button(content_frame, text="Back", command=lambda: login_register(app['role']),
              width=12).pack()

# ------------------ PICK STORE ------------------
  # (used by both buyers(customers) and donors)
  
def pick_store(donating): #--> called in def submit()
    clear_content()       # donating = True (user is doner) else False
    tk.Label(content_frame, text="Pick a Store", font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=(8,10))

    lb = tk.Listbox(content_frame, width=50, height=6)
    lb.pack(pady=10)
    for s, addr in app['stores']:   # s->store name , addr->address
        lb.insert('end', f"{s} — {addr}")

    btn = tk.Button(content_frame, text="Next", state='disabled',  #Prevents moving forward without selection
                    command=lambda: after_store(lb, donating), bg=btn_color, fg="white", width=12)
    btn.pack(pady=8)

    def on_select(evt): #called after 2 lines
        if lb.curselection():
            btn.config(state='normal')
    lb.bind('<<ListboxSelect>>', on_select)

def after_store(lb, donating): #called 6 lines before this(Called when Next is clicked)
    pick = lb.curselection()  #Returns a tuple containing the index of the selected item in the Listbox.
                              #if the user selected “GreenGrocer”, then pick = (1,)
    if not pick: return       
    app['store'] = app['stores'][pick[0]][0]   #it picks the first value (store name) and stores it in app['store'].
    app['stage'] = 0 #This variable tracks which category we are currently on
    if donating:
        donate_screen()
    else:
        buy_screen()

# ------------------ BUY FLOW ------------------
def buy_screen():
    clear_content()
    cats = list(category_data().keys())  #['Fruits','Vegetables',...]
    cat = cats[app['stage']]     #app['stage'] = 0 (initially)
    tk.Label(content_frame, text=f"{app['store']} — {cat}", font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=8) # heading like : FreshMart — Fruits

    
    total_amt = sum(app['prices'][i]*q for i,q in app['buy_cart'].items())
    app['tot_lbl'] = tk.Label(content_frame, text=f"Total: ₹{total_amt}", font=("Segoe UI", 12, "bold"), bg=card_bg)
    app['tot_lbl'].pack(pady=6)

    #---GUI------
    box = tk.Frame(content_frame, bg=card_bg); box.pack(expand=True, fill='both', padx=10, pady=6)
    canvas = tk.Canvas(box, bg=card_bg, highlightthickness=0)
    sb = ttk.Scrollbar(box, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas, bg=card_bg)
    canvas.create_window((0,0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=sb.set)
    inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.pack(side='left', fill='both', expand=True); sb.pack(side='right', fill='y')

    for item in category_data()[cat]:
        row = tk.Frame(inner, bg=card_bg); row.pack(fill='x', pady=4)
        stock_qty = app['stock'].get(item, 0)   # get current stock from app state
        tk.Label(row, text=f"{item} (₹{app['prices'][item]}) - Stock: {stock_qty}", width=40, anchor='w', bg=card_bg).pack(side='left')
        v = tk.IntVar(value=app['buy_cart'].get(item,0))
        entry = tk.Entry(row, width=5, textvariable=v)
        entry.pack(side='left', padx=6)
        entry.bind("<FocusIn>", lambda e, var=v: (var.set("") if var.get() == 0 else None))
        #When user clicks on the box, it clears "0" for easy typing.
        v.trace_add('write', lambda *_, it=item, var=v: update_buy(it,var))


    nav = tk.Frame(content_frame, bg=card_bg); nav.pack(pady=10)
    tk.Button(nav, text="Back", command=buy_back, width=12).pack(side='left', padx=12)
    btn_text = "Pay" if app['stage']==len(category_data())-1 else "Next"
    tk.Button(nav, text=btn_text, command=buy_next, bg=btn_color, fg="white", width=12).pack(side='right', padx=12)

def update_buy(item,var):
    try:
        q = int(var.get())
    except:
        q = 0
    stock = app['stock'].get(item,0)
    if q < 0:
        q = 0
    if q > stock:
        show_error(f"Only {stock} {item}(s) available.")
        q = stock
    app['buy_cart'][item] = q
    var.set(q)
    total = sum(app['prices'][i]*n for i,n in app['buy_cart'].items())
    app['tot_lbl'].config(text=f"Total: ₹{total}")


def buy_back():
    if app['stage']==0: pick_store(donating=False)
    else:
        app['stage']-=1
        buy_screen()

def buy_next():
    if app['stage']==len(category_data())-1:
        pay_screen()
    else:
        app['stage']+=1
        buy_screen()

def pay_screen():
    clear_content()
    amt = sum(app['prices'][i]*n for i,n in app['buy_cart'].items())
    tk.Label(content_frame, text=f"Pay ₹{amt}", font=("Segoe UI",16,"bold"), bg=card_bg).pack(pady=20)
    tk.Button(content_frame, text="Cash on Delivery",
          command=lambda: complete_purchase("Cash on Delivery"),
          bg=btn_color, fg="white", width=20).pack(pady=8)
    tk.Button(content_frame, text="Pay (simulate)",
          command=lambda: complete_purchase("Online Payment"),
          bg=btn_color, fg="white", width=20).pack(pady=8)
# WHY: Connects payment buttons to function that updates stock & generates receipt


#(UPDATES STOCK AND GENERATES RECIEPT AFTER PAYMENT)


def complete_purchase(payment_mode):

    # ---------------- UPDATE STOCK ----------------
    for item, qty in app['buy_cart'].items():
        app['stock'][item] -= qty  # decrease stock for next buyers

    # ---------------- GENERATE RECEIPT ----------------
    today = date.today()
    store_name = app.get('store', 'GROCERY STORE')
    customer = app.get('username', 'Customer')
    folder = "receipts"
    if not os.path.exists(folder):
        os.makedirs(folder)  # create folder if missing
    filename = os.path.join(folder, f"receipt_{customer}_{today}.txt")


    # Calculate total
    total_amt = 0
    for item, qty in app['buy_cart'].items():             # app['buy_cart'] = {'Apple': 2,'Banana': 5,'Milk': 1}
                                                          # [('Apple', 2),('Banana', 5),('Milk', 1)]-->items()
        if qty > 0:
            total_amt += app['prices'][item] * qty

    # Create formatted receipt text
    lines = []
    lines.append(f"{store_name.center(35)}")
    lines.append("-" * 35)
    lines.append("GROCERY PURCHASE RECEIPT".center(35))
    lines.append("-" * 35)
    lines.append(f"Customer : {customer}")
    lines.append(f"Date     : {today}")
    lines.append(f"Payment  : {payment_mode}")
    lines.append("-" * 35)
    lines.append(f"{'Item':15}{'Qty':>5}{'Price':>10}")
    lines.append("-" * 35)

    for item, qty in app['buy_cart'].items():
        if qty > 0:
            price = app['prices'][item] * qty
            # Format so columns align (left, right justified)
            lines.append(f"{item:15}{qty:>5}{price:>10}")

    lines.append("-" * 35)
    lines.append(f"{'TOTAL AMOUNT:':<20}{'₹'+str(total_amt):>14}")
    lines.append("-" * 35)
    lines.append("Thank you for shopping with us!".center(35))
    lines.append("-" * 35)

    receipt_text = "\n".join(lines)

    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(receipt_text)

    # ---------------- SHOW RECEIPT ON SCREEN ----------------
    clear_content()
    tk.Label(content_frame, text="Payment Successful!", font=("Segoe UI",16,"bold"), bg=card_bg, fg="green").pack(pady=(10,5))
    tk.Label(content_frame, text="Your receipt has been generated:", font=("Segoe UI",12,"bold"), bg=card_bg).pack(pady=(0,10))

    # Scrollable display area
    box = tk.Frame(content_frame, bg=card_bg)
    box.pack(expand=True, fill='both', padx=10, pady=6)
    canvas = tk.Canvas(box, bg="white", highlightthickness=1)
    sb = ttk.Scrollbar(box, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas, bg="white")
    canvas.create_window((0,0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=sb.set)
    inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.pack(side='left', fill='both', expand=True)
    sb.pack(side='right', fill='y')

    tk.Label(inner, text=receipt_text, bg="white", font=("Courier New",11), justify='left', anchor='w').pack(padx=10, pady=10)

    tk.Button(content_frame, text="Back to Home", command=home_screen, bg=btn_color, fg="white", width=18).pack(pady=12)

    # ---------------- CLEANUP ----------------
    app['buy_cart'].clear()



# ------------------ DONATE FLOW ------------------
def donate_screen():
    clear_content()
    cats = list(category_data().keys()) #category_data()-->{ 'Fruits': [...], 'Vegetables': [...] }
    cat = cats[app['stage']]   #cat=Current category user is donating from
    tk.Label(content_frame, text=f"Donate — {cat}", font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=8)

    total_items = sum(app['donate_cart'].values())  #{'Rice': 5,'Milk': 2}-->app['donate_cart']  
    app['don_lbl'] = tk.Label(content_frame, text=f"Total items: {total_items}", font=("Segoe UI", 12, "bold"), bg=card_bg)
    app['don_lbl'].pack(pady=6)

    #---GUI---
    box = tk.Frame(content_frame, bg=card_bg); box.pack(expand=True, fill='both', padx=10, pady=6)
    canvas = tk.Canvas(box, bg=card_bg, highlightthickness=0)
    sb = ttk.Scrollbar(box, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas, bg=card_bg)
    canvas.create_window((0,0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=sb.set)
    inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.pack(side='left', fill='both', expand=True); sb.pack(side='right', fill='y')

    for item in category_data()[cat]:
        row = tk.Frame(inner, bg=card_bg); row.pack(fill='x', pady=4)
        stock_qty = app['stock'].get(item, 0)
        tk.Label(row, text=item + " - Stock: " + str(stock_qty), width=40, anchor='w', bg=card_bg).pack(side='left')#Donor can see how many of this item are currently available

        v = tk.IntVar(value=app['donate_cart'].get(item,0))
        entry = tk.Entry(row, width=5, textvariable=v)
        entry.pack(side='left', padx=6)
        entry.bind("<FocusIn>", lambda e, var=v: (var.set("") if var.get() == 0 else None))
        v.trace_add('write', lambda *_, it=item, var=v: update_donate(it,var))


    nav = tk.Frame(content_frame, bg=card_bg); nav.pack(pady=10)
    tk.Button(nav, text="Back", command=donate_back, width=12).pack(side='left', padx=12)
    btn_text = "Finish" if app['stage']==len(category_data())-1 else "Next"
    tk.Button(nav, text=btn_text, command=donate_next, bg=btn_color, fg="white", width=12).pack(side='right', padx=12)

def update_donate(item,var):
    try:
        q = int(var.get())
    except:
        q = 0
    if q < 0:
        q = 0
    if q > 9999:  
        show_error("Invalid donation quantity!")
        q = 9999
    app['donate_cart'][item] = q
    var.set(q)
    total = sum(app['donate_cart'].values())
    app['don_lbl'].config(text=f"Total items: {total}")


def donate_back():
    if app['stage']==0: pick_store(donating=True)
    else:
        app['stage']-=1
        donate_screen()

def donate_next():
    if app['stage']==len(category_data())-1:
        save_donation()
    else:
        app['stage']+=1
        donate_screen()

def save_donation():
    conn = db_conn()
    cur = conn.cursor()
    today = date.today()
    for item,qty in app['donate_cart'].items():
        if qty<=0: continue
        for cat,items in category_data().items():
            if item in items:
                # Check if the donor already donated this item
                cur.execute("SELECT id, quantity FROM app_donations WHERE item=%s AND donor_id=%s", (item, app['user_id']))
                row = cur.fetchone()
                if row:
                    cur.execute("UPDATE app_donations SET quantity = quantity + %s WHERE id=%s", (qty, row[0])) #Aggregates donations for the same donor/item, prevents multiple rows
                else:
                    cur.execute('INSERT INTO app_donations (donor_id,category,item,quantity,donated_on) VALUES (%s,%s,%s,%s,%s)',
                (app['user_id'],cat,item,qty,today))
                #Update in-memory stock
                app['stock'][item] += qty #Makes newly donated items visible to all users

                break
    conn.commit()
    cur.close()
    conn.close()
    app['donate_cart'].clear()
    msg_screen("Thank you for donating!")

# ------------------ NGO FLOW ------------------

def ngo_portal():
    
    clear_content()
    tk.Label(content_frame, text="Available Donations", font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=10)

    conn = db_conn()
    cur = conn.cursor()
    # Fetch all donations with positive qty, ordered by id so we can consume oldest-first.
    cur.execute("SELECT id, category, item, quantity FROM app_donations WHERE quantity > 0 ORDER BY id ASC") #ORDER BY id ASC → oldest donations are consumed first (FIFO)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        tk.Label(content_frame, text="No items available yet.", font=("Segoe UI", 12), bg=card_bg).pack(pady=40)
        tk.Button(content_frame, text="Back", command=home_screen, width=12).pack(pady=10)
        return

    # Build aggregated view and per-row mapping
    by_cat_agg = {}     # { category: { item: total_qty } } eg:{'Fruits': {'Apple': 10, 'Banana': 5}}
    by_cat_rows = {}    # { category: { item: [(donation_id, qty), ...] } } eg: {'Fruits': {'Apple': [[1, 5], [3, 5]]}}

    for did, cat, item, qty in rows:
        by_cat_agg.setdefault(cat, {})
        by_cat_rows.setdefault(cat, {})
        by_cat_agg[cat][item] = by_cat_agg[cat].get(item, 0) + qty
        by_cat_rows[cat].setdefault(item, []).append([did, qty])  # list of [id, qty]

    # Convert aggregated dict to list-of-tuples for UI consistency
    ui_data = {}
    for cat, items in by_cat_agg.items():
        ui_data[cat] = [(item, items[item]) for item in items]

    # Save durable state for UI and for consumption later
    app['ngo_data'] = ui_data         # used by ngo_category_screen() to show (item, total)
    app['_ngo_rows'] = by_cat_rows    # used by save_claims() to consume donation rows
    app['ngo_stage'] = 0
    app['claim_cart'] = {}           # keyed by item name (aggregated)

    ngo_category_screen()



def ngo_category_screen():
    clear_content()
    cat_list = list(app.get('ngo_data', {}).keys())
    if not cat_list:
        tk.Label(content_frame, text="No categories found.", font=("Segoe UI", 12), bg=card_bg).pack(pady=40)
        tk.Button(content_frame, text="Back", command=home_screen, width=12).pack(pady=10)
        return

    cat = cat_list[app['ngo_stage']]
    tk.Label(content_frame, text=f"{cat}", font=("Segoe UI", 16, "bold"), bg=card_bg).pack(pady=10)

    total = sum(app['claim_cart'].values())  #{'Rice': 10, 'Milk': 3}-->claim_cart format

    app['claim_lbl'] = tk.Label(content_frame, text=f"Items to claim: {total}", font=("Segoe UI", 12, "bold"), bg=card_bg)
    app['claim_lbl'].pack(pady=6)

    box = tk.Frame(content_frame, bg=card_bg); box.pack(expand=True, fill='both', padx=10, pady=6)
    canvas = tk.Canvas(box, bg=card_bg, highlightthickness=0)
    sb = ttk.Scrollbar(box, orient='vertical', command=canvas.yview)
    inner = tk.Frame(canvas, bg=card_bg)
    canvas.create_window((0,0), window=inner, anchor='nw')
    canvas.configure(yscrollcommand=sb.set)
    inner.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.pack(side='left', fill='both', expand=True); sb.pack(side='right', fill='y')

    # app['ngo_data'][cat] is list of (item, total_qty)
    for item, avail in app['ngo_data'][cat]:
        row = tk.Frame(inner, bg=card_bg); row.pack(fill='x', pady=4)
        tk.Label(row, text=item + " (Available: " + str(avail) + ")", width=40, anchor='w', bg=card_bg).pack(side='left')

        v = tk.IntVar(value=app['claim_cart'].get(item, 0))
        ent = tk.Entry(row, width=5, textvariable=v)
        ent.pack(side='left', padx=6)
        ent.bind("<FocusIn>", lambda e, var=v: (var.set("") if var.get() == 0 else None))
        v.trace_add('write', lambda *_, it=item, a=avail, var=v: update_claim(it, a, var))
        

    nav = tk.Frame(content_frame, bg=card_bg); nav.pack(pady=10)
    tk.Button(nav, text="Back", command=claim_back, width=12).pack(side='left', padx=12)
    nxt = "Finish" if app['ngo_stage'] == len(cat_list)-1 else "Next"
    tk.Button(nav, text=nxt, command=claim_next, bg=btn_color, fg="white", width=12).pack(side='right', padx=12)



def update_claim(item, avail, var):
    """
    Update app['claim_cart'] using item name as the key.
    Parameters:
      item: item name (string)
      avail: maximum available (aggregated)
      var: IntVar bound to the Entry widget
    """
    try:
        q = int(var.get())
    except Exception:
        q = 0
    if q < 0:
        q = 0
    if q > avail:
        show_error(f"Only {avail} {item}(s) available to claim.")
        q = avail
    app['claim_cart'][item] = q
    var.set(q)  # ensure Entry shows the clamped value
    total = sum(app['claim_cart'].values())
    # update label if present
    if 'claim_lbl' in app:
        try:
            app['claim_lbl'].config(text=f"Items to claim: {total}")
        except Exception:
            pass


def claim_back():
    if app['ngo_stage'] == 0:
        home_screen()
    else:
        app['ngo_stage'] -= 1
        ngo_category_screen()

def claim_next():
    cat_list = list(app['ngo_data'].keys())
    if app['ngo_stage'] == len(cat_list)-1:
        save_claims()
    else:
        app['ngo_stage'] += 1
        ngo_category_screen()


def save_claims():
    if not app.get('claim_cart'):
        msg_screen("No items selected to claim.")
        return

    conn = db_conn()
    cur = conn.cursor()
    today = date.today()

    # app['_ngo_rows'] must exist: {category: { item: [[donation_id, qty], ...] } }
    ngo_rows = app.get('_ngo_rows', {})

    # We'll build a list of DB updates/inserts to do; but we'll perform them as we go.
    for item, need_qty in list(app['claim_cart'].items()):
        if need_qty <= 0:
            continue

        # Find which category contains this item (ui stored by category)
        found_cat = None
        for cat, lst in app.get('ngo_data', {}).items():
            if any(it == item for (it, _) in lst):
                found_cat = cat
                break
        if not found_cat:
            # item not present (maybe stale UI) — skip
            continue

        row_list = ngo_rows.get(found_cat, {}).get(item, [])
        # row_list is list of [donation_id, qty_available_in_that_row]
        i = 0
        while need_qty > 0 and i < len(row_list):
            donation_id, available_in_row = row_list[i]
            if available_in_row <= 0:
                i += 1
                continue

            take = min(need_qty, available_in_row)
            # Insert claim referencing the donation row
            cur.execute(
                "INSERT INTO app_claims (ngo_id, donation_id, claimed_qty, claimed_on) VALUES (%s,%s,%s,%s)",
                (app['user_id'], donation_id, take, today)
            )

            # Decrease donation row quantity
            new_row_qty = available_in_row - take
            if new_row_qty > 0:
                cur.execute("UPDATE app_donations SET quantity=%s WHERE id=%s", (new_row_qty, donation_id))
                # update the local cached row quantity too
                row_list[i][1] = new_row_qty
            else:
                # fully consumed -> set to 0 (or delete if you prefer)
                cur.execute("UPDATE app_donations SET quantity=0 WHERE id=%s", (donation_id,))
                row_list[i][1] = 0

            need_qty -= take
            # move to next donation row if needed
            if row_list[i][1] == 0:
                i += 1

        # If we couldn't satisfy the full need_qty (not enough donations), we claim whatever we could.
        claimed_for_item = app['claim_cart'][item] - max(0, need_qty)
        if claimed_for_item > 0:
            # Update in-memory stock exactly once per claimed amount
            app['stock'][item] = app.get('stock', {}).get(item, 0) - claimed_for_item
            # Also update the aggregated UI data so next view shows updated totals
            # reduce value in app['ngo_data']
            for idx, (it, qty) in enumerate(app['ngo_data'][found_cat]):
                if it == item:
                    app['ngo_data'][found_cat][idx] = (it, max(0, qty - claimed_for_item))
                    break

    conn.commit()
    cur.close()
    conn.close()
    app['claim_cart'].clear()
    clear_content()
    tk.Label(content_frame, text="Items successfully claimed!", font=("Segoe UI",16,"bold"), bg=card_bg, fg="green").pack(pady=30)
    tk.Button(content_frame, text="Back to Home", command=home_screen, bg=btn_color, fg="white", width=18).pack(pady=8)



# ------------------ ADMIN PORTAL ------------------
def admin_portal():
    clear_content()
    tk.Label(content_frame, text="Admin Portal", font=("Segoe UI",16,"bold"), bg=card_bg).pack(pady=10)

    btn_frame = tk.Frame(content_frame, bg=card_bg); btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="Manage Users", width=18, command=admin_manage_users, bg=btn_color, fg='white').grid(row=0,column=0,padx=6,pady=6)
    tk.Button(btn_frame, text="Manage NGOs", width=18, command=admin_manage_ngos, bg=btn_color, fg='white').grid(row=0,column=1,padx=6,pady=6)
    tk.Button(btn_frame, text="Manage Donations", width=18, command=admin_manage_donations, bg=btn_color, fg='white').grid(row=1,column=0,padx=6,pady=6)
    tk.Button(btn_frame, text="Manage Claims", width=18, command=admin_manage_claims, bg=btn_color, fg='white').grid(row=1,column=1,padx=6,pady=6)

    file_frame = tk.Frame(content_frame, bg=card_bg); file_frame.pack(pady=10)
    tk.Button(file_frame, text="Export Donations to CSV", command=admin_export_donations).grid(row=0,column=0,padx=6,pady=6)
    tk.Button(file_frame, text="Import Donations from CSV", command=admin_import_donations).grid(row=0,column=1,padx=6,pady=6)
    tk.Button(file_frame, text="Backup Donations (binary)", command=admin_backup_donations).grid(row=1,column=0,padx=6,pady=6)
    tk.Button(file_frame, text="Restore Donations (binary)", command=admin_restore_donations).grid(row=1,column=1,padx=6,pady=6)
    tk.Button(content_frame, text="Back", command=home_screen).pack(pady=12)

# ----- Admin: Manage Users -----
def admin_manage_users():
    clear_content()
    tk.Label(content_frame, text="Manage Users", font=("Segoe UI",14,"bold"), bg=card_bg).pack(pady=6)
    frame = tk.Frame(content_frame, bg=card_bg); frame.pack(fill='both', expand=True, padx=6, pady=6)

    cols = ('ID','Username')
    lb = ttk.Treeview(frame, columns=cols, show='headings')
    for c in cols: lb.heading(c, text=c)
    lb.pack(side='left', fill='both', expand=True)

    sb = ttk.Scrollbar(frame, orient='vertical', command=lb.yview); sb.pack(side='right', fill='y')
    lb.configure(yscrollcommand=sb.set)

    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, username FROM app_users")
    for r in cur.fetchall():
        lb.insert('', 'end', values=r)
    cur.close(); conn.close()

    btnf = tk.Frame(content_frame, bg=card_bg); btnf.pack(pady=6)
    tk.Button(btnf, text="Add User", command=lambda: admin_add_user(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Edit Selected", command=lambda: admin_edit_user(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Delete Selected", command=lambda: admin_delete_user(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Back", command=admin_portal).pack(side='left', padx=6)

def admin_add_user(tree):
    username = simpledialog.askstring("Add user", "Username:", parent=app['root'])
    if not username: return
    password = simpledialog.askstring("Add user", "Password:", parent=app['root'])
    if password is None: return
    conn = db_conn(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO app_users (username,password) VALUES (%s,%s)", (username, password))
        conn.commit()
        tree.insert('', 'end', values=(cur.lastrowid, username))
    except mysql.connector.IntegrityError:
        tk.messagebox.showerror("Error", "Username taken")
    cur.close(); conn.close()

def admin_edit_user(tree):
    sel = tree.selection()
    if not sel: return
    item = tree.item(sel[0])['values']
    uid = item[0]
    new_username = simpledialog.askstring("Edit user", "New username:", initialvalue=item[1], parent=app['root'])
    if not new_username: return
    new_pass = simpledialog.askstring("Edit user", "New password (leave blank to keep):", parent=app['root'])
    conn = db_conn(); cur = conn.cursor()
    try:
        if new_pass:
            cur.execute("UPDATE app_users SET username=%s,password=%s WHERE id=%s", (new_username, new_pass, uid))
        else:
            cur.execute("UPDATE app_users SET username=%s WHERE id=%s", (new_username, uid))
        conn.commit()
        tree.item(sel[0], values=(uid, new_username))
    except mysql.connector.IntegrityError:
        tk.messagebox.showerror("Error", "Username taken")
    cur.close(); conn.close()

def admin_delete_user(tree):
    sel = tree.selection()
    if not sel: return
    item = tree.item(sel[0])['values']
    uid = item[0]

    # Check if user has donations
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM app_donations WHERE donor_id=%s", (uid,))
    donation_count = cur.fetchone()[0]

    if donation_count > 0:
        # Ask if admin wants to delete donations too
        msg = f"User {item[1]} has {donation_count} donation(s).\nDelete user AND all their donations?"
        if not tk.messagebox.askyesno("Confirm", msg):
            cur.close(); conn.close()
            return
        # Delete donations first (and their claims)
        cur.execute("DELETE FROM app_claims WHERE donation_id IN (SELECT id FROM app_donations WHERE donor_id=%s)", (uid,))
        cur.execute("DELETE FROM app_donations WHERE donor_id=%s", (uid,))
    else:
        # No donations, just confirm normal delete
        if not tk.messagebox.askyesno("Confirm", f"Delete user {item[1]}?"):
            cur.close(); conn.close()
            return

    # Now safe to delete user
    cur.execute("DELETE FROM app_users WHERE id=%s", (uid,))
    conn.commit(); cur.close(); conn.close()
    tree.delete(sel[0])

# ----- Admin: Manage NGOs (similar) -----
def admin_manage_ngos():
    clear_content()
    tk.Label(content_frame, text="Manage NGOs", font=("Segoe UI",14,"bold"), bg=card_bg).pack(pady=6)
    frame = tk.Frame(content_frame, bg=card_bg); frame.pack(fill='both', expand=True, padx=6, pady=6)
    cols = ('ID','Username')
    lb = ttk.Treeview(frame, columns=cols, show='headings')
    for c in cols: lb.heading(c, text=c)
    lb.pack(side='left', fill='both', expand=True)
    sb = ttk.Scrollbar(frame, orient='vertical', command=lb.yview); sb.pack(side='right', fill='y')
    lb.configure(yscrollcommand=sb.set)
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, username FROM app_ngos")
    for r in cur.fetchall(): lb.insert('', 'end', values=r)
    cur.close(); conn.close()
    btnf = tk.Frame(content_frame, bg=card_bg); btnf.pack(pady=6)
    tk.Button(btnf, text="Add NGO", command=lambda: admin_add_ngo(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Edit Selected", command=lambda: admin_edit_ngo(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Delete Selected", command=lambda: admin_delete_ngo(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Back", command=admin_portal).pack(side='left', padx=6)

def admin_add_ngo(tree):
    username = simpledialog.askstring("Add NGO", "Username:", parent=app['root'])
    if not username: return
    password = simpledialog.askstring("Add NGO", "Password:", parent=app['root'])
    if password is None: return
    conn = db_conn(); cur = conn.cursor()
    try:
        cur.execute("INSERT INTO app_ngos (username,password) VALUES (%s,%s)", (username, password))
        conn.commit()
        tree.insert('', 'end', values=(cur.lastrowid, username))
    except mysql.connector.IntegrityError:
        tk.messagebox.showerror("Error", "Username taken")
    cur.close(); conn.close()

def admin_edit_ngo(tree):
    sel = tree.selection()
    if not sel: return
    item = tree.item(sel[0])['values']
    uid = item[0]
    new_username = simpledialog.askstring("Edit NGO", "New username:", initialvalue=item[1], parent=app['root'])
    if not new_username: return
    new_pass = simpledialog.askstring("Edit NGO", "New password (leave blank to keep):", parent=app['root'])
    conn = db_conn(); cur = conn.cursor()
    try:
        if new_pass:
            cur.execute("UPDATE app_ngos SET username=%s,password=%s WHERE id=%s", (new_username, new_pass, uid))
        else:
            cur.execute("UPDATE app_ngos SET username=%s WHERE id=%s", (new_username, uid))
        conn.commit()
        tree.item(sel[0], values=(uid, new_username))
    except mysql.connector.IntegrityError:
        tk.messagebox.showerror("Error", "Username taken")
    cur.close(); conn.close()

def admin_delete_ngo(tree):
    sel = tree.selection()
    if not sel: return
    item = tree.item(sel[0])['values']
    uid = item[0]

    # Check if NGO has claims
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM app_claims WHERE ngo_id=%s", (uid,))
    claim_count = cur.fetchone()[0]

    if claim_count > 0:
        # Ask if admin wants to delete claims too
        msg = f"NGO {item[1]} has {claim_count} claim(s).\nDelete NGO AND all their claims?"
        if not tk.messagebox.askyesno("Confirm", msg):
            cur.close(); conn.close()
            return
        # Delete claims first
        cur.execute("DELETE FROM app_claims WHERE ngo_id=%s", (uid,))
    else:
        # No claims, just confirm normal delete
        if not tk.messagebox.askyesno("Confirm", f"Delete NGO {item[1]}?"):
            cur.close(); conn.close()
            return

    # Now safe to delete NGO
    cur.execute("DELETE FROM app_ngos WHERE id=%s", (uid,))
    conn.commit(); cur.close(); conn.close()
    tree.delete(sel[0])

# ----- Admin: Manage Donations -----
def admin_manage_donations():
    clear_content()
    tk.Label(content_frame, text="Manage Donations", font=("Segoe UI",14,"bold"), bg=card_bg).pack(pady=6)
    frame = tk.Frame(content_frame, bg=card_bg); frame.pack(fill='both', expand=True, padx=6, pady=6)
    cols = ('ID','Donor_ID','Category','Item','Quantity','Donated_on')
    lb = ttk.Treeview(frame, columns=cols, show='headings')
    for c in cols: lb.heading(c, text=c)
    lb.pack(side='left', fill='both', expand=True)
    sb = ttk.Scrollbar(frame, orient='vertical', command=lb.yview); sb.pack(side='right', fill='y')
    lb.configure(yscrollcommand=sb.set)
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, donor_id, category, item, quantity, donated_on FROM app_donations")
    for r in cur.fetchall(): lb.insert('', 'end', values=r)
    cur.close(); conn.close()
    btnf = tk.Frame(content_frame, bg=card_bg); btnf.pack(pady=6)
    tk.Button(btnf, text="Add Donation", command=lambda: admin_add_donation(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Edit Selected", command=lambda: admin_edit_donation(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Delete Selected", command=lambda: admin_delete_donation(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Back", command=admin_portal).pack(side='left', padx=6)

def admin_add_donation(tree):
    donor_id = simpledialog.askinteger("Add donation", "Donor ID:", parent=app['root'])
    if donor_id is None: return
    category = simpledialog.askstring("Add donation", "Category:", parent=app['root'])
    item = simpledialog.askstring("Add donation", "Item:", parent=app['root'])
    qty = simpledialog.askinteger("Add donation", "Quantity:", parent=app['root'], minvalue=1)
    if None in (category, item, qty): return
    today = date.today()
    conn = db_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO app_donations (donor_id,category,item,quantity,donated_on) VALUES (%s,%s,%s,%s,%s)",
                (donor_id, category, item, qty, today))
    conn.commit()
    tree.insert('', 'end', values=(cur.lastrowid, donor_id, category, item, qty, today))
    cur.close(); conn.close()

def admin_edit_donation(tree):
    sel = tree.selection(); 
    if not sel: return
    item = tree.item(sel[0])['values']
    did = item[0]
    new_qty = simpledialog.askinteger("Edit donation", "New quantity:", initialvalue=item[4], parent=app['root'], minvalue=0)
    if new_qty is None: return
    conn = db_conn(); cur = conn.cursor()
    if new_qty > 0:
        cur.execute("UPDATE app_donations SET quantity=%s WHERE id=%s", (new_qty, did))
    else:
        cur.execute("DELETE FROM app_donations WHERE id=%s", (did,))
    conn.commit()
    # refresh view
    admin_manage_donations()
    cur.close(); conn.close()

def admin_delete_donation(tree):
    sel = tree.selection()
    if not sel: return
    item = tree.item(sel[0])['values']
    did = item[0]

    # Check if donation has claims
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM app_claims WHERE donation_id=%s", (did,))
    claim_count = cur.fetchone()[0]

    if claim_count > 0:
        # Ask if admin wants to delete claims too
        msg = f"Donation ID {did} has {claim_count} claim(s).\nDelete donation AND all related claims?"
        if not tk.messagebox.askyesno("Confirm", msg):
            cur.close(); conn.close()
            return
        # Delete claims first
        cur.execute("DELETE FROM app_claims WHERE donation_id=%s", (did,))
    else:
        # No claims, just confirm normal delete
        if not tk.messagebox.askyesno("Confirm", f"Delete donation ID {did}?"):
            cur.close(); conn.close()
            return

    # Now safe to delete donation
    cur.execute("DELETE FROM app_donations WHERE id=%s", (did,))
    conn.commit(); cur.close(); conn.close()
    tree.delete(sel[0])

# ----- Admin: Manage Claims -----
def admin_manage_claims():
    clear_content()
    tk.Label(content_frame, text="Manage Claims", font=("Segoe UI",14,"bold"), bg=card_bg).pack(pady=6)
    frame = tk.Frame(content_frame, bg=card_bg); frame.pack(fill='both', expand=True, padx=6, pady=6)
    cols = ('ID','NGO_ID','Donation_ID','Claimed_qty','Claimed_on')
    lb = ttk.Treeview(frame, columns=cols, show='headings')
    for c in cols: lb.heading(c, text=c)
    lb.pack(side='left', fill='both', expand=True)
    sb = ttk.Scrollbar(frame, orient='vertical', command=lb.yview); sb.pack(side='right', fill='y')
    lb.configure(yscrollcommand=sb.set)
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, ngo_id, donation_id, claimed_qty, claimed_on FROM app_claims")
    for r in cur.fetchall(): lb.insert('', 'end', values=r)
    cur.close(); conn.close()
    btnf = tk.Frame(content_frame, bg=card_bg); btnf.pack(pady=6)
    tk.Button(btnf, text="Delete Selected", command=lambda: admin_delete_claim(lb)).pack(side='left', padx=6)
    tk.Button(btnf, text="Back", command=admin_portal).pack(side='left', padx=6)

def admin_delete_claim(tree):
    sel = tree.selection(); 
    if not sel: return
    item = tree.item(sel[0])['values']
    cid = item[0]
    if not tk.messagebox.askyesno("Confirm", f"Delete claim id {cid}?"): return
    conn = db_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM app_claims WHERE id=%s", (cid,))
    conn.commit(); cur.close(); conn.close()
    tree.delete(sel[0])

# ----- File operations for admin -----
def admin_export_donations():
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, donor_id, category, item, quantity, donated_on FROM app_donations")
    rows = cur.fetchall()
    cur.close(); conn.close()
    if not rows:
        tk.messagebox.showinfo("Export", "No donations to export.")
        return
    fn = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if not fn: return
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id','donor_id','category','item','quantity','donated_on'])
        writer.writerows(rows)
    tk.messagebox.showinfo("Export", f"Exported {len(rows)} donations to {os.path.basename(fn)}")

def admin_import_donations():
    fn = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
    if not fn: return
    with open(fn, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        conn = db_conn(); cur = conn.cursor()
        count = 0
        for r in reader:
            try:
                cur.execute("INSERT INTO app_donations (donor_id,category,item,quantity,donated_on) VALUES (%s,%s,%s,%s,%s)",
                            (int(r.get('donor_id') or 0), r['category'], r['item'], int(r['quantity']), r.get('donated_on') or date.today()))
                count += 1
            except Exception:
                continue
        conn.commit(); cur.close(); conn.close()
    tk.messagebox.showinfo("Import", f"Imported {count} donations from CSV.")
    generate_prices_and_stock()  # refresh in-memory stock display


def admin_backup_donations():
    conn = db_conn(); cur = conn.cursor()
    cur.execute("SELECT id, donor_id, category, item, quantity, donated_on FROM app_donations")
    rows = cur.fetchall()
    cur.close(); conn.close()
    if not rows:
        tk.messagebox.showinfo("Backup", "No donations to backup.")
        return
    fn = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files","*.pkl")])
    if not fn: return
    with open(fn, 'wb') as f:
        pickle.dump(rows, f)
    tk.messagebox.showinfo("Backup", f"Backed up {len(rows)} donations to {os.path.basename(fn)}")

def admin_restore_donations():
    fn = filedialog.askopenfilename(filetypes=[("Pickle files","*.pkl")])
    if not fn: return
    with open(fn, 'rb') as f:
        rows = pickle.load(f)
    conn = db_conn(); cur = conn.cursor()
    count = 0
    for r in rows:
        try:
            cur.execute("INSERT INTO app_donations (id,donor_id,category,item,quantity,donated_on) VALUES (%s,%s,%s,%s,%s,%s)",
                        (r[0], r[1], r[2], r[3], r[4], r[5]))
            count += 1
        except mysql.connector.IntegrityError:
            # skip if already exists
            continue
    conn.commit(); cur.close(); conn.close()
    tk.messagebox.showinfo("Restore", f"Restored {count} donations from binary backup.")
    generate_prices_and_stock()  # refresh in-memory stock display

# ------------------ START APP ------------------
def start_app():
    init_db()
    generate_prices_and_stock()

    root = tk.Tk()
    app['root'] = root
    root.title("Grocery Management & Donation")
    root.geometry("980x700")
    root.configure(bg="#eef3f7")

    global card_bg, content_frame, btn_color
    card_bg = "white"
    btn_color = "#2e86c1"

    header = tk.Frame(root, bg=btn_color, height=70)
    header.pack(fill='x')
    tk.Label(header, text="GROCERY MANAGEMENT & DONATION", bg=btn_color, fg="white",
             font=("Segoe UI", 18, "bold")).pack(pady=14)

    shadow = tk.Frame(root, bg="#cfd8e3")
    shadow.place(relx=0.5, rely=0.52, anchor='center', width=860, height=520)
    card = tk.Frame(root, bg=card_bg)
    card.place(relx=0.5, rely=0.5, anchor='center', width=820, height=500)

    global content_frame
    content_frame = tk.Frame(card, bg=card_bg)
    content_frame.pack(expand=True, fill='both', padx=18, pady=18)

    home_screen()
    root.mainloop()

if __name__ == "__main__":
    start_app()
