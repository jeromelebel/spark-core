#!/usr/bin/python

import argparse
import pprint
import httplib
import urllib2
import urllib
import base64
import json
import os

proxy = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8888'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

class RequestWithMethod(urllib2.Request):
  def __init__(self, *args, **kwargs):
    self._method = kwargs.pop('method', None)
    urllib2.Request.__init__(self, *args, **kwargs)

  def get_method(self):
    return self._method

sparkcore_token_file = os.path.expanduser("~/.sparkcore_token")
default_token = None
if os.path.isfile(sparkcore_token_file):
  try:
    with open(sparkcore_token_file, 'r') as the_file:
      default_token = json.loads(the_file.read())["access_token"]
  except:
    pass

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help = "User name", type = str)
parser.add_argument("-p", "--password", help = "Password", type = str)
parser.add_argument("-s", "--sparkcore", help = "Spark Core Name", type = str)
parser.add_argument("-t", "--token", help = "Token", type = str, default = default_token)
parser.add_argument("action", help = "Action", choices = [ "execute", "tokenlist", "newtoken", "deletetoken", "devicelist", "execute" ], type = str)
parser.add_argument("parameters", help = "Function name", nargs = "*", type = str)

args = parser.parse_args()
if args.action:
  print args.action

if args.action == "tokenlist":
  if not args.user:
    parser.error("argument -u/--user is required")
    exit(2)
  if not args.password:
    parser.error("argument -p/--password is required")
    exit(2)
  request = urllib2.Request("https://api.spark.io/v1/access_tokens")
  request.add_header("Authorization", "Basic " + base64.b64encode(args.user + ":" + args.password))
  try:
    result = urllib2.urlopen(request)
  except urllib2.URLError as e:
    print(str(e.code) + " " + e.reason)
  else:
    tokens = json.loads(result.read())
    for token in tokens:
      print(token["token"] + ", " + token["client"] + ", " + token["expires_at"])

elif args.action == "devicelist":
  if not args.token:
    parser.error("argument -t/--token is required")
    exit(2)
  request = urllib2.Request("https://api.spark.io/v1/devices?access_token=" + args.token)
  try:
    result = urllib2.urlopen(request)
  except urllib2.URLError as e:
    print(str(e.code) + " " + e.reason)
  else:
    devices = json.loads(result.read())
    for device in devices:
      try:
        print(str(device["name"]))
        print("  id: " + str(device["id"]))
        print("  last app: " + str(device["last_app"]))
        print("  last heard: " + str(device["last_heard"]))
        print("  connected: " + str(device["connected"]))
      except:
        pprint.pprint(device)
      
elif args.action == "execute":
  if not args.token:
    parser.error("argument -t/--token is required")
    exit(2)
  if not args.parameters:
    parser.error("needs the device and the function to execute")
    exit(2)
  if len(args.parameters) < 1:
    parser.error("needs the device and the function to execute")
    exit(2)
  if len(args.parameters) < 2:
    parser.error("needs the function to execute")
    exit(2)
  request = urllib2.Request("https://api.spark.io/v1/devices/" + args.parameters[0] + "/" + args.parameters[1])
  try:
    params = { "access_token": args.token }
    if len(args.parameters) == 3:
      params[args] = args.parameters[2]
    result = urllib2.urlopen(request, urllib.urlencode(params))
  except urllib2.URLError as e:
    print(str(e.code) + " " + e.reason)
  else:
    data = result.read()
    token = json.loads(data)
    pprint.pprint(token)
      
elif args.action == "newtoken":
  if not args.user:
    parser.error("argument -u/--user is required")
    exit(2)
  if not args.password:
    parser.error("argument -p/--password is required")
    exit(2)
  request = urllib2.Request("https://api.spark.io/oauth/token")
  request.add_header("Authorization", "Basic " + base64.b64encode("python:python"))
  try:
    params = { "grant_type": "password", "username": args.user, "password" : args.password }
    result = urllib2.urlopen(request, urllib.urlencode(params))
  except urllib2.URLError as e:
    print(str(e.code) + " " + e.reason)
  else:
    data = result.read()
    token = json.loads(data)
    pprint.pprint(token)
    with open(sparkcore_token_file, 'w+') as the_file:
      the_file.write(data)
    
elif args.action == "deletetoken":
  if not args.user:
    parser.error("argument -u/--user is required")
    exit(2)
  if not args.password:
    parser.error("argument -p/--password is required")
    exit(2)
  if not args.token:
    parser.error("argument -t/--token is required")
    exit(2)
  request = RequestWithMethod("https://api.spark.io/v1/access_tokens/" + args.token, method = "DELETE")
  request.add_header("Authorization", "Basic " + base64.b64encode(args.user + ":" + args.password))
  try:
    result = urllib2.urlopen(request)
  except urllib2.URLError as e:
    print(str(e.code) + " " + e.reason)
  else:
    tokens = json.loads(result.read())
    pprint.pprint(tokens)
else:
  parser.print_help()
