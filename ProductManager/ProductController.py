from flask import Flask , render_template, request
app=Flask(__name__)

@app.route("/")
def Homepage():
    return render_template("pro_register.html")

@app.route("/pro_register/", methods=["GET", "POST"])
def pro_register_page():

    # if request.form == "POST":
    p_name = request.form["pro_name"]
    p_no = request.form["pro_no"]
    p_price = request.form["pro_price"]
    # p_expired = request.form["pro_expired"]
    # else:
    #     p_name = request.args.get("pro_name")
    #     p_no = request.args.get("pro_no")
    #     p_price = request.args.get("pro_price")
    #     p_expired = request.args.get("pro_expired")

    name = p_name
    no = p_no
    price = p_price


    # Connecting Database; driver(connector)
    # installed by: pip install mysql-connector
    import mysql.connector 
    dbconfig={'host':'localhost','user':'root','password':'','database':'product_db'}
    conn=mysql.connector.connect(**dbconfig)
    cursor=conn.cursor(prepared=True) 
    SQL= ("INSERT INTO product_info (p_no, p_name, p_price) VALUES (%s, %s, %s)") # %s doesn't represent string / everything is covered by"%s"
    data_user = (no, name, price)
    cursor.execute(SQL, data_user, )
    # SQL="INSERT INTO product_info (p_no, p_name, p_price) VALUES (p_no, p_name, p_price);"
    # cursor.execute(SQL) 
    # SQL="INSERT INTO product_info (p_no, p_name, p_price) VALUES (p_no, p_name, p_price);"
    # cursor.execute(SQL) 

    conn.commit()
    conn.close()

    return render_template("pro_register_display.html", pname=p_name, pno=p_no, pprice=p_price)

@app.route("/product_delete/", methods=["GET", "POST"])
def pro_del():

    p_num = request.form["productNum"]

    import mysql.connector
    dbconfig={'host':'localhost','user':'root','password':'','database':'product_db'}
    conn=mysql.connector.connect(**dbconfig) 
    cursor=conn.cursor(prepared=True)

    SQL_check = ("SELECT p_no FROM product_info WHERE p_no = %s")
    cursor.execute(SQL_check, (p_num, ))
    check = cursor.fetchall()

    if (check):
        SQL2 = ("DELETE FROM  product_info WHERE p_no = %s")
        cursor.execute(SQL2, (p_num, ))
        conn.commit()
    else:
        return render_template("pro_register.html")
        

    SQL_select = ("SELECT * FROM product_info")
    cursor.execute(SQL_select)
    myresult = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("pro_del_result.html", pNum = p_num, result=myresult)

app.run(debug=True)