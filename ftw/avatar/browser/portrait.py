from email.utils import formatdate
from OFS.Image import Pdata
from plone.protect.interfaces import IDisableCSRFProtection
from plone.scale.scale import scaleImage
from plone.scale.storage import AnnotationStorage
from Products.Five.browser import BrowserView
from zope.annotation import IAttributeAnnotatable
from zope.interface import alsoProvides


class PortraitScalingView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        form = self.request.form
        size = form.get('size', form.get('s', None))
        if size is None:
            # return original - no scaling required
            return self.context.index_html(self.request, self.request.RESPONSE)
        else:
            size = int(size)

        if not IAttributeAnnotatable.providedBy(self.context):
            alsoProvides(self.context, IAttributeAnnotatable)

        storage = AnnotationStorage(self.context)
        scale = storage.scale(self.scale_factory,
                              width=size,
                              height=size)

        response = self.request.RESPONSE
        response.setHeader('Last-Modified', formatdate(timeval=scale['modified'], localtime=False, usegmt=True))
        response.setHeader('Content-Type', scale['mimetype'])
        response.setHeader('Content-Length', len(scale['data']))
        response.setHeader('Accept-Ranges', 'bytes')
        return scale['data']

    def scale_factory(self, **parameters):
        portrait = self.context.data
        if isinstance(portrait, Pdata):
            portrait = bytes(portrait)
        return scaleImage(portrait, **parameters)
