# -*- coding: utf-8 -*-
"""
    ReST directive for embedding Youtube and Vimeo videos.
    There are two directives added: ``youtube`` and ``vimeo``. The only
    argument is the video id of the video to include.
    Both directives have three optional arguments: ``height``, ``width``
    and ``align``. Default height is 281 and default width is 500.
    Example::
        .. youtube:: anwy2MPT5RE
            :height: 315
            :width: 560
            :align: left
    :copyright: (c) 2012 by Danilo Bargen.
    :license: BSD 3-clause
"""
from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('start', 'center', 'end'))


class IframeVideo(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': align,
    }
    default_width = 500
    default_height = 281

    def run(self):
        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'left'
        return [nodes.raw('', self.html % self.options, format='html')]


class Youtube(IframeVideo):
    html = '''
    <div class="d-flex justify-content-%(align)s">
        <iframe 
            src="https://www.youtube.com/embed/%(video_id)s"
            width="%(width)u" 
            height="%(height)u" 
            frameborder="0"
            webkitAllowFullScreen 
            mozallowfullscreen 
            allowfullscreen
        >
        </iframe>
    </div>
    '''


class Vimeo(IframeVideo):
    html = '''
    <div class="d-flex justify-content-%(align)s">
        <iframe 
            src="https://player.vimeo.com/video/%(video_id)s"
            width="%(width)u" 
            height="%(height)u" 
            frameborder="0"
            webkitAllowFullScreen 
            mozallowfullscreen 
            allowFullScreen
            class="align-%(align)s"
        >
        </iframe>
    </div>
    '''


def setup(builder):
    directives.register_directive('youtube', Youtube)
    directives.register_directive('vimeo', Vimeo)