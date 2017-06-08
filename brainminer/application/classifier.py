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
# from sklearn.model_selection import StratifiedKFold


class ClassifiersResource(HtmlResource):

    URI = '/classifiers'

    def get(self):
        """
        Returns a pull-down menu containing all supported classifiers. If the list is empty, 
        it will be automatically populated in the database.
        :return: 
        """
        classifier_dao = ClassifierDao(self.db_session())
        classifiers = classifier_dao.retrieve_all()
        if len(classifiers) == 0:
            classifiers.append(classifier_dao.create(**{'name': 'SVM', 'external_id': 'SVM-' + generate_string(8)}))

        html = ''
        html += '<h3>Step 1 - Select a classifier</h3>'
        html += '<p>Select a classifier from the pull-down menu below. Then click<br>'
        html += 'the select button to proceed.</p>'
        html += '<form method="post" action="/classifiers">'
        html += '  <select name="classifier_id">'

        for classifier in classifiers:
            html += '    <option value="{}">Support Vector Machine</option>'.format(classifier.id)

        html += '  </select>'
        html += '  <input type="submit" value="Select">'
        html += '</form>'

        return self.output_html(html, 200)

    def post(self):
        """
        Handles selection of a classifier type (note that usually a PUT request would be
        used for this because the classifier resources already exists but UI forms do not
        support PUT requests, only GET and POST). 
        :return: 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('classifier_id', type=int, location='form')
        args = parser.parse_args()

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=args['classifier_id'])
        nr_sessions = len(classifier.sessions)

        # Retrieve training sessions from classifier and display them (if list > 0)
        # Also show a form to create a new training session

        html = ''
        html += '<h3>Step 2 - Train your classifier</h3>'
        html += '<p>You selected the {} classifier. Provide the name of the target<br>'.format(classifier.name)
        html += 'label you wish to predict. Also, specify which column name is associated<br>'
        html += 'with identifying your cases, e.g., SubjectID.</p>'

        if nr_sessions > 0:
            html += '<p>There are training sessions associated with your classifier. To run<br>'
            html += 'a prediction right-away, select a session.</p>'
            html += '<ul>'
            for session in classifier.sessions:
                html += '<li><a href="/sessions/{}">Session {}</a></li>'.format(session.id, session.id)
            html += '</ul>'

        html += '<form method="post" enctype="multipart/form-data" action="/classifiers/{}/sessions">'.format(classifier.id)
        html += '  <input type="file" name="file"><br><br>'
        html += '  <input type="text" name="target_column" value="Diagnosis">Target label<br><br>'
        html += '  <input type="text" name="subject_id" value="MRid">Case identifier<br><br>'
        # html += '  <input type="text" name="exclude_columns"> Exclude columns (comma-separated list)<br><br>'
        # html += '  <input type="text" name="nr_iters" value="1">Nr. iterations<br><br>'
        # html += '  <input type="text" name="nr_folds" value="2">Nr. folds (>= 2)<br><br>'
        html += '  <input type="checkbox" name="R" value="true">Use R<br><br>'
        html += '  <input type="submit" value="Train"><br><br>'
        html += '</form>'

        return self.output_html(html, 200)


class ClassifierSessionsResource(HtmlResource):

    URI = '/classifiers/{}/sessions'

    def get(self, id):
        """
        Returns a list of training sessions for this classifier (if available). This 
        allows re-running a prediction for a classifier that was already trained.
        :param id: 
        :return: 
        """
        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)

        html = ''
        html += '<p>This classifier has {} training sessions.<br>'.format(len(classifier.sessions))
        if len(classifier.sessions) > 0:
            html += 'Click a link below to use one of the sessions.'
        html += '</p><ul>'

        for session in classifier.sessions:
            html += '<li><a href="/sessions/{}">Session {}</a></li>'.format(session.id, session.id)

        html += '</ul>'

        return self.output_html(html, 200)

    def post(self, id):
        """
        Creates a new training session for classifier {id}. The classifier uses the
        uploaded file for training.
        :param id: 
        :return: 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, required=True, location='files')
        parser.add_argument('R', type=str, location='form')
        parser.add_argument('target_column', type=str, location='form')
        # parser.add_argument('exclude_columns', type=str, location='form')
        # parser.add_argument('nr_iters', type=str, location='form')
        # parser.add_argument('nr_folds', type=str, location='form')
        parser.add_argument('subject_id', type=str, required=True, location='form')
        args = parser.parse_args()

        subject_id = args['subject_id']
        R = args['R']
        target_column = args['target_column']
        # exclude_columns = args['exclude_columns'].split(',')
        # nr_iters = int(args['nr_iters'])
        # nr_folds = int(args['nr_folds'])

        args['storage_id'] = generate_string()
        args['storage_path'] = os.path.join(current_app.root_path, self.config()['UPLOAD_DIR'], args['storage_id'])
        args['file'].save(args['storage_path'])
        args['name'] = args['file'].filename
        args['extension'] = '.'.join(args['name'].split('.')[1:])
        args['content_type'] = 'application/octet-stream'
        args['media_link'] = args['storage_path']
        args['size'] = 0

        del args['subject_id']
        del args['file']
        del args['R']
        del args['target_column']
        # del args['exclude_columns']
        # del args['nr_iters']
        # del args['nr_folds']

        f_dao = FileDao(self.db_session())
        f = f_dao.create(**args)

        classifier_dao = ClassifierDao(self.db_session())
        classifier = classifier_dao.retrieve(id=id)
        print('Training classifier {} on file {}'.format(classifier.name, f.name))
        if R == 'true':
            print('Running R script (works only in Docker)...')
            os.system('/usr/local/bin/Rscript /Users/Ralph/development/brainminer/R/svm.R 1')

        # After classifier training finishes, create a session that captures the results
        print('Calculating classifier performance...')
        features = pd.read_csv(f.storage_path, index_col=subject_id)
        x, y = get_xy(features, target_column=target_column)

        # scores = 0
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

        html = '<h3>Step 3 - View training session</h3>'
        html += '<p>You have successfully trained your classifier. Click the link below<br>'
        html += 'To view the training session and upload a file with cases to predict.</p>'

        html += '<a href="/sessions/{}">Session {}</a>'.format(session.id, session.id)

        return self.output_html(html, 201)
