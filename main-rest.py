import web

from smart_client_python import oauth
from smart_client_python import smart
from smart_client_python.common import util as smart_util
from xml.etree import ElementTree
import urllib

urls = (
  '/smartapp/index.html', 'index',
  '/smartapp/bootstrap.html', 'bootstrap'
)

app = web.application(urls, globals())

class bootstrap:
  def GET(self):
    return """<!DOCTYPE html>
                       <html>
                        <head>
                         <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-client.js"></script>
                        </head>
                        <body></body>
                       </html>"""
    
class index:
  def GET(self):
    # get the SMArt cookie name
    cookie_name = web.input().cookie_name

    # extract the cookie and parse it as an oAuth authorization header
    smart_connect_cookie = urllib.unquote(web.cookies().get(cookie_name))
    oauth_params = oauth.parse_header(smart_connect_cookie)

    # extract the parameters needed
    record_id = oauth_params['smart_record_id']
    resource_credentials = {'oauth_token' : oauth_params['smart_oauth_token'],
                            'oauth_token_secret' : oauth_params['smart_oauth_token_secret']}

    # instantiate the smart client
    smart_client = smart.SmartClient(
      'my-app@apps.smartplatforms.org',
      {'api_base' : 'http://sandbox-api.smartplatforms.org'},
      {'consumer_key' : 'my-app@apps.smartplatforms.org',
       'consumer_secret' : 'smartapp-secret'},
      resource_credentials)

    # get the meds
    query = """
        PREFIX dcterms:<http://purl.org/dc/terms/>
        PREFIX sp:<http://smartplatforms.org/terms#>
        PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT  ?drugname ?rxcui
        WHERE {
           ?med rdf:type sp:Medication .
           ?med sp:drugName ?drugname_code .
           ?drugname_code dcterms:title ?drugname .
           ?drugname_code sp:code ?rxcui_url .
           ?rxcui_url dcterms:identifier ?rxcui .
        }
        """

    medications = smart_client.records_X_medications_GET(record_id = record_id)

    med_names_and_cuis = medications.query(query)
    meds = [{'name': med[0], 'rxcui': med[1]} for med in med_names_and_cuis]

    # go through the meds and get the FDA Unique Identifier Code
    for med in meds:
      rxnav_info_xml = urllib.urlopen("http://rxnav.nlm.nih.gov/REST/rxcui/%s/related?rela=has_ingredient" % med['rxcui']).read()
      info = ElementTree.fromstring(rxnav_info_xml)
      med['ingredients'] = [ing.text for ing in info.findall('relatedGroup/conceptGroup/conceptProperties/name')]

    med_names_html = "\n".join(["<li>%s<br /><small>ingredients: %s</small><br /><br /></li>" % (str(med['name']), ", ".join(med['ingredients'])) for med in meds])
    
    return """<!DOCTYPE html>
                       <html>
                        <head>
                         <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-page.js"></script>
                        </head>
                        <body><h1>Hello <span id="name"></span></h1>
                        <script>
                        document.getElementById('name').innerHTML = SMART.record.full_name;
                        </script>
                        <ul>
                        %s
                        </ul>
                        </body>
                       </html>""" % med_names_html


def get_smart_client(request):
  pass
    
if __name__ == '__main__':
  app.run()
