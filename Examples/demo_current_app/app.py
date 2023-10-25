# https://gist.github.com/rtzll/8f0f7668c4ca9813e9380b45b932e7c2

from flask import Flask

from blueprint import sample

app = Flask(__name__)
app.register_blueprint(sample)
app.config['SOMETHING'] = 'something'

if __name__ == '__main__':
    app.run()