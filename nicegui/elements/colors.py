from operator import neg
from turtle import pos
from .custom_view import CustomView
from .element import Element

class ColorsView(CustomView):

    def __init__(self, primary, secondary, accent, positive, negative, info, warning):
        super().__init__('colors', __file__,
                         primary=primary,
                         secondary=secondary,
                         accent=accent,
                         positive=positive,
                         negative=negative,
                         info=info,
                         warning=warning)
        self.initialize(temp=False)

class Colors(Element):

    def __init__(self, *,
                 primary='#1976d2',
                 secondary='#26a69a',
                 accent='#9c27b0',
                 positive='#21ba45',
                 negative='#c10015',
                 info='#31ccec',
                 warning='#f2c037'):
        super().__init__(ColorsView(primary, secondary, accent, positive, negative, info, warning))
