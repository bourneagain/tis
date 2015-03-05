from elasticsearch import Elasticsearch
import time
import pprint
import sys
import subprocess
import os
JSON_FILE="/Users/sam/cs410/TEAM_BHP_DATA_TOPARSE/srajend2.json"
INDEX_NAME="srajend2_index"
APPEND_FILE="/Users/sam/cs410/TEAM_BHP_DATA_TOPARSE/SCRIPTS/append_create_line.sh"
es=Elasticsearch()

def main():
	
	delete_index(INDEX_NAME)
	create_index(INDEX_NAME)
	# pprint.pprint(es.indices.stats())
	# split_file_into_chunks(JSON_FILE)
	load_bulk_data_in_chunks()

def delete_index(_index):
	global es
	print es.indices.delete(index=_index, ignore=[400, 404])

def create_index(_index):
	global es
	print es.indices.create(index=_index, ignore=400)

def listFiles(dirpath):
	filenames = next(os.walk(dirpath))[2]
	yield filenames


def checkass(file_name):
	cmd=['/bin/bash',APPEND_FILE,file_name,INDEX_NAME]
	# res = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
	# res.communicate()
	try:
		print "CAALING FUCK"
		subprocess.check_call(cmd)
	except subprocess.CalledProcessError:
		print "ERROR!"

def curljson(fil):
	checkass(fil)
	# res = es.bulk(index="srajend2_index", body = fil, refresh = True, request_timeout=100)
	start_time = time.time()
	PWD = os.getcwd()
	cmd = ['curl','-s','-XPOST','localhost:9200/_bulk','--data-binary','@'+str(fil)]
	print cmd
	# process = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	try:
		res = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
		res.communicate()
	except subprocess.CalledProcessError:
		print "ERROR"
	elp_time=time.time() - start_time
	return elp_time



def load_bulk_data_in_chunks():
	i=2
	iterList=[]
	outfile=open('choot.csv',"w")
	while i < 257:
		iterList.append(i)
		i=i*2
	for chunk in iterList:
		print "********* CHUNK ",chunk ," *******************"
		PWD = os.getcwd()
		timeelp=0
		for jsons in listFiles("/tmp/JUNKS_"+str(chunk)):
			delete_index(INDEX_NAME)
			create_index(INDEX_NAME)
			p = "/tmp/JUNKS_"+str(chunk)
			os.chdir(p)
			for json in jsons:
				timeelp+=curljson(json)
		linechoot="TABLE,"+str(chunk)+","+str(timeelp)+"\n"
		outfile.write(linechoot)
		os.chdir(PWD)

			
def split_file_into_chunks(json_file):
	cmd = ['/bin/sh','splitJunks.sh',json_file]
	print cmd
	#process = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	try:
		subprocess.check_call(cmd)
	except subprocess.CalledProcessError:
		print "ERROR!"
	
	print "*** DONE saved in /tmp/JUNKS* *** "


if __name__ == "__main__":
    main()

#collect the chunks
# split_file_into_chunks(JSON_FILE)


