import requests
from datetime import datetime, timedelta
import os

filename = "zonas.txt" 
with open(filename) as obj:  
    for i in obj: 
        cf_date = datetime.today().strftime('%Y-%m-%d')
        cf_from_time = datetime.today().strftime('%H:%M:%S')
        cf_to_time = datetime.today().strftime('%H:%M:%S')

        start = datetime.today()
        end = datetime.today().strftime("%Y-%m-%dT%H:%M:%SZ") 

        url  = 'https://api.cloudflare.com/client/v4/zones/%s' % i

        x_auth_email = "<EMAIL>"
        x_auth_key = "<API-KEY>"

        headers = {
        'X-Auth-Email': x_auth_email,
        'X-Auth-Key': x_auth_key,
        'Content-Type': 'application/json'
        }

        past_date_before_5minutes = start - timedelta(minutes = 5)
        past_date_before_5minutes = past_date_before_5minutes.strftime("%Y-%m-%dT%H:%M:%SZ")

        params = (
        ('start', past_date_before_5minutes),
        ('end', end),
        ('fields', 'FirewallMatchesActions,FirewallMatchesSources,RayID,ClientDeviceType,EdgeRateLimitID,WAFRuleMessage,WAFRuleID,EdgeRateLimitAction,WAFAction,EdgePathingStatus,EdgePathingOp,EdgePathingSrc,CacheCacheStatus,ClientRequestHost,ClientRequestURI,CacheResponseStatus,EdgeResponseStatus,OriginResponseStatus,EdgeStartTimestamp,ClientIP,ClientRequestBytes,CacheResponseBytes,EdgeResponseBytes,ClientRequestMethod,ZoneID,ClientRequestProtocol,ClientRequestUserAgent,WorkerSubrequest'),
        )

        response = requests.get(url + '/logs/received', params=params, headers=headers).text
        payload = i.strip()
        try: 
            os.makedirs(payload,exist_ok=True) 
        except OSError as error: 
            print(error) 
        
        writeFile = open('{}/{}.json'.format(payload,cf_date), 'w')
        writeFile.write(response)
        writeFile.close()
        
        


