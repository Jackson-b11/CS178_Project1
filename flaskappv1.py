# Import necessary modules from Flask and other libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *              # Custom database functions (e.g., execute_query, show_country)
import boto3                      # AWS SDK to connect to DynamoDB

# Create Flask app instance
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages to the user

# --------- DynamoDB Configuration ---------
TABLE_NAME = "Users"  # Name of the DynamoDB table
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")  # Connect to DynamoDB in us-east-1
table = dynamodb.Table(TABLE_NAME)  # Get a reference to the "Users" table

# --------- Routes ---------

# Home route - shows main menu
@app.route('/')
def home():
    return render_template('home.html')

# --------- CRUD: Add User to DynamoDB ---------
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get form values
        id = request.form['id']
        name = request.form['name']
        life_expected = int(request.form['life_expected'])

        # Add a new item to DynamoDB
        table.put_item(Item={
            'ID': id,
            'Name': name,
            'LifeExpected': life_expected
        })

        flash("User added successfully!", "success")  # Flash success message
        return redirect(url_for('home'))              # Redirect to homepage
    return render_template('add_user.html')           # Show form

# --------- CRUD: Retrieve a Single User ---------
@app.route('/get-user', methods=['GET', 'POST'])
def get_user():
    user = None
    if request.method == 'POST':
        id = request.form['id']
        response = table.get_item(Key={'ID': id})     # Get user by primary key (ID)
        user = response.get('Item')                   # Extract user object
        if not user:
            flash("User not found.", "warning")       # Flash warning if no user found
    return render_template('get_user.html', user=user)

# --------- CRUD: Retrieve All Users ---------
@app.route('/all-users')
def all_users():
    response = table.scan()                           # Scan all users from table
    users = response.get("Items", [])                 # Extract items or empty list
    return render_template('all_users.html', users=users)

# --------- CRUD: Update LifeExpected Field ---------
@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        id = request.form['id']
        new_life_expected = int(request.form['life_expected'])

        # Update LifeExpected attribute for the user with specified ID
        table.update_item(
            Key={'ID': id},
            UpdateExpression="SET LifeExpected = :val",
            ExpressionAttributeValues={':val': new_life_expected}
        )
        flash("User updated successfully!", "info")
        return redirect(url_for('home'))
    return render_template('update_user.html')

# --------- CRUD: Delete User by ID ---------
@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        id = request.form['id']
        table.delete_item(Key={'ID': id})             # Delete user by primary key
        flash("User deleted successfully!", "danger")
        return redirect(url_for('home'))
    return render_template('delete_user.html')

# --------- Analytics: Compare User LifeExpected to Countries ---------
@app.route('/compare-life')
def compare_life():
    users = table.scan().get('Items', [])             # Get all users from DynamoDB
    results = []

    for user in users:
        user_id = user.get('ID')
        name = user.get('Name')
        life_expected = float(user.get('LifeExpected', 0))

        # Query SQL database to count how many countries have lifeexpectancy greater than user's
        sql = "SELECT COUNT(*) AS count FROM country WHERE lifeexpectancy > %s"
        count_result = execute_query(sql, [life_expected])[0]["count"]

        results.append({
            "id": user_id,
            "name": name,
            "life_expected": life_expected,
            "higher_country_count": count_result
        })

    return render_template('compare-life.html', results=results)

# --------- Query Country by Minimum Life Expectancy (Join with Language) ---------
@app.route('/query_country', methods=['GET', 'POST'])
def query_country():
    if request.method == 'POST':
        min_lifeexpectancy = request.form.get('lifeexpectancy')

        # Join country and countrylanguage tables, filter by lifeexpectancy
        query = """
            SELECT country.name AS name,
                   country.lifeexpectancy AS lifeexpectancy,
                   countrylanguage.language AS language
            FROM country
            JOIN countrylanguage ON country.code = countrylanguage.countrycode
            WHERE country.lifeexpectancy >= %s
        """
        params = [min_lifeexpectancy]
        results = execute_query(query, params)

        if not results:
            flash("No countries match your criteria", "info")

        return render_template('query_country.html', results=results)

    return render_template('query_country.html')

# --------- View First 5 Countries from SQL DB ---------
@app.route('/all-countries')
def all_countries():
    countries = show_country()                        # Get first 5 countries from dbCode helper
    return render_template('all-countries.html', results=countries)

# --------- Run the App ---------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)    # Run on all IPs for cloud deployment

