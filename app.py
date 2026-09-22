import random
import time

import streamlit as st

from rand_question_v4.selector import rand_draw, rand_draw_no_repeat

FLASH_ROUNDS = 20
FLASH_DELAY_SECONDS = 0.15

if "roster" not in st.session_state:
    st.session_state.roster = []
if "question_list" not in st.session_state:
    st.session_state.question_list = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "current_pick" not in st.session_state:
    st.session_state.current_pick = None

st.title("Random Question Draw")

with st.form("add_name_form", clear_on_submit=True):
    new_name = st.text_input("Name")
    if st.form_submit_button("Add name") and new_name.strip():
        st.session_state.roster.append(new_name.strip())

with st.form("add_question_form", clear_on_submit=True):
    new_question = st.text_input("Question")
    if st.form_submit_button("Add question") and new_question.strip():
        st.session_state.question_list.append(new_question.strip())

st.subheader("Roster")
st.write(st.session_state.roster or "No names added yet.")

st.subheader("Questions")
st.write(st.session_state.question_list or "No questions added yet.")

no_repeats = st.checkbox("No repeats within this session")

col_draw, col_reset = st.columns(2)

with col_draw:
    if st.button("Draw"):
        if not st.session_state.roster or not st.session_state.question_list:
            st.error("Add at least one name and one question before drawing.")
            st.stop()

        # Blocking loop to render a ~3s flashing effect before the real pick.
        placeholder = st.empty()
        for _ in range(FLASH_ROUNDS):
            flash_name = random.choice(st.session_state.roster)
            flash_question = random.choice(st.session_state.question_list)
            placeholder.write(f"{flash_name}, please answer: {flash_question}")
            time.sleep(FLASH_DELAY_SECONDS)
        placeholder.empty()

        if no_repeats:
            chosen_name, chosen_question = rand_draw_no_repeat(
                random,
                st.session_state.roster,
                st.session_state.question_list,
                st.session_state.used_names,
                st.session_state.used_questions,
            )
            st.session_state.used_names.add(chosen_name)
            st.session_state.used_questions.add(chosen_question)
        else:
            chosen_name, chosen_question = rand_draw(
                random, st.session_state.roster, st.session_state.question_list
            )

        st.session_state.current_pick = (chosen_name, chosen_question)

with col_reset:
    if st.button("Reset"):
        st.session_state.roster = []
        st.session_state.question_list = []
        st.session_state.used_names = set()
        st.session_state.used_questions = set()
        st.session_state.current_pick = None

st.subheader("Result")
if st.session_state.current_pick:
    chosen_name, chosen_question = st.session_state.current_pick
    st.write(f"{chosen_name}, please answer: {chosen_question}")
else:
    st.write("No draw yet.")
