from exam_tests.models import Question


def generate_ai_questions(content, ai_service):
    """
    Generates AI questions for a given content using an AI service.
    """
    if content.content_type != 'test':
        raise ValueError("Content must be of type 'test' to generate questions.")

    ai_questions = ai_service.generate(content)  # Hypothetical AI service
    for question in ai_questions:
        Question.objects.create(
            content=content,
            text=question['text'],
            options=question['options'],
            correct_answer=question['correct_answer'],
            explanation=question['explanation'],
            is_ai_generated=True
        )
