from src.agentPrograms import TableDrivenAgentProgram
from src.rules import cat_table
from src.task2.Task2Classes import Agent_Cat, Sausage, Milk
from src.task2.CatFriendlyHouse import CatFriendlyHouse
import streamlit as st


def setup():
    # Create Cat Agent Program and agent
    td_catAP = TableDrivenAgentProgram(cat_table)
    cat_agent = Agent_Cat(td_catAP)

    # Create house environment
    house = CatFriendlyHouse()

    # Create food items
    milk = Milk()
    sausage = Sausage()

    house.add_thing(cat_agent)
    house.add_thing(milk)
    house.add_thing(sausage)

    return house


def display_info(house: CatFriendlyHouse):
    cat = house.agents[0]
    st.info(f"Cat performance: {cat.performance}")
    st.info(f"State of the environment: {house.get_status()}.")
    st.info(f"Current step: {st.session_state['step']}")


def drawBtn(e,a):
    option = [e,a]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    e, a = opt[0], opt[1]
    
    if not e.is_done():
        stepActs = e.step()
        st.success("Agent decided to do: {}.".format(",".join(stepActs)))
        st.session_state["step"] += 1
    else:
        if e.is_agent_alive(a):
            st.success("Cat Won!!!")
        else:
            st.error("Cat died :(")
        
        st['reset'] = True


def main():
    # Initialize house if missing
    if "house" not in st.session_state:
        st.session_state["house"] = None

    house = st.session_state["house"]

    st.session_state['reset'] = False

    if house is None or st.session_state['reset']:
        house = setup()
        st.session_state["house"] = house
        st.session_state["step"] = 1 

    st.title('Lab 2 Task 2')

    display_info(house)

    drawBtn(house, house.agents[0])


if __name__ == '__main__':
    main()