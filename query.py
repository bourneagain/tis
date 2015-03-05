import httplib
import pprint
import requests
import json
def search(search_term):
	query = {
         "match": {
           "body": {
             "query": "what do you think is the best handling car"
          } }}
	# es_query = json.dumps(query)
	uri = 'http://localhost:9200/srajend2_index/doc/_search?size=200'
	r = requests.get(uri, params=query)
	results = json.loads( r.text )
	pprint.pprint(len(results['hits']['hits']))
    # data = [res['_source']['api_id'] for res in results['hits']['hits'] ]
    # print "results: %d" % len(data)
    # pprint(data)
search("think")