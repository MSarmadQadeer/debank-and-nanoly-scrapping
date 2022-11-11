from app import app
from flask import render_template, request, redirect
from flask_mail import Mail, Message
from scrapper.scrapper import getScrappedData
from eth_utils import is_hex_address


# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nadim.hafez@gmail.com'
app.config['MAIL_PASSWORD'] = 'mvpbdxtmcctiwpyf'
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Home Screen")


@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html", title="About Us")


@app.route('/insights', methods=["GET"])
def insights():
    return render_template("insights.html", title="Insights")


@app.route('/insights/bitcoin-bulls-marching-20k', methods=["GET"])
def bitcoinBullsMarching20k():
    return render_template("bitcoin-bulls-marching-20k.html", title="Bitcoin Bulls Marching 20k")


@app.route('/trust', methods=["GET"])
def trust():
    return render_template("trust.html", title="Trust")


# For Testing
# @app.route('/api/<publicAddress>')
# def testApi(publicAddress):
#     if is_hex_address(publicAddress):
#         return {
#             'result': getScrappedData(publicAddress)
#         }
#     else:
#         return {
#             'result': 'Invalid Address'
#         }


@app.route('/apiCall', methods=['GET', 'POST'])
def apiCall():
    if is_hex_address(request.args['public-address']):
        results = getScrappedData(request.args['public-address'])
        if results == 'no-assets':
            return render_template('index.html', title="Results Screen", error="No Assets Found")
        else:
            return render_template("index.html", title="Results Screen", results=results, publicAddress=request.args['public-address'])

    else:
        print("Invalid Address")
        return render_template('index.html', title="Results Screen", error="Invalid Public Address")


@app.route('/sendMail', methods=['GET', 'POST'])
def sendMail():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    publicAddress = request.form['public-address']
    contact = request.form['contact-number']
    baseUrl = request.base_url
    baseUrl = baseUrl.split('/')[:-1]
    baseUrl = '/'.join(baseUrl)
    # print("Base url: ", baseUrl)

    msg = Message(subject, sender='info@iqcapital.io',
                  recipients=['marketing@iqcapital.io'])

    msg.html = render_template("email-template.html", name=name, email=email, message=message,
                               publicAddress=publicAddress, contact=contact, baseUrl=baseUrl)  # Template should be in 'templates' folder
    mail.send(msg)
    return redirect('/')
