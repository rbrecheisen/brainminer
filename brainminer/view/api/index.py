from brainminer.base.api import HtmlResource


# ----------------------------------------------------------------------------------------------------------------------
class IndexResource(HtmlResource):
    
    URI = '/'
    
    def get(self):
        return self.output_html('''
            <h3>Step 1 - Create classifier</h3>
            <p>First create a new classifier (defaults to SVM)</p>
            <form method="post" action="/classifiers">
                <input type=submit value="Create classifier"></p>
            </form>
            ''', 200)
