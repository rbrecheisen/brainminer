from flask_restful import reqparse
from brainminer.base.api import HtmlResource
from brainminer.compute.dao import ClassifierDao, SessionDao


# ----------------------------------------------------------------------------------------------------------------------
class ClassifiersResource(HtmlResource):
    
    URI = '/classifiers'
    
    def post(self):

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.create(**{'name': 'SVM'})

        html = '<h3>Congratulations!</h3>'
        html += '<p>You created your classifier successfully!</p>'
        html += '<p>Next step is to create a new training session for the classifier. Click the following link:</p>'
        html += '<form method="post" action="/classifiers/{}/sessions">'.format(classifier.id)
        html += '  <input type="submit" value="Create training session">'
        html += '</form>'

        return self.output_html(html, 200)
    
    
# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionsResource(HtmlResource):
    
    URI = '/classifiers/{}/sessions'
    
    def post(self, id):

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)
        session_dao = SessionDao(self.db_session())
        session = session_dao.create(**{'classifier': classifier})

        html = '<h3>Nice!</h3>'
        html += '<p>You created a training session for your classifier!</p>'
        html += '<p>Now specify the file to use for training by uploading it.</p>'
        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/files">'.format(session.id)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Upload training file">'
        html += '</form>'

        return self.output_html(html, 201)
