# this is the script to run our application
from simulating_twitter import create_app

app = create_app()

if __name__ == '__main__':
    app.run()