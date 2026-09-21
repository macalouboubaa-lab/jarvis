from collections.abc import Mapping

from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config import settings
from agent.context import current_user_id
from agent.prompts import JARVIS_SYSTEM_PROMPT
from agent.tools.memory_tools import remember, recall
from agent.tools.job_tools import search_jobs, apply_job
from agent.tools.course_tools import update_course
from agent.tools.code_tools import analyze_code

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=settings.OPENAI_API_KEY
)

tools = [remember, recall, search_jobs, apply_job, update_course, analyze_code]

prompt = ChatPromptTemplate.from_messages([
    ("system", JARVIS_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def to_langchain_messages(
    rows: list[Mapping[str, object]],
) -> list[BaseMessage]:
    messages: list[BaseMessage] = []

    for row in rows:
        sender = row.get("sender")
        content = row.get("content")

        if not isinstance(content, str) or not content:
            continue

        if sender == "user":
            messages.append(HumanMessage(content=content))
        elif sender == "assistant":
            messages.append(AIMessage(content=content))

    return messages


async def ask_jarvis(
    user_message: str,
    user_id: str,
    history: list[BaseMessage] | None = None,
) -> str:
    token = current_user_id.set(user_id)
    try:
        result = await agent_executor.ainvoke({
            "input": user_message,
            "chat_history": history or []
        })
        return result["output"]
    finally:
        current_user_id.reset(token)
