from src.CSPclass import CSP

class CourseCSP(CSP):
    def __init__(self, variables, domains, neighbors, constraints, amountsDict):
        """
        amountsDict is in the form {
            item_name: amount,
            ...
        }
        Where each item is a lecture or lab
        """

        self.amountsDict = amountsDict

        super().__init__(variables, domains, neighbors, constraints)


    def nconflicts(self, var, val, assignment):
        # Find out how many of this item are in the current assignment
        current_item_count = sum(
            1 for (k, v) in assignment.items()
            if v == val and k != var
        ) + 1

        amountConflictCount = 0
        # Add 1 conflict for each variable that shares this value over or under the limit
        amountConflictCount += abs(current_item_count - self.amountsDict[val])

        return super().nconflicts(var, val, assignment) + amountConflictCount