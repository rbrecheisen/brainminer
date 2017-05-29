from brainminer.base.api import HtmlResource


class IndexResource(HtmlResource):

    URI = '/'

    def get(self):

        html = ''
        html += '<form method="get" action="/classifiers">'
        html += '  <input type=submit value="Get started">'
        html += '</form>'

        return self.output_html(html, 200)
