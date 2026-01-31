import importlib.metadata
from typing import List, Type
from universalviewer.plugins.base import ViewerPlugin

class PluginManager:
    """Handles discovery and loading of plugins via entry points."""
    
    ENTRY_POINT_GROUP = "universalviewer.plugins"

    @classmethod
    def load_plugins(cls) -> List[ViewerPlugin]:
        """Discover and instantiate all registered plugins."""
        plugins = []
        # Support for Python < 3.10 would require different syntax, 
        # but 3.10+ is specified in pyproject.toml
        eps = importlib.metadata.entry_points(group=cls.ENTRY_POINT_GROUP)
        
        for ep in eps:
            try:
                plugin_class: Type[ViewerPlugin] = ep.load()
                plugins.append(plugin_class())
            except Exception as e:
                # In a real app, we'd log this carefully
                print(f"Error loading plugin {ep.name}: {e}")
                
        return plugins
