import tkinter as tk
import socket
import ssl
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adit@1705",
    database="site_checker"
)
cursor = conn.cursor()

def check_website():
    url = entry_url.get()
    status = ""
    response_time = ""

    try:
      
        connection = socket.create_connection((url, 80), timeout=5)
        connection.close()
        status = "up"
    except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
        print("HTTP Error:", e)
        status = "down"

    try:
       
        context = ssl.create_default_context()
        with socket.create_connection((url, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=url) as ssock:
                status = "up"
    except Exception as e:
        print("HTTPS Error:", e)
        status = "down"

    try:
        
        import time
        start_time = time.time()
        connection = socket.create_connection((url, 80), timeout=5)
        connection.close()
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000, 2)
    except Exception as e:
        print("Response Time Error:", e)
        response_time = None

    try:
     
        sql = "INSERT INTO checked_sites (site_name, url, status, response_time) VALUES (%s, %s, %s, %s)"
        val = (url, url, status, response_time)
        cursor.execute(sql, val)
        conn.commit()

        if status == "up":
            result_label.config(text="Website is Accessible", fg='green')
        else:
            result_label.config(text="Website is Not Accessible", fg='red')
    except Exception as e:
        print("Database Error:", e)
        result_label.config(text="Failed to Store Information in Database", fg='red')

def show_checked_websites():
    try:
        
        cursor.execute("SELECT site_name, url, status, response_time FROM checked_sites")
        checked_websites = cursor.fetchall()

        websites_text.delete(1.0, tk.END)
        for website in checked_websites:
            websites_text.insert(tk.END, f"Site Name: {website[0]}\nURL: {website[1]}\nStatus: {website[2]}\nResponse Time: {website[3]} ms\n\n")

    except Exception as e:
        print("Database Error:", e)
        result_label.config(text="Failed to Retrieve Information from Database", fg='red')

root = tk.Tk()
root.geometry("800x440")
root.title("Website Connectivity Checker")
root.config(bg='#F0F0F0')

header_label = tk.Label(root, text="Website Connectivity Checker", font=('Arial bold', 18), bg='Blue', fg='white')
header_label.pack(pady=10)


check_frame = tk.Frame(root, bg='#F0F0F0')
check_frame.pack(pady=10)

url_label = tk.Label(check_frame, text="Enter Website URL:", font=('Arial', 12), bg='#F0F0F0')
url_label.grid(row=0, column=0, padx=(20, 10))

entry_url = tk.Entry(check_frame, font=('Arial', 12), justify=tk.CENTER, relief=tk.SOLID, width=30)
entry_url.grid(row=0, column=1, padx=(0, 20))

check_button = tk.Button(check_frame, text="Check", font=('Arial bold', 12), bg='black', fg='white', bd=3, padx=10, command=check_website)
check_button.grid(row=0, column=2, padx=(0, 20))

result_label = tk.Label(check_frame, text="", font=('Arial bold', 14), bg='#F0F0F0')
result_label.grid(row=1, column=0, columnspan=3)


show_frame = tk.Frame(root, bg='#F0F0F0')
show_frame.pack(pady=10)

show_button = tk.Button(show_frame, text="Show Checked Websites", font=('Arial bold', 12), bg='red', fg='white', bd=3, padx=10, command=show_checked_websites)
show_button.pack(pady=10)

websites_text = tk.Text(show_frame, font=('Arial', 12), width=80, height=10, wrap=tk.WORD)
websites_text.pack()

root.mainloop()


cursor.close()
conn.close()
