# https://gist.github.com/iki/d65eb46929c7c8cc306d911b5ae4384a
# Ported python-graphql-client to use micropython-urequests.
# - https://github.com/prismagraphql/python-graphql-client
# - https://github.com/micropython/micropython-lib/tree/master/urequests

from urequests import post


def shrink_query(query):
    query = query.replace(r'\n', ' ')
    query = query.replace(r'\t', ' ')

    while query != query.replace('  ', ' '):
        query = query.replace('  ', ' ')

    return query


class GraphQLClient:
    def __init__(self, endpoint, useGet=False):
        self.endpoint = endpoint
        self.useGet = useGet
        self.token = None

    def execute(self, query, variables=None, headers=None):
        return self._send(query, variables, headers)

    def inject_token(self, token):
        self.token = token

    def _send(self, query, variables, headers):
        query = shrink_query(query)

        inner_headers = {
            'Accept': 'application/json'
        }
        if headers is not None:
            inner_headers.update(headers)

        if self.token is not None:
            headers['Authorization'] = '{}'.format(self.token)

        response = post(
            self.endpoint,
            headers=inner_headers,
            json=dict(query=query, variables=variables))

        return response.json()
