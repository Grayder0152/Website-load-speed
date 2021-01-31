import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asf3f4678jf2e34Ae'

history_website_load_speed = ()


def speed_test(urls):
    global history_website_load_speed
    websites_load_speed = []
    for url in urls:
        try:
            speed = requests.get(url).elapsed.total_seconds()
            websites_load_speed.append(speed)
        except:
            speed = 'Incorrect URL'
            websites_load_speed.append('Incorrect URL')
        history_website_load_speed += ((url, str(datetime.now())[:19], speed),)
    return zip(urls, websites_load_speed)


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        urls = []
        for name in request.form:
            urls.append(request.form[name].replace(' ', ''))
        return render_template('index.html', test=True, speed_test=speed_test(set(urls)),
                               history_website_load_speed=history_website_load_speed)
    return render_template('index.html', test=False, history_website_load_speed=history_website_load_speed)


if __name__ == '__main__':
    app.run(debug=False)
