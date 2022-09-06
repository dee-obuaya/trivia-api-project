import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,OPTIONS,DELETE')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            category.id: category.type for category in categories
        }
        # category_dict = {}
        # for c in categories:
        #     category_dict[c.id] = c.type

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories,
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        formatted_categories = formatted_categories = {
            category.id: category.type for category in categories
        }
        current_categories = [Category.query.filter(
            Category.id == q['category']).one_or_none().type for q in current_questions]
        formatted_current_category = []

        for category in current_categories:
            if category in formatted_current_category:
                pass 
            else:
                formatted_current_category.append(category)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': formatted_categories,
            'current_category': formatted_current_category
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            question.delete()
            selection = Question.query.order_by(Question.category).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection)
            })

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"])
    def add_new_question():
        body = request.get_json()
        search = body.get('searchTerm', None)

        if search is None:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            try:
                question = Question(question=new_question, answer=new_answer,
                                        category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.category).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(selection)
                })

            except:
                abort(405)
        else:
            search_selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search}%') | Question.question.contains(search)).all()
              
            if search_selection:
                return jsonify({
                    "success": True,
                    "questions": [q.format() for q in search_selection],
                    "total_questions": len(search_selection),
                    "current_category": [Category.query.filter(Category.id == q.category).one_or_none().type for q in search_selection]
                    })
            else: 
                abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_for_specific_category(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).all()
            current_questions = paginate_questions(request, selection)
            current_category = Category.query.filter(Category.id == category_id).one_or_none()

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "current_category": current_category.type
            })

        except:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category', '')
        category = quiz_category['id']
        previous_questions = body.get('previous_questions')

        if category != '' and category != 0:
            questions = Question.query.filter(Question.category == category).all()
        elif category == 0:
            questions = Question.query.all()
        else:
            abort(400)

        repeated_question = True
                
        if len(questions) < 5 and len(previous_questions) == len(questions) or len(previous_questions) == 5:
            return jsonify({
                "success": True,
                "question": None
            })
        else:
            while repeated_question:
                new_question = random.choice(questions)
                formatted_question = new_question.format()

                if formatted_question['id'] in previous_questions:
                    new_question = random.choice(questions)
                else:
                    repeated_question = False
            
            return jsonify({
                "success": True,
                "question": formatted_question
            })



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app

