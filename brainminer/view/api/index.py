from brainminer.base.api import HtmlResource


# ----------------------------------------------------------------------------------------------------------------------
class IndexResource(HtmlResource):
    
    URI = '/'
    
    def get(self):
        
        # import subprocess
        # subprocess.call('Rscript Rscripts/test.R', shell=True)
        
        html = '<h3>Welcome!</h3>'
        html += '<p>This page allows you to train a classifier and run predictions with it</p>'
        html += '<p>Press the button below to get started and select a classifier.</p>'
        html += '<br>'
        html += '<form method="get" action="/classifiers">'
        html += '  <input type=submit value="Get started">'
        html += '</form>'
        
        return self.output_html(html, 200)
