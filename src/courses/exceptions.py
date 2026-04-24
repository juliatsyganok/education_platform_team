from rest_framework.exceptions import ValidationError

class CourseNotPublishedError(ValidationError):
    def __init__(self):
        super().__init__(detail={"course": "Нельзя записаться на неопубликованный курс"})

class SelfEnrollmentError(ValidationError):
    def __init__(self):
        super().__init__(detail={"course": "Автор курса не может записаться на свой курс"})

class AlreadyEnrolledError(ValidationError):
    def __init__(self):
        super().__init__(detail={"course": "Вы уже записаны на этот курс"})

class PaymentError(ValidationError):
    def __init__(self):
        super().__init__(detail={"payment": "Оплата не прошла"})