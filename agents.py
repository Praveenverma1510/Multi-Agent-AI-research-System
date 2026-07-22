from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


# first agent


def build_search_agent():
    return create_agent(model=llm, tools=[web_search])


# second agent


def build_reader_agent():
    return create_agent(model=llm, tools=[scrape_url])


# writer chain

write_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "ai",
            "You are an expert research writer. Write clear, structured and insightful reports.",
        ),
        (
            "human",
            """ Write a detailed reseach report on the topic below.
     
     Topic: {topic}
     
     Research Gathered:
     {research}
     
     Structure the report as:
     - Introduction
     - Key findings (minimum 3 well-explained points)
     - Conclusion
     - Sources (list all URLs found in the research)
     
     Be detailed, factual and professional.
     """,
        ),
    ]
)

parser = StrOutputParser()

writer_chain = write_prompt | llm | parser

# Critic Chain

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "ai",
            "You are a sharp and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """ Review the research report below and evaluate it strictly.
     
     Report:
     {report}
     
     Respond in this exact format:
     
     Score: X/10
     
     Strengths:
     
     - ...
     - ...
     
     Areas to improve:
     
     - ...
     - ...
     
     One line verdict:
     ...
     """,
        ),
    ]
)

critic_chain = critic_prompt | llm | parser
