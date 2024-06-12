# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import json
import urllib.request

client_id = "pt4OvN2fzzLJgFJxIaQf"
client_secret = "deXXmDzy6w"

def get_news(keyword):
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(response_body.decode('utf-8'))
        return response_json["items"]
    else:
        print("Error Code:" + rescode)
        return False
    

def get_blog(keyword):
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/blog.json?query=" + encText # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_json = json.loads(response_body.decode('utf-8'))
        return response_json["items"]
    else:
        print("Error Code:" + rescode)
        return False