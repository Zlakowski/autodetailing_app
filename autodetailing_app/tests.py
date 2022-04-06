from django.test import TestCase
from django.test import Client
import pytest

from django.urls import reverse

from autodetailing_app.forms import AddServiceForm, AddOpinionForm, AddWorkerForm, OrderForm
from autodetailing_app.models import Service, Opinion, Worker, Order


@pytest.mark.django_db
def test_main(about):
    client = Client()
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_category(category):
    client = Client()
    url = reverse('categories')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_outside(category):
    client = Client()
    url = reverse('outside')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_inside(category_id_2):
    client = Client()
    url = reverse('inside')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_to_card_not_login(some_id):
    client = Client()
    url = reverse('add-service-to-card', args=some_id)
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('login')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_add_to_card_login(user, some_id, service):
    client = Client()
    client.force_login(user)
    url = reverse('add-service-to-card', args=some_id)
    response = client.get(url)
    assert response.status_code == 302
    new_url = reverse('services')
    assert response.url.startswith(new_url)
    # assert response.context['services'].count() == 0


@pytest.mark.django_db
def test_add_service_view_get():
    client = Client()
    url = reverse('service-add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddServiceForm)


@pytest.mark.django_db
def test_add_service_view_post(category):
    client = Client()
    url = reverse('service-add')
    data = {
        'name': 'example',
        'description': 'some text',
        'duration': 1,
        'price': 1,
        'categories': [category.id]
    }
    response = client.post(url, data)
    # form = response.context['form']
    # print(form.errors)
    assert response.status_code == 302
    new_url = reverse('services')
    assert response.url.startswith(new_url)
    Service.objects.get(name='example')


@pytest.mark.django_db
def test_del_service(some_id, service):
    client = Client()
    url = reverse('service-delete', args=some_id)
    response = client.get(url)
    assert Service.objects.count() == 0
    assert response.status_code == 302
    new_url = reverse('services')
    assert response.url.startswith(new_url)


@pytest.mark.django_db
def test_add_opinion_get():
    client = Client()
    url = reverse('opinion-add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddOpinionForm)


@pytest.mark.django_db
def test_add_opinion_post(user):
    client = Client()
    client.force_login(user)
    url = reverse('opinion-add')
    data = {
        'nick': 'python',
        'description': 'IS THE BEST'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('main')
    assert response.url.startswith(new_url)
    Opinion.objects.get(**data)


@pytest.mark.django_db
def test_all_opinions():
    client = Client()
    url = reverse('all-opinions')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_worker_get():
    client = Client()
    url = reverse('worker-add')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddWorkerForm)


@pytest.mark.django_db
def test_add_worker_post():
    client = Client()
    url = reverse('worker-add')
    data = {
        'name': 'python is the best'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    new_url = reverse('worker-add')
    assert response.url.startswith(new_url)
    Worker.objects.get(**data)


@pytest.mark.django_db
def test_services():
    client = Client()
    url = reverse('services')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_service_detail(some_id, service):
    client = Client()
    url = reverse('service-detail', args=some_id)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_remove_service_from_cart(some_id, service, user, cart):
    client = Client()
    client.force_login(user)
    url = reverse('remove-service', args=some_id)
    response = client.get(url)
    assert cart.services.count() == 0
    assert response.status_code == 302
    new_url = reverse('order')
    assert response.url.startswith(new_url)


@pytest.mark.django_db
def test_create_order_view_get(user, cart):
    client = Client()
    client.force_login(user)
    url = reverse('order')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], OrderForm)


@pytest.mark.django_db
def test_create_order_view_post(user, cart, service, is_done, worker):
    client = Client()
    client.force_login(user)
    url = reverse('order')
    data = {
        'services': [service.id],
        'worker': worker.id,
        'user': user,
        'is_done': is_done,
        'meeting_date': '2020-01-01'
    }
    response = client.post(url, data)
    # form = response.context['form']
    # print(form.errors)
    assert response.status_code == 302
    new_url = reverse('user-orders')
    assert response.url.startswith(new_url)
    Order.objects.get(worker=worker.id)


@pytest.mark.django_db
def test_user_orders_view(user):
    client = Client()
    url = reverse('user-orders')

# @pytest.mark.django_db
# def test_add_publisher_get():
#     client = Client()
#     url = reverse('add_publisher_model')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert isinstance(response.context['form'], AddPublisherModelForm)

# @pytest.mark.django_db
# def test_add_publisher_post():
#     client = Client()
#     url = reverse('add_publisher_model')
#     date = {
#         'name':'ala',
#         'address' : 'poznanska',
#         "street" : "poznanska",
#         "city" : "bździna dolna",
#         'description':'najlepsze wyd na świecie'
#     }
#     response = client.post(url, date)
#     assert response.status_code == 302
#     new_url = reverse('list_author')
#     assert response.url.startswith(new_url)
#     Publisher.objects.get(**date)


# @pytest.mark.django_db
# def test_booklist_login(user):
#     client = Client()
#     client.force_login(user)
#     url = reverse('list_books')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.context['object_list'].count() == 0

# @pytest.mark.django_db
# def test_booklist_not_login():
#     client = Client()
#     url = reverse('list_books')
#     response = client.get(url)
#     assert response.status_code == 302
#     url = reverse('login')
#     assert response.url.startswith(url)
#

#
#
# @pytest.mark.django_db
# def test_booklist_login(user, books):
#     client = Client()
#     client.force_login(user)
#     url = reverse('list_books')
#     response = client.get(url)
#     assert response.status_code == 200
#     assert response.context['object_list'].count() == len(books)
#     for book in books:
#         assert book in response.context['object_list']
#
#
# @pytest.mark.django_db
# def test_book_update_view(books):
#     book = books[0]
#     client = Client()
#     url = reverse('update_book', args=(book.id,))
#     data = {
#         'title':'?',
#         'year':123,
#         'author': book.author.id#### TO JEST WAŻNE
#     }
#     response = client.post(url, data)
#
#     Book.objects.get(title="?")
