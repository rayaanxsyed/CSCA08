CA"""Program for formatting and assigning values to Ontario Bridges"""
import csv
from copy import deepcopy
from math import sin, cos, asin, radians, sqrt, inf
from typing import TextIO

from constants import (
    ID_INDEX, NAME_INDEX, HIGHWAY_INDEX, LAT_INDEX,
    LON_INDEX, YEAR_INDEX, LAST_MAJOR_INDEX,
    LAST_MINOR_INDEX, NUM_SPANS_INDEX,
    SPAN_DETAILS_INDEX, LENGTH_INDEX,
    LAST_INSPECTED_INDEX, BCIS_INDEX, FROM_SEP, TO_SEP,
    HIGH_PRIORITY_BCI, MEDIUM_PRIORITY_BCI,
    LOW_PRIORITY_BCI, HIGH_PRIORITY_RADIUS,
    MEDIUM_PRIORITY_RADIUS, LOW_PRIORITY_RADIUS,
    EARTH_RADIUS)
EPSILON = 0.01

LEVELS = [(HIGH_PRIORITY_BCI, HIGH_PRIORITY_RADIUS),
          (MEDIUM_PRIORITY_BCI, MEDIUM_PRIORITY_RADIUS),
          (LOW_PRIORITY_BCI, LOW_PRIORITY_RADIUS)]


# We provide this function for you to use as a helper.
def read_data(csv_file: TextIO) -> list[list[str]]:
    """Read and return the contents of the open CSV file csv_file as a
    list of lists, where each inner list contains the values from one
    line of csv_file.

    Docstring examples not given since the function reads from a file.

    """
    lines = csv.reader(csv_file)
    return list(lines)[2:]


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.

    >>> abs(calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    ...     - 0.338) < EPSILON
    True
    >>> abs(calculate_distance(43.42, -79.24, 53.32, -113.30)
    ...     - 2713.226) < EPSILON
    True
    """

    lat1, lon1, lat2, lon2 = (radians(lat1), radians(lon1),
                              radians(lat2), radians(lon2))

    haversine = (sin((lat2 - lat1) / 2) ** 2
                 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2)

    return round(2 * EARTH_RADIUS * asin(sqrt(haversine)), 3)


# We provide this sample data to help you set up example calls.
THREE_BRIDGES_UNCLEANED = [
    ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403', '43.167233',
     '-80.275567', '1965', '2014', '2009', '4',
     'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', '72.3', '',
     '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9',
     ''],
    ['1 -  43/', 'WEST STREET UNDERPASS', '403', '43.164531', '-80.251582',
     '1963', '2014', '2007', '4',
     'Total=60.4  (1)=12.2;(2)=18;(3)=18;(4)=12.2;', '61', '04/13/2012',
     '71.5', '', '71.5', '', '68.1', '', '69', '', '69.4', '', '69.4', '',
     '70.3', '73.3', ''],
    ['2 -   4/', 'STOKES RIVER BRIDGE', '6', '45.036739', '-81.33579', '1958',
     '2013', '', '1', 'Total=16  (1)=16;', '18.4', '08/28/2013', '85.1',
     '85.1', '', '67.8', '', '67.4', '', '69.2', '70', '70.5', '', '75.1', '',
     '90.1', '']
]

THREE_BRIDGES = [
    [1, 'Highway 24 Underpass at Highway 403', '403', 43.167233, -80.275567,
     '1965', '2014', '2009', 4, [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
     [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
     '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
     [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
     '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
     [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]
]


# We provide the header and doctring for this function to help get you
# started.
def get_bridge(bridge_data: list[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridge data
    bridge_data. If there is no bridge with id bridge_id, return [].

    >>> result = get_bridge(THREE_BRIDGES, 1)
    >>> result == [
    ...    1, 'Highway 24 Underpass at Highway 403', '403', 43.167233,
    ...    -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
    ...    [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    >>> get_bridge(THREE_BRIDGES, 42)
    []
    """
    for item in bridge_data:
        if item[ID_INDEX] == bridge_id:
            return item
    return []


def get_average_bci(bridge_data: list[list], bridge_id: int) -> float:
    """Return the average bci for the bridge with id bridge_id from 
    bridge_data.
    
    >>> get_average_bci(THREE_BRIDGES, 1)
    70.8857
    >>> get_average_bci(THREE_BRIDGES, 55)
    0
    """
    if get_bridge(bridge_data, bridge_id) == []:
        return 0

    bridge = get_bridge(bridge_data, bridge_id)
    average = 0
    for num in bridge[BCIS_INDEX]:
        average = num + average
    return round(average / len(bridge[BCIS_INDEX]), 4)


