# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### API Documentation

Endpoints:

`GET "/categories"`:
  - fetches a dictionary of all categories, containing their id and category name(type).
  - needs no arguments
  -returns two objects, `success` and `categories` with the values `True` and an object with `{"category id": "category name"}` key:value pair, respectively.

  Sample request: `curl http://127.0.0.1:5000/categories`
  Response: 
  ``` json 
    {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    } 
  ```
`GET "/questions"`:
  - fetches a list of all questions, containing a paginated (10 per page) dictionary of each question; its answer, category(id), difficulty.
  - needs no arguments.
  -returns five objects;`categories`, `current_category`, `questions`, `success` and `total_questions`.

  Sample request: `curl http://127.0.0.1:5000/questions` (defaults page=1)
                  `curl http://127.0.0.1:500/questions?page=2`
  Response: 
  ``` json 
    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "current_category": [
        "Science",
        "Art",
        "Geography",
        "History"
      ],
      "questions": [
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "One",
          "category": 2,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Lake Victoria",
          "category": 3,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "Agra",
          "category": 3,
          "difficulty": 2,
          "id": 15,
          "question": "The Taj Mahal is located in which Indian city?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
      ],
      "success": true,
      "total_questions": 23
  }
  ```

`DELETE "/questions/<int:question_id>"`:
  - deletes the question with id `question_id`.
  - requires no argument.
  - returns four objects; `success`, `deleted`, `questions` and `total_questions` with values `true`, id of deleted question, a paginated set of questions and the total number of questions, respectively, as key value pairs.

  Sample request: `curl -X DELETE http://127.0.0.1:5000/questions/1`
  Response: 
  ``` json 
    {
      "deleted": 1,
      "questions": [
        {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
          "answer": "Alexander Fleming",
          "category": 1,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "The Liver",
          "category": 1,
          "difficulty": 4,
          "id": 20,
          "question": "What is the heaviest organ in the human body?"
        },
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "One",
          "category": 2,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 3,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
          "answer": "Lake Victoria",
          "category": 3,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "Agra",
          "category": 3,
          "difficulty": 2,
          "id": 15,
          "question": "The Taj Mahal is located in which Indian city?"
        },
        {
          "answer": "Muhammad Ali",
          "category": 4,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        }
      ],
      "success": true,
      "total_questions": 22
    }
  ```

`POST "/questions"`:
  - this endpoint serves two purpose depending of the data/arguments passed.
  `ADDING A NEW QUESTION`:
    - posts a new question to the database.
    - requires `question`, `answer`, `category` and `difficulty` in json format as an argument.
    - returns the following as key-value pairs:
      - `created`: value of the new questions id in the database.
      - `questions`: list of the dictionary of questions on current page.
      - `success`: true
      - `total_questions`: total number of questions.

    Sample request: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d '{"question": "Whose autobiography is entitled I Know Why the Caged Bird Sings?", "answer": "Maya Angelou", "category": "4", "difficulty": "5"}'`

    Response: 
    ``` json 
      {
        "created": 30,
        "questions": [
          {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
          },
          {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
          },
          {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
          },
          {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
          },
          {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
          },
          {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
          },
          {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
          },
          {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
          },
          {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
          },
          {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 5,
            "id": 30,
            "question": "Whose autobiography is entitled I Know Why the Caged Bird Sings?"
          }
        ],
        "success": true,
        "total_questions": 23
      }
    ```

  `SEARCHING FOR A QUESTION/QUESTIONS`:
    - fetches all questions matching the players search term.
    - requires `searchTerm` in json format as an argument.
    - returns an object with the following as key-value pairs:
      - `current_category`: an array of the categories of each question in the search result.
      - `questions`: an array of the questions containing the search term.
      - `success`: true.
      - `total_questions`: total number of questions returned containing the search term.

    Sample request: `curl -X POST http://127.0.0.1:5000/questions -H 'Content-Type: application/json' -d '{"searchTerm": "La Giaconda"}'`
    Response: 
    ``` json 
      {
        "current_category": [
          "Art"
        ],
        "questions": [
          {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
          }
        ],
        "success": true,
        "total_questions": 1
      }
    ```

`GET "/categories/<int:category_id>/questions"`:
  - fetches all questions in the category with id of 2.
  - requires no arguments.
  - returns an object with the following as key-value pairs:
    - `current_category`: the category name for the corresponding category_id.
    - `questions`: an array of all questions in that category.
    - `success`: true.
    - `total_questions`: total number of questions in specified category.

  Sample request: `curl http://127.0.0.1:5000/categories/2/questions`
  Response:
  ``` json 
    {
      "current_category": "Art",
      "questions": [
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "Mona Lisa",
          "category": 2,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "One",
          "category": 2,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        }
      ],
      "success": true,
      "total_questions": 3
    }
  ```

`POST "/quizzes"`:
  - fetches all questions for selected category
  - requires `quiz_category` and `previous_questions` as arguments.
  - returns an object with the following key-value pairs:
    - `question`: a random question from all questions in selected category.
    - `success: true

  Sample request: `curl -X POST http://127.0.0.1:5000/quizzes -H 'Content-Type: application/json' -d '{"quiz_category": {"type": "Art", "id": 2, "previous_questions": []}'`
  Response:
  ``` json 
    {
      "question": {
        "answer": "One",
        "category": 2,
        "difficulty": 4,
        "id": 18,
        "question": "How many paintings did Van Gogh sell in his lifetime?"
      },
      "success": true
    }
  ```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
