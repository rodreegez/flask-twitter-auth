from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
  user = { 'nickname': 'Rodreegez' }
  return render_template('index.html', user = user)


if __name__ == '__main__':
  app.run(debug=True)
