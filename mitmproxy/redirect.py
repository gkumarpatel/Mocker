from mitmproxy import http
import datetime
import re

def request(flow):
	print("inside request(flow) : " + str(datetime.datetime.now())+ "\n")
	print("original Request : " + str(flow.request)+"\n")
	if flow.request.pretty_host.endswith("webcopas00.ver.sul.t-online.de"):
		#flow.request.host = "moquer.centralindia.cloudapp.azure.com"
		flow.request.host = "moquer"
		flow.request.scheme = "http"
		flow.request.port = 8080
		flow.request.path = re.sub(r"billing",r"moquer/mockbillingBinding",flow.request.path)
		print("manipulated Request : " + str(flow.request)+"\n")
def response(flow):
	print("inside response(flow) : " + str(datetime.datetime.now())+ "\n")
	print("Response : " + str(flow.response)+"\n")
	
def clientconnect(root_layer):
	print("inside clientconnect : " + str(datetime.datetime.now())+ "\n")

def clientdisconnect(root_layer):
	print("inside clientdisconnect : " + str(datetime.datetime.now())+ "\n")

def serverconnect(server_conn):
	print("inside serverconnect : " + str(datetime.datetime.now())+ "\n")

def serverdisconnect(server_conn):
	print("inside server disconnect : " + str(datetime.datetime.now())+ "\n")
