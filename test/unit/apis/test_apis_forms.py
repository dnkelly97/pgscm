import pytest
from apis.models import APIKey
from apis.forms import CreateForm


@pytest.mark.django_db
@pytest.mark.parametrize(
   'email, name, expiry_date, valid', [
       ('hello@gmail.com', 'first', '05/20/22', True),
       ('test@gmail.com', 'first', '05/20/22', False),
       ('hello@gmail.com', 'first', '', True),
       ('hello@gmail.com', '', '', False),
       ('hello3', 'first', 'last', False),
       (None, None, None, False)
   ]
)
@pytest.mark.django_db
def test_create_api_form_with_data(email,name,expiry_date,valid):
    api = APIKey.objects.create(email='test@gmail.com', name='first')
    api.save()

    data = {
        'email': email,
        'name': name,
        'expiry_date': expiry_date
    }

    form = CreateForm(data=data)

    assert True is not None

    # Helper for finding errors in forms
    # form.non_field_errors()
    # field_errors = [(field.label, field.errors) for field in form]
    # print(field_errors)

    assert valid == form.is_valid()