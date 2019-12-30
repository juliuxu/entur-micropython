import log
import clock
import util
import utime as time
import display
import machine
from graphqlclient import GraphQLClient

ENTUR_API = "https://api.entur.io/journey-planner/v2/graphql"

# QUAY Mot Bergkrystallen: NSR:Quay:10850
# QUAY Mot Sentrum: NSR:Quay:10851

query = '''
query Depatures($quayid: String!) {
  quay(id: $quayid) {
    estimatedCalls(numberOfDepartures: 2) {
      realtime
      expectedDepartureTime
    }
  }
}
'''

debug_query = '''
query Depatures($quayid: String!) {
  quay(id: $quayid) {
    name
    estimatedCalls(numberOfDepartures: 2) {
      realtime
      expectedDepartureTime
	  destinationDisplay {
        frontText
      }
    }
  }
}
'''


def get_current_time_text():
    (_, _, _, hour, minute, _, _, _) = clock.localtime()
    s = str(minute)
    if minute < 10:
        s = "0" + s
    s = str(hour) + s
    if hour < 10:
        s = "0" + s
    return s


def seconds_to_text(seconds):
    if seconds < 45:
        return "now"

    if seconds > 584:
        # TODO: Show absolute time
        pass

    return str(int(((seconds - 45) / 60) + 1)) + "m"


def main():
    client = GraphQLClient(ENTUR_API)

    display.text(get_current_time_text())
    state = "time"
    while True:
        if state == "time":
            state = "departure"
            result = client.execute(
                query, variables={"quayid": "NSR:Quay:10851"})
            expectedDepartureTime_s = result["data"]["quay"]["estimatedCalls"][0]["expectedDepartureTime"]
            expectedDepartureTime = util.parse_iso8601(expectedDepartureTime_s)
            log.debug(expectedDepartureTime)

            departure_seconds = time.mktime(expectedDepartureTime + (0, 0))
            diff = departure_seconds - clock.gettime()
            display.text(seconds_to_text(diff))
        else:
            state = "time"
            display.text(get_current_time_text())

        machine.sleep(3000)


main()
