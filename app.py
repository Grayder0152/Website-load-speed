import requests
from flask import Flask, render_template, request, Response
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asf3f4678jf2e34Ae'

history_website_load_speed = ()


def website_load_speed(urls):
    global history_website_load_speed
    for url in urls:
        try:
            speed = requests.get(url).elapsed.total_seconds()
            yield url, speed
        except:
            speed = 'Incorrect URL'
            yield url, speed
        history_website_load_speed += ((url, str(datetime.now())[:19], speed),)


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(10)
    return rv


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        urls = []
        for name in request.form:
            urls.append(request.form[name].replace(' ', ''))
        url_speed = website_load_speed(set(urls))
        return Response(stream_template('index.html', test=True, url_speed=url_speed,
                                       history_website_load_speed=history_website_load_speed))
    return render_template('index.html', test=False, history_website_load_speed=history_website_load_speed)


if __name__ == '__main__':
    app.run(debug=True)
