from src.locations import loc_A,loc_B

actionList = ['Right', 'Left', 'Suck', 'NoOp']

table =     {((loc_A, 'Clean'),): 'Right',
             ((loc_A, 'Dirty'),): 'Suck',
             ((loc_B, 'Clean'),): 'Left',
             ((loc_B, 'Dirty'),): 'Suck',
             ((loc_A, 'Dirty'), (loc_A, 'Clean')): 'Right',
             ((loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean')): 'Left',
             ((loc_A, 'Dirty'), (loc_A, 'Clean'), (loc_B, 'Dirty')): 'Suck',
             ((loc_B, 'Dirty'), (loc_B, 'Clean'), (loc_A, 'Dirty')): 'Suck'
            }


vacuumRules={((0, 0), 'Dirty'): 'Suck', 
       ((1, 0), 'Dirty'): 'Suck', 
       ((0, 0), 'Clean'): 'Right',
       ((1, 0), 'Clean'): 'Left'}


# Actions for Task1
cat_actions = ['Right', 'Left', 'Eat', 'Drink', 'Fight']

# Table for Task2
cat_table = {
  ((1, 'SausageHere'),): 'Eat',
  ((1, 'MilkHere'   ),): 'Drink',
  ((2, 'SausageHere'),): 'Eat',
  ((2, 'MilkHere'   ),): 'Drink',
  ((1, 'SausageHere'), (1, 'Empty')): 'Right',
  ((1, 'MilkHere'   ), (1, 'Empty')): 'Right',
  ((2, 'SausageHere'), (2, 'Empty')): 'Left',
  ((2, 'MilkHere'   ), (2, 'Empty')): 'Left',
  ((1, 'SausageHere'), (1, 'Empty'), (2, 'MilkHere'   ),): 'Drink',
  ((1, 'MilkHere'   ), (1, 'Empty'), (2, 'SausageHere'),): 'Eat',
  ((2, 'SausageHere'), (2, 'Empty'), (1, 'MilkHere'   ),): 'Drink',
  ((2, 'MilkHere'   ), (2, 'Empty'), (1, 'SausageHere'),): 'Eat',
}

# Rules for Task3

a2proRules={'Office manager': 'Give mail', 
'IT': 'Give donuts', 
'Student':'Give pizza',
'Clear':'Go ahead',
'Last room':'Stop'
}