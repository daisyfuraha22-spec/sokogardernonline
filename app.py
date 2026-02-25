# import flask and ist components
# from flask import everything
from flask import *
import os

# import the pymysql modle - it helps us to create connection between python flask and mysqldatabse
import pymysql

# create an application and give it a name
app = Flask(__name__)

# configure the location to where your product images will be saved
app.config["UPLOAD_FOLDER"] = "static/images"

# below is the sign up route
@app.route("/api/signup",methods = ["POST"])
def signup():
    if request.method =="POST":
        # EXTRACT THE DIFF DETAILS ENTERED ON THE FORM

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        # by use of the print function lets print all those details sent on the upcoming with the upcoming request
        # print(username,email,password,phone)
        # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root",password = "", database = "sokogardenonline")
        # create a cursor to execute the sql queries
        cursor = connection.cursor()
        # structure an sql to insert the details received from the form
        sql = "INSERT INTO USERS (username,email,phone,password) VALUES(%s,%s,%s,%s)"
        # create a tuple that will hold all the data gotten from the form
        data = (username,email,phone,password)

        # by use of the cursor execute the sql as you replca the folders with the actual values
        cursor.execute(sql,data)
        # commit the changes to the database
        connection.commit() 


        return jsonify({"message":"user registered successfully."})
# below is the login/signin route
@app.route("/api/signin",methods=["POST"])
def signin():
    if request.method=="POST":

        # extract
        email = request.form["email"]
        password = request.form["password"]
        # print
        # print(email,password)
        # create aND ESTABLISH
        connection = pymysql.connect(host="localhost", user="root",password = "", database = "sokogardenonline")

        # create a curssor
        cursor =connection.cursor(pymysql.cursors.DictCursor)
        #  structure the sql query that will check whether the email or the passsword enterd are correct
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        # put the data
        data = (email,password)
        # by use of the cursor execute the sql
        cursor.execute(sql,data)
        # check whether they are rules returned and store the same on a variable
        count = cursor.rowcount

        # if ther are rows returned it means the password and the email are correct otherwise it means they are wrong
        if count==0:
            return jsonify({"message":"login fail"})
        else:
            # they must be a user so we create that will hold the detils of the userfetched from the database
            user = cursor.fetchone()
            # return the details to the contentas well as a message
            return jsonify({"message":" login successful","user":user})



            # below is theroute of adding products

@app.route("/api/app_product", methods =["POST"])  
def Addproducts():
    if request.method == "POST":
        # extract the data entred on the form
        product_name = request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from the files as shown below

        product_photo = request.files["product_photo"]

        # extract the file name of the product photo
        filename = product_photo.filename
        # print 
        # by use of the os module(operating system)we can extract the file path where the image is currently saved
        photo_path =os.path.join(app.config["UPLOAD_FOLDER"],filename)
        # print("this is the phot  path:",photo_path)
        # save the product photo image into the new location
        product_photo.save(photo_path)




        # print them out to test whether you are receiving the deatails sent withthe request
        # print(product_name,product_description,product_cost,product_photo)
        # establish a connection 
        connection = pymysql.connect(host="localhost", user="root",password="", database="sokogardenonline")
        # create a cursor
        cursor =connection.cursor()
        # structture the sql
        sql = "INSERT INTO product_details(product_name,product_description,product_cost,product_photo) VALUES(%s,%s,%s,%s)"
        # create a topple that will hold the data from which the which are current held onto the diffrent variable
        data = (product_name,product_description,product_cost,filename)
        # use the cursor to execute the sql and replace the placeholders with the actual data
        cursor.execute(sql,data)
        # commit the changes to the database
        connection.commit()




        




        return jsonify({"message":"product addeed successfully"})
# below is the route for fetching products    
@app.route("/api/get_products")
def get_products():
    # create a connection
     connection=pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")
    #  connect to cursor
     cursor =connection.cursor(pymysql.cursors.DictCursor)
    #  structure the query
     sql = "SELECT * FROM product_details"
    #  execute the query
     cursor.execute(sql)

    #  create a variable

     products = cursor.fetchall()

     return jsonify(products)




# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})








        
        

    
    




# run the apllication
app.run(debug = True)
