import os 
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner, 
    RunConfig, 
    OpenAIChatCompletionsModel, 
    AsyncOpenAI,
    handoff, 
    RunContextWrapper
)
import chainlit as cl
from typing import cast



load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

@cl.on_chat_start
async def on_chat_start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )   

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )


    def on_handoff(agent: Agent , ctx: RunContextWrapper[None]):
        agent = agent.name
        print("-----------------")
        print(f"Handing off to {agent}....")
        print("-----------------")
        cl.Message(
            content=f"Handing off to {agent}....**\n\nI'm transferring your request to our {agent} who will be able to better assists you.",
            author="System"
        ).send()


    billing_agent = Agent(
        name="Billing Agent",
        instructions="""You are a billing support agent for an internet service provider. 
        Your job is to help customers understand their bills, explain charges, check payment status, and assist with payment issues or discrepancies.
        Be clear, accurate, and polite.""",
    )

    complaint_agent = Agent(
        name="Complaint Agent",
        instructions="""
        You are a customer care agent responsible for handling complaints. Listen empathetically, 
        log the customer's issue, offer solutions when possible, and escalate when necessary. 
        Your tone should be calm, professional, and supportive.
        """,
    )

    plan_agent = Agent(
        name="Plan Agent",
        instructions="""
        You assist customers with information about internet plans and packages. 
        Provide details about speed, price, data limits, and promotions.
        Help users compare and upgrade plans based on their needs.
        """,
   
    )

    connection_agent = Agent(
        name= "Connection Agent",
        instructions="""
        You help customers with connection-related issues.
        Diagnose internet problems, guide them through basic troubleshooting, check for outages, and book technicians if needed.
        Keep instructions simple and step-by-step.
        """,
   
)

    general_query_agent = Agent(
        name="General Query Agent",
        instructions="""
        You are a general help assistant.
        Answer basic questions about the company, services, account details, support hours, and more. 
        If a query falls into another category (billing, connection, etc.), redirect to the correct agent.""",
  
)



    triage_agent = Agent(
        name="Triage Agent",
        instructions="""
        You are a triage agent for an internet service provider. 
        Your job is to understand the user's question and decide which department (agent) should handle it. 
        You do not answer the question yourself — you only classify it and route it to the right agent.

        The available agents are:

        billing: For payment, charges, refunds, due dates.

        complaints: For service dissatisfaction, repeated issues, or customer grievances.

        plans: For plan upgrades, downgrades, speed comparisons, and offers.

        connection: For technical support, internet not working, router issues, or outages.

        general: For anything else, like business hours, contact info, or account setup.

        Be accurate and fast. If it's unclear, route to general.
        And if the query is complex and not related to any agents then send it to human support.
        """,
        handoffs=[
            handoff(billing_agent, on_handoff= lambda ctx : on_handoff(billing_agent , ctx)),
            handoff(complaint_agent, on_handoff=lambda ctx: on_handoff(complaint_agent, ctx)),
            handoff(plan_agent, on_handoff=lambda ctx: on_handoff(plan_agent , ctx)),
            handoff(connection_agent, on_handoff=lambda ctx: on_handoff(connection_agent, ctx)),
            handoff(general_query_agent, on_handoff=lambda ctx: on_handoff(general_query_agent, ctx))
        ],
  
    )


    cl.user_session.set("triage_agent" , triage_agent)
    cl.user_session.set("config", config)
    cl.user_session.set("billing_agent", billing_agent)
    cl.user_session.set("complaint_agent", complaint_agent)
    cl.user_session.set("plan_agent", plan_agent)
    cl.user_session.set("connection_agent", connection_agent)
    cl.user_session.set("general_query_agent", general_query_agent)
    cl.user_session.set("chat_history" , [])


    await cl.Message(
        content="Hello! I'm your customer support agent. How can I help you today?",
        author="System"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Thinking...", author="System")
    await msg.send()


    triage_agent =cast(Agent , cl.user_session.get("triage_agent"))
    config = cast(RunConfig, cl.user_session.get("config"))

    history =  cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    try:
        result= Runner.run_sync(triage_agent, history , run_config=config)

        response_content = result.final_output

        msg.content = response_content

        await msg.update()


        history.append({"role": "assistant", "content": response_content})


        cl.user_session.set("chat_history", history)
        print(f"History: {history}")

    
    except Exception as e:
        msg.content = "Sorry, I encountered an error. Please try again."
        await msg.update()
        print(f"Error: {e}")
