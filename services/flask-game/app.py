from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'flask-game'
app.config['SECRET_KEY'] = '1234'  # Change this to a secure secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    resources = db.Column(db.Integer, default=1000)
    buildings = db.relationship('Building', backref='player', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'resources': self.resources,
            'buildings': [building.serialize() for building in self.buildings]
        }

# Define the Building model
class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level
        }

# Route to get player data
@app.route('/api/player/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    return jsonify(player.serialize())

# Route to upgrade a building for a player
@app.route('/api/player/<int:player_id>/upgrade-building', methods=['POST'])
def upgrade_building(player_id):
    player = Player.query.get_or_404(player_id)

    # Get building information from the request
    building_id = request.json.get('building_id')
    building = Building.query.get_or_404(building_id)

    # Check if the player owns the building
    if building.player_id != player.id:
        return jsonify({'error': 'Player does not own this building.'}), 403

    # Check if the player has enough resources to upgrade the building
    upgrade_cost = 100  # Adjust this based on your game balance
    if player.resources < upgrade_cost:
        return jsonify({'error': 'Not enough resources to upgrade the building.'}), 400

    # Update player resources and building level
    player.resources -= upgrade_cost
    building.level += 1

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Building upgraded successfully.'})

# Define the User model for Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Initialize Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Validate email and password, and handle other necessary checks
        # For simplicity, you can perform basic validation here.
        if not email or not password:
            return render_template('signup.html', error='Please provide both email and password')

        # Check if the email is not already taken
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', error='Email already in use')

        # Create a new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
