import os
from flask_restful import reqparse
from flask import current_app, request
from werkzeug.datastructures import FileStorage
from brainminer.base.util import generate_string, get_xy, score_svm, train_svm
from brainminer.base.api import HtmlResource
from brainminer.storage.dao import FileDao
from brainminer.compute.dao import ClassifierDao, SessionDao

import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedKFold


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
        
        if args['classifier'] is not None:
            
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
            html += '  <input type="submit" value="Train classifier"><br><br>'
            html += '  <input type="checkbox" name="R" value="true">Use R<br><br>'
            html += '  <input type="text" name="target_column" value="Diagnosis"> Target column<br><br>'
            html += '  <input type="text" name="exclude_columns"> Exclude columns (comma-separated list)<br><br>'
            html += '  <input type="text" name="nr_iters" value="1">Nr. iterations<br><br>'
            html += '  <input type="text" name="nr_folds" value="2">Nr. folds (>= 2)<br><br>'
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
        parser.add_argument('R', type=str, location='form')
        parser.add_argument('target_column', type=str, location='form')
        parser.add_argument('exclude_columns', type=str, location='form')
        parser.add_argument('nr_iters', type=str, location='form')
        parser.add_argument('nr_folds', type=str, location='form')
        args = parser.parse_args()

        R = args['R']
        target_column = args['target_column']
        exclude_columns = args['exclude_columns'].split(',')
        nr_iters = int(args['nr_iters'])
        nr_folds = int(args['nr_folds'])

        args['storage_id'] = generate_string()
        args['storage_path'] = os.path.join(current_app.root_path, self.config()['UPLOAD_DIR'], args['storage_id'])
        args['file'].save(args['storage_path'])
        args['name'] = args['file'].filename
        args['extension'] = '.'.join(args['name'].split('.')[1:])
        args['content_type'] = 'application/octet-stream'
        args['media_link'] = args['storage_path']
        args['size'] = 0

        del args['file']
        del args['R']
        del args['target_column']
        del args['exclude_columns']
        del args['nr_iters']
        del args['nr_folds']

        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)
        print('Training classifier {} on file {}'.format(classifier.name, f.name))
        if R == 'true':
            print('R scripting is not implemented yet...')
        
        # After classifier training finishes, create a session that captures the results
        print('Calculating classifier performance...')
        scores = 0
        features = pd.read_csv(f.storage_path)
        x, y = get_xy(features, target_column=target_column, exclude_columns=exclude_columns)
        for i in range(nr_iters):
            for train, test in StratifiedKFold(n_splits=nr_folds).split(x, y):
                _, score = score_svm(x, y, train, test)
                scores += score
        avg_score = scores / (nr_iters * nr_folds)

        path = f.storage_path + '.classifier'
        print('Building optimized classifier and storing in {}'.format(path))
        classifier_model = train_svm(x, y)
        joblib.dump(classifier_model, path)

        session_dao = SessionDao(self.db_session())
        session = session_dao.create(**{
            'classifier': classifier,
            'training_file_path': f.storage_path,
            'classifier_file_path': path,
        })

        html = '<h3>Congratulations!</h3>'
        html += '<p>You have successfully trained your classifier! It has an average '
        html += 'classification accuracy of {} after {} iterations and {} folds.</p>'.format(
            avg_score, nr_iters, nr_folds)
        html += '<p>The next step is to use your classifier for predictions. Again, upload a<br>'
        html += 'CSV file with the cases you want to predict.</p>'
        html += '<form method="post" enctype="multipart/form-data" action="/sessions/{}/predictions">'.format(session.id)
        html += '  <input type="file" name="file">'
        html += '  <input type="submit" value="Upload predictions">'
        html += '</form>'

        return self.output_html(html, 201)
