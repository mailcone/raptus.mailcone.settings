import grok
import smtplib
from StringIO import StringIO

from zope.schema import vocabulary
from zope.i18n import translate

from email.mime.text import MIMEText

from raptus.mailcone.core import utils
from raptus.mailcone.core import bases
from raptus.mailcone.core.interfaces import IMailcone

from raptus.mailcone.settings import _
from raptus.mailcone.settings import interfaces





class SettingsContainer(bases.Container):
    grok.implements(interfaces.ISettingsContainer)

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_settings_container(obj, event):
    obj['settings'] = SettingsContainer()



class SMPTSettings(bases.Container):
    grok.implements(interfaces.ISMTPSettings)
    
    protocol = smtplib.SMTP
    
    fraddr = 'mailcone@raptus.com'
    host = 'localhost'
    port = ''
    local_hostname = ''
    timeout = 300

    use_login = False
    username = 'admin'
    password = ''

    use_tls = False
    keyfile = ''
    certfile = ''
    

    def send(self, message, subject, toaddr=list(), fraddr = None):
        if not isinstance(toaddr, (list,tuple,)):
            toaddr = [toaddr]
        if fraddr is None:
            fraddr = self.fraddr
        request = utils.getRequest()
        msg = MIMEText(translate(message, context=request), 'plain', 'utf-8')
        msg['Subject'] = translate(subject, context=request)
        msg['From'] = fraddr
        msg['To'] = ', '.join(toaddr)
        
        self.connect()
        self._v_connection.sendmail(fraddr, toaddr, msg.as_string())
        
    
    def connect(self):
        kw= dict()
        ignors = ('self',)
        keyfile = lambda v: StringIO(v)
        certfile = lambda v:StringIO(v)
        replaces = dict(keyfile=keyfile, certfile=certfile)
        for key in self.protocol.__init__.im_func.func_code.co_varnames:
            if key in ignors:
                continue
            value = getattr(self, key, None)
            # skip by None or empty
            if not value:
                continue
            if key in replaces:
                value = replaces[key](value)
            
            kw[key] = value
            
            
        self._v_connection = self.protocol(**kw)
        if self.use_login:
            self._v_connection.login(str(self.username), str(self.password))
        if self.use_tls:
            self._v_connection.starttls(keyfile(self.keyfile), certfile(self.certfile))
        #self._v_connection.connect()
    
    def close(self):
        if self._v_connection is not None:
            self._v_connection.quit()

    def reconnect(self):
        self.close()
        self.connect()

@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_smtp_container(obj, event):
    obj['settings']['smtp'] = SMPTSettings()

register = vocabulary.getVocabularyRegistry().register
def vocabulary_smtp(context):
    terms = list()
    terms.append(vocabulary.SimpleTerm(value=smtplib.SMTP, token='smtp', title=_('SMTP')))
    terms.append(vocabulary.SimpleTerm(value=smtplib.SMTP_SSL, token='smtp_ssl', title=_('SMTP SSL')))
    terms.append(vocabulary.SimpleTerm(value=smtplib.LMTP, token='lmtp', title=_('LMTP')))
    return vocabulary.SimpleVocabulary(terms)
register('raptus.mailcone.settings.smtp', vocabulary_smtp)

class SMTPLocator(bases.BaseLocator):
    splitedpath = ['settings','smtp']
grok.global_utility(SMTPLocator, provides=interfaces.ISMTPLocator)



class LogoSettings(bases.Container):
    grok.implements(interfaces.ILogoSettings)
    
    grok.traversable('image')
    image = None
    
    


@grok.subscribe(IMailcone, grok.IApplicationInitializedEvent)
def init_logo_container(obj, event):
    obj['settings']['logo'] = LogoSettings()

class LogoLocator(bases.BaseLocator):
    splitedpath = ['settings','logo']
grok.global_utility(LogoLocator, provides=interfaces.ILogoLocator)








