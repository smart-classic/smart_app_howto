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
                        %s
                        </body>
                       </html>"""
    
if __name__ == '__main__':
  app.run()