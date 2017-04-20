from brainminer.base.api import HtmlResource


# ----------------------------------------------------------------------------------------------------------------------
class IndexResource(HtmlResource):
    
    URI = '/'
    
    def get(self):
        return self.output_html('''
            <h3>Upload file</h3>
            <form method="post" enctype="multipart/form-data" action="/files">
            <p><input type=file name=file>
            <input type=submit value=Upload>
            </form>
            ''', 200)
