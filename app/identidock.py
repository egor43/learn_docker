from flask import Flask, Response, request
import requests
import hashlib
import redis
import html

app = Flask(__name__)
salt = "UNIQUE_SALT"
default_name = "Egor Bloggs"
cache = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = default_name
    if request.method == 'POST':
        name = html.escape(request.form['name'], quote=True)
    
    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = '<head><title>Identidock</title></head>'
    body = f'''<body>
                <form method="POST">
                    Hello 
                    <input type="text" name="name" value="{name}">
                    <input type="submit" value="submit">
                </form>
                <p>You look like a:
                <img src="/monster/{name_hash}">
              </body>'''
    return f'<html>\n{header}\n{body}\n</html>'

@app.route('/monster/<name>')
def get_identicons(name):
    name = html.escape(name, quote=True)
    image = cache.get(name)
    if not image:
        resp = requests.get(f'http://dnmonster:8080/monster/{name}?size=80')
        image = resp.content
        cache.set(name, image)
    return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
