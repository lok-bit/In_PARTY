from ctypes.wintypes import BYTE
from pickletools import pybytes
from flask import Flask, render_template, request, jsonify, session, redirect,url_for,flash
from flask_session import Session
from geopy.geocoders import Nominatim
import geocoder
import pymysql
import bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'party',
    'charset': 'utf8mb4',
}

db = pymysql.connect(host='localhost', port=3306, user='root', password='')
cur = db.cursor(pymysql.cursors.DictCursor)
geolocator = Nominatim(user_agent="nkustdemo")


def getActivitiesAround(x=120.328436019052, y=22.652236997454):
    connection = pymysql.connect(**db_config)
    result = {}
    try:
        with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            sql = f"SELECT *, ST_X(location),ST_Y(location) FROM party_3 WHERE ST_Distance_Sphere(location, ST_GeomFromText('POINT({x} {y})')) < 5000;"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"發生錯誤：{str(e)}")
    finally:
        connection.close()
    return result


@app.route('/')
def home():
    markers = getActivitiesAround()
    return render_template('Front_Page.html', markers=markers)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/test2')
def test2():
    return render_template('test2.html')


@app.route('/get_current', methods=['POST'])
def get_current():
    data = request.json
    x = float(data.get('x'))
    y = float(data.get('y'))
    markers = getActivitiesAround(x, y)
    for m in markers:
        m.pop('location')
        m.pop('image')
    return jsonify(markers)

@app.route('/activity_info', methods=['GET'])
def activaityInfo():
    connection = pymysql.connect(**db_config)
    party_id = request.args.get('id')
    with connection.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        sql="SELECT `id`,`name`,`url`,`date_start`,`date_end`,`address`,`content`,`image`,`kind` FROM `party_3` WHERE `id` = %s"
        cursor.execute(sql,(party_id))
        result = cursor.fetchall()
        sql1="SELECT COUNT(*) FROM `user_upload` WHERE `party_id` = %s AND `type` <> %s"
        cursor.execute(sql1,(party_id, "0"))
        count = cursor.fetchone()['COUNT(*)']
        sql = "SELECT * FROM user_upload WHERE user_id = %s AND party_id = %s"
        cursor.execute(sql, (session.get("user_id"), party_id))
        info = cursor.fetchone()
    connection.commit()
    connection.close()
    activity_info = result[0]
    responds = {
        'id' : activity_info['id'],
        'name':activity_info['name'],
        'url':activity_info['url'],
        'date_start':activity_info['date_start'],
        'date_end':activity_info['date_end'],
        'address' : activity_info['address'],
        'image_name' : activity_info['image'] if activity_info['image'] != "" else "game_demo.jpg",
        'content' : activity_info['content'],
        'count' : count,
        'kind' : activity_info['kind'],
        'info' : info
    }
    return jsonify(responds)

@app.route('/join', methods=['GET'])
def join():
    id = request.args.get('id')
    print(id)
    join = True
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        sql = "INSERT INTO `user_upload`(`user_id`, `party_id`, `type`) VALUES (%s,%s,%s)"
        cursor.execute(sql,(session.get("user_id"), id, "1"))
    connection.commit()
    connection.close()
    responds = {
        'result' : True,
    }
    return jsonify(responds)

@app.route('/disjoin', methods=['GET'])
def disjoin():
    id = request.args.get('id')
    join = False
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        sql = "DELETE FROM `user_upload` WHERE `user_id` = %s and `party_id` = %s"
        cursor.execute(sql,(session.get("user_id"), id))
    connection.commit()
    connection.close()
    responds = {
        'result' : True,
    }
    return jsonify(responds)

@app.route('/characters')
def get_character():
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:

        sql = "SELECT `name`,`occupation`,`level`,`experience`,`partner`  FROM `role` WHERE `id` = %s"
        cursor.execute(sql,session.get("role_id"))
        activity_info=cursor.fetchone()
    connection.commit()
    connection.close()
    print("1:", activity_info)
    character = {
        'name' : activity_info[0],
        'occupation' : activity_info[1],
        'level' : activity_info[2],
        'experience' : activity_info[3],
        'partner': activity_info[4],
    }
    return jsonify(character)

@app.route('/check_in', methods=['GET'])
def check_in():
    id = request.args.get('id')
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        sql = "UPDATE `user_upload` SET `check_in` = %s WHERE `user_id` = %s and `party_id` = %s"
        cursor.execute(sql,("True",session.get("user_id"),id))
    connection.commit()
    connection.close()
    data = {
        'result' : True
    }
    return jsonify(data)

@app.route('/cancel', methods=['GET'])
def cancel():
    id = request.args.get('id')
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        sql = "UPDATE `user_upload` SET `check_in` = %s WHERE `user_id` = %s and `party_id` = %s"
        cursor.execute(sql,("False",session.get("user_id"),id))
    connection.commit()
    connection.close()
    data = {
        'result' : True
    }
    return jsonify(data)

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('location')
    location = geolocator.geocode(name)
    if location is None:
        return jsonify()
    return jsonify({'x' : location.latitude, 'y' : location.longitude})

#存圖片的資料夾
UPLOAD_FOLDER = r'static/image'
#圖片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadForm.html')
def upload_form():
    return render_template('uploadForm.html')


