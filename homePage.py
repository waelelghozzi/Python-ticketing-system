from datetime import timedelta
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'waelKey'  # Required for session management and flashing messages
app.permanent_session_lifetime = timedelta(minutes=1)

# Sample data to simulate tickets coming from a database or API
tickets = [
    {
        'id': 1,
        'ticket_type': 'Bug',
        'title': 'Issue found in sales API needs to be fixed',
        'priority': 'P1',
        'description': 'Detailed description about the sales API issue.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 2,
        'ticket_type': 'Feature',
        'title': 'Add new reporting feature',
        'priority': 'P2',
        'description': 'Description about the new reporting feature to be implemented.',
        'link': '#',
        'status': 'Closed',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 3,
        'ticket_type': 'Bug',
        'title': 'Fix login page error',
        'priority': 'P1',
        'description': 'Detailed description about the login page issue.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 4,
        'ticket_type': 'Bug',
        'title': 'Fix another login page error',
        'priority': 'P3',
        'description': 'Detailed description about another login page issue.',
        'link': '#',
        'status': 'Closed',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 5,
        'ticket_type': 'Improvement',
        'title': 'Enhance user profile page',
        'priority': 'P2',
        'description': 'Improve the layout and add additional fields to the user profile page.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 6,
        'ticket_type': 'Feature',
        'title': 'Implement dark mode in the application',
        'priority': 'P1',
        'description': 'Add a toggle to switch between light and dark modes for better accessibility.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 7,
        'ticket_type': 'Bug',
        'title': 'Crash on mobile when submitting a form',
        'priority': 'P1',
        'description': 'Application crashes on mobile devices when the user submits a form.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 8,
        'ticket_type': 'Feature',
        'title': 'Add multi-language support',
        'priority': 'P2',
        'description': 'Implement support for multiple languages in the application.',
        'link': '#',
        'status': 'Closed',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 9,
        'ticket_type': 'Improvement',
        'title': 'Optimize loading speed of the dashboard',
        'priority': 'P3',
        'description': 'Reduce loading times for the dashboard by optimizing queries and resources.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 10,
        'ticket_type': 'Bug',
        'title': 'Error 404 on help documentation link',
        'priority': 'P3',
        'description': 'Fix the broken link in the help documentation leading to a 404 error.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 11,
        'ticket_type': 'Bug',
        'title': 'Fix email notification system',
        'priority': 'P2',
        'description': 'Email notifications are not being sent for new tickets.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 12,
        'ticket_type': 'Feature',
        'title': 'Create a user onboarding tutorial',
        'priority': 'P1',
        'description': 'Develop a tutorial to guide new users through the application features.',
        'link': '#',
        'status': 'Closed',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 13,
        'ticket_type': 'Improvement',
        'title': 'Revamp the main navigation menu',
        'priority': 'P2',
        'description': 'Make the navigation menu more user-friendly and visually appealing.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    },
    {
        'id': 14,
        'ticket_type': 'Bug',
        'title': 'Database connection timeout issue',
        'priority': 'P1',
        'description': 'Frequent timeout errors when connecting to the database.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'ayoub ksouri'
    },
    {
        'id': 15,
        'ticket_type': 'Feature',
        'title': 'Integrate payment processing',
        'priority': 'P2',
        'description': 'Implement payment processing for in-app purchases.',
        'link': '#',
        'status': 'Open',
        'AssignedTo': 'wael el ghozzi'
    }
]

USER_CREDENTIALS = {
    'wael el ghozzi': 'wael',
    'ayoub ksouri': 'ayoub'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')

        # Check if the credentials are valid
        if checkCredentials(user, password):
            session.permanent = True
            session['user'] = user
            return redirect(url_for("home"))
        else:
            flash('Password or username is not correct', category='error')
    return render_template('LoginPage.html')

def checkCredentials(user, password):
    return USER_CREDENTIALS.get(user) == password

@app.route('/home')
def home():
    if 'user' not in session:
        flash('You need to login first.', category='warning')
        return redirect(url_for('login'))

    user = session['user']
    return render_template('HomePage.html', tickets=tickets, user=user)

@app.route('/ticket/<int:ticket_id>')
def ticket_details(ticket_id):
    if 'user' not in session:
        flash('You need to login first.', category='warning')
        return redirect(url_for('login'))

    user = session['user']
    ticket = next((ticket for ticket in tickets if ticket['id'] == ticket_id), None)
    if ticket:
        return render_template('ticket_details.html', ticket=ticket, user=user)
    else:
        return "<h1>Ticket not found</h1>", 404


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', category='info')
    return redirect(url_for('login'))

from flask import request, jsonify

@app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    # Retrieve the ticket from the form data
    title = request.form.get('title')
    description = request.form.get('description')
    status = request.form.get('status')

    # Find the ticket by ticket_id
    ticket = next((ticket for ticket in tickets if ticket['id'] == ticket_id), None)

    if ticket:
        # Update the ticket details
        ticket['title'] = title
        ticket['description'] = description
        if status != None:
            ticket['status'] = status

    return redirect(url_for('ticket_details', ticket_id=ticket_id))

@app.route('/get_joke')
def get_joke():
    joke_api_url = 'https://official-joke-api.appspot.com/jokes/general/random'
    try:
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            joke = response.json()[0]  # Extract the first joke from the response list
            return jsonify(joke)
        else:
            return jsonify({'error': 'Could not fetch joke'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
