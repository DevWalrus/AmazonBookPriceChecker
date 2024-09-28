from flask import Flask, render_template, request, flash, redirect
from zeep import Client

app = Flask(__name__)
app.secret_key = b'\x17\xea\xf5\xf5\xc2\xf1E\x1c\t\x9dC\xdb\x81WH\x00\xde\xc0xDg\xa7\x18W'

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/lookup", methods=['POST', 'GET'])
def lookup():
	isbn = request.form['isbn_input']
	# SOAP Request
	client = Client('http://webservices.daehosting.com/services/ISBNService.wso?WSDL')
	is_valid_isbn13 = client.service.IsValidISBN13(isbn)
	is_valid_isbn10 = client.service.IsValidISBN10(isbn)
	if not (is_valid_isbn13 or is_valid_isbn10):
		flash(f"I'm sorry, \"{isbn}\" is not a valid ISBN number", category='error')
		return redirect("/")
