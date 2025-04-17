# CS178 - Project 1:

## Overview of Project 1
You will build a self-contained web application using Flask that connects to both a relational (SQL via AWS RDS) and a non-relational (NoSQL via AWS DynamoDB) database. [More found here](https://docs.google.com/document/d/1KcldyOEqKJrbJXvPy1aujHrb5jhhmeaMDVR5r-9wXqk/edit?tab=t.0)



## Features

- View the first 5 countries from the database
- Query countries based on life expectancy, showing matching countries and their languages
- Add, update, get, and delete users stored in DynamoDB
- Compare each user’s expected life to the number of countries exceeding that value

## File Structure

- `flaskapp.py`: Main Flask routes for the web app
- `dbCode.py`: Handles SQL connection and query execution
- `templates/`: All HTML files used for rendering pages
  - `home.html`: Main navigation page
  - `query_country.html`: Form and results for country queries
  - `add_user.html`, `get_user.html`, `all_users.html`, `update_user.html`, `delete_user.html`: CRUD pages for users
  - `compare-life.html`: Shows comparison between user life expectancy and country data
  - `all-countries.html`: Displays the first 5 countries
- `README.md`: Project overview and structure

---