from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from django.template.context import RequestContext
import requests
import json
from datetime import datetime, timedelta
from django.utils.datetime_safe import strftime
from django.utils.lorem_ipsum import paragraph


def getallissues(request):
    val = requests.get('https://api.github.com/search/issues?q=state=closed&per_page=100&sort=created&dir=asc', headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    print val
    print dir(val)
    print type(val)
    json_data = json.loads(val.text);
    print json_data["total_count"]
    print dir(json_data["items"])
    return render(request, 'getallissues.html', {'data': json_data["items"]})

def get_issues_in_last_24hrs(request,page_id):
    yesterday = datetime.now() - timedelta(days=1)
    print yesterday.isoformat()
    print int(page_id)
    page_id = int(page_id)
    print page_id>10
    
    if page_id>10 or page_id<1:
        print "hello"
        return render(request, 'getallissues.html', {'data': "" ,"page_id":"", "invalid":True})
    
#     val = requests.get('https://api.github.com/search/issues?q=state:closed&since=2015-12-30T22:52:57Z&sort=created&per_page=100&order=desc&page=1', headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    val = requests.get('https://api.github.com/search/issues?q=state:open+created:>='+yesterday.isoformat()+'&per_page=100&order=asc&page='+str(page_id), headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    print val
    json_data = json.loads(val.text);
    print json_data["total_count"]
    print len(json_data["items"])
    return render(request, 'getallissues.html', {'data': json_data["items"] ,"page_id":page_id,"count":json_data["total_count"],"invalid":False})

def home(request):
    yesterday = datetime.now() - timedelta(days=1)
    val = requests.get('https://api.github.com/search/issues?q=state:open+created:>='+yesterday.isoformat()+'&per_page=100&order=asc', headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    json_data = json.loads(val.text);
    week = datetime.now() - timedelta(days=7)
    val = requests.get('https://api.github.com/search/issues?q=state:open+created:"'+week.isoformat()+' .. '+yesterday.isoformat()+'"&per_page=100&order=asc', headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    week_data = json.loads(val.text);
    yesterday = datetime.now() - timedelta(days=1)
    val = requests.get('https://api.github.com/search/issues?q=state:open+created:<='+week.isoformat()+'&per_page=100&order=asc', headers={'Authorization': 'token 6947404bbe7514aa274d0e73cb1600cfb72b232b'})
    more_than_week_data = json.loads(val.text);
    return render(request, 'home.html',{"yesterday_count":json_data["total_count"],"btw_yesterday_and_week":week_data["total_count"],"more_than_week_data":more_than_week_data["total_count"]})