import requests
from flask import Flask, render_template, request, flash, redirect
from zeep import Client
import re

GRAPH_QL_URL = "https://graphql.canopyapi.co/"
SOAP_URL = "http://webservices.daehosting.com/services/ISBNService.wso?WSDL"
GRAPH_QL_QUERY = '''{
	amazonProductSearchResults(input: { searchTerm: "$0" }) {
		productResults {
            results {
                title
                mainImageUrl
                price {
                    display
                }
            }
        }
	}	
}
'''
REST_URL= "https://www.googleapis.com/books/v1/volumes?q=isbn:$0"

GRAPH_QL_HEADERS = {
    'Authorization': 'Bearer 5d4cb91a-c93d-4d78-85c2-924f48bd2277',
}


app = Flask(__name__)
app.secret_key = b'\x17\xea\xf5\xf5\xc2\xf1E\x1c\t\x9dC\xdb\x81WH\x00\xde\xc0xDg\xa7\x18W'

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/lookup", methods=['POST', 'GET'])
def lookup():
	isbn = request.form['isbn_input']

	# SOAP Request
	client = Client(SOAP_URL)
	is_valid_isbn13 = client.service.IsValidISBN13(isbn)
	is_valid_isbn10 = client.service.IsValidISBN10(isbn)
	if not (is_valid_isbn13 or is_valid_isbn10):
		flash(f"I'm sorry, \"{isbn}\" is not a valid ISBN number", category='error')
		return redirect("/")

	#GraphQL Request
	result = {'query': GRAPH_QL_QUERY.replace('$0', isbn)}
	r = requests.post(
		GRAPH_QL_URL,
		json=result,
		headers=GRAPH_QL_HEADERS
	)

	if r.status_code == 200:
		# Convert the response to JSON
		output = r.json()
		if len(output['data']['amazonProductSearchResults']['productResults']['results']) < 1:
			flash(
				f"I'm sorry, we could not find \"{isbn}\" in the Amazon database.",
				category='error')
			return redirect("/")

		# REST Request

		google_books_r = requests.get(
			REST_URL.replace('$0', re.sub("[^0-9]", "", isbn)),
		).json()

		is_available_on_gbooks = google_books_r['totalItems'] > 0 and \
								 google_books_r['items'][0]['accessInfo']['viewability'] == 'ALL_PAGES'

		return render_template("lookup.html", data={
			'title': output['data']['amazonProductSearchResults']['productResults']['results'][0]['title'],
			'img_link': output['data']['amazonProductSearchResults']['productResults']['results'][0]['mainImageUrl'],
			'cost': output['data']['amazonProductSearchResults']['productResults']['results'][0]['price']['display'],
			'g_book_option': is_available_on_gbooks
		})
	else:
		flash(
			f"I'm sorry, something went wrong looking up \"{isbn}\" in the Amazon database. Please try again later.",
			category='error')
		return redirect("/")

