# this is the script to run our application
from flask_chirper import create_app

app = create_app()

if __name__ == '__main__':
    app.run()