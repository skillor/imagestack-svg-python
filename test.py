import unittest

from imagestack_svg.imageresolve import ImageStackResolveString
from imagestack_svg.imagecreator import ImageCreator
from imagestack_svg.helpers import is_emoji, from_char, to_char


class Tests(unittest.IsolatedAsyncioTestCase):
    def test_is_emoji(self):
        self.assertTrue(is_emoji('🎈'))

    def test_emoji_conversion(self):
        self.assertEqual(from_char('🎈'), 'f09f8e88')
        self.assertEqual(to_char('f09f8e88'), '🎈')
        self.assertEqual(to_char(from_char('🎈')), '🎈')

    async def test_simple_resolve_string(self):
        creator = ImageCreator()

        svg = '{% for user in users %}' \
              '<rect x="0" y="{{(loop.index - 1) * 150}}"' \
              ' width="600" height="150" rx="20" ry="20" fill="rgb(48, 50, 55)"/>\n' \
              '<text x="300" y="{{((loop.index - 1) * 150)+50}}" fill="blue">{{ user.name  }}</text>\n' \
              '{% endfor %}'

        s = ImageStackResolveString(svg)
        s(**{
            'users': [{
                'name': 'User {}'.format(x + 1),
            } for x in range(2)]})

        res = await creator.create_bytes(s)

        self.assertGreater(len(res.read()), 1)

        res = await creator.create_inner_svg(s)
        self.assertEqual(res, '<rect x="0" y="0" width="600" height="150" rx="20" ry="20" fill="rgb(48, 50, 55)"/>\n'
                              '<text x="300" y="50" fill="blue">User 1</text>\n'
                              '<rect x="0" y="150" width="600" height="150" rx="20" ry="20" fill="rgb(48, 50, 55)"/>\n'
                              '<text x="300" y="200" fill="blue">User 2</text>\n')

    async def test_replace(self):
        creator = ImageCreator()

        svg = '<rect width="250" height="40" rx="10" ry="10" fill="red"/>\n' \
              '<text id="title" text-anchor="middle" fill="white">{{ name }}</text>'

        s = ImageStackResolveString(svg)
        s(**{
            'name': 'Legginsdarry'
        })

        s = s.replace('title', '<text id="title" text-anchor="start" fill="white">Leggins</text>')

        s = s.replace('title', '<image id="userEmoji" x="147" y="15" width="40" height="40" xlink:href="house"/>')

        res = await creator.create_inner_svg(s)
        self.assertEqual(res, '<rect width="250" height="40" rx="10" ry="10" fill="red"/>\n'
                              '<image id="userEmoji" x="147" y="15" width="40" height="40" xlink:href="house"/>')


if __name__ == '__main__':
    unittest.main()