def get_total_length_on_hwy(bridge_data: list[list], hwy: str) -> float:
    """Return the total length on the given highway hwy from a bridge in 
    bridge_data.
    
    >>> get_total_length_on_hwy(THREE_BRIDGES, '403')
    126.0
    >>> get_total_length_on_hwy(THREE_BRIDGES, '401')
    0.0
    """
    total_length = 0.0
    for bridge in bridge_data:
        if bridge[HIGHWAY_INDEX] == hwy:
            total_length += bridge[LENGTH_INDEX]
    return total_length


def get_distance_between(bridge1: list, bridge2: list) -> int:
    """Returns the distance between two bridges, bridge1 and bridge2.
    
    >>> get_distance_between(THREE_BRIDGES[0], THREE_BRIDGES[1])
    1.968
    >>> get_distance_between(THREE_BRIDGES[0], THREE_BRIDGES[2])
    224.451
    """
    lat1 = bridge1[LAT_INDEX]
    lon1 = bridge1[LON_INDEX]
    lat2 = bridge2[LAT_INDEX]
    lon2 = bridge2[LON_INDEX]
    return round(calculate_distance(lat1, lon1, lat2, lon2), 3)


def get_closest_bridge(bridge_data: list[list], bridge_id: int) -> int:
    """Returns the ID of the closest bridge in bridge_data
    given another bridge id bridge_id. The function will not return the 
    closest distance itself. Returns -1 if does not exist.
    
    >>> get_closest_bridge(THREE_BRIDGES, 1)
    2
    >>> get_closest_bridge(THREE_BRIDGES, 2)
    1
    """
    closest_bridge = {}
    for bridge in bridge_data:
        if bridge[ID_INDEX] != bridge_id:
            distance = get_distance_between(bridge_data[bridge_id - 1], bridge)
            closest_bridge[bridge[ID_INDEX]] = distance
    lowest_val = min(closest_bridge.values())
    for num, dist in closest_bridge.items():
        if dist == lowest_val:
            return num
    return -1


def get_bridges_with_bci_below(bridge_data: list[list], bridge_ids: list[int],
                               bci: float) -> list[int]:
    """Returns a list of the bridges in bridge_data given the bridge ids 
    bridge_ids that are lower than bci.
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [1,2], 72)
    [2]
    >>> get_bridges_with_bci_below(THREE_BRIDGES, [2,3], 65)
    []
    """
    bci_below = []

    for bridge in bridge_data:
        if bridge[ID_INDEX] in bridge_ids:
            if bridge[BCIS_INDEX] and bridge[BCIS_INDEX][0] <= bci:
                bci_below.append(bridge[ID_INDEX])

    return bci_below


def get_bridges_containing(bridge_data: list[list], search: str) -> list[int]:
    """Returns the the bridges in bridge_data which have the keywords of 
    search. The function is not case sensitive.
    
    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> get_bridges_containing(bridges, 'underpass')
    [1, 2]
    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> get_bridges_containing(bridges, 'pass')
    [1, 2]
    """
    ids = []
    new_bridge_data = []
    search = search.lower()
    for bridge in bridge_data:
        bridge[NAME_INDEX] = bridge[NAME_INDEX].lower()
        new_bridge_data.append(bridge)

    for bridge in new_bridge_data:
        for item in bridge:
            if search in str(item):
                ids.append(bridge[ID_INDEX])
    return ids


def get_bridges_in_radius(bridge_data: list[list], lat: float, lon: float,
                          radius: float) -> list[int]:
    """Returns the bridges in radius given bridge_data, coordinates of lat and
    lon, and radius.
    
    >>> get_bridges_in_radius(THREE_BRIDGES, 43.10, -80.15, 50)
    [1, 2]
    >>> get_bridges_in_radius(THREE_BRIDGES, 50.2, -74.3, 30)
    []
    """
    result = []
    for bridge in bridge_data:
        bridge_lat = bridge[LAT_INDEX]
        bridge_lon = bridge[LON_INDEX]
        distance = calculate_distance(lat, lon, bridge_lat, bridge_lon)
        if distance <= radius:
            result.append(bridge[ID_INDEX])
    return result


