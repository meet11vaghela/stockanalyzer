import threading
from typing import Any, Dict, Optional

class StateManager:
    """
    Thread-safe shared memory/state manager for multi-agent collaboration.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(StateManager, cls).__new__(cls)
                    cls._instance._state = {}
                    cls._instance._state_lock = threading.Lock()
        return cls._instance

    def set(self, key: str, value: Any):
        """Set a value in the shared state."""
        with self._state_lock:
            self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the shared state."""
        with self._state_lock:
            return self._state.get(key, default)

    def update(self, key: str, value: Any):
        """Update a dictionary or list in the shared state."""
        with self._state_lock:
            if key in self._state:
                if isinstance(self._state[key], dict) and isinstance(value, dict):
                    self._state[key].update(value)
                elif isinstance(self._state[key], list) and isinstance(value, list):
                    self._state[key].extend(value)
                else:
                    self._state[key] = value
            else:
                self._state[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get the entire state."""
        with self._state_lock:
            return self._state.copy()

    def clear(self):
        """Clear the state."""
        with self._state_lock:
            self._state.clear()
