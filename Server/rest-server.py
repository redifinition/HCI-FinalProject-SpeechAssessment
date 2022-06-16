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
from algorithm.speechAssessment import denoise

UPLOAD_FOLDER = 'audioFile'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
from tensorflow.python.platform import gfile
app = Flask(__name__, static_folder="static",template_folder="templates",static_url_path="/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

CORS(app, supports_credentials=True)  # 注意这一行-02
ALGORITHM_INFO = {"mosnet":"absolute",
                  "srmr":"absolute",
                  "bsseval":"relative",
                  "pesq":"relative",
                  "sisdr":"relative",
                  "stoi":"relative"}
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
    import moviepy.editor as moviepy
    import time
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
        flag = 0
        for algorithm in algorithms.get('algorithms').split(','):
            info= {}
            # 计算运行时间
            print(algorithm)
            if algorithm == "bsseval":
                if flag == 0:
                    result_info = single_speech_assessment(inputloc,algorithm,True)
                    score_list = result_info['score']
                else:
                    result_info = single_speech_assessment(inputloc,algorithm,False)
                    score_list = result['score']
                score_list['isr'] = score_list['isr'].tolist()[0]
                score_list['sar'] = score_list['sar'].tolist()[0]
                score_list['sdr'] = score_list['sdr'].tolist()[0]
                time_num = result_info['time']
            elif flag == 0:
                result_info = single_speech_assessment(inputloc,algorithm,True)
                score_list = result_info['score'][algorithm].tolist()
                time_num = result_info['time']
            else:
                result_info = single_speech_assessment(inputloc, algorithm,False)
                score_list = result_info['score'][algorithm].tolist()
                time_num = result_info['time']
            info["score"] = score_list
            avg_score = 0
            if algorithm == "bsseval":
                avg_score = {}
                avg_score['isr'] = get_avg(score_list['isr'])
                avg_score['sar'] = get_avg(score_list['sar'])
                avg_score['sdr']  = get_avg(score_list['sdr'])

            else:
                avg_score = get_avg(score_list)
            info["time"] = time_num
            info["avgScore"] = avg_score
            result[algorithm] = info
            if ALGORITHM_INFO[algorithm] == 'relative':
                flag = 1
        print('dwdd{}'.format(result))
    return jsonify(result)


def get_avg(score_list):
    sum = 0
    for item in score_list:
        sum += item
    return sum/len(score_list)

#==============================================================================================================================
#
#  This function is used to do Audio Noise Reduction
#
#==============================================================================================================================
@app.route('/audioDenoising', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_audio_denoising():
    # 获取通过url请求传参的数据
    # 算法
    audio_file = request.files.to_dict()
    audio = audio_file['audioFile']
    filename = secure_filename(audio.filename)
    filename += '.wav'
    audio.save('../algorithm/' + filename)
    inputloc = '../algorithm/' + filename
    result = denoise(inputloc)
    return result.url




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
