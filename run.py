from app import create_app, db
from app.auth.models import User, Role

app = create_app('development')

if __name__ == "__main__":
    app.run(debug=True)
