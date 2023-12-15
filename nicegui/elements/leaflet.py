from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, cast

from typing_extensions import Self

from .. import binding
from ..awaitable_response import AwaitableResponse, NullResponse
from ..element import Element
from ..events import GenericEventArguments
from .leaflet_layer import Layer


class Leaflet(Element, component='leaflet.js'):
    # pylint: disable=import-outside-toplevel
    from .leaflet_layers import GenericLayer as generic_layer
    from .leaflet_layers import Marker as marker
    from .leaflet_layers import TileLayer as tile_layer

    center = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_center(value))
    zoom = binding.BindableProperty(lambda sender, value: cast(Leaflet, sender).set_zoom(value))

    def __init__(self,
                 center: Tuple[float, float] = (0.0, 0.0),
                 zoom: int = 13,
                 *,
                 options: Dict = {},
                 draw_control: Union[bool, Dict] = False,
                 ) -> None:
        """Leaflet map

        This element is a wrapper around the `Leaflet <https://leafletjs.com/>`_ JavaScript library.

        :param center: initial center location of the map (latitude/longitude, default: (0.0, 0.0))
        :param zoom: initial zoom level of the map (default: 13)
        :param draw_control: whether to show the draw toolbar (default: False)
        :param options: additional options passed to the Leaflet map (default: {})
        """
        super().__init__()
        self.add_resource(Path(__file__).parent / 'lib' / 'leaflet')
        self._classes.append('nicegui-leaflet')

        self.layers: List[Layer] = []
        self.is_initialized = False

        self.center = center
        self.zoom = zoom
        self._props['center'] = center
        self._props['zoom'] = zoom
        self._props['options'] = options
        self._props['draw_control'] = draw_control

        self.on('init', self._handle_init)
        self.on('map-moveend', lambda e: self.set_center(e.args['center']))
        self.on('map-zoomend', lambda e: self.set_zoom(e.args['zoom']))

        self.tile_layer(
            url_template=r'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
            options={'attribution': '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'},
        )

    def __enter__(self) -> Self:
        Layer.current_leaflet = self
        return super().__enter__()

    def __getattribute__(self, name: str) -> Any:
        attribute = super().__getattribute__(name)
        if isinstance(attribute, type) and issubclass(attribute, Layer):
            Layer.current_leaflet = self
        return attribute

    def _handle_init(self, e: GenericEventArguments) -> None:
        self.is_initialized = True
        with self.client.individual_target(e.args['socket_id']):
            for layer in self.layers:
                self.run_method('add_layer', layer.to_dict())

    def run_method(self, name: str, *args: Any, timeout: float = 1, check_interval: float = 0.01) -> AwaitableResponse:
        if not self.is_initialized:
            return NullResponse()
        return super().run_method(name, *args, timeout=timeout, check_interval=check_interval)

    def set_center(self, center: Tuple[float, float]) -> None:
        """Set the center location of the map."""
        if self._props['center'] == center:
            return
        self._props['center'] = center
        self.run_method('setCenter', center)

    def set_zoom(self, zoom: int) -> None:
        """Set the zoom level of the map."""
        if self._props['zoom'] != zoom:
            return
        self._props['zoom'] = zoom
        self.run_method('setZoom', zoom)

    def _handle_delete(self) -> None:
        binding.remove(self.layers, Layer)
        super().delete()
