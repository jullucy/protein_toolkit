from typing import Dict, Callable, Tuple
from PySide6.QtWidgets import QWidget

class ToolRegistry:
    """Registry for managing different tools in the application"""
    
    def __init__(self):
        self._tools: Dict[str, Tuple[str, Callable]] = {}
    
    def register_tool(self, tool_id: str, display_name: str, factory_func: Callable[[], QWidget]):
        """
        Register a tool with the registry
        
        Args:
            tool_id: Unique identifier for the tool
            display_name: Human-readable name for the tool
            factory_func: Function that returns a QWidget instance of the tool
        """
        self._tools[tool_id] = (display_name, factory_func)
    
    def create_tool(self, tool_id: str) -> QWidget:
        """Create and return an instance of the specified tool"""
        if tool_id not in self._tools:
            raise ValueError(f"Tool '{tool_id}' not found in registry")
        
        display_name, factory_func = self._tools[tool_id]
        return factory_func()
    
    def get_tool_name(self, tool_id: str) -> str:
        """Get the display name for a tool"""
        if tool_id not in self._tools:
            return "Unknown Tool"
        return self._tools[tool_id][0]
    
    def get_available_tools(self) -> Dict[str, str]:
        """Get a dictionary of all available tools (id -> display_name)"""
        return {tool_id: display_name for tool_id, (display_name, _) in self._tools.items()}
    
    def is_tool_available(self, tool_id: str) -> bool:
        """Check if a tool is registered and available"""
        return tool_id in self._tools

# Global registry instance
tool_registry = ToolRegistry()
