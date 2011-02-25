import web

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
    return """<!DOCTYPE html>
                       <html>
                        <head>
                         <script src="http://sample-apps.smartplatforms.org/framework/smart/scripts/smart-api-page.js"></script>
                        </head>
                        <body><h1>Hello <span id="name"></span></h1>
                        
                        <ul id="med_list">
                        </ul>
                        
                        <script>
                        document.getElementById('name').innerHTML = SMART.record.full_name;
                        SMART.MEDS_get(function(meds) {
                          var med_names = meds.where("?medication rdf:type sp:Medication")
                            .where("?medication sp:drugName ?drug_name_code")
                            .where("?drug_name_code dcterms:title ?drugname");
                            
                          var med_list = document.getElementById('med_list');
                          med_names.each(function(i, single_med) {
                            med_list.innerHTML += "<li> " + single_med.drugname + "</li>";
                          });
                        });
                        </script>
                        </body>
                       </html>"""
    
if __name__ == '__main__':
  app.run()