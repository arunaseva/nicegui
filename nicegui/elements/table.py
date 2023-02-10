from typing import Dict, List

from .. import globals
from ..dependencies import register_component
from ..element import Element

register_component('table', __file__, 'table.js', ['lib/ag-grid-community.min.js'])


class Table(Element):

    def __init__(self, options: Dict, *, html_columns: List[int] = [], theme: str = 'balham') -> None:
        """Table

        An element to create a table using `AG Grid <https://www.ag-grid.com/>`_.

        The `call_api_method` method can be used to call an AG Grid API method.

        :param options: dictionary of AG Grid options
        :param html_columns: list of columns that should be rendered as HTML (default: `[]`)
        :param theme: AG Grid theme (default: 'balham')
        """
        super().__init__('table')
        self._props['options'] = options
        self._props['html_columns'] = html_columns
        self._classes = [f'ag-theme-{theme}', 'w-full', 'h-64']

    @property
    def options(self) -> Dict:
        return self._props['options']

    def update(self) -> None:
        super().update()
        self.run_method('update_grid')

    def call_api_method(self, name: str, *args) -> None:
        """Call an AG Grid API method.

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/grid-api/>`_ for a list of methods.

        :param name: name of the method
        :param args: arguments to pass to the method
        """
        self.run_method('call_api_method', name, *args)

    async def get_selected_rows(self, single: bool = False) -> list[dict[str, any]] | None:
        """Returns an unsorted list of selected rows (i.e. row data that you provided).

        See `AG Grid API <https://www.ag-grid.com/javascript-data-grid/row-selection/#reference-selection-getSelectedRows>`_ for a doc of method.

        :param single: return a single row (default: `False`)
        """

        selected_rows: list[dict] = await globals.get_client().run_javascript(
            f'return getElement({self.id}).gridOptions.api.getSelectedRows();'
        )

        if len(selected_rows) == 0:
            return None

        if single:
            return selected_rows[0]

        return selected_rows
