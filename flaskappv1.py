from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
import boto3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DynamoDB configuration
TABLE_NAME = "Users"
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(TABLE_NAME)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# ---------- CRUD Routes for DynamoDB Users ----------

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        life_expected = int(request.form['life_expected'])
        table.put_item(Item={
            'ID': id,
            'Name': name,
            'LifeExpected': life_expected
        })
        flash("User added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/get-user', methods=['GET', 'POST'])
def get_user():
    user = None
    if request.method == 'POST':
        id = request.form['id']
        response = table.get_item(Key={'ID': id})
        user = response.get('Item')
        if not user:
            flash("User not found.", "warning")
    return render_template('get_user.html', user=user)

@app.route('/all-users')
def all_users():
    response = table.scan()
    users = response.get("Items", [])
    return render_template('all_users.html', users=users)

@app.route('/update-user', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        id = request.form['id']
        new_life_expected = int(request.form['life_expected'])
        table.update_item(
            Key={'ID': id},
            UpdateExpression="SET LifeExpected = :val",
            ExpressionAttributeValues={':val': new_life_expected}
        )
        flash("User updated successfully!", "info")
        return redirect(url_for('home'))
    return render_template('update_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        id = request.form['id']
        table.delete_item(Key={'ID': id})
        flash("User deleted successfully!", "danger")
        return redirect(url_for('home'))
    return render_template('delete_user.html')



@app.route('/compare-life')
def compare_life():
  
    users = table.scan().get('Items', [])

    results = []

    for user in users:
        user_id = user.get('ID')
        name = user.get('Name')
        life_expected = float(user.get('LifeExpected', 0))

        sql = "SELECT COUNT(*) AS count FROM country WHERE lifeexpectancy > %s"
        count_result = execute_query(sql, [life_expected])[0]["count"]

        results.append({
            "id": user_id,
            "name": name,
            "life_expected": life_expected,
            "higher_country_count": count_result
        })

    return render_template('compare-life.html', results=results)

@app.route('/query_country', methods=['GET', 'POST'])
def query_country():
    if request.method == 'POST':
        min_lifeexpectancy = request.form.get('lifeexpectancy')
        query = "SELECT name, lifeexpectancy FROM country WHERE lifeexpectancy >= %s"
        params = [min_lifeexpectancy]
        results = execute_query(query, params)
        if not results:
            flash("No countries match your criteria", "info")
        return render_template('query_country.html', results=results)
    return render_template('query_country.html')

@app.route('/all-countries')
def all_countries():
    countries = show_country()
    return render_template('all-countries.html', results=countries)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
