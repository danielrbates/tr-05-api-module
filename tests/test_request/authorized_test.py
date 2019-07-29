from six.moves.http_client import UNAUTHORIZED
from mock import Mock

from ..common import patch

from threatresponse.request.base import Request
from threatresponse.request.authorized import AuthorizedRequest


@patch(Request)
def test_that_authorized_request_provides_header_with_token(request):
    request.post.return_value = token('Cake')

    authorized = AuthorizedRequest(request, 'x', 'y')
    authorized.post('/some', headers={'Just': 'Test'})

    request.perform.assert_called_once_with(
        'POST',
        '/some',
        headers={
            'Just': 'Test',
            'Authorization': 'Bearer Cake'
        }
    )


@patch(Request)
def test_that_authorized_request_retrieves_token_on_init(request):
    AuthorizedRequest(request, 'x', 'y')

    request.post.assert_called_once_with(
        AuthorizedRequest.TOKEN_URL,
        auth=('x', 'y'),
        data={'grant_type': 'client_credentials'},
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    )


@patch(Request)
def test_that_authorized_request_retrieves_token_on_expiration(request):
    response = Mock()
    response.status_code = UNAUTHORIZED

    request.post.return_value = token('Cake')
    request.perform.return_value = response

    authorized = AuthorizedRequest(request, 'x', 'y')
    authorized.post('/some')

    assert request.post.call_count == 2
    assert (
        request.post.call_args_list[0] ==
        request.post.call_args_list[1]
    )


def token(bearer):
    mocked = Mock()
    mocked.json.return_value = {'access_token': bearer}

    return mocked