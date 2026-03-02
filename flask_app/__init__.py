from flask import Flask

app = Flask(__name__)
app.secret_key = 'its a secret to everybody'
DATABASE = "dahmes_bom_db"
HISTORY = 3600 
