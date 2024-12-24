from django.db import models

QUESTIONS = [
    {
        'id': question_id,
        'title': f'Qestion #{question_id}',
        'answers_number': question_id * question_id,
        'text': f'Text of question #{question_id}',
        'tags': ['tag' for i in range(question_id)],
    } for question_id in range(10)
]

ANSWERS = [
    {
        'id': answer_id,
        'text': f'Text of question #{answer_id}',
        'tags': ['tag' for i in range(answer_id)],
    } for answer_id in range(6)
]

TAGS = [
    {
        'id': tags_id,
        'text': f'Text of question #{tags_id}',
        'tags': ['tag' for i in range(tags_id)],
    } for tags_id in range(6)
]