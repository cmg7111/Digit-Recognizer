# -*- coding: utf-8 -*- 
import tensorflow as tf
import matplotlib.pyplot as plts
import numpy as np
from PIL import Image
import sys
import os
import json
#
#
#
X = tf.placeholder(tf.float32, [None, 128, 128, 1])
Y = tf.placeholder(tf.int32, [None])
L1 = tf.layers.conv2d(X, 32, [3, 3], (2, 2), activation=tf.nn.relu)
L1 = tf.layers.max_pooling2d(L1, [2, 2], [2, 2])
L1 = tf.layers.dropout(L1, 0.7)
L2 = tf.layers.conv2d(L1, 64, [3, 3], (2, 2), activation=tf.nn.relu)
L2 = tf.layers.max_pooling2d(L2, [2, 2], [2, 2])
L2 = tf.layers.dropout(L2, 0.7)
L3 = tf.contrib.layers.flatten(L2)
L3 = tf.layers.dense(L3, 256, activation=tf.nn.relu)
L3 = tf.layers.dropout(L3, 0.5)
model = tf.layers.dense(L3, 10, activation=tf.nn.softmax)
cost = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=model, labels=Y))
optimizer = tf.train.AdamOptimizer(0.001).minimize(cost)

saver = tf.train.Saver()
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
checkpoint = tf.train.latest_checkpoint('trained_model') 
if checkpoint:
    saver.restore(sess, checkpoint)
#
#
#
def predict_image(image_dir):
    test_img = np.zeros((1,16384))
    test_img[0] = np.invert(Image.open(image_dir).convert('L')).ravel()  
    test_img = np.reshape(test_img,(-1,128,128,1))
    prediction = sess.run(model, feed_dict={X: test_img})
    predicted_digit = np.argmax(prediction[0]) 
    confidence = prediction[0]		     
    #print('Prediction: ' + str(predicted_digit))    
    confidence.sort()
    #print(confidence[9])

    #result['pre_list'].append(str(predicted_digit))
    #result['conf_list'].append(str(confidence[9]))
    result[0].append(predicted_digit)
    result[1].append(confidence[9])
    

directory='numimg_conv'

#result={'pre_list':[],'conf_list':[]}
result=[[],[],[]]
pre_list=[]
conf_list=[]

for cnt in range(0,(len(next(os.walk(directory))[2]))):
    filename=directory+"/crop_"+str(cnt)+".jpg"
    predict_image(filename)

result[2].append(cnt)

print(result)
#json.dumps(result)


