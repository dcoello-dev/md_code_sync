from abc import ABC, abstractmethod
from textual.widget import Widget

class ViewerPlugin(ABC):
    """Base class for all Universal Viewer plugins."""
    
    @property
    @abstractmethod
    def title(self) -> str:
        """The title that will appear in the tab."""
        pass

    @abstractmethod
    def get_widget(self) -> Widget:
        """Returns the Textual widget to be rendered in the tab."""
        pass
