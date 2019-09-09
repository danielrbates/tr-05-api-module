import pytest
from mock import MagicMock

from threatresponse.api.response import ResponseAPI


def test_respond_observables_succeeds():
    response = MagicMock()

    request = MagicMock()
    request.post.return_value = response

    payload = {'foo': 'bar'}

    api = ResponseAPI(request)
    api.respond.observables(payload)

    request.post.assert_called_once_with(
        '/iroh/iroh-response/respond/observables',
        json=payload,
    )

    response.json.assert_called_once_with()


def test_respond_observables_fails():
    class TestError(Exception):
        pass

    response = MagicMock()
    response.raise_for_status.side_effect = TestError('Oops!')

    request = MagicMock()
    request.post.return_value = response

    payload = {'foo': 'bar'}

    api = ResponseAPI(request)
    with pytest.raises(TestError):
        api.respond.observables(payload)

    request.post.assert_called_once_with(
        '/iroh/iroh-response/respond/observables',
        json=payload,
    )

    response.raise_for_status.assert_called_once_with()


def test_respond_trigger_succeeds():
    response = MagicMock()

    request = MagicMock()
    request.post.return_value = response

    api = ResponseAPI(request)
    api.respond.trigger(
        'Monty Python!',
        'x|y&z',
        'spam',
        'eggs',
        x=1, y=2, z=3,  # extra params
    )

    request.post.assert_called_once_with(
        '/iroh/iroh-response/respond/trigger/Monty%20Python%21/x%7Cy%26z',
        params={'x': 1, 'y': 2, 'z': 3,
                'observable_type': 'spam',
                'observable_value': 'eggs'},
    )

    response.json.assert_called_once_with()


def test_respond_trigger_fails():
    class TestError(Exception):
        pass

    response = MagicMock()
    response.raise_for_status.side_effect = TestError('Oops!')

    request = MagicMock()
    request.post.return_value = response

    api = ResponseAPI(request)
    with pytest.raises(TestError):
        api.respond.trigger(
            'Monty Python!',
            'x|y&z',
            'spam',
            'eggs',
            x=1, y=2, z=3,  # extra params
        )

    request.post.assert_called_once_with(
        '/iroh/iroh-response/respond/trigger/Monty%20Python%21/x%7Cy%26z',
        params={'x': 1, 'y': 2, 'z': 3,
                'observable_type': 'spam',
                'observable_value': 'eggs'},
    )

    response.raise_for_status.assert_called_once_with()