def assign_inspectors(bridge_data: list[list], inspectors: list[list[float]],
                      max_bridges: int) -> list[list[int]]:
    """Return a list of bridge IDs from bridge data bridge_data, to be
    assigned to each inspector in inspectors. inspectors is a list
    containing (latitude, longitude) pairs representing each
    inspector's location. At most max_bridges are assigned to each
    inspector, and each bridge is assigned once (to the first
    inspector that can inspect that bridge).

    See the "Assigning Inspectors" section of the handout for more details.

    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15], [42.10, -81.15]], 0)
    [[], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 1)
    [[1]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 2)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.10, -80.15]], 3)
    [[1, 2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 1)
    [[1], [2]]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [43.10, -80.15]], 2)
    [[1, 2], []]
    >>> assign_inspectors(THREE_BRIDGES, [[43.20, -80.35], [45.0368, -81.34]],
    ...                   2)
    [[1, 2], [3]]
    >>> assign_inspectors(THREE_BRIDGES, [[38.691, -80.85], [43.20, -80.35]],
    ...                   2)
    [[], [1, 2]]
    """
    if max_bridges == 0:
        return [[] for number in inspectors]

    assigned_bridges = {i: [] for i in
                        range(len(inspectors))}
    eligible_bridges = [possible_bridge[ID_INDEX]
                        for possible_bridge in bridge_data]
    for index, inspector in enumerate(inspectors):
        inspection = (index, inspector, eligible_bridges,
                      assigned_bridges, max_bridges, LEVELS, bridge_data)
        assign_bridge_to_inspector(inspection)

    return [assigned_bridges[i] for i in range(len(inspectors))]


def can_assign_bridge(inspector: list[float], bridge: list, bci: int,
                      radius: int) -> bool:
    """Returns True or False for the inspector values inspector, given
    the bridge bridge, and if it's lower than radius radius and bci bci.
    >>> can_assign_bridge([43.10, -80.15], THREE_BRIDGES[0], 50, 60)
    False
    >>> can_assign_bridge([43.10, -80.15], THREE_BRIDGES[0], 150, 300)
    True
    >>>
    """
    return (calculate_distance(inspector[0], inspector[1], bridge[LAT_INDEX],
            bridge[LON_INDEX]) <= radius and bridge[BCIS_INDEX][0] <= bci)


def assign_bridge_to_inspector(inspection: list) -> None:
    """Returns an updated list where bridges is assigned to inspectors given
    all the inspection data inspection. This works as a helper function
    for assign_inspectors.
    
    Docstring examples not included as the function does not modify or return
    any value, only used to update eligible bridges in function 
    assign_inspectors.
    """
    (index, inspector, eligible_bridges, assigned_bridges,
     max_bridges, levels, bridge_data) = inspection
    for bridge_id in eligible_bridges[:]:
        bridge = bridge_data[bridge_id - 1]
        if any(can_assign_bridge(inspector, bridge, bci, radius) for bci,
               radius in levels):
            assigned_bridges[index].append(bridge_id)
            eligible_bridges.remove(bridge_id)
            max_bridges -= 1
            if max_bridges <= 0:
                break

# We provide the header and doctring for this function to help get you
# started. Note the use of the built-in function deepcopy (see
# help(deepcopy)!): since this function modifies its input, we do not
# want to call it with THREE_BRIDGES, which would interfere with the
# use of THREE_BRIDGES in examples for other functions.


def inspect_bridges(bridge_data: list[list], bridge_ids: list[int], date: str,
                    bci: float) -> None:
    """Update the bridges in bridge_data with id in bridge_ids with the new
    date and BCI score for a new inspection.

    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> inspect_bridges(bridges, [1], '09/15/2018', 71.9)
    >>> bridges == [
    ...   [1, 'Highway 24 Underpass at Highway 403', '403',
    ...    43.167233, -80.275567, '1965', '2014', '2009', 4,
    ...    [12.0, 19.0, 21.0, 12.0], 65, '09/15/2018',
    ...    [71.9, 72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]],
    ...   [2, 'WEST STREET UNDERPASS', '403', 43.164531, -80.251582,
    ...    '1963', '2014', '2007', 4, [12.2, 18.0, 18.0, 12.2],
    ...    61, '04/13/2012', [71.5, 68.1, 69.0, 69.4, 69.4, 70.3, 73.3]],
    ...   [3, 'STOKES RIVER BRIDGE', '6', 45.036739, -81.33579,
    ...    '1958', '2013', '', 1, [16.0], 18.4, '08/28/2013',
    ...    [85.1, 67.8, 67.4, 69.2, 70.0, 70.5, 75.1, 90.1]]]
    True
    """
    new_bridge_data = []
    for bridge in bridge_data:
        if bridge[ID_INDEX] in bridge_ids:
            bridge[LAST_INSPECTED_INDEX] = date
            bridge[BCIS_INDEX].insert(0, bci)
            new_bridge_data.append(bridge)
    bridge_data = new_bridge_data


