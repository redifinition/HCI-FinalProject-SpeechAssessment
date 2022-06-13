#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
import json

from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
import tarfile
from datetime import datetime
from scipy import ndimage
#from scipy.misc import imsave
from flask_cors import *  # 注意这一行-01

from algorithm.speechAssessment import single_speech_assessment

UPLOAD_FOLDER = 'audioFile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
from tensorflow.python.platform import gfile
app = Flask(__name__, static_folder="static",template_folder="templates",static_url_path="/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

CORS(app, supports_credentials=True)  # 注意这一行-02

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================


#==============================================================================================================================
#                                                                                                                              
#  This function is used to do speech assessment scoring
#                                                                                                                              
#==============================================================================================================================
@app.route('/audioQuality', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_audio_quality():
    # 获取通过url请求传参的数据
    # 算法
    algorithms = request.form.to_dict()
    audio_file = request.files.to_dict()
    audio = audio_file['audioFile']
    result = {}
    if audio:  # and allowed_file(file.filename):
        filename = secure_filename(audio.filename)
        filename += '.wav'
        audio.save('../algorithm/'+filename)
        inputloc = '../algorithm/'+filename
        for algorithm in algorithms.get('algorithms').split(','):
            result[algorithm] = single_speech_assessment(inputloc,algorithm)[algorithm].tolist()
        print(result)
    return jsonify(result)
#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    return render_template("main.html")   
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
