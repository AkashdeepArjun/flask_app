import flask
from flask_wtf.csrf import CSRFProtect
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from flask_migrate import Migrate
from markupsafe import escape
from pack.mymod import linear_search
import os 
from wtforms import Form,StringField,SubmitField,PasswordField
from database.InstanceManager import InstanceManager
from sqlalchemy.exc import IntegrityError
import traceback
import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,Length

from flask_wtf.file import FileField,FileAllowed,FileRequired

from flask_sqlalchemy import SQLAlchemy

from database import InstanceManager, db

from werkzeug.utils import secure_filename 

from utils.Helper import is_file_format_valid

from werkzeug.datastructures import CombinedMultiDict

from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps
from flask_cors import CORS 

from flask_limiter import Limiter

import logging
from logging.handlers import RotatingFileHandler


from flask_limiter.util import get_remote_address

# from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.utils import make_msgid
from werkzeug.middleware.proxy_fix import ProxyFix  

import smtplib

global message

global projects 

projects = ["Project 1", "Project 2", "Project 3", "Project 4", "Project 5"]

message = "default message"

# UPLOAD_DIRE̥̥̥CTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

#testiing flow

def get_ip():
    return flask.request.headers.get("X-Forwarded-For", flask.request.remote_addr)


def get_client_ip():
  # Extract true client IP from cPanel proxy headers

  try:
    return (
        flask.request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or flask.request.remote_addr
        or "127.0.0.1"
    )
  except Exception as e:
      app.logger.warning(f"ip error {str(e)}")

      


def db_rate_limit(max_requests:int=5,window_in_seconds:int=60):

    def decorator(f):

        @wraps(f)
        def wrapper(*args,**kwargs):
            try:
                client_ip = get_client_ip()
                endpoint = request.path
                now = datetime.datetime.now(timezone.utc)
                cutoff = now - timedelta(seconds=window_in_seconds)

                recent_count = db.session.scalar(
                db.select(db.func.count(RateLimiting.id)).where(
                RateLimiting.ip == client_ip,
                RateLimiting.endpoint == endpoint,
                RateLimiting.timestamp >= cutoff,
                )
                ) or 0

                if recent_count >= max_requests:
                    return (
                        jsonify({
                    "error": "hit limits",
                    "message": f"Too many requests. Limit is {max_requests} per {window_in_seconds} seconds.",
                        }),
                            429,
                    )

                new_log = RateLimiting(ip=client_ip, endpoint=endpoint, timestamp=now)
                db.session.add(new_log)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                app.logger.warning(f"RATE LIMIT ISSUE {str(e)}")
                return (
                    jsonify({
                        'error': 'RateLimiterError',
                        'details': str(e),
                        'type': type(e).__name__,
                    }),
                    500,
                  ) 

            return f(*args, **kwargs)

        return wrapper

    return decorator



from functools import wraps
import time
from flask import jsonify, request

# Simple in-memory rate storage: { ip: [timestamp1, timestamp2, ...] }
rate_store = {}


