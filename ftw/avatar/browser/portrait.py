from Products.Five.browser import BrowserView
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from webdav.common import rfc1123_date
from zope.annotation import IAttributeAnnotatable
from zope.interface import alsoProvides


class PortraitScalingView(BrowserView):

    def __call__(self):
        form = self.request.form
        size = form.get('size', form.get('s', None))
        if size is None:
            # return original - no scaling required
            return self.context.index_html(self.request, self.request.RESPONSE)
        else:
            size = int(size)

        if not IAttributeAnnotatable.providedBy(self.context):
            alsoProvides(self.context, IAttributeAnnotatable)

        storage = AnnotationStorage(self.context, self.context.modified)
        scale = storage.scale(self.scale_factory,
                              width=size,
                              height=size)

        response = self.request.RESPONSE
        response.setHeader('Last-Modified', rfc1123_date(scale['modified']))
        response.setHeader('Content-Type', scale['mimetype'])
        response.setHeader('Content-Length', len(scale['data']))
        response.setHeader('Accept-Ranges', 'bytes')
        return scale['data']

    def scale_factory(self, **parameters):
        return scaleImage(self.context.data, **parameters)
