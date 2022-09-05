import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "dee1500", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "How much does the Chewbacca costume weigh?",
            "answer": "8 pounds",
            "category": "6",
            "difficulty": "5"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
 
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]), 6)
    
    def test_404_no_available_categories(self):
        res = self.client().get("/categories/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"], 19)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]), 6)
        self.assertTrue(data["current_category"])

    def test_404_get_invalid_page_questions(self):
        res = self.client().get("/questions?page=50")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/19")
    #     data = json.loads(res.data)

    #     question = Question.query.filter(Question.id == 19).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted"], 19)
    #     self.assertTrue(data["questions"])
    #     self.assertTrue(data["total_questions"])
    #     self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/500")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # def test_add_new_question(self):
    #     res = self.client().post("/questions", json=self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["created"])
    #     self.assertTrue(len(data["questions"]))

    def test_405_add_new_question_method_failed(self):
        res = self.client().post("/questions/50", json={"question": "What is the capital of Spain"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_get_paginated_search_results(self):
        res = self.client().post('/questions', json={'query': 'La Gioconda'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data["total_questions"], 2)

    def test_404_get_paginated_search_no_results(self):
        res = self.client().post("/questions", json={"query": "pigry"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found") 

    def test_get_questions_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"], 3)
        self.assertTrue(data["current_category"], "Geography")

    def test_404_get_questions_for_invalid_category(self):
        res = self.client().get("/categories/50/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_post_new_quiz_question(self):
        res = self.client().post("/quizzes", json={'quiz_category': {'type': 'click', 'id': 0}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_405_post_quiz_method_not_allowed(self):
        res = self.client().post("/quizzes/2", json={'quiz_category': {'type': 'Sports', 'id': '6'}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()