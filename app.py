from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Connect to the database
server = 'product2-sql.database.windows.net'
database = 'product-sql'
username = 'ee1200496'
password = 'Yes123456'
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

@app.route("/")
def index():
    # List all products
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FinalProducts")
    products = cursor.fetchall()
    return render_template("index.html", products=products)

@app.route("/add_product", methods=["POST"])
def add_product():
    try:
        # Add new product
        cursor = conn.cursor()
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        # Execute SQL query to insert data
        cursor.execute("INSERT INTO FinalProducts (ProductName, Description, Price, StockQuantity) VALUES (?, ?, ?, ?)", (name, description, price, quantity))
        
        # Commit the transaction
        conn.commit()
        
        return redirect(url_for("index", message="Product added successfully"))
    
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route("/delete_product", methods=["POST"])
def delete_product():
    try:
        # Delete product
        cursor = conn.cursor()
        name = request.form["name"]

        # Execute SQL query to delete data
        cursor.execute("DELETE FROM FinalProducts WHERE ProductName = ?", (name,))
        
        # Commit the transaction
        conn.commit()
        
        return redirect(url_for("index", message="Product deleted successfully"))
    
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route("/update_product", methods=["POST"])
def update_product():
    try:
        # Update product
        cursor = conn.cursor()
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        # Execute SQL query to update data
        cursor.execute("UPDATE FinalProducts SET Description = ?, Price = ?, StockQuantity = ? WHERE ProductName = ?", (description, price, quantity, name))
        
        # Commit the transaction
        conn.commit()
        
        return redirect(url_for("index", message="Product updated successfully"))
    
    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    app.run()
