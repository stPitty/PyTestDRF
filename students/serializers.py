from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_testing.settings import MAX_STUDENTS_PER_COURSE
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if data.get('students'):
            if len(data.get('students')) > MAX_STUDENTS_PER_COURSE:
                raise ValidationError({'students': f'Вы превысили максимальное значение студентов на курсе ({MAX_STUDENTS_PER_COURSE})'})
        return super().validate(data)
