from src.courses.exceptions import AlreadyEnrolledError, CourseNotPublishedError, SelfEnrollmentError
from models import Enrollment
class EnrollmentService:
    @staticmethod
    def create_enrollment(user, course):
        if not course.published:
            raise CourseNotPublishedError
        if course.author.user==user:
            raise SelfEnrollmentError
        if Enrollment.objects.filter(user=user,course=course).exists():
            raise AlreadyEnrolledError
        enrollment = Enrollment.objects.create(user=user, course=course, status='active')
        return enrollment
