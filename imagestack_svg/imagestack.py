from PySide2.QtCore import QByteArray, QBuffer, QIODevice
from PySide2.QtGui import QImage, QPainter
from PySide2.QtSvg import QSvgRenderer
from .imagecreator import ImageCreator, SVG_PREFIX, SVG_SUFFIX


class ImageStack:
    def __init__(self, svg: str):
        self.svg = svg

    def __str__(self):
        return self.svg

    @staticmethod
    async def _create_bytes(svg: str, max_size: tuple = None):
        svg = f'{SVG_PREFIX}{svg}{SVG_SUFFIX}'
        svg_renderer = QSvgRenderer(svg.encode())
        orig_svg = QImage(svg_renderer.defaultSize(), QImage.Format_RGBA64)
        painter = QPainter(orig_svg)

        svg_renderer.render(painter)

        ba = QByteArray()
        buffer = QBuffer(ba)
        buffer.open(QIODevice.ReadWrite)

        orig_svg.save(buffer, 'PNG', -1)
        painter.end()
        buffer.seek(0)
        return bytes(buffer.readAll())

    async def create_bytes(self, image_creator: ImageCreator, max_size: tuple = None):
        return self._create_bytes(self.svg, max_size)

    async def _create_raw_svg(self, svg: str):
        return f'{SVG_PREFIX}{svg}{SVG_SUFFIX}'

    async def create_raw_svg(self, image_creator: ImageCreator):
        return await self._create_raw_svg(self.svg)

    async def _create_inner_svg(self, svg: str):
        return svg

    async def create_inner_svg(self, image_creator: ImageCreator):
        return await self._create_inner_svg(self.svg)
