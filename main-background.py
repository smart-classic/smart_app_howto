from smart_client_python import oauth
from smart_client_python import smart
from smart_client_python.common import util as smart_util
from xml.etree import ElementTree
import urllib

def get_smart_client(resource_tokens=None):
  # instantiate the smart client
  smart_client = smart.SmartClient(
    'smart-background-app@apps.smartplatforms.org',
    {'api_base' : 'http://sandbox-api.smartplatforms.org'},
    {'consumer_key' : 'smart-background-app@apps.smartplatforms.org',
     'consumer_secret' : 'smartapp-secret'},
    resource_tokens)

  return smart_client

def print_drugnames():
  """
  map a function onto every record
  """
  smart_client = get_smart_client()

  for record_id in smart_client.loop_over_records():
    query = """
        PREFIX dcterms:<http://purl.org/dc/terms/>
        PREFIX sp:<http://smartplatforms.org/terms#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT  ?drugname
        WHERE {
           ?med rdf:type sp:Medication .
           ?med sp:drugName ?drugname_code .
           ?drugname_code dcterms:title ?drugname .
        }
        """

    medications = smart_client.records_X_medications_GET(record_id = record_id)
    med_names = medications.query(query)
    print "%s: %s" % (record_id, med_names)

def run():
  print_drugnames()

if __name__ == '__main__':
  run()
