from flask import Flask,request,jsonify,Response
from getSNMP import consultaSNMP, consultaSNMP2,obtener,getDir
from flask_cors import CORS, cross_origin
from bson import json_util
from bson.objectid import ObjectId
import time

app = Flask(__name__)
cors = CORS(app)

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
    #response=json_util.dumps(obtener('comunidadA','192.168.0.9'))
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
    
if __name__ == "__main__":
    app.run(debug=True,port=8000)