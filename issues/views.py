from django.shortcuts import render_to_response,render
from django.http import HttpResponse
from django.template.context import RequestContext
import requests
import json
from datetime import datetime, timedelta
from django.utils.datetime_safe import strftime
from django.utils.lorem_ipsum import paragraph


def getallissues(request):
    val = requests.get('https://api.github.com/search/issues?q=state=open&per_page=100&sort=created&dir=asc')
    print val
    print dir(val)
    print type(val)
    json_data = json.loads(val.text);
    print json_data["total_count"]
    print dir(json_data["items"])
    return render(request, 'getallissues.html', {'data': json_data["items"]})

def get_issues_in_last_24hrs(request,page_id):
    yesterday = datetime.now() - timedelta(days=1)
    page_id = int(page_id)
    
    if page_id>10 or page_id<1:
        return render(request, 'getallissues.html', {'data': "" ,"page_id":"", "invalid":True})
        val = requests.get('https://api.github.com/search/issues?q=state:open+created:>='+yesterday.isoformat()+'&per_page=100&order=asc&page='+str(page_id))
    
    json_data = json.loads(val.text);
    return render(request, 'getallissues.html', {'data': json_data["items"] ,"page_id":page_id,"count":json_data["total_count"],"invalid":False})

def home(request):
#     get all open issues
    all_issues = requests.get('https://api.github.com/search/issues?q=state=open&per_page=100&sort=created&dir=asc')
    all_issues_json = json.loads(all_issues.text)
#     get open issues in last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_response = requests.get('https://api.github.com/search/issues?q=state:open+created:>='+yesterday.isoformat()+'&per_page=100&order=asc')
    json_data = json.loads(yesterday_response.text);
#     Number of open issues that were opened more than 7 days ago
    week = datetime.now() - timedelta(days=7)
    week_response = requests.get('https://api.github.com/search/issues?q=state:open+created:"'+week.isoformat()+' .. '+yesterday.isoformat()+'"&per_page=100&order=asc')
    week_data = json.loads(week_response.text);
#   Number of open issues that were opened more than 24 hours ago but less than 7 days ago 
    inbetween_response = requests.get('https://api.github.com/search/issues?q=state:open+created:<='+week.isoformat()+'&per_page=100&order=asc')
    more_than_week_data = json.loads(inbetween_response.text);
    return render(request, 'home.html',{"yesterday_count":json_data["total_count"],"btw_yesterday_and_week":week_data["total_count"],"more_than_week_data":more_than_week_data["total_count"],"all_issues":all_issues_json["total_count"]})