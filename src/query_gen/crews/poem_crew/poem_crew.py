from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.custom_tool import query_executer, idu_query_executer

@CrewBase
class MainAgent:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def main_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["main_agent"],
        )
    @task
    def main_task(self) -> Task:
        return Task(
            config=self.tasks_config["main_task"],
            agent=self.main_agent(),
            # human_input=True
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class GeneralQA:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def general_qa_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["general_qa_agent"],
        )
    @task
    def general_qa_task(self) -> Task:
        return Task(
            config=self.tasks_config["general_qa_task"],
            agent=self.general_qa_agent(),
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class QueryCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def query_gen_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["database_agent"],
        )
    @task
    def query_gen_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_sql_task"],
            agent=self.query_gen_agent(),
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
@CrewBase
class QueryGenCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def query_executer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["generate_human_language"],
            tools=[query_executer],
        )
    @task
    def query_executer_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_human_language_task"],
            agent=self.query_executer_agent(),
            # human_input=True,
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
    
@CrewBase
class IDUGenCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def idu_executer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["generate_human_language"],
            tools=[idu_query_executer],
        )
    @task
    def idu_executer_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_human_language_task"],
            agent=self.idu_executer_agent(),
            # human_input=True,
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )