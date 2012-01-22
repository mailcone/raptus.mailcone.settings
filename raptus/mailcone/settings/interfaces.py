import zope
from zope import schema
from zope import interface

from raptus.mailcone.core.interfaces import IContainer
from raptus.mailcone.core.interfaces import IContainerLocator

from raptus.mailcone.settings import _





class ISettingsContainer(IContainer):
    """ a container to store all settigns items
    """



class ISMTPSettings(interface.Interface):
    """ setting for smpt, manage connection and sending mails
    """
    protocol = schema.Choice(title=_(u'Protocol'),
                             required=True,
                             vocabulary='raptus.mailcone.settings.smtp')
    
    fraddr = schema.TextLine(title=_(u'From Address'), required=True)
    host = schema.TextLine(title=_(u'Host'), required=True)
    port = schema.TextLine(title=_(u'Port'), required=False)
    local_hostname = schema.TextLine(title=_(u'Local Hostname'), required=False)
    timeout = schema.Int(title=_(u'Timeout'), required=False)

    use_login = schema.Bool(title=_(u'Use login'))
    username = schema.TextLine(title=_(u'Username'), required=False)
    password = schema.TextLine(title=_(u'Password'), required=False)

    use_tls = schema.Bool(title=_(u'Use TLS'))
    keyfile = schema.Text(title=_(u'Key'), required=False)
    certfile = schema.Text(title=_(u'Certification'), required=False)
    
    def send(self, message, subject, toaddr=list(), fraddr = None):
        """ send a email
            the message will be translate with zope.i18n before sending
        """
    
    def conntect(self):
        """ build a new connection
        """
    
    def close(self):
        """ try to close the actual connection
        """

    def reconnect(self):
        """ rebuild a connection
        """



class ISMTPLocator(IContainerLocator):
    """ locator
    """



class ILogoSettings(interface.Interface):
    """ allow to change the default logo
        http://www.stereoplex.com/blog/blob-support-in-the-zodb-with-zeo
    """
    image = schema.Object(title=_('Logo'),
                          description=_(u'Use a logo 300x90px.'),
                          required=False,
                          schema=zope.app.file.interfaces.IImage)
    url = interface.Attribute('return image url or None')


class ILogoLocator(IContainerLocator):
    """ locator
    """












