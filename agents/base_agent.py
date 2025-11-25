from core.adk_core import Agent
from core.state_manager import StateManager
from typing import Any
import logging

class BaseAgent(Agent):
    """
    Base Agent class for Stock Analysis System.
    Integrates with StateManager for shared memory.
    """
    def __init__(self, name: str, role: str, goal: str, backstory: str = "", tools: list = None):
        super().__init__(name=name, role=role, goal=goal, backstory=backstory, tools=tools)
        self.state_manager = StateManager()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, message: str):
        self.logger.info(message)

    def save_to_memory(self, key: str, value: Any):
        """Save data to shared memory."""
        self.state_manager.set(key, value)
        self.log(f"Saved to memory: {key}")

    def read_from_memory(self, key: str) -> Any:
        """Read data from shared memory."""
        return self.state_manager.get(key)
