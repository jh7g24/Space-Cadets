from flask import Flask, request, redirect, url_for, render_template_string
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

messages = []




@app.route("/")
def main():
    messages_jinja_html = '{% extends "base.html" %} {% block messages %}'
    messages_jinja_html += format_messages_to_html()
    messages_jinja_html += "{% endblock %}"
    return render_template_string(messages_jinja_html)

def format_messages_to_html():
    messages_html = ""
    for message in messages:
        messages_html += message + "\n"
    return messages_html


@app.route("/", methods=["POST"])
def add_message():
    global messages
    message = request.form["message"]
    name = request.form['name']
    if len(re.findall("</script>", message)) == 0:
        message = f"""<div class="message">
                     <div class="message-name">
                     <p class="name-text">{name}</p>
                     </div>
                     <div class="message-content">
                     <p>{str(BeautifulSoup(message, "html.parser"))}</p>
                     </div>
                     </div>"""
        messages.append(message)
    return redirect(url_for("main"))

@app.route("/fetch_messages")
def return_messages_html():
    return format_messages_to_html()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
