import urequests
import log
from util import cache, parse_iso8601
from graphqlclient import GraphQLClient
import config

ENTUR_API = "https://api.entur.io/journey-planner/v2/graphql"

# QUAY Mot Bergkrystallen: NSR:Quay:10850
# QUAY Mot Sentrum: NSR:Quay:10851
query = '''
query Depatures($quay_id: String!, $numberOfDepartures:Int) {
  quay(id: $quay_id) {
    estimatedCalls(numberOfDepartures: $numberOfDepartures) {
      realtime
      expectedDepartureTime
    }
  }
}
'''

USER_AGENT = "jark_technology - departure-iot"
client = GraphQLClient(ENTUR_API)


@cache(30 * 1000)
def get_departures(n=5):
    result = client.execute(
        query,
        variables={"quay_id": config.get("quay_id"), "numberOfDepartures": n},
        headers={"ET-Client-Name": USER_AGENT}
    )
    expectedDepartureTimes_s = result["data"]["quay"]["estimatedCalls"]
    expectedDepartureTimes = map(lambda x: parse_iso8601(
        x["expectedDepartureTime"]), expectedDepartureTimes_s)
    return list(expectedDepartureTimes)
