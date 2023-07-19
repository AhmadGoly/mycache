from flask import Flask, jsonify
from flask_cors import CORS
from kafka import KafkaConsumer
import re
import threading
import datetime
import json
import pandas as pd
app = Flask(__name__)
CORS(app)

#Goly Edits:
kafkaPort = 19092
bootstrap_servers = [f'127.0.0.1:{kafkaPort}']
topicName = 'gaam5'
consumer = KafkaConsumer(topicName, bootstrap_servers = bootstrap_servers, auto_offset_reset = 'latest')
def current_time():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("[%Y-%m-%d_%H:%M:%S]")
#End of Goly Edits.

dic_hashtag_count = {}
sorted_list = []
message_last = ''

list_10_score = []
avg_score = 0


def moving_average(nums, new_num):
    if len(nums) < 10:
        nums.append(new_num)
    else:
        nums.pop(0)
        nums.append(new_num)
    return sum(nums) / len(nums)


def read_messages(consumer):
    global sorted_list
    global message_last
    global avg_score

    for message in consumer:
        #Goly Edits:
        print(f'{current_time()}: Received a msg from Preprocessing. Showing data using flask...')
        json_row = message.value.decode('utf-8')
        x = json.loads(json_row)
        receivedRowDF = pd.DataFrame([x])
        for _, row in receivedRowDF.iterrows():
            message_str = '**'.join(str(value) for value in row)
        #End of Goly Edits.
        message_str = message_str.split('**')
        message_f = re.sub(r'[\[\]#\'\']', '', message_str[2]).replace(" ", "").split(',')
        if message_f[0] != '':
            for word in message_f:
                if word in dic_hashtag_count:
                    dic_hashtag_count[word] += 1
                else:
                    dic_hashtag_count[word] = 1
        
        sorted_list = sorted(dic_hashtag_count.items(), key=lambda x: x[1],  reverse=True)
        message_last = message_str[1]
        
        avg_score = moving_average(list_10_score, float(message_str[6]))
        #print(list_10_score, '\t' , avg_score)


thread = threading.Thread(target=read_messages, args=(consumer,))
thread.start()


@app.route('/inf')
def get_data():
    return jsonify(sorted_list,message_last,avg_score)


if __name__ == '__main__':
    app.run()

