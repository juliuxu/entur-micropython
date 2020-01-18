import urequests
from util import cache, parse_iso8601
import config
import log


@cache(30 * 1000)
def get_departures():
    ENTUR_API = "https://api.entur.io/journey-planner/v2/graphql"
    USER_AGENT = "jark_technology - departure-iot"
    QUERY = '''
query Depatures($quay_id: String!, $numberOfDepartures: Int) {
  quay(id: $quay_id) {
    estimatedCalls(numberOfDepartures: $numberOfDepartures) {
      expectedDepartureTime
      situations {
        reportType
      }
    }
  }
}
    '''

    response = urequests.post(
        ENTUR_API,
        headers={'Accept': 'application/json',
                 "ET-Client-Name": USER_AGENT},
        json=dict(query=QUERY, variables={"quay_id": config.get("quay_id"), "numberOfDepartures": 3}))
    result = None
    try:
        result = response.json()
    except Exception as e:
        raise e
    finally:
        response.close()

    if __debug__:
        log.debug(result)

    estimatedCalls = result["data"]["quay"]["estimatedCalls"]
    expectedDepartureTimes = map(lambda x: (
        parse_iso8601(x["expectedDepartureTime"]),
        any(map(lambda y: y['reportType'] == "incident", x['situations']))
    ), estimatedCalls)
    return list(expectedDepartureTimes)
