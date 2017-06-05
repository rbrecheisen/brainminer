from brainminer.base.api import HtmlResource


class IndexResource(HtmlResource):

    URI = '/'

    def get(self):

        html = ''
        html += '<h3>Welcome to BrainMiner!</h3>'
        html += '<p>This web application allows you to upload known examples to train<br>'
        html += 'your classifier of choice and then run predictions using the trained<br>'
        html += 'classifier.</p>'
        html += '<p>Click the button below to get started.</p>'
        html += '<form method="get" action="/classifiers">'
        html += '  <input type=submit value="Get started">'
        html += '</form>'

        return self.output_html(html, 200)
