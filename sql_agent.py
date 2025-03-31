from typing import Any 
from pydantic import BaseModel
from langchain.agents import create_sql_agent
from langchain.agents.agent import AgentExecutor
from langchain_agents.agents_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase

class SQLAgent(BaseModel):
    database: SQLDatabase
    llm_model: Any

    class Config:
        arbitrary_types_allowed = True

    def get_agent_toolkit(self)-> SQLDatabaseToolkit:
        """ Get SQL Database Toolkit"""
        return SQLDatabaseToolkit(db=self.database, llm=self.llm_model)
    
    def create_agent(self, memory: Any) -> AgentExecutor:
        """ Create an SQL Agent"""
        return create_sql_agent(
            prefix="",
            format_instructions= "",
            llm=self.llm_model,
            toolkit=self.get_agent_toolkit(),
            input_variables=["input", "agent_scratchpad", "history"],
            suffix= "",
            top_k=10,
            verbose=True,
            agent_executory_kwargs={"memory": memory, "handle_parsing_errors": True}
        )
