from src.CSPclass import CSP

class CourseCSP(CSP):
    def __init__(self, variables, courses, neighbors, constraints):

        """
        Construct Domains:
        
        courses is in the form 
        [
            [course_name, lecture_count, lab_count],
            ...
        ]

        We want to make domains a dict mapping all variables to a list of all lectures and labs, duplicates included
        We will then remove an item (lecture or lab) from the domain of all unassigned variables when it is assigned to another variable,
        and add it back to those domains when it is unassigned from a variable
        """

        items = []

        for courseData in courses:
            course_name = courseData[0]
            lecture_count = courseData[1]
            lab_count = courseData[2]

            for i in range(lecture_count):
                items.append(f'{course_name}-lc')

            for i in range(lab_count):
                items.append(f'{course_name}-lb')

        # If more variables than total items, add a None item for each extra variable
        for i in range(len(variables) - len(items)):
            items.append('None')

        # Initialize each variable's domain to the full items list
        domains = {}
        for var in variables:
            domains[var] = items

        super().__init__(variables, domains, neighbors, constraints)

    
    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any.
        Also remove the value from the domains of all unassigned variables"""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that. Also add the value to the domain"""
        if var in assignment:
            del assignment[var]