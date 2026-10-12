#!/usr/bin/env python3
"""
HAE Tool Hub
Unified interface for autonomous agents to access system tools, 
external APIs, and specialized revenue-generating scripts.
"""
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolHub")

class ToolHub:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_internal_tools()

    def register_tool(self, name: str, func: Callable):
        """Registers a new tool for agent use."""
        self.tools[name] = func
        logger.info(f"Tool registered: {name}")

    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Executes a registered tool with provided arguments."""
        if tool_name not in self.tools:
            return {"status": "ERROR", "message": f"Tool {tool_name} not found."}
        
        try:
            logger.info(f"Executing tool: {tool_name} with args: {kwargs}")
            result = self.tools[tool_name](**kwargs)
            return {"status": "SUCCESS", "result": result}
        except Exception as e:
            logger.exception(f"Error executing tool {tool_name}: {e}")
            return {"status": "ERROR", "message": str(e)}

    def _register_internal_tools(self):
        """Registers basic system tools for agents."""
        self.register_tool("shell_exec", self._shell_exec)
        self.register_tool("read_config", self._read_config)
        self.register_tool("write_config", self._write_config)

    def _shell_exec(self, command: str) -> str:
        """Executes a shell command and returns stdout."""
        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return res.stdout if res.returncode == 0 else res.stderr

    def _read_config(self, path: str) -> Any:
        """Reads a JSON config file."""
        with open(path, 'r') as f:
            return json.load(f)

    def _write_config(self, path: str, data: Any) -> bool:
        """Writes data to a JSON config file."""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True

# Singleton instance
hub = ToolHub()