def rate_limit(requests_per_minute=5):

  def decorator(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
      client_ip = (
          request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
          or request.remote_addr
      )
      now = time.time()
      window = 60  # 1 minute window

      # Clean old requests for this IP
      user_requests = rate_store.get(client_ip, [])
      user_requests = [t for t in user_requests if now - t < window]

      if len(user_requests) >= requests_per_minute:
        return (
            jsonify(
                {"error": "hit limits", "message": "exceeded request limit"}
            ),
            429,
        )

      user_requests.append(now)
      rate_store[client_ip] = user_requests
      return f(*args, **kwargs)

    return decorated_function

  return decorator







try:
    
    app = InstanceManager.get_instance(flask.Flask,__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    #settings for server  
    # CORS(app, resources={r"/api/*":{"origins": ["http://localhost:5173", "https://www.laziakeey.in"]}})

    CORS(
     app,
            resources={
            r"/api/*": {
                "origins": ["http://localhost:5173", "https://www.laziakeey.in"],
                "supports_credentials": True  # <--- CRITICAL FOR SESSIONS/COOKIES!
            }
        }
    )


    # CORS(app=app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}}) 
    csrf = CSRFProtect(app)
    
    limiter = Limiter(
            # get_remote_address,
            get_ip,
            # get_client_ip,
            app=app,
            default_limits=["200 per day","50 per hour"],
            storage_uri="memory://",
            enabled=True
    
        )










    # 
    #see if  works
    basedir = os.path.abspath(os.path.dirname(__file__))
    log_file_path = os.path.join(basedir, 'flask_error.log')
# Set up logging to a local file inside your project folder
    if not app.debug:
        file_handler = RotatingFileHandler(log_file_path, maxBytes=10240, backupCount=5)
        file_handler.setFormatter(
            logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
        # app.logger.
        app.logger.addHandler(file_handler)

        app.logger.error('Flask application startup')













   

    

except Exception as e:
    app.logger.info(f"ERROR {str(e)}")
    print("ERRORRRR {} ".format(e))


app.config.update(
    TESTING=True,
    SECRET_KEY='akeeydemoproject007'
)

# DATABASE SETTINGS 
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://akash:akash%40mysql@localhost/dev"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

# UPLOAD FOLDER_CONFIG
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static','uploads')

app.config['WTF_CSRF_ENABLED'] = False

app.config["RATELIMIT_ENABLED"] = True

#mail settings 
# app.config['MAIL_SERVER'] = 'mail.laziakeey.in' 
app.config['MAIL_SERVER'] = 'sg2plzcpnl508264.prod.sin2.secureserver.net'   # Server host from cPanel
  # Server host from cPanel
app.config['MAIL_PORT'] = 465                  # Usually 465 for SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'akash@laziakeey.in'
app.config['MAIL_PASSWORD'] = 'akash@cpanel007007'
app.config['MAIL_DEFAULT_SENDER'] = 'akash@laziakeey.in'
app.config['SECURITY_PASSWORD_SALT'] = 'akash@la007'

SMTP_SERVER = 'sg2plzcpnl508264.prod.sin2.secureserver.net'
SMTP_PORT = 465
SMTP_USER = 'akash@laziakeey.in'
SMTP_PASS = 'akash@cpanel007007'

# mail = Mail(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY']) 

def generate_verification_token(email): #server side 

    return serializer.dumps(email,app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token,expiration=1800): #client side clicks verification will done at server 
    try:
        email = serializer.loads(token,
                                 salt=app.config['SECURITY_PASSWORD_SALT'],max_age=expiration)

        return email

    except (SignatureExpired,BadTimeSignature):
        return None


def send_mail_logic(reciever,subject,body,body_html=None):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject 
    # msg['From'] = f'LaziAkeey <{app.config['MAIL_USERNAME']}>'
    msg['From'] = f"LaziAkeey <{app.config['MAIL_USERNAME']}>"
    msg['To'] = reciever
    msg['Message-ID'] = make_msgid(domain='laziakeey.in')

    msg.attach(MIMEText(body, 'plain'))

    if body_html:
        msg.attach(MIMEText(body_html, 'html'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [reciever], msg.as_string())


@app.route('/test_api')
def test():
    return flask.jsonify({"status":"okay","message":"rocks oh yea lolwa"}) 



@app.route('/send_verification',methods=['POST'])
def send_verification():

    data = flask.request.get_json() or {}

    email = data.get('email',None)

    current_user = flask.g.user

#check if valid mail is sent by user
    if not email or not current_user:
        return flask.jsonify({"error":"email required"}),400

    if current_user.email != email:
        return flask.jsonify({"error":"verify the email you logged in via  not oher email allows"}),400

    token = generate_verification_token(email=email)

    verify_mail = f"https://www.laziakeey.in/api/verify_email/{token}"

    body= f"""Hello,

        Thank you for signing up with Laziakeey.

        Please verify your email address by clicking the link below:
        {verify_mail}

        If you did not request this email, please ignore it.

        Best regards,
        Laziakeey Team
""" 
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #0284c7;">Welcome to Laziakeey</h2>
            <p>Please confirm your email address to complete your account setup.</p>
            <div style="margin: 25px 0;">
                <a href="{verify_mail}" style="background-color: #0284c7; color: #ffffff; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Verify Email Address</a>
            </div>
            <p style="font-size: 13px; color: #666;">Or copy and paste this link into your browser:</p>
            <p style="font-size: 13px; word-break: break-all; color: #0284c7;">{verify_mail}</p>
        </div>
    </body>
    </html>
    """



    try:
        send_mail_logic(reciever=email,subject='VERIFY MAIL',body=body,body_html=html_content)
        return (
            flask.jsonify({'success': True, 'message': 'Verification email sent!'}),
            200,
        )

    except Exception as e:
        return flask.jsonify({"error":str(e)}),400


@app.route('/logs/<int:n>')
def get_debug_logs(n):
  try:
    with open(log_file_path, 'r') as f:
      lines = f.readlines()

    # Reverse the array so the newest log entry is at the top
    reversed_logs = lines[-1:-n-1:-1]

    # Return top 50 newest lines
    return flask.jsonify({'success': True, 'logs': reversed_logs[:50]}), 200
  except Exception as e:
    return flask.jsonify({'success': False, 'error': str(e)}), 500

    




@app.route('/verify_email/<token>',methods=['GET'])
def verify_email(token):

 



    try:

           
        email = confirm_token(token)
        
        if not email:
                
            return flask.jsonify({"status":"failed","details":"token is expired "}),400
        
        user = User.query.filter_by(email=email).first()
        
        
        if not user:
        
            return flask.jsonify({"status":"failed","details":"not such user exist "}),400
        
        
        if user.email_verified_at is not None:
            return flask.jsonify({"status":"success","message":"user is already verified"}) ,200
        
        
        user.email_verified_at = datetime.datetime.now(datetime.timezone.utc)





        db.session.commit()

        return flask.jsonify({"status":"success","message":"user is  verified"}) ,200




    except Exception  as e :
        db.session.rollback()
        app.logger.error(str(e))
        return flask.jsonify({"status":"Failed","message":str(e)}),400
    









@app.errorhandler(429)
def show_message(e):
    return flask.jsonify({"error":"hit limits","message":"exceeded request limit"}),429


db.init_app(app)
migrate = Migrate(app, db)
InstanceManager._instances[SQLAlchemy] = db

@app.before_request
def load_current_user():

    name = flask.session.get('user')

    if not name:
        flask.g.user=None

    else:
        flask.g.user = User.query.filter_by(username=name).first()
        # flask.g.user.rol

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response





def admin_required(f):
    @wraps(f)
    def wrapper_function(*args,**kwargs):
        user = flask.g.user

        if not user:
            return flask.jsonify({"error":"Unauthorised Access "},401)
        return f(*args,**kwargs)
    
    return wrapper_function


def login_required(f):
    @wraps(f)
    def login_middleware(*args,**kwargs):
        user = getattr(flask.g,'user',None)

        if not user:
            return flask.jsonify({"error":"login required"})
        return f(*args,**kwargs)

    return login_middleware


# @app.route('/tester')
# def test_route():
#     return f"Github workflow is working"


@app.route('/cart/add',methods=['POST'])
@login_required
def add_to_cart():
    try:
        data = flask.request.get_json() or {}

        app.logger.info(f"CART ITEM RECIEVED {data}")

        product_id = data.get("product_id")

        quantity = data.get("quantity",1)

        app.logger.info(f"cart add request recieved {product_id} and {quantity}")

        #  check for invalid product 
        if not product_id or not isinstance(quantity,int) or quantity <1:
            return flask.jsonify({"error":"invalid product id or quantity"}),400

        # check if product exist 
        product = Product.query.get(product_id)

        if not product:
            return flask.jsonify({"error":"product not found "}),400

        user = flask.g.user

        cart = user.cart

        #  check if cart exist 
        if not cart :
            cart = Cart(user_id = user.id)
            db.session.add(cart)
            db.session.flush()

        # check if product exist 
        cart_item = CartProduct.query.filter_by(cart_id= cart.id,product_id=product_id).first()

        if cart_item:
            cart_item.quantity = quantity
        else:
            cart_item = CartProduct(cart_id=cart.id,product_id=product_id,quantity=quantity)

        db.session.add(cart_item)

    

        db.session.commit()


        

        db.session.rollback()

           

        
        return flask.jsonify({
            "status":"ok",
            "message": "Item added to cart successfully",
            "cart_item": {
                "product_id": cart_item.product_id,
                "quantity": cart_item.quantity
            }
        }), 200
    except Exception as e :
        app.logger.error(f"ADD TO CART ERROR :{str(e)}")
        return flask.jsonify({"error":"database issue","details":str(e)})

@app.route('/cart',methods=['GET'])
@login_required
def my_cart():
    try:
        user = flask.g.user

        cart = user.cart 

        if not cart :
            # return flask.render_template("error.html",error="Cart is Empty")
            return flask.jsonify({"status":"failed","message":"cart is empty"})
        cart_items = CartProduct.query.filter_by(cart_id=cart.id).all()
        items_list = []

        total = 0

        #ulala

        for item in cart_items:

            product = item.product

            if not product:
                continue

            sub_total = float(product.price)*item.quantity 
            total+=sub_total

            items_list.append({
                "product_id": product.product_id,
                "name": product.name,
                "brand": product.brand,
                "price": float(product.price),
                "quantity": item.quantity,
                "image_url": product.image_url,
                "subtotal": round(sub_total, 2)
            })


        # JSON.DATA ={PRODUCTS,TOTAL}
        # return flask.render_template("cart.html",products = items_list,total=total)
        return flask.jsonify({"status":"ok", "products":items_list,"total":total,"cart_id":cart.id}),200
    except Exception as e:

        app.logger.error(f"CART ERROR {str(e)}")
        return flask.jsonify({"status":"failed","message":str(e)}),400

    # return flask.jsonify({"products":items_list,"total":total}),200



@app.route('/cart/delete')
def delete_cart_item():

    
    try:
        cart_id = request.args.get('cart_id',None)

        product_id = request.args.get('product_id',None)

        if not cart_id or not product_id:
            return flask.jsonify({"status":"failed","reason":"either cart is invalid or product is invalid"}),404

        target_product  = CartProduct.filter_by(cart_id=cart_id,product_id =product_id).first()

        if not target_product:

           return flask.jsonify({"status":"failed","reason":"not such product found in cart "}),404

        db.session.delete(target_product)

        db.session.commit()

        


    except Exception as e:

        return flask.jsonify({"status":"failed","reason":str(e)})

    





@app.route('/place_order',methods=['POST'])
@login_required
def place_order():
    try:
        user = flask.g.user

        cart =  user.cart 

        if not cart or not cart.product_items:

            return flask.jsonify({"error":"cart is empty"}),400

        order_items_result = []

        grand_total = Decimal('0.00')

            # PRPARE ITEMS FROM CART TO BE SEND TO ORDER
        for cart_item in cart.product_items:

            product = cart_item.product

            if not product:
                continue

            product_price = Decimal(product.price)

            sub_total = cart_item.quantity * product_price

            grand_total +=sub_total

            order_items_result.append({

                "product_id":product.product_id,
                "quantity":cart_item.quantity,
                "unit_price":product_price


            })

        if not order_items_result:
            return flask.jsonify({"error":"not valid product found in cart"}),400

        new_order = Order(user_id = user.id,
                        amount=grand_total,
                        created_at = datetime.datetime.utcnow())

        db.session.add(new_order)

        db.session.flush()

        for item in order_items_result:

            order_product = OrderProduct(order_id=new_order.order_id,
                                        product_id = item["product_id"],
                                        quantity = item["quantity"],
                                        unit_price = item["unit_price"]
                                        )

            db.session.add(order_product)

        CartProduct.query.filter_by(cart_id=cart.id).delete()

        db.session.commit()

        cart.query.filter_by(id = cart.id).delete()

        db.session.commit()

    

        return flask.jsonify({
                "message": "Order placed successfully!",
                "order_id": new_order.order_id,
                "total_amount": float(grand_total),
            }), 201
    except Exception as e:

            db.session.rollback()
            app.logger.error(f"ORDER PLACE ISSUE:{str(e)}")
            return flask.jsonify({"message":"order failed","detail":str(e)})


 



       

@app.route('/my_orders',methods = ['GET'])
@login_required
def my_orders():
    try:
        user = flask.g.user
        
        orders = user.orders.order_by(Order.created_at.desc()).all()
        
        if not orders :
            # return flask.render_template("error.html",error="Cart is Empty") 
            return flask.jsonify({"status":"failed","message":"cart is empty"},400)


        return  flask.jsonify({"status":"success","orders":[o.to_dict() for o in orders]}),200
    except Exception as e :

        app.logger.error(f"FETCH ORDERS ERROR: {str(e)}")
        return flask.jsonify({"status":"failed","message":str(e)},400)



@app.route('/my_orders/<int:order_id>')
@login_required
def order_details(order_id):
    
    try:
        user = flask.g.user

        order_x = user.orders.filter_by(order_id=order_id).first()

        if not order_x:
            return flask.jsonify({"error":"not such order found"}),400

        products_order_x = order_x.product_items

        purchased_products =[]

        total_bill =Decimal('0.00')

        for item in products_order_x:

            product = item.product

            if not product:
                continue 

            sub_total = Decimal (item.unit_price * item.quantity)

            total_bill+=sub_total


            purchased_products.append({
                "product_id":product.product_id,
                "product_name":product.name,
                "quantity":item.quantity,
                "price":item.unit_price,
                "subtotal":sub_total

            })


        if not purchased_products:
            return flask.jsonify({"error":"not valid purchase found"}),400

        # return flask.jsonify({"data":purchased_products,"message":"orders fetch success"})
        # return flask.render_template("order_detail.html",order_items = purchased_products,total_bill=total_bill)
        return flask.jsonify({"status":"success","order_items":purchased_products,"total_bill":total_bill}),200

    except Exception as e:

            app.logger.error(f"ORDER DETAILS ISSUE {str(e)}")

            return flask.jsonify({"status":"failed","message":str(e)}),400





    





    

    















        












@app.route('/inventory',methods=['POST'])
@admin_required
def manage_products():

    product_id = flask.request.form.get('product_id')
    product_name = flask.request.form.get("name")
    product_slug = flask.request.form.get("slug")
    product_brand = flask.request.form.get("brand")
    product_price= flask.request.form.get("price")
    product_category = flask.request.form.get("category")
    json_info ={}
    keys = flask.request.form.getlist("json_keys")  
    values= flask.request.form.getlist("json_values")

    for k,v in zip(keys,values):
        json_info[k.strip()] = v.strip()

    file = flask.request.files['file']

    if file.filename =='':
        return flask.jsonify({"error":"file is empty"}),500
    else:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(file_path)

        new_product = Product(product_id=product_id,
                                name=product_name,
                                category=product_category,
                                specs =json_info,
                                price=product_price,
                                slug=product_slug,
                                image_url=file.filename,
                                brand=product_brand,
                                description="",
                                created_at =datetime.datetime.now()
                    
                                )
        
        # Product.query.add_entity(new_product)

        db.session.add(new_product)


        try:

            db.session.commit()
        except IntegrityError as e:

            return   flask.jsonify({"error":"duplicate entry"}),500




        res = flask.jsonify({"message":"product added"}),201
    
        return res
        # return f"aya dekho kaun"
    
with app.app_context():

    from data.User import User
    from data.Order import Order
    from data.Product import Product
    from data.Cart import Cart

    from data.OrderProduct import OrderProduct
    
    from data.CartProduct import CartProduct

    from data.RateLimiting import RateLimiting

    # import data.User, data.Product,data.Cart, data.Order, data.OrderProduct, data.CartProduct


    db.create_all()


    RateLimiting.__table__.create(bind=db.engine, checkfirst=True)
    print("Rate limit table initialized successfully!") 


class  RegisterationForm(FlaskForm):
        
        username = StringField("Username",validators=[DataRequired()])
        email = StringField("UserEmail",validators=[DataRequired(),Email()])
        password =PasswordField("Password",validators=[DataRequired()])
        profile_picture = FileField("profile photo",validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'Only Images are allowed')])
        submit= SubmitField("Join Us")


class LoginForm(FlaskForm):
    usermail=StringField("Username",validators=[DataRequired(),Email()])
    userpassword =PasswordField("Userpassword",validators=[DataRequired()])
    submit=SubmitField("Login")

@app.route('/logout')
def logout():
    flask.session.clear()
    response= flask.jsonify({"status":"ok","message":"logout succesfully"})
    response.delete_cookie('user')
    return response


@app.route('/debug-ip')
def debug_ip():
  return jsonify({
      'remote_addr': request.remote_addr,
      'x_forwarded_for': request.headers.get('X-Forwarded-For'),
      'client_ip_header': request.headers.get('CF-Connecting-IP'),
      'all_headers': dict(request.headers),
  })



@app.route('/login',methods =['POST'])
@csrf.exempt
@db_rate_limit(max_requests=5,window_in_seconds=60)
def login_user():
    # existing_user_client = flask.request.cookies.get('user') 

    try:
        existing_user_server = flask.session.get('user')

        existing_user  = flask.g.user

        app.logger.info(f"CONTENT TYPE {request.content_type}")
        app.logger.info(f"RAW FORM {request.form}")
        app.logger.info(f"JSON {request.get_json(silent=True)}")
            
        form = LoginForm(flask.request.form,meta={'csrf': False})
    
        if form.validate_on_submit:
            username=form.usermail.data
            userpassword = form.userpassword.data

            app.logger.info(f"request from user {username} with password {userpassword} recieved")
                
            user =User.query.filter_by(email=username).first()
            if user:
                is_valid = check_password_hash(user.password,userpassword)
                if is_valid:

                    flask.session['user'] = user.username
                    flask.session['isLoggedIn'] = True
                    # response= flask.make_response(flask.render_template("products.html",user=user),201)
                    # response = flask.make_response(flask.redirect(flask.url_for('get_products')), 302)
                    # response.set_cookie('user',user.username,15*60)                     
                    return flask.jsonify({"status":"ok","message":"login success","user":{
                    "usermail":username,"profile_url":user.profile_url,
                    "is_verified":bool(user.email_verified_at)
                    }}),200
                else:
                    return flask.jsonify({"status":"failed","message":"login failed"}),400
                   
            else:
                    return flask.jsonify({"status":"failed","message":"no user found"}),200
               
    except Exception as e:
        app.logger.info(f"ERROR OCCURED {str(e)}")
            
@app.route('/register',methods =['OPTIONS','POST'])
@csrf.exempt
def register_user():

    if flask.request.method == 'OPTIONS':
        return '', 200

    try:
        errors={}


        



        form = RegisterationForm(CombinedMultiDict((flask.request.files,flask.request.form)))
    
        if form.validate_on_submit():
            # file = request.files['file']

            # if file.filename == '':
            #     errors['file_upload'] = " file is empty"
            #     return jsonify({"message":"register user failed","errors":errors}),500
            
            
            profile_url = form.profile_picture.data
            app.logger.info(f" tpye of  profile url is {type(profile_url)}")
            filename = secure_filename(profile_url.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            profile_url.save(file_path)

            name= form.username.data.strip()
            email = form.email.data.strip()
            password = form.password.data
            hashed_password = generate_password_hash(password=password)       
            new_user = User(username=name,email=email,password=hashed_password,profile_url=filename)
            db.session.add(new_user)
            db.session.commit() 
            # return flask.redirect(flask.url_for('get_products'))
            return flask.jsonify({"status":"success","message":"user created successfully", "user":{"usermail":email,"profile_url":profile_url.filename},

                    "is_verified":bool(new_user.email_verified_at)

                                   }),201
                

        else:
            print('FORM NOT VALIDATED')
            clean_errors = {}
            for field_name, error_messages in form.errors.items():
                clean_errors[field_name] = error_messages
            return flask.jsonify({"status":"failed","reason":clean_errors})

                # return f"form submitted successfully"
    except Exception as e:
        app.logger.error(f"REGISTERATION ERROR: {traceback.format_exc()} ")




@app.route('/products',methods=['GET'])
@csrf.exempt
def get_products():
    try:
        query = db.select(Product).order_by(Product.product_id)
        page = flask.request.args.get('page',1,type=int)
        per_page= flask.request.args.get('per_page',10,type=int)
        pagination = db.paginate(query,page=page,per_page=per_page)
        products = pagination.items

            # return jsonify({"products":products})
            # return flask.render_template("products.html",user=user_obj, products=products,pagination=pagination)
        return flask.jsonify({"status":"success","products":[p.to_dict() for p in products],"pagination": {
              "page": pagination.page,
              "per_page": pagination.per_page,
              "total_items": pagination.total,
              "total_pages": pagination.pages,
              "has_next": pagination.has_next,
              "has_prev": pagination.has_prev,
          }}),200
    except Exception as  e:

        app.logger.error(f"PRODUCTS FETCH  ERROR {str(e)} ")

    

@app.route('/search-suggestions')
def get_suggestions():

    query_text = flask.request.args.get('q','',type=str)

    if not query_text or len(query_text) < 2:
        return flask.jsonify({"items": [], "has_next": False})

    page = flask.request.args.get('page',1,type=int)

    per_page = flask.request.args.get('per_page',5,type=int)

    database_query = db.select(Product).where(Product.name.ilike(f"%{query_text}%")).order_by(Product.name)
    
    


    # Paginate the results cleanly
    pagination = db.paginate(database_query, page=page, per_page=per_page, error_out=False)
    
    # Format current page payload
    suggestions = [{"id": item.product_id, "name": item.name} for item in pagination.items]
    
    return flask.jsonify({
        "items": suggestions,
        "has_next": pagination.has_next # Tells frontend whether to allow more scrolling
    })




@app.route('/products/<int:id>')
def product_detail(id):
    try:
        target_product = Product.query.get(id)

        if target_product:
           return flask.jsonify({"status":"success","product":target_product.to_dict()}),200
        # return flask.render_template("product_detail.html",product=target_product)
        else:
        # return flask.render_template("error.html",error = "could not find product")
          return flask.jsonify({"status":"failed","message":'product did not found'})

    except Exception as e:
            app.logger.error(f"PRODUCT DETAIL ERROR {str(e)}")  
    










# @app.route('/customers')
# def getCustomers():
#     users =User.query.all()
#     print('users ',users)
#     return flask.jsonify([user.to_dict() for user in users])

# @app.route('/customers/<id>')
# def customer_detail(id):

#     user = User.query.get(id)

#     if user:
#         return flask.jsonify(user.to_dict())
    
#     else:
#         return flask.jsonify({"error":"could not find user "}),400



# @app.route('/upload',methods=['POST'])
# def upload_file():

#     if not 'file' in flask.request.files:
#         return flask.jsonify({'message':"not file found for upload",'error':400}),400

#     file = flask.request.files['file']

#     if file.filename == '':
#         return flask.jsonify({"error":"no selected file"}),400
    
#     if file and is_file_format_valid(file.filename,ALLOWED_EXTENSIONS):

#         fname = secure_filename(file.filename)
#         fpath = os.path.join(app.config['UPLOAD_FOLDER'],fname)

#         file.save(fpath)

#         return flask.jsonify({"status":"success"}),201
    
#     return flask.jsonify({"status":"failed"}),401   


# @app.route('/download/<filename>',methods=['GET'])
# def download_file(filename):
#     try:

#         safe_file_name = secure_filename(filename)

#         return flask.send_from_directory(app.config['UPLOAD_FOLDER'],safe_file_name,as_attachment=True)
    

    
#     except FileNotFoundError as e:
#         print("errror occured ",e)
#         return flask.jsonify({"error":e}),404


# @app.route('/test_download')
# def test():
#     return flask.render_template("download.html")



class MyForm(FlaskForm):
    name =StringField('Name',validators=[DataRequired()])
    submit =SubmitField('Submit')


class RegisterForm(FlaskForm):

    username = StringField("Username",validators=[DataRequired(),Length(min=4,max=20)])
    usermail = StringField("Usermail",validators=[DataRequired(),Email()])
    userpass = PasswordField("Userpass",validators=[DataRequired(),Length(min=8)])
    submit =SubmitField('Submit')

# @app.route('/signing_up',methods=['GET','POST'])
# def signing_up():
#     form = RegisterForm()
#     errors =None
#     if form.validate_on_submit():
#         return f"registeration succesful"
    
#     if form.errors:
#         errors =form.errors
#         return flask.render_template("signing_up.html",form=form,errors=errors)

#     return flask.render_template("signing_up.html",form=form,errors=errors)



# @app.get("/signup")
# def signup():
#     form = MyForm()
#     return flask.render_template("signup.html",form=form)

# @app.post('/signup')
# def signup_post():
#     return f"welcome {flask.request.form.get("name")}"

@app.route("/")
def home():
    return flask.render_template("index.html",name="akash")
#  dangerous 
# @app.route("/test_route")
# def test_route():
#     arg_x= request.args.get("x", "No parameter provided")
#     return f"<h1>Value of x: {arg_x}</h1>"


# @app.route("/test_route")
# def test_route():
#     arg_x = flask.request.args.get("x", "No parameter provided")
#     return f"<h1>Value of x: {escape(arg_x)}</h1>"

# @app.route("/myroute/<name>")
# def myroute(name):
#     return f"<h1>Hello, variable name is  {escape(name)}!</h1>"


# @app.route("/myposts/<int:post_id>")
# def myposts(post_id):
#     return f"<h1>Post ID is {escape(post_id)}</h1>"


# @app.route("/mybuilds/<path:subpath>")
# def mybuilds(subpath):
#     return f"<h1>Subpath is {escape(subpath)} args :{flask.request.args.get("x","x not specified")},{flask.request.args.get("y","y not specified")}  </h1>" 



    
# @app.route('/welcome')
# def welcome():
#     return flask.render_template("welcome.html")



# @app.route("/profile/<username>")
# def profile(username):
#     if username=="admin":
#         return flask.redirect(flask.url_for('home'))
    


# @app.route("/specso")
# def specs():
#    specs ={"RAM":"16GB","CPU":"Intel i7","Storage":"1TB SSD"}
#    return flask.render_template("specs.html",specs=specs)

# @app.route('/test_logic')
# def grade_calculator():
#     # Define a list of student dictionaries with name and score.
#     students = [
#         {'name': 'Alice', 'score': 85.234},
#         {'name': 'Bob', 'score': 59.567},
#         {'name': 'Charlie', 'score': 72.3},
#         {'name': 'David', 'score': 49.8},
#         {'name': 'Eve', 'score': 91.456}
#     ]
#     # Render the 'grades.html' template with the students data.
#     return flask.render_template('grades.html', students=students)


# @app.route("/my_projects")
# def my_projects():
#     global projects
#     res = flask.jsonify(projects)
#     return res




# @app.route('/samples')
# def projects():
#     projects = [
#         {"name": "Library Management System"},
#         {"name": "Personal Blog"},
#         {"name": "Data Structures Visualizer"}
#     ]
#     # res = jsonify(sample_projects)

#     return flask.render_template('samples.html',projects=projects)
