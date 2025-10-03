from src.agentPrograms import TableDrivenAgentProgram
from src.rules import cat_table
from src.task2.Task2Classes import Agent_Cat, Sausage, Milk
from src.task2.CatFriendlyHouse import CatFriendlyHouse
import streamlit as st


def setup():
    # Create Cat Agent Program and agent
    td_catAP = TableDrivenAgentProgram(cat_table)
    cat_agent = Agent_Cat(TableDrivenAgentProgram(cat_table))

    # Create house environment
    env = CatFriendlyHouse()

    # Create food items
    milk = Milk()
    sausage = Sausage()

    # Add everything to environment
    env.add_thing(cat_agent)
    env.add_thing(milk)
    env.add_thing(sausage)


def display_info(env: CatFriendlyHouse):
    cat = env.agents[0]
    st.info(f"Cat performance: {cat.performance}")
    st.info(f"State of the Environment: {env.get_status()}.")
    st.info(f"Current step: {st.session_state["step"]}")


def drawBtn(e,a):
    option = [e,a]
    st.button("Run One Agent's Step", on_click= AgentStep, args= [option])
    
def AgentStep(opt):
    e, a = opt[0], opt[1]
    
    if e.is_agent_alive(a):
        stepActs = e.step()
        st.success("Agent decided to do: {}.".format(",".join(stepActs)))
        st.session_state["step"] += 1
    

def main():
    # Initialize env if missing
    if "env" not in st.session_state:
        st.session_state["env"] = None

    env = st.session_state["env"]

    if env is None or env.is_done():

        # If is done, then agent just died
        if env is not None:
            st.error("Agent has died :(")

        env = setup()
        st.session_state["env"] = env
        st.session_state["step"] = 1 

    st.title('Lab 2 Task 2')

    display_info(env)

    drawBtn(env, env.agents[0])


if __name__ == '__main__':
    main()