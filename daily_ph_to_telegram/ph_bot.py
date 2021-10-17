import pandas as pd
import requests
import urllib.parse
import os
import re
import math
import pandas as pd
from datetime import datetime

#get the data
ph_data = pd.ExcelFile('ph_data.xlsx')
df = ph_data.parse('ph_data')

counter_file = pd.read_csv("counter_file.csv")
counter = counter_file.iloc[0]['counter']

hebcal = pd.read_csv("hebcal.csv")['Start_Date']


#get keys
api_key = ws.environment['ph_key']
chat_id = ws.environment['chat_id']

if (datetime.today().strftime('%A') != 'Saturday') and (datetime.today().strftime('%d-%m-%Y') not in hebcal):
    
    # ph daily data:
    content = urllib.parse.quote_plus(df.iloc[counter]['content'])
    breadcrumbs = urllib.parse.quote_plus(df.iloc[counter]['breadcrumbs'])

    #find the spaces for the ~4000 chars limit
    spaces = pd.Series([m.start() for m in re.finditer(r"\+", content)])
    string_chunks = math.ceil(len(content)/4000) #chunks of ~4000 chars
    last_limit = 0 #lower limit of chunks (will change)

    requests.get("https://api.telegram.org/bot"+api_key+"/sendMessage?chat_id="+chat_id+"&text="+breadcrumbs)
    for i in range(1,string_chunks+1):
        msg_positions = spaces[spaces.between(last_limit,4000*i)]
        msg_chunks = [min(msg_positions),max(msg_positions)]
        send_msg = content[min(msg_positions):max(msg_positions)]
        requests.get("https://api.telegram.org/bot"+api_key+"/sendMessage?chat_id="+chat_id+"&text="+send_msg)
        last_limit = max(msg_positions)

    #update the counter file:
    counter_file.iloc[0]['counter'] = counter + 1
    counter_file.to_csv("counter_file.csv",index=False)
