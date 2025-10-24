1. Specify variables
2. Specify domains
3. Define constraints

CSPBasic class has 2 different properties for domains
`domains` has the original domains and does not change from propagation
- This is saved so we can run different propagation algorithms on the original domain so it's good to save
`curr_domains` has current domains that does change from propagation

Look at ...v2.py for the streamlit
- Not the copy