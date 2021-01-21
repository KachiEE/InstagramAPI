import flask

from scraper import InstaSpider


app = flask.Flask(__name__)

@app.route('/')
def home():
    
    return

@app.route('/insta/<string:username>')
def get_instagram_user_info(username):
    spider = InstaSpider(username=['jayconsults', 'cristiano'])
    data = spider.run()
    return {'response': data}
    

if __name__ == '__main__':
    app.run()
