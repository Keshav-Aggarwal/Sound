import random
import json


from flask import Flask, jsonify, make_response
from flask import request
from random import randint
import subprocess
import time
import os

app = Flask(__name__)

items = [
    {
        'id': 1,
        'address_1': u'images/1.jpg',
		'address_2': u'images/2.jpg',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False,
        'pie_chart_1' :[['Item','Competitor'], ['Apple',2], ['Orange',4],['Banana',1]],
        'pie_chart_2' :[['Brand','Competitor'], ['Samsung',3], ['Xiaomi',4]],
        'pie_chart_3' :[['Brand','Coverage'], ['Dell',3], ['HP',7]],
        'bounding_box_img' : u'images/3.jpg',
        'current_product_affinity' : 90
    },
    {
        'id': 2,
        'address_1': u'images/2.jpg',
		    'address_2': u'images/1.jpg',
        'description': u'Cold Storage', 
        'done': False
    }
]


#  Entry level method for SMART analyzer.
#  It accpets aisle image path and product image path
#  as input and calls model pipeline to process
@app.route('/smart/analyze', methods = ['POST'])
def analyze_aisle_image():
   print('request.args ', request.form)
   ais_audio_file = request.files['AIS_IMG']
   print('request audio', ais_audio_file)
   ais_audio_name = ais_audio_file.filename.split('.')[0] + str(time.time()) + '.wav'
   print('ais_audio_name ', ais_audio_name)
   file_path = './audio/{}'.format(ais_audio_name)
   print('file_path ', file_path)
   ais_audio_file.save(file_path)
   
  
   #ais_img=request.form.get('AIS_IMG', default='./ais_repo/ais1.png', type=str)
   brand=request.form.get('BRAND', type=str)
   item=request.form.get('ITEM', type=str)
   req_no=randint(1, 1001) 
   #ais_img = './ais_repo/{}'.format(ais_img.split('\\')[-1])
   #response_text = process_pipeline(file_path, brand, item)
   #resp = make_response(json.dumps(response_text))

   path_models = os.getcwd()+"/models/models/"
   path_audio = os.getcwd()+"/audio/"
   print(path_models)
   #out, err = p.communicate()
   out = subprocess.check_output(["deepspeech", "{}output_graph.pb".format(path_models), "{}{}".format(path_audio, ais_audio_name), "{}alphabet.txt".format(path_models)])
   print("Output of the subprocess is ***********")
   print(str(out))
   resp = make_response(json.dumps(str(out)[2:-3]))
   resp.headers['Access-Control-Allow-Origin'] = '*'
   return resp


if __name__ == '__main__':
  app.run(host='0.0.0.0')
