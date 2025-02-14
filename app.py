import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = "3B5F1C6A4E8F1A2B7C8D9E0F123456789ABCDEF0123456789ABCDEF01234567"

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'  # You can set this to any path you prefer

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

# User model for the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relationship with ExcelFile model (one-to-many)
    files = db.relationship('ExcelFile', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Define the model for the uploaded Excel file
class ExcelFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key, must not be null

    def __repr__(self):
        return f"<ExcelFile {self.filename}>"

# Create the database tables
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Redirect root route to the login page
@app.route('/')
def root():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):  # Password is hashed
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials.", "danger")
            return render_template('login.html', error="Invalid credentials.")
    
    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')
        
        # Check if username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.", "danger")
            return render_template('register.html')
        
        # Hash the password and save the new user to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/index')
@login_required
def index():
    # Get the last uploaded Excel file for the logged-in user
    uploaded_file = ExcelFile.query.filter_by(user_id=current_user.id).order_by(ExcelFile.id.desc()).first()
    
    table_data = []
    columns = []

    if uploaded_file and uploaded_file.filepath:
        try:
            # Load the Excel file safely
            df_dict = pd.read_excel(uploaded_file.filepath, None)  # Load all sheets
            if not df_dict:
                flash("The uploaded Excel file is empty or invalid.", "warning")
                return render_template('index.html', table={"columns": columns, "values": table_data})

            first_sheet_name = list(df_dict.keys())[0]  # Get first sheet name
            df = df_dict[first_sheet_name]

            # Ensure df is not empty
            if df.empty:
                flash("The first sheet in the Excel file is empty.", "warning")
                return render_template('index.html', table={"columns": columns, "values": table_data})

            # Clean and prepare the data
            for i, row in df.iterrows():
                if row.notna().sum() > 3:
                    df.columns = df.iloc[i].values  # Set this row as header
                    df = df.iloc[i+1:].reset_index(drop=True)  # Keep only actual table rows
                    break

            if df.empty:
                flash("No valid data found in the Excel file.", "warning")
                return render_template('index.html', table={"columns": columns, "values": table_data})

            df.dropna(axis=1, how='all', inplace=True)  # Drop empty columns
            df.fillna("", inplace=True)  # Fill NaN values

            table_data = df.values.tolist()
            columns = df.columns.tolist()

        except Exception as e:
            flash(f"Error reading the Excel file: {str(e)}", "danger")
            return render_template('index.html', table={"columns": columns, "values": table_data})

    return render_template('index.html', table={"columns": columns, "values": table_data})

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET'])
def search():
    global uploaded_data
    query = request.args.get('query', '').lower()
    
    if uploaded_data is not None:
        # Filter the dataframe based on the query
        filtered_data = uploaded_data[uploaded_data.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]
        
        # Prepare filtered table data
        table_data = filtered_data.values.tolist()
        columns = filtered_data.columns.tolist()
        
        return render_template('search_result.html', query=query, table={"columns": columns, "rows": table_data})
    else:
        return render_template('search_result.html', query=query, table={"columns": [], "rows": []})

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    global uploaded_data
    
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):

        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Load the Excel file
        df = pd.read_excel(filepath, None)  # Load all sheets
        first_sheet_name = list(df.keys())[0]  # Assume first sheet is relevant
        df = df[first_sheet_name]
        
        # Identify the row containing actual headers
        for i, row in df.iterrows():
            if row.notna().sum() > 3:  # Checking for at least 3 non-empty values
                df.columns = df.iloc[i].values  # Set this row as header
                df = df.iloc[i+1:].reset_index(drop=True)  # Keep only actual table rows
                break
        
        # Drop completely empty columns
        df.dropna(axis=1, how='all', inplace=True)
        
        # Fill NaN values with empty strings for display
        df.fillna("", inplace=True)
        
        # Store the dataframe in the global variable
        uploaded_data = df
        
        # Prepare cleaned-up table data
        table_data = df.values.tolist()
        columns = df.columns.tolist()

        # Save the Excel file info in the database
        new_file = ExcelFile(filename=filename, filepath=filepath, user_id=current_user.id)
        try:
            db.session.add(new_file)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        # Fetch the latest uploaded file info to display on the page
        uploaded_file = ExcelFile.query.order_by(ExcelFile.id.desc()).first()

        return render_template('index.html', 
                               table={"columns": columns, "values": table_data}, 
                               uploaded_file=uploaded_file)
    
    else:
        return 'Invalid file type. Please upload an Excel file.'

if __name__ == '__main__':
    app.run(debug=True)
