from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from scrapper import getScrappedData

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'crypto.breakint.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@crypto.breakint.com'
app.config['MAIL_PASSWORD'] = '6un-wGVMiSZ5'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", title="Home Screen")


@app.route('/blogs', methods=["GET"])
def blogs():
    return render_template("blogs.html", title="Blogs")


@app.route('/blogs/cryptocurrency-investing-beginners-guide', methods=["GET"])
def cryptocurrencyInvestingBeginnersGuide():
    return render_template("cryptocurrency-investing-beginners-guide.html", title="Cryptocurrency Investing")


# @app.route('/api/<publicAddress>')
# def apiCall(publicAddress):
#     results = getScrappedData(publicAddress)
#     return render_template("index.html", title="Results Screen", results=results)


@app.route('/apiCall', methods=['GET', 'POST'])
def apiCall():
    results = getScrappedData(request.args['public-address'])
    return render_template("index.html", title="Results Screen", results=results, publicAddress=request.args['public-address'])


@app.route('/sendMail', methods=['GET', 'POST'])
def sendMail():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    publicAddress = request.form['public-address']
    contact = request.form['contact-number']

    msg = Message(subject, sender='info@crypto.breakint.com',
                  recipients=['msarmadqadeer@gmail.com'])
    
    msg.html = render_template("email-template.html", name=name, email=email, message=message, publicAddress=publicAddress, contact=contact) # Template should be in 'templates' folder
    mail.send(msg)
    return redirect('/')


if __name__ == "__main__":
    print("Starting server...")
    app.run(debug=True)
