from flask import Flask 
from flask import render_template
from flask import request
from flask_mysqldb import MySQL
import MySQLdb




app = Flask(__name__)

app.secret_key="akash"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_PORT"]=3307
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="project2"
con=MySQL(app)

@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/login',methods=["get","post"])
def login():
    if request.method=='POST':
        username=request.form["username"]
        password=request.form["password"]
        cur=con.connection.cursor()
        cur.execute("select * from admin where username=%s and password=%s",(username,password))
        data=cur.fetchall()
        cur.close()
        if len(data)>0:
            return render_template("hrhome.html")
        else:
            msg="invalid username or password"
            return render_template("adminlogin.html",msg=msg)
    else:
        return render_template("adminlogin.html")

@app.route('/contact.html')
def contact():
    return render_template('contactus.html')
  
@app.route('/add_employee',methods=["GET", "POST"])
def add_employee():
    if request.method=="POST":
        employee_id=request.form["employee_id"]
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        address=request.form["address"]
        department=request.form["department"]
        salary=request.form["salary"]
        save="add successfully"
        ##data base conection
        
        cur = con.connection.cursor()
        #insert data in table
        try:
             cur.execute("insert into addemployee(employee_id,name,email,phone,address,department,salary) values(%s,%s,%s,%s,%s,%s,%s)",(employee_id,name,email,phone,address,department,salary))
             #data save in table
             con.connection.commit()
             #close connection
             cur.close()
        except MySQLdb.IntegrityError as e:
            # Duplicate error handling
            if "email" in str(e):
                save = "❌ Email already exists!"
            elif "phone" in str(e):
                save = "❌ Phone number already exists!"
            else:
                save = "❌ Duplicate entry error!"

        finally:
            cur.close()
    else:
        save="add employee"    

    return render_template('addemploy.html',save=save)    
@app.route('/show_employee')

def show_employee():
    cur=con.connection.cursor()
    cur.execute("select * from addemployee")
    data=cur.fetchall()
    cur.close()
    return render_template('sgowemply.html',data=data)    
@app.route('/searchemployee',methods=["get","post"])
def search_employee():
    if request.method=="POST":
        name=request.form["txtname"]
        cur=con.connection.cursor()
        cur.execute("select * from addemployee where name like %s",("%"+name+"%",))
        data=cur.fetchall()
        cur.close()
        return render_template('searchemployee.html',data=data)
    else:
        return render_template('searchemployee.html')
            




    return render_template('searchemply.html')    
@app.route('/logout')
def logout():
    return render_template('logout.html') 
@app.route('/view_employee')
def view_employee():
    id=request.args.get("id")
    cur=con.connection.cursor()
    cur.execute("select * from addemployee where employee_id=%s",(id,))
    data=cur.fetchall()
    cur.close()
    return render_template('view_employee.html',data=data)    
@app.route('/update_employee',methods=["get","post"])
def update_employee():
    if request.method=="POST":
        employee_id=request.form["employee_id"]
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        address=request.form["address"]
        department=request.form["department"]
        salary=request.form["salary"]
        save="update successfully"
        ##data base conection
        
        cur = con.connection.cursor()
        #insert data in table
        cur.execute("update addemployee set name=%s,email=%s,phone=%s,address=%s,department=%s,salary=%s where employee_id=%s",(name,email,phone,address,department,salary,employee_id))
        #data save in table
        con.connection.commit()
        #close connection
        cur.close()
        message="update successfully"
        return render_template('update_employee.html',m=message)   
    else:
        id=request.args.get("id")
        cur=con.connection.cursor()
        cur.execute("delete from addemployee where employee_id=%s",(id,))
        con.connection.commit()
        
        cur.close()
        message="delet successfully"
        return render_template('update_employee.html',m=message)     
   
        
if __name__ == '__main__':
    app.run(debug=True)
r