from flask import render_template, send_from_directory
import connexion
import os

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml', strict_validation=True, validate_responses=True)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True)
