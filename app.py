from flask import Flask,jsonify, request,render_template
import test
import datetime
import database

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png'])  # only allowed the png pics could be uploaded


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')  # main page of the web application
def index():
    return render_template('index.html')

# 上传文件
@app.route('/up', methods=['POST'], strict_slashes=False)
def api_upload():
    try:
        f = request.files['photo'] # get the route of the uploaded picture
        result =test.Test(f)   # deal the picture with nervous network
        final=result.work()   # get the result
        name=request.form.get("name")  # get document's name
        if f and allowed_file(f.filename):
            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y%m%d%H%m")  #get the upload time and turn it to string form
            database.insert_data(name,otherStyleTime,str(final))
            database.test()      # could be used to check data in the table.
            para={'result': str(final),"name": name}  #prepare the parameter for the webpage
            return render_template("template.html",para=para) # return the recongnition result
    except Exception as e:
        error={'reason':str(e)} # print error track
        return render_template('errorpage.html',error=error)



if __name__ == '__main__':
    database.createKeySpace() #set the keysapce and table
    app.run(host='0.0.0.0',port=5000,debug=True) # set the port and host,open debugger for figuring out reason of the errors
