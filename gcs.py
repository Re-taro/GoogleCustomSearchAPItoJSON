#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
import json

from time import sleep
from googleapiclient import discovery

Google_API_KEY = "Google_API_key"
CSE_ID = "Custom_Search_ID"

DATA_DIR = 'data'
def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def getSearchResponse(keyword):
    today = datetime.datetime.today().strftime("%Y%m%d")
    timestamp = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
    
    makeDir(DATA_DIR)
    
    service = discovery.build("customsearch","v1",developerKey=Google_API_KEY)
    
    page_limit =10
    start_index =1
    response = []
    for n_page in range(0,page_limit):
        try:
            sleep(1)
            response.append(service.cse().list(
                q = keyword,
                cx = CSE_ID,
                lr = 'lang_ja',
                num = 10,
                start = start_index
            ).execute())
            start_index = response[n_page].get("queries").get("nextpage")[0].get("startIndex")
        except Exception as e:
            print(e)
            break
    
    
    save_response_dir = os.path.join(DATA_DIR,"response")
    makeDir(save_response_dir)
    out = {'snapshot_itkw':today,'snapshot_timestamp':timestamp,'response':[]}
    out['response'] = response
    jsonstr = json.dumps(out,ensure_ascii=False)
    with open(os.path.join(save_response_dir,'response_'+today+'.json'),mode='w') as response_file:
        response_file.write(jsonstr)
    
if __name__ == '__main__':
    target_keyword = '高専はクソだと言うことです' #ここに検索したい単語を入れましょう
    
    getSearchResponse(target_keyword)