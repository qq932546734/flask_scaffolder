from flask.session import SessionInterface
from flask import session, Flask
from flask_cors import CORS
from flask_session import Session
import redis
from datetime import timedelta

from werkzeug.serving import run_simple


# 创建APP
app = Flask(__name__)
# 让url可以跨域
CORS(app, support_credentials=True)
redis_instance = redis.StrictRedis()

# 以下是关于session的设置，在app的configuration中设置之后，
# flask_session会从中读取
app.config['SECRET_KEY'] = "your secret key"
app.config['SESSION_TYPE'] = 'redis'
# 是否使用secret_key对session cookie的sid进行加密，若设置为True，也需要设置secret_key
app.config["SESSION_USE_SIGNER"] = False
app.config["SESSION_KEY_PREFIX"] = "set your key prefix"
# 该redis instance同时也用来做其他工作
app.config['SESSION_REDIS'] = redis_instance
# session的生命周期
app.config['SESSION_REFRESH_EACH_REQUEST'] = False
app.config['PERMANENT_SESSION_LIEFTIME'] = timedelta(days=3)

# 添加session
Session(app)

app.register_blueprint(my_blueprint, url_prefix="your url prefix")


if __name__ == "__main__":
    # threaded默认是false，不开启多线程处理多个request
    app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)



# ANOTHER MODULE
from flask import Blueprint

my_blueprint = Blueprint("your name", __name__)

@my_blueprint.route("/url", methods=['POST', 'GET'])
def view_fn():
    pass