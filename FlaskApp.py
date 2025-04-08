from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/all-countries')
def all_countries():
    countries = show_country()
    return render_template('all-countries.html',results=countries)



# AI generated
@app.route('/query_country', methods=['GET', 'POST'])
def query_country():
    if request.method == 'POST':
        # Extract the life expectancy value from the form
        min_lifeexpectancy = request.form.get('lifeexpectancy')
        
        # Build the query to select countries with lifeexpectancy >= the provided value.
        query = "SELECT name, lifeexpectancy FROM country WHERE lifeexpectancy >= %s"
        params = [min_lifeexpectancy]
        
        # Execute the query using your helper function
        results = execute_query(query, params)
        
        # If no results, optionally flash a message
        if not results:
            flash("No countries match your criteria", "info")
            
        # Render the template and pass the results
        return render_template('query_country.html', results=results)
    else:
        # Render the form on GET request
        return render_template('query_country.html')



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)