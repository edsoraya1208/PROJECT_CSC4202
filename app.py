from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # HTML content for the form page
    form_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trip Planner</title>
    </head>
    <body>
        <h1>Trip Planner</h1>
        <form action="/plan_trip" method="post">
            Budget ($): <input type="text" name="budget"><br>
            Time Limit (hours): <input type="text" name="time_limit"><br>
            Distance Limit (km): <input type="text" name="distance_limit"><br>
            Minimum Rating: <input type="text" name="min_rating"><br>
            <input type="submit" value="Plan Trip">
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    budget = request.form['budget']
    time_limit = request.form['time_limit']
    distance_limit = request.form['distance_limit']
    min_rating = request.form['min_rating']

    # HTML content for the result page
    result_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trip Planner Results</title>
    </head>
    <body>
        <h1>Trip Planner Results</h1>
        <p>Budget: {budget}</p>
        <p>Time Limit: {time_limit}</p>
        <p>Distance Limit: {distance_limit}</p>
        <p>Minimum Rating: {min_rating}</p>
    </body>
    </html>
    """
    return render_template_string(result_html)

if __name__ == '__main__':
    app.run(debug=True)
