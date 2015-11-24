import json
import requests

FUSION_QUERY_URL = "https://www.googleapis.com/fusiontables/v2/query"
FUSION_TABLE_ID = "16I6HWZd8PrvjlzvcKsCWShHii8RaMA_vux8sTQPI"
API_KEY = "AIzaSyDDYAfEQUBkHy6_0ysfwIRe6PucjpVoVFE"
FIELDS = ['id','name','country','sitename','latitude','longitude','collector','collectiondate','CS_number','pilot_projects','Nordborg2005','Nordborg2012','Cao2011','Schmitz2013','Long2013','1001genomes','seq_by']

def search(arg):
    where = _get_where_from_params(arg)
    where = 'WHERE %s' % 'AND'.join(where) if len(where) > 0 else ''
    order_by = 'ORDER BY %s' % arg['ORDERBY'] if 'ORDERBY' in arg else ''
    offset = 'OFFSET %s' % arg['OFFSET'] if 'OFFSET' in arg else ''
    limit = 'LIMIT %s' % arg['LIMIT'] if 'LIMIT' in arg else ''
    query = "SELECT %s FROM %s %s %s %s %s" % (','.join(FIELDS), FUSION_TABLE_ID, where,order_by,offset,limit)
    payload = {'sql':query,'key':API_KEY}
    ret = requests.get(FUSION_QUERY_URL, params=payload)
    if ret.ok:
        print json.dumps(ret.json())
        print '---'
    else:
        raise Exception(ret.text + query)

def list(arg):
    for key in ('ORDERBY','LIMIT','OFFSET'):
        _flatten_param(arg,key)    
    search(arg)

def _flatten_param(arg,key):
    if key in arg and len(arg[key]) > 0:
        arg[key] = arg[key][0]

def _get_where_from_params(args):
    filtered = []
    for arg,value in args.iteritems():
        if arg in FIELDS:
            filtered.append("'%s' = '%s'" % (arg,value))
    return filtered 
