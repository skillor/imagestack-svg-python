import unittest

from imagestack_svg.loaders import *
from imagestack_svg.imageresolve import *


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

        self.assertGreater(len(res), 1)

        res = await creator.create_inner_svg(s)
        self.assertEqual(res, '<rect x="0" y="0" width="600" height="150" rx="20" ry="20" fill="rgb(48, 50, 55)"/>\n'
                              '<text x="300" y="50" fill="blue">User 1</text>\n'
                              '<rect x="0" y="150" width="600" height="150" rx="20" ry="20" fill="rgb(48, 50, 55)"/>\n'
                              '<text x="300" y="200" fill="blue">User 2</text>\n')


if __name__ == '__main__':
    unittest.main()
