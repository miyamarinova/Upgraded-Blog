from flask import Flask, render_template, request
import requests
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

response = requests.get("https://api.npoint.io/9f0456cb01ef08e9ed7f")
all_posts = response.json()

username = "mariayoana.marinova@gmail.com"
password = "sptbetfbeymsaiku"

@app.route("/")
@app.route("/index")
def home_page():
    return render_template("index.html", all_posts=all_posts)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        sender_name = data["name"]
        sender_email = data["email"]
        sender_phone = data["phone"]
        message = data["message"]
        send_email(sender_name, sender_email, sender_phone, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=username,
            msg="Subject: New Form Filled\n\n"
                f"Name: {name}\n"
                f"Phone: {phone}\n"
                f"Email: {email}\n"
                f"Message: {message}"
        )

@app.route("/<filename>")
def about_page(filename):
    return render_template(filename)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/post/<int:id>')
def blog_page(id):
    post = all_posts[id-1]
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)