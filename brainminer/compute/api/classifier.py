import os
from flask_restful import reqparse
from flask import current_app
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string
from brainminer.base.api import HtmlResource
from brainminer.storage.dao import FileDao
from brainminer.compute.dao import ClassifierDao, SessionDao


# ----------------------------------------------------------------------------------------------------------------------
class ClassifiersResource(HtmlResource):
    
    URI = '/classifiers'

    def get(self):
    
        classifier_dao = ClassifierDao(self.db_session())
        classifiers = classifier_dao.retrieve_all()
        if len(classifiers) == 0:
            classifiers.append(classifier_dao.create(**{'name': 'SVM', 'external_id': 'SVM-' + generate_string(8)}))
    
        parser = reqparse.RequestParser()
        parser.add_argument('classifier', type=int, required=False, location='args')
        args = parser.parse_args()
        
        html = ''
        
        if not args['classifier'] is None:
            
            classifier = classifier_dao.retrieve(id=args['classifier'])
            html += '<h3>Congratulations!</h3>'
            html += '<p>You selected the following classifier: {}</p>'.format(classifier.name)
            nr_sessions = len(classifier.sessions)
            if nr_sessions > 0:
                html += '<p'
                html += 'This classifier has already been trained {} times.<br>'.format(nr_sessions)
                html += 'If you wish to re-use one of these training sessions,<br>'
                html += 'click the button below.'
                html += '</p>'
                html += '<form method="get" action="/classifiers/{}/sessions">'.format(classifier.id)
                html += '  <input type="submit" value="View training sessions">'
                html += '</form>'
    
            html += '<p>'
            html += 'To train this classifier with new examples, upload a CSV file below. After<br>'
            html += 'you click the button, it may take a few minutes for the page to respond. DO NOT<br>'
            html += 'REFRESH THE PAGE OR NAVIGATE TO ANOTHER PAGE because this will interrupt the<br>'
            html += 'training process.'
            html += '</p>'
            html += '<form method="post" enctype="multipart/form-data" action="/classifiers/{}/sessions">'.format(
                classifier.id)
            html += '  <input type="file" name="file">'
            html += '  <input type="submit" value="Train classifier">'
            html += '</form>'
            
        else:
            
            html += '<h3>Select classifier</h3>'
            html += '<p>Select a classifier from the pull-down menu below.</p>'
            html += '<br>'
            html += '<form method="get" action="/classifiers">'
            html += '  <select name="classifier">'
            for classifier in classifiers:
                html += '    <option value="{}">SVM</option>'.format(classifier.id)
            html += '  </select>'
            html += '  <input type="submit" value="Select classifier">'
            html += '</form>'
            
        return self.output_html(html, 200)
    
    
# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionsResource(HtmlResource):
    
    URI = '/classifiers/{}/sessions'

    def get(self, id):
        
        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)

        if len(classifier.sessions) > 0:
    
            html = ''
            html += '<h3>Training sessions</h3>'
            html += '<p>Classifier {} has the following training sessions:</p>'
            html += '<ul>'
            for session in classifier.sessions:
                html += '<li>{}</li>'.format(session.training_file_path)
            html += '</ul>'
            
            return self.output_html(html, 200)
            
        else:
            return self.output_html('No classifier training sessions found', 200)

    def post(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, required=True, location='files')
        args = parser.parse_args()

        args['storage_id'] = generate_string()
        args['storage_path'] = os.path.join(current_app.root_path, self.config()['UPLOAD_DIR'], args['storage_id'])
        args['file'].save(args['storage_path'])
        args['name'] = args['file'].filename
        args['extension'] = '.'.join(args['name'].split('.')[1:])
        args['content_type'] = 'application/octet-stream'
        args['media_link'] = args['storage_path']
        args['size'] = 0
        del args['file']

        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)
        print('Training classifier {} on file {}'.format(classifier.name, f.name))
        
        # After classifier training finishes, create a session that captures the results
        
        session_dao = SessionDao(self.db_session())
        session = session_dao.create(**{
            'classifier': classifier,
            'training_file_path': f.storage_path,
            'classifier_file_path': '/path_to_classifier',
        })

        html = '<h3>Nice!</h3>'
        html += '<p>You have successfully trained your classifier!</p>'
        html += '<p>'
        html += 'You can view the uploaded file here:<br>'
        html += '<a target="_blank" href="/files/{}/content">{}</a>'.format(f.id, f.storage_id)
        html += '</p>'
        html += '<p>'
        html += 'The next step is to use your classifier for predictions. Again, upload a<br>'
        html += 'CSV file with the cases you want to predict.'
        html += '</p>'
        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/predictions">'.format(session.id)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Upload predictions">'
        html += '</form>'

        return self.output_html(html, 201)
