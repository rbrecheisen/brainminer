from flask_restful import reqparse
from brainminer.base.api import HtmlResource
from brainminer.compute.dao import ClassifierDao
from brainminer.base.api import HtmlResource


class ClassifierResource(HtmlResource):

    URI = '/classifier'

    def get(self):

        classifier_dao = ClassifierDao(self.db_session())
        classifiers = classifier_dao.retrieve_all()

        html = ''
        html += '<form method="post" action="/classifiers">'
        html += '  <select name="classifier">'
        for classifier in classifiers:
            html += '    <option value="{}">SVM</option>'.format(classifier.id)
        html += '  </select>'
        html += '  <input type="submit" value="Select classifier">'
        html += '</form>'

        return self.output_html(html, 200)

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('classifier', type=int, location='form')
        args = parser.parse_args()

        i = args['classifier']

        html = ''
        html += '<p>You selected classifier {}. Click "Train" to start training.</p>'.format(i)
        html += '<form method="post" enctype="multipart/form-data" action="/classifiers/{}/sessions">'.format(i)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Train classifier"><br><br>'
        html += '  <input type="text" name="target_column" value="Diagnosis"> Target column<br><br>'
        html += '  <input type="text" name="exclude_columns"> Exclude columns (comma-separated list)<br><br>'
        html += '  <input type="text" name="nr_iters" value="1">Nr. iterations<br><br>'
        html += '  <input type="text" name="nr_folds" value="2">Nr. folds (>= 2)<br><br>'
        html += '  <input type=submit value="Train">'
        html += '</form>'

        return self.output_html(html, 200)
