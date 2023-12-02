'''
Run from root directory:
flask --app lib/api run
'''
# api.py
from flask import Flask
from sensor_api import sensor_api
from path_api import path_api

app = Flask(__name__)

# Register blueprints
app.register_blueprint(sensor_api, url_prefix='/sensors')
app.register_blueprint(path_api, url_prefix='/path')


# put this sippet ahead of all your bluprints
# blueprint can also be app~~
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    # Other headers can be added here if needed
    return response


if __name__ == '__main__':
    app.run(debug=True)