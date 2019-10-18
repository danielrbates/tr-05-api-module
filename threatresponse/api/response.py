from .. import urls
from .base import API
from .routing import Router


class ResponseAPI(API):
    __router, route = Router.new()

    @route('respond.observables')
    def _perform(self, payload, **kwargs):
        """
        https://visibility.amp.cisco.com/iroh/iroh-response/index.html#!/Response/post_iroh_iroh_response_respond_observables
        """

        return self._post(
            '/iroh/iroh-response/respond/observables',
            json=payload,
            **kwargs
        )

    @route('respond.trigger')
    def _perform(self,
                 module_name,
                 action_id,
                 observable_type,
                 observable_value,
                 **kwargs):
        """
        https://visibility.amp.cisco.com/iroh/iroh-response/index.html#!/Response/post_iroh_iroh_response_respond_trigger_module_name_action_id
        """

        url = urls.join(
            '/iroh/iroh-response/respond/trigger',
            module_name,
            action_id
        )

        # Extend optional module-specific query params with the required ones.
        query = kwargs.pop('params', {})
        query.update({
            'observable_type': observable_type,
            'observable_value': observable_value,
        })

        return self._post(url, params=query, **kwargs)
