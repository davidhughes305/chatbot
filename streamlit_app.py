import streamlit as st
import openai
import asyncio
from agents import Agent, Runner, WebSearchTool, trace

# Initialize OpenAI API key (you can also store it in secrets)
openai.api_key = st.text_input("OpenAI API Key", type="password")

# Show title and description.
st.title("💬 AI Interview Coach")
st.write("Welcome to your custom AI Interview Coach!")

# Collect Job Title, Employer, and Resume Input
job_title = st.text_input("Enter the Job Title you're preparing for", "Vice President of Operations")
employer = st.text_input("Enter the Employer's Name", "First Health, Moore Hospital, Pinehurst, NC")
resume = st.text_area("Enter your Resume (or copy-paste text)", "Your resume text goes here.")

# Asynchronous method to generate interview questions
async def generate_interview_question(job_title, employer, resume):
    context = f"Generate a concise interview question for a {job_title} position at {employer}. Customize it based on the following resume:\n{resume}"
    agent = Agent(
        name="Interview Question Generator",
        instructions="You are a helpful assistant generating one concise interview question.",
        model="gpt-4o-mini",
        tools=[],
    )
    with trace("Interview question generation"):
        result = await Runner.run(agent, context)
    return result.final_output

# Asynchronous method to evaluate user's answer
async def evaluate_answer(answer, job_title, employer, resume):
    context = f"Provide feedback on the following answer for a {job_title} position at {employer}, considering the resume: {resume}\nAnswer: {answer}"
    agent = Agent(
        name="Answer Evaluator",
        instructions="You are an evaluator providing one sentence of positive feedback and one sentence of constructive feedback to each interview answer.",
        model="gpt-4o-mini",
        tools=[],
    )
    with trace("Answer evaluation"):
        result = await Runner.run(agent, context)
    return result.final_output

# Start Interview Session
async def interview_session(job_title, employer, resume):
    while True:
        question = await generate_interview_question(job_title, employer, resume)
        st.write(f"Interview Question: {question}")

        # Capture user answer
        user_answer = st.text_input("Your Answer (type 'exit' to quit):")
        if user_answer.lower() == 'exit':
            break

        # Evaluate the answer
        feedback = await evaluate_answer(user_answer, job_title, employer, resume)
        st.write(f"Feedback: {feedback}")

if openai.api_key:
    # When the API key is provided, initiate the interview session
    if job_title and employer and resume:
        asyncio.run(interview_session(job_title, employer, resume))
else:
    st.info("Please enter a valid OpenAI API Key.")
