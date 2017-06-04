import os
from werkzeug.datastructures import FileStorage
from flask_restful import reqparse
from flask import current_app
from brainminer.base.api import HtmlResource
from brainminer.compute.dao import ClassifierDao, SessionDao
from brainminer.storage.dao import FileDao
from brainminer.base.util import generate_string, get_xy, score_svm, train_svm
from brainminer.base.api import HtmlResource

import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedKFold


class ClassifiersResource(HtmlResource):

    URI = '/classifiers'

    def get(self):

        classifier_dao = ClassifierDao(self.db_session())
        classifiers = classifier_dao.retrieve_all()
        if len(classifiers) == 0:
            classifiers.append(classifier_dao.create(**{'name': 'SVM', 'external_id': 'SVM-' + generate_string(8)}))

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

        # Retrieve training sessions from classifier and display them (if list > 0)
        # Also show a form to create a new training session

        html = ''
        html += '<p>You selected classifier {}. Click "Train" to start training.<br>'.format(i)
        html += 'Or select one of the training sessions to run a prediction.</p>'

        html += '<form method="get" action="/classifiers/{}/sessions">'.format(i)
        html += '  <input type="submit" value="View training sessions">'
        html += '</form>'

        html += '<form method="post" enctype="multipart/form-data" action="/classifiers/{}/sessions">'.format(i)
        html += '  <input type="file" name="file"><br><br>'
        html += '  <input type="text" name="target_column" value="Diagnosis"> Target column<br><br>'
        html += '  <input type="text" name="exclude_columns"> Exclude columns (comma-separated list)<br><br>'
        html += '  <input type="text" name="nr_iters" value="1">Nr. iterations<br><br>'
        html += '  <input type="text" name="nr_folds" value="2">Nr. folds (>= 2)<br><br>'
        html += '  <input type="submit" value="Train classifier"><br><br>'
        html += '</form>'

        return self.output_html(html, 200)


class ClassifierSessionsResource(HtmlResource):

    URI = '/classifiers/{}/sessions'

    def get(self, id):

        html = 'Sessions:'
        return self.output_html(html, 200)

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

        avg_score = 0

        # # Run performance evaluation on classifier
        # for i in range(nr_iters):
        #     for train, test in StratifiedKFold(n_splits=nr_folds).split(x, y):
        #         _, score = score_svm(x, y, train, test)
        #         scores += score
        # avg_score = scores / (nr_iters * nr_folds)

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
        html += 'accuracy of {} after {} iterations and {} folds.</p>'.format(avg_score, nr_iters, nr_folds)

        html += '<p>The next step is to view your trained classifier and use it for predictions.<br>'
        html += 'Click the button below to proceed.</p>'

        html += '<form method="get" action="/sessions/{}">'.format(session.id)
        html += '  <input type="submit" value="View session">'
        html += '</form>'

        return self.output_html(html, 201)
