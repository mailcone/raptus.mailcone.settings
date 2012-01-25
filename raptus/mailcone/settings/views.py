import grok

from raptus.mailcone.layout.views import Page, EditFormPage
from raptus.mailcone.layout.interfaces import IPreferencesMenu
from raptus.mailcone.layout.navigation import locatormenuitem
from raptus.mailcone.layout.formlib import ImageWidget

from raptus.mailcone.settings import _
from raptus.mailcone.settings import interfaces





class SMTP(EditFormPage):
    grok.name('index')
    grok.context(interfaces.ISMTPSettings)
    locatormenuitem(IPreferencesMenu, interfaces.ISMTPLocator, _(u'SMTP Configuration'))
    label = _(u'SMTP Configuration')
    prefix = 'settings'
    
    def message(self, mapping=None):
        return super(SMTP, self).message(mapping=dict(object=_('SNMP')))


class Logo(EditFormPage):
    grok.name('index')
    grok.context(interfaces.ILogoSettings)
    locatormenuitem(IPreferencesMenu, interfaces.ILogoLocator, _(u'Change Logo'))
    form_fields = grok.AutoFields(interfaces.ILogoSettings)
    form_fields['image'].custom_widget = ImageWidget
    label = _(u'Logo Configuration')
    prefix = 'settings'

    def message(self, mapping=None):
        return super(Logo, self).message(mapping=dict(object=_('Logo')))