@app.route('/upload', methods=['POST'])
def upload():
    activity_name = request.form['activityName']
    activity_location = request.form['activityLocation']
    activity_start_date = request.form['activityStartDate']
    activity_start_time = request.form['activityStartTime']
    activity_end_date = request.form['activityEndDate']
    activity_end_time = request.form['activityEndTime']
    activity_content = request.form['activityContent']
    activity_image = request.files['activityImage']
    activity_url = request.form['activityUrl']
    activity_kind = request.form['activityKind']

    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            name = activity_name
            url = activity_url
            date_start = activity_start_date + " " + activity_start_time  # yyyy/mm/dd hh:mm:ss 2024/4/1 11:11:11 or 2024/04/01 11:11:11
            date_end = activity_end_date + " " + activity_end_time
            address = activity_location
            content = activity_content
            image = activity_image.filename

            g = geocoder.arcgis(address)
            if g.json is not None:
                longitude = g.lng  # 經度
                latitude = g.lat  # 緯度

            else:
                # 處理無法解析地址的情況
                print("無法解析地址")
                return "無法解析地址"

            # 設定sql指令，使用UNHEX()函數轉換十六進制字符串為二進制數據
            sql = "INSERT INTO party_3 (name, url, date_start,date_end, address, content, image, location, kind) VALUES (%s, %s, %s, %s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)'), %s)"
            # 執行sql指令
            cursor.execute(sql, (name, url, date_start, date_end, address, content, image,  longitude, latitude, activity_kind))
            #取得活動id
            sql = "SELECT `id` FROM `party_3` WHERE `name` = %s"
            cursor.execute(sql, name)
            party_id=cursor.fetchone()[0]
            #取得使用者id
            #user_id=request.cookies.get('user_id')
            user_id=session.get("user_id")
            #type為0表示活動舉辦者
            sql = "INSERT INTO `user_upload`(`user_id`, `party_id`, `type`) VALUES (%s,%s,%s)"
            cursor.execute(sql,(user_id, party_id, "0"))

        connection.commit()
        print("資料新增成功")
        if 'activityImage' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['activityImage']
        if file.filename == '':
            print("No selected file")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

        return ("表單提交成功")
    except Exception as e:

        connection.rollback()
        print(f"發生錯誤：{str(e)}")
        return '發生錯誤'
    finally:
        # 關閉資料庫連線
        connection.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("logged_in"):
        return redirect('/')
    if request.method == 'POST':
        try:
            # 連接資料庫
            connection = pymysql.connect(**db_config)
            request.method == 'POST'
            username = request.form['username']
            password = request.form['password']
            with connection.cursor() as cursor:
            # 從資料庫中查詢帳號密碼是否存在
                sql = "SELECT `id`,`password`,`permissions` FROM `user` WHERE `name` = %s"
                cursor.execute(sql, (username))
                user = cursor.fetchone()
                print(user[1])
                if bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                    sql = "SELECT `id` FROM `role` WHERE `user_id` = %s"
                    cursor.execute(sql,(user[0]))
                    role=cursor.fetchone()
                    if role:
                        session['role_id'] = role[0]
                    session['user_id'] = user[0]
                    session['name'] = username
                    session['logged_in'] = True
                    if user[1]:
                        session['permissions'] = user[1]
                        return redirect("/")
                else :
                    return render_template('login.html', error=True)
        except Exception as e:
            print(f"發生錯誤：{str(e)}")
            return render_template('login.html')
        finally:
            connection.close()
    return render_template('login.html')
        



@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("logged_in"):
        return redirect('/')
    if request.method == 'POST':
        try:
            connection = pymysql.connect(**db_config)
            request.method == 'POST'
            username = request.form['username']
            password = request.form['password']
            #取得角色資料
            role_occupation = "冒險者"
            role_partner = "小夥伴"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
            with connection.cursor() as cursor:
            # 從資料庫中查詢帳號是否存在
                sql = "SELECT `id` FROM `user` WHERE `name` = %s"
                cursor.execute(sql, (username,))
                userid = cursor.fetchone()
                if userid == None:
                    sql = "INSERT INTO `user`(`name`, `password`,`permissions`) VALUES (%s,%s,%s)"
                    cursor.execute(sql,(username, hashed,0))
                    sql = "SELECT `id`,`permissions` FROM `user` WHERE `name` = %s"
                    cursor.execute(sql, (username))
                    user = cursor.fetchone()
                    #創建角色
                    sql = "INSERT INTO `role`(`name`, `occupation`, `level`, `experience`, `partner`, `user_id`) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,(username, role_occupation,1,0,role_partner,user[0]))
                    sql = "SELECT `id` FROM `role` WHERE `name` = %s"
                    cursor.execute(sql, (username))
                    role_id = cursor.fetchone()
                    if role_id:
                        session['role_id'] = role_id[0]
                    session['user_id'] = user[0]
                    session['name'] = username
                    session['logged_in'] = True
                    session['permissions'] = user[1]
                    connection.commit()
                    return redirect('/login')
                else :
                    print("註冊失敗")
                    return render_template('register.html', error=True)
        except Exception as e:
            connection.rollback()
            print(f"發生錯誤：{str(e)}")
            return render_template('register.html')
        finally:
            connection.close()
    return render_template('register.html')
   
@app.route('/logout')
def logout():
    if session.get("logged_in"):
        session['name'] = None
        session['logged_in'] = None
    return redirect('/')
    
@app.route('/service')
def service():
    if session.get("logged_in"):
        return render_template('index.html')
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
