from flask_restful import reqparse
from brainminer.base.util import generate_string
from brainminer.base.api import HtmlResource
from brainminer.compute.dao import ClassifierDao, SessionDao


# ----------------------------------------------------------------------------------------------------------------------
class ClassifiersResource(HtmlResource):
    
    URI = '/classifiers'

    def get(self):
        # This endpoint should return a list of classifiers in a pull-down menu. After
        # selecting a classifier we can immediately proceed with creating a training session.
        # Each classifier has an associated list (possibly empty) with training sessions (link).

        # In the final version the post() should be removed. We don't want people to create
        # classifiers themselves
        return self.output_html('No classifiers available', 200)
    
    def post(self):

        name = 'SVM_' + generate_string(8)
        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.create(**{'name': name})

        html = '<h3>Congratulations!</h3>'
        html += '<p>You successfully create a classifier with the following name: {}</p>'.format(name)
        html += '<p>Next step is to create a training session for your classifier.'
        html += '<p>Click the following link to do this:</p>'
        html += '<form method="post" action="/classifiers/{}/sessions">'.format(classifier.id)
        html += '  <input type="submit" value="Create training session">'
        html += '</form>'

        return self.output_html(html, 200)
    
    
# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionsResource(HtmlResource):
    
    URI = '/classifiers/{}/sessions'

    def get(self, id):
        return self.output_html('No classifier training sessions available', 200)

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