def add_rehab(bridge_data: list[list], bridge_id: int, date: str, major:
              bool) -> None:
    """Returns given id bridge_id in the bridge in bridge_data given 
    the new rehab date date and if the rehab is major major.
    
    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> add_rehab(bridges, 1, '09/15/2023', False)
    >>> bridges[0] == [1, 'Highway 24 Underpass at Highway 403', '403', 
    ...               43.167233, -80.275567, '1965', '2014', '2023', 4,
    ...               [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', [72.3, 69.5, 
    ...               70.0, 70.3, 70.5, 70.7, 72.9]]
    True
    
    >>> bridges = deepcopy(THREE_BRIDGES)
    >>> add_rehab(bridges, 1, '09/15/2023', True)
    >>> bridges[0] == [1, 'Highway 24 Underpass at Highway 403', '403', 
    ...               43.167233, -80.275567, '1965', '2014', '2023', 4,
    ...               [12.0, 19.0, 21.0, 12.0], 65, '04/13/2012', [72.3, 69.5, 
    ...               70.0, 70.3, 70.5, 70.7, 72.9]]
    False
    """
    for bridge in bridge_data:
        if bridge[ID_INDEX] == bridge_id:
            if major:
                bridge[LAST_MAJOR_INDEX] = date[-4:]
            else:
                bridge[LAST_MINOR_INDEX] = date[-4:]


# We provide the header and doctring for this function to help get you started.
def format_data(data: list[list[str]]) -> None:
    """Modify the uncleaned bridge data data, so that it contains proper
    bridge data, i.e., follows the format outlined in the 'Data
    formatting' section of the assignment handout.

    >>> d = deepcopy(THREE_BRIDGES_UNCLEANED)
    >>> format_data(d)
    >>> d == THREE_BRIDGES
    True
    """
    count = 1
    updated_bridges = []

    for bridge in data:
        bridge[ID_INDEX] = count
        format_spans(bridge)
        format_length(bridge)
        format_bcis(bridge)
        format_location(bridge)
        updated_bridges.append(bridge)
        count = count + 1
    data.clear()
    data.extend(updated_bridges)


# This is a suggested helper function for format_data. We provide the
# header and doctring for this function to help you structure your
# solution.
def format_location(bridge_record: list) -> None:
    """Format latitude and longitude data in the bridge record bridge_record.

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_location(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           43.167233, -80.275567, '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    """
    lon = float(bridge_record[LON_INDEX])
    lat = float(bridge_record[LAT_INDEX])
    bridge_record[LON_INDEX] = lon
    bridge_record[LAT_INDEX] = lat


def format_spans(bridge_record: list) -> None:
    """Format the bridge spans data in the bridge record bridge_record.

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_spans(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', 4,
    ...           [12.0, 19.0, 21.0, 12.0], '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    True
    """
    spans_string = bridge_record[SPAN_DETAILS_INDEX]
    span_parts = str(spans_string).split(';')
    spans = []
    for part in span_parts:
        if '(' in part:
            span_value = float(part.split(')=')[-1])
            spans.append(span_value)

    bridge_record[SPAN_DETAILS_INDEX] = spans
    bridge_record[NUM_SPANS_INDEX] = len(spans)


def format_length(bridge_record: list) -> None:
    """Format the bridge length data in the bridge record bridge_record.

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_length(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...            '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...            'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', 65, '04/13/2012',
    ...            '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...            '70.5', '', '70.7', '72.9', '']
    True

    """
    if bridge_record[LENGTH_INDEX] == '':
        bridge_record[LENGTH_INDEX] = 0.0
    bridge_record[LENGTH_INDEX] = float(bridge_record[LENGTH_INDEX])


# This is a suggested helper function for format_data. We provide the
# header and doctring for this function to help you structure your
# solution.

def format_bcis(bridge_record: list) -> None:
    """Format the bridge BCI data in the bridge record bridge_record.

    >>> record = ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '',
    ...           '70.5', '', '70.7', '72.9', '']
    >>> format_bcis(record)
    >>> record == ['1 -  32/', 'Highway 24 Underpass at Highway 403', '403',
    ...           '43.167233', '-80.275567', '1965', '2014', '2009', '4',
    ...           'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012',
    ...           [72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    True

    """
    bcis_data = []
    updated_bridge = bridge_record[BCIS_INDEX + 1:]
    for num in updated_bridge:
        if num != '':
            bcis_data.append(float(num))
    del bridge_record[BCIS_INDEX + 1:]
    bridge_record[LAST_INSPECTED_INDEX + 1] = bcis_data


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # with open('bridge_data.csv', encoding='utf-8') as bridge_data_file:
    # BRIDGES = read_data(bridge_data_file)
    # format_data(BRIDGES)
    # For example:
    # print(get_bridge(BRIDGES, 3))
    # EXPECTED = [3, 'NORTH PARK STEET UNDERPASS', '403', 43.165918, -80.263791,
    #             '1962', '2013', '2009', 4, [12.2, 18.0, 18.0, 12.2], 60.8,
    #             '04/13/2012', [71.4, 69.9, 67.7, 68.9, 69.1, 69.9, 72.8]]
    # print('Testing get_bridge: ', get_bridge(BRIDGES, 3) == EXPECTED)
