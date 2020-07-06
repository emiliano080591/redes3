from flask import Flask,request,jsonify,Response
from getSNMP import consultaSNMP, consultaSNMP2,obtener,getDir
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from bson import json_util
from bson.objectid import ObjectId
import time,os,fnmatch,shutil

UPLOAD_FOLDER = '/home/emiliano/Documentos/python/proyecto_redes/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
cors = CORS(app)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
Peticiones GET
'''
@app.route('/getIps',methods=['GET'])
@cross_origin()
def getIps():
    response=json_util.dumps(getDir('192.168.0.0'))
    return Response(response,mimetype='application/json')
    

'''
Peticiones POST
'''
@app.route('/getAncho',methods=['POST'])
@cross_origin()
def getAncho():
    com=str(request.form['comunidad'])
    sIp=str(request.form['ip'])
    r=[]
    cont=0
    while cont<5:
        s=obtener(com,sIp)
        if s != False:
            r.append(s)
            cont=cont+1
            time.sleep(5)
        else:
            r.append(s)
    response=json_util.dumps(r)
    return Response(response,mimetype='application/json')

@app.route('/getDatos',methods=['POST'])
@cross_origin()
def getDatos():
    com=str(request.form['comunidad'])
    sIp=str(request.form['ip'])
    res=consultaSNMP2(com,sIp,'1.3.6.1.2.1.1.1.0')
    response=jsonify({'ok':True,'data':res})
    response.status_code=200
    return response
    
@app.route('/upload',methods=['POST'])
@cross_origin()
def upload_file():
    #si no hay un archivo enviado
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request','ok':'false'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    #si el archivo esta vacio
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading','ok':'false'})
        resp.status_code = 400
        return resp
    #si hay un archivo y contiene la extension permitida se guarda
    if file and allowed_file(file.filename):
        t = time.localtime()
        timestamp = time.strftime('%b_%d-%Y_%H%M%S', t)
        filename = secure_filename(file.filename)
        filename = timestamp+'_'+filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message' : 'File successfully uploaded','archivo':filename,'ok':'true'})
        resp.status_code = 201
        return resp
    #si no contiene una extension permitida
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg','ok':'false'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    app.run(debug=True,port=8000)