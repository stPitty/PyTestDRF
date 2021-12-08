import pytest
from django.urls import reverse


class TestStudents():

    @pytest.mark.django_db
    def test_list_courses(self, api_client, url, courses_factory):
        courses = courses_factory(_quantity=14)
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.json()) == len(courses)
        for index, course in enumerate(response.json()):
            assert course['name'] == courses[index].name

    @pytest.mark.django_db
    def test_retrieve_course(self, api_client, courses_factory):
        courses = courses_factory(_quantity=3)
        for course in courses:
            url = reverse('courses-detail', args=[course.id])
            response = api_client.get(url)
            assert response.status_code == 200
            assert response.json()['name'] == course.name

    @pytest.mark.django_db
    def test_list_courses_filter(self, api_client, courses_factory, url):
        courses = courses_factory(_quantity=5)
        response = api_client.get(url, {'id': courses[1].id, 'name': courses[1].name})
        assert response.status_code == 200
        assert response.json()[0]['id'] != courses[0].id
        assert response.json()[0]['id'] == courses[1].id
        assert response.json()[0]['name'] != courses[0].name
        assert response.json()[0]['name'] == courses[1].name

    @pytest.mark.parametrize(
        ['course_name', 'exp_status'],
        [
            ['1st', 201],
            ['2nd', 201]
        ]
    )
    @pytest.mark.django_db
    def test_create_course(self, api_client, url, course_name, exp_status):
        upload_data = {'name': course_name}
        response = api_client.post(url, upload_data)
        assert response.status_code == exp_status
        assert response.json()['name'] == course_name

    @pytest.mark.parametrize(
        ['course_name', 'exp_status'],
        [
            ['1st', 200],
            ['2nd', 200]
        ]
    )
    @pytest.mark.django_db
    def test_update_course(self, api_client, courses_factory, course_name, exp_status):
        courses = courses_factory(_quantity=1)
        upload_data = {'name': course_name}
        for course in courses:
            url = reverse('courses-detail', args=[course.id])
            response = api_client.patch(url, upload_data)
            assert response.status_code == exp_status
            assert response.json()['name'] == course_name

    @pytest.mark.django_db
    def test_delete_course(self, api_client, courses_factory):
        courses = courses_factory(_quantity=5)
        for course in courses:
            url = reverse('courses-detail', args=[course.id])
            response = api_client.delete(url)
            assert response.status_code == 204


    @pytest.mark.parametrize(
        ['qty', 'exp_status'],
        [
            [23, 400],
            [11, 200]
        ]
    )
    @pytest.mark.django_db
    def test_max_student_with_creation(self, api_client, courses_factory, students_factory, qty, exp_status):
        students = students_factory(_quantity=qty)
        course = courses_factory(_quantity=1)[0]
        url = reverse('courses-detail', args=[course.id])
        upload_data = {"students": [student.id for student in students]}
        response = api_client.patch(url, upload_data)
        assert response.status_code == exp_status
