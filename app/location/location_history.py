class CurrentLocation:
    """
    現在地点
    """

    def __init__(self, current_point: list):
        self.current_point = current_point


class StartLocation:
    """
    スタート地点特有の処理
    """

    def __init__(self, start_point: list):
        self.start_point = start_point


class EndLocation:
    """
    最終地点
    """

    def __init__(self, end_point: list):
        self.end_point = end_point


class NextLocation:
    """
    次の目指す地点
    """

    def __init__(self, next_point):
        self.next_point = next_point


class VisitedLocation:
    """
    通った地点
    """

    def __init__(self, visited_point):
        self.visited_point = visited_point
