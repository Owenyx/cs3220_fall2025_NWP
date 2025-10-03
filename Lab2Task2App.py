from src.agentPrograms import TableDrivenAgentProgram
from src.rules import cat_table
from src.task2.Task2Classes import Agent_Cat, Sausage, Milk
from src.task2.CatFriendlyHouse import CatFriendlyHouse
import streamlit as st

from PIL import Image


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


def getImg(string):
    if string == 'cat':
        return 'imgs/cat.jpg'
    if string == 'sausage':
        return 'imgs/sausage.jpg'
    if string == 'milk':
        return 'imgs/milk.jpg'

def display_info(house: CatFriendlyHouse):
    cat = house.agents[0]
    st.info(f"Cat performance: {cat.performance}")

    # Get the original status string
    status = house.get_status().lower()

    # Replace keywords with inline images using Markdown
    def img_md(name):
        return f"![{name}]({getImg(name)})"

    status = status.replace("<agent_cat>", img_md("cat"))
    status = status.replace("<Sausage>", img_md("sausage"))
    status = status.replace("<Milk>", img_md("milk"))

    # Display using markdown so images render
    st.markdown(f"**State of the environment:** {status}", unsafe_allow_html=True)

    st.info(f"Current step: {st.session_state['step']}")


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
    if "house" not in st.session_state:
        st.session_state["house"] = None

    house = st.session_state["house"]

    if house is None:
        house = setup()
        st.session_state["house"] = house
        st.session_state["step"] = 1 

    st.title('Lab 2 Task 2')

    display_info(house)

    drawBtn(house, house.agents[0])


if __name__ == '__main__':
    main()