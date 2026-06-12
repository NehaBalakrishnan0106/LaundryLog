from flask import Flask,render_template,request
import sqlite3


app = Flask(__name__)

@app.route('/view')
def view():
    conn=sqlite3.connect("laundry.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM laundry")
    rows=cursor.fetchall()
    conn.close()
    return str(rows)

def init_db():
    conn=sqlite3.connect("laundry.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS
laundry(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        cloth_type TEXT,
        quantity INTEGER,
        services TEXT
        )
        """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('laundry.html')
@app.route('/submit',methods=['POST'])
def submit():
    customer=request.form['customer']
    cloth_type=request.form['cloth_type']
    quantity=request.form['quantity']
    services=request.form.getlist('service')
    conn=sqlite3.connect("laundry.db")
    cursor=conn.cursor()
    cursor.execute("""
    INSERT INTO laundry(customer_name,cloth_type,
    quantity,services)
    VALUES(?,?,?,?)
    """,(customer,cloth_type,quantity,",".join(services)))
    conn.commit()
    conn.close()
    return"Laundry Entry Stored Successfully!"

    #print("Customer:",customer)
    #print("Cloth type:",cloth_type)
    #print("Quantity:",quantity)
    #print("Services:",services)
    
    return "Form submitted successfully!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
