from src.agentClass import Agent
from src.rules import cat_actions
from src.agentPrograms import RandomAgentProgram
from src.task1.HouseEnvironment import HouseEnvironment
from src.task1.Task1Classes import *
import streamlit as st


def setup():
    # Create cat agent
    cat_program = RandomAgentProgram(cat_actions)
    cat_agent = Agent(cat_program)

    # Create house environment
    house = HouseEnvironment()

    # Create other things
    dog = Dog()
    mouse = Mouse()
    milk = Milk()

    # Add Everything to house environment
    house.add_thing(cat_agent)
    house.add_thing(dog)
    house.add_thing(mouse)
    house.add_thing(milk)

    return house


def display_info(house: HouseEnvironment):
    cat = house.agents[0]
    st.info(f"Cat performance: {cat.performance}")
    st.info(f"State of the Environment: {house.get_status()}.")
    st.info(f"Current step: {st.session_state["step"]}")


def drawBtn(e,a):
    option = [e,a]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    e, a = opt[0], opt[1]
    
    if e.is_agent_alive(a):
        stepActs = e.step()
        st.success("Agent decided to do: {}.".format(",".join(stepActs)))
    else:
        st.error("Agent in location {} and it is dead.".format(a.location))
        
    st.session_state["step"] += 1


def main():
    # Initialize house if missing
    if "house" not in st.session_state:
        st.session_state["house"] = None

    house = st.session_state["house"]

    if house is None or house.is_done():
        house = setup()
        st.session_state["house"] = house
        st.session_state["step"] = 1 

    st.title('Lab 2 Task 1')

    display_info(house)

    drawBtn(house, house.agents[0])


if __name__ == '__main__':
    main()