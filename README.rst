ftw.avatar
==========

``ftw.avatar`` generates a personal default avatar for new Plone users.



Installation
------------

Simply install the ``ftw.avatar`` egg by adding it to the dependencies in your package
or by adding it to your buildout configuration::

    [instance]
    eggs +=
        ftw.avatar

There is no need to install the addon in the Plone site, it automatically hooks in.



Default avatar generation
-------------------------

``ftw.avatar`` generates default avatars for users which have not yet defined
an avatar (Personal portrait) in the personal preferences.
The avatar is generated with a random background color and two characters of
their name.

**Examples:**

.. image:: https://raw.github.com/4teamwork/ftw.avatar/master/docs/examples/an.png

.. image:: https://raw.github.com/4teamwork/ftw.avatar/master/docs/examples/ct.png

.. image:: https://raw.github.com/4teamwork/ftw.avatar/master/docs/examples/pi.png



Plone patches
-------------

**Maximum user portait scale**

``Products.PlonePAS`` limits the maximum size of user portraits
(a.k.a. avatars) to  75x100.
``ftw.avatar`` increases the size to a maximum of 300x300, allowing to
build pages with bigger avatars such as user pages.


**Default user portrait patch**

``ftw.avatar`` patches ``Products.PlonePAS`` to generate a default avatar
when the user portrait is retrieved the first time and the user has not yet
set an avatar.
``membership_tool.getPersonalPortrait()`` is patched.



Avatar scaling
--------------

``ftw.avatar`` extends the avatar default view to accept a scaling parameter.
The ``size`` parameter is used as maximum width and maximum height for
the scale.

Example URL: ``http://localhost:8080/Plone/portal_memberdata/portraits/admin?size=26``



Font licensing
--------------

For generating the avatar the font ``Fantasque Sans Mono`` is used.
The font is licensed under the SIL Open Font License, see the
`License File <https://github.com/4teamwork/ftw.avatar/blob/master/ftw/avatar/font/OFL.txt>`_



Links
-----

- github project: https://github.com/4teamwork/ftw.avatar
- Issue tracker: https://github.com/4teamwork/ftw.avatar/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.avatar
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.avatar


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.avatar`` is licensed under GNU General Public License, version 2.
