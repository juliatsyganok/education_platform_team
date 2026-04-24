from django.shortcuts import get_object_or_404
from ..models import Lesson, LessonProgress, Enrollment
from ..exceptions import AlreadyEnrolledError, CourseNotPublishedError, SelfEnrollmentError


def complete_lesson_service(user, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    enrollment = Enrollment.objects.filter(
        user=user, course=lesson.course, status='active'
    ).first()
    if not enrollment:
        raise Exception("Вы не записаны на этот курс или он уже завершён")

    progress, created = LessonProgress.objects.get_or_create(
        user=user,
        lesson=lesson,
        defaults={'is_completed': True}
    )
    if not created:
        progress.is_completed = True
        progress.save()

    total_lessons = lesson.course.lessons.count() 
    completed_lessons = LessonProgress.objects.filter(
        user=user, lesson__course=lesson.course, is_completed=True
    ).count()

    if total_lessons == completed_lessons:
        enrollment.status = 'completed'
        enrollment.save()

    return progress


def get_course_progress(user, course):
    total_lessons = course.lessons.count()  
    completed_lessons = LessonProgress.objects.filter(
        user=user,
        lesson__course=course,
        is_completed=True
    ).count()

    return {
        "progress_display": f"{completed_lessons} / {total_lessons}",
        "completed_count": completed_lessons,
        "total_count": total_lessons,
    }


class EnrollmentService:
    @staticmethod
    def create_enrollment(user, course):
        if not course.published:
            raise CourseNotPublishedError()

        if hasattr(user, 'userprofile') and user.userprofile == course.author:
            raise SelfEnrollmentError()

        if Enrollment.objects.filter(user=user, course=course).exists():
            raise AlreadyEnrolledError()

        enrollment = Enrollment.objects.create(user=user, course=course, status='active')
        return enrollment