import logging

# Try to import Google ADK, otherwise provide a mock for development
try:
    import google.adk as adk
    from google.adk import Agent, Task
    print("Google ADK imported successfully.")
except ImportError:
    print("Google ADK not found. Using mock implementation.")
    
    class Agent:
        """Mock Agent class compatible with Google ADK interface."""
        def __init__(self, name: str, role: str, goal: str, backstory: str = "", tools: list = None, allow_delegation: bool = False, verbose: bool = True):
            self.name = name
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.tools = tools or []
            self.allow_delegation = allow_delegation
            self.verbose = verbose
            self.logger = logging.getLogger(name)

        def execute_task(self, task_description: str, context: dict = None) -> str:
            """Simulate task execution."""
            self.logger.info(f"Executing task: {task_description}")
            return f"Result from {self.name}"

    class Task:
        """Mock Task class."""
        def __init__(self, description: str, agent: Agent, expected_output: str = ""):
            self.description = description
            self.agent = agent
            self.expected_output = expected_output

        def execute(self, context: dict = None):
            return self.agent.execute_task(self.description, context)
