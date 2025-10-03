from src.task3.CompanyEnvironmentClass import CompanyEnvironment
from src.task3.Task3Classes import Student, ITStaff, OfficeManager
from src.agents import ReflexAgentA2pro
import streamlit as st


def setup():
    ce=CompanyEnvironment()

    s=Student()
    i=ITStaff()
    o=OfficeManager()

    ce.add_thing(i)
    ce.add_thing(s)
    ce.add_thing(o)

    raTask3pro1=ReflexAgentA2pro()

    ce.add_thing(raTask3pro1)

    return ce


def display_info(company: CompanyEnvironment):
    agent = company.agents[0]
    st.info(f"Agent performance: {agent.performance}")
    st.info(f"State of the environment: {company.get_status()}.")
    st.info(f"Current step: {st.session_state["step"]}")


def drawBtn(e,a):
    option = [e,a]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    

def AgentStep(opt):
    e, a = opt[0], opt[1]

    if st.session_state["reset"]: # Reset on next button press if flag is on
        st.session_state["house"] = None
        st.session_state["reset"] = False
        return
    
    if not e.is_done():
        stepActs = e.step()
        st.success("Agent decided to do: {}.".format(",".join(stepActs)))
        st.session_state["step"] += 1
    else:
        if e.is_agent_alive(a):
            st.success("Cat Won!!!")
        else:
            st.error("Cat died :(")
        
        st.session_state['reset'] = True
    

def main():
    # Initialize reset flag if missing
    if "reset" not in st.session_state:
        st.session_state["reset"] = False

    # Initialize house if missing
    if "company" not in st.session_state:
        st.session_state["company"] = None

    company = st.session_state["company"]

    if company is None:
        company = setup()
        st.session_state["company"] = company
        st.session_state["step"] = 1 

    st.title('Lab 2 Task 2')

    display_info(company)

    drawBtn(company, company.agents[0])


if __name__ == '__main__':
    main()