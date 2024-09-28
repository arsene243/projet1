from flask import Flask, request, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'  # Nécessaire pour utiliser les sessions

# Exemple d'utilisateur (vous pouvez remplacer cela par une base de données)
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'password123'

# Fonction pour lire un fichier JSON
def read_json_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return json.load(file)

# Fonction pour écrire dans un fichier JSON
def write_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)  # Ajout d'indentation pour une meilleure lisibilité

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request', methods=['GET', 'POST'])
def request_vehicle():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'identity_photo': request.files['identity_photo'].filename,
            'phone': request.form['phone'],
            'brand': request.form['brand'],
            'model': request.form['model'],
            'price': request.form['price'],
            'car_photos': [request.files[f'car_photo_{i}'].filename for i in range(2)]
        }
        
        # Sauvegarder les fichiers téléchargés dans le dossier static/uploads
        os.makedirs('static/uploads', exist_ok=True)  # Crée le dossier s'il n'existe pas
        for file in request.files.values():
            file.save(os.path.join('static/uploads', file.filename))

        requests = read_json_file('requests.json')
        requests.append(data)
        write_json_file('requests.json', requests)

        # Rediriger vers la page d'accueil après soumission
        return redirect(url_for('index'))  # Changement ici

    return render_template('request.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Vérification des informations d'identification
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['logged_in'] = True  # Marquer l'utilisateur comme connecté
            return redirect(url_for('admin'))  # Rediriger vers la page admin
        else:
            return "Identifiants incorrects", 401  # Gérer l'erreur d'authentification

    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si non connecté
    requests = read_json_file('requests.json')
    return render_template('admin.html', requests=requests)

@app.route('/approve/<int:index>')
def approve_request(index):
    requests = read_json_file('requests.json')
    vehicle_data = requests.pop(index)
    
    vehicles = read_json_file('vehicles.json')
    vehicles.append(vehicle_data)
    
    write_json_file('requests.json', requests)
    write_json_file('vehicles.json', vehicles)

    return redirect(url_for('admin'))

@app.route('/vehicles')
def vehicles():
    vehicles = read_json_file('vehicles.json')
    return render_template('vehicle.html', vehicles=vehicles)

if __name__ == '__main__':
    app.run(debug=True)