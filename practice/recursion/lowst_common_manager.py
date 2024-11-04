def getLowestCommonManager(topManager, reportOne, reportTwo):
    # Write your code here.
    #
    result = []

    def _dfs(currentManager):
        if currentManager.name == reportOne.name:
            return True, False

        if currentManager.name == reportTwo.name:
            return False, True

        found_first, found_second = False, False
        for report in currentManager.directReports:
            first_in_report, second_in_report = _dfs(report)

            found_first = found_first or first_in_report
            found_second = found_second or second_in_report

            if found_first and found_second:
                if not result:
                    result.append(currentManager)
                break

        return found_first, found_second

    return _dfs(topManager)[0]


if __name__ == '__main__':
    pass