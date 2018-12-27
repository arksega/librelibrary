from flask import render_template
import connexion

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml', strict_validation=True, validate_responses=True)


@app.route('/')
def home():
    '''
    :return:    the rendered template 'home.html'
    '''
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
