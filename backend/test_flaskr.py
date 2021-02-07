import os
import unittest
import json
import time

from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import EnvironBuilder


from flaskr import create_app
from models import setup_db, Question, Category
from flask import Flask, url_for

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('trivia:trivia@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.category = Category("Science")
        
        self.question = Question('test_question', 'test_answer', self.category.id, 5)
        
        self.new_question_correct = {
            'question' : 'test_question', 
            'answer' : 'test_answer', 
            'category' : '2', 
            'difficulty' : '5'
        }

        self.new_question_false = {
            'answer' : 'test_answer', 
            'category' : '2', 
            'difficulty' : '5'
        }

        self.id = 0

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            print("drop db")
            self.db.drop_all()        
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET '/api/v1/categories' Bad Input Categories not loaded to database
    def test_get_categories_bad(self):
        res = self.client.get('/api/v1/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    # GET '/api/v1/categories' Happy Scenario
    def test_get_categories_happy(self):
        self.category.insert() 
        res = self.client.get('/api/v1/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    #GET '/api/v1/questions' Bad Input

    def test_getQuestions_bad(self):
        res = self.client.get('/api/v1/questions')
        self.assertEqual(res.status_code, 404)    

    #GET '/api/v1/questions' Happy Scenario

    def test_getQuestions_happy(self):
        self.question.insert() 
        res = self.client.get('/api/v1/questions')
        self.assertEqual(res.status_code, 200)     

    #POST '/api/v1/questions' Happy Scenario

    def test_submitQuestion(self):
        res = self.client.post('/api/v1/questions', json=self.new_question_correct)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.id = data['id']

 


    #DELETE '/api/v1/questions/<int:question_id>' Happy Scenario

    #def test_delete_question_happy(self):
    #    res = self.client.delete('/api/v1/questions/' + str(self.id))
    #    self.assertEqual(res.status_code, 200)  

    
    #GET '/api/v1/questions' Happy Scenario

    
    
    
    #DELETE '/api/v1/questions/<int:question_id>' Bad Input


    
    #POST '/api/v1/questions' Bad Input


    #POST '/api/v1/questions/search' Happy Scenario
    #POST '/api/v1/questions/search' Bad Input


    #GET '/api/v1/categories/<int:category_id>/questions' Happy Scenario
    #GET '/api/v1/categories/<int:category_id>/questions' Bad Input




"""     def test_getQuestions(self):
        res = self.client.get('/api/v1/questions')
        self.assertEqual(res.status_code, 200)


    def test_submitQuestion(self):
        res = self.client.post('/api/v1/questions', json=self.new_question_correct)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_submitQuestion(self):
        res = self.client.post('/api/v1/questions', json=self.new_question_false)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False) """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
