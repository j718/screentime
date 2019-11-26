class Toolbar:
    def __init__(self, mw, web):
        self.mw = mw
        self.web = web
        self.link_handlers = {
            "decks": self._deckLinkHandler,
        }

    def draw(self):
        self.web.onBridgeCmd = self._linkHandler
        self.web.setHtml(self._body % self._centerLinks())

    # Available links
    ######################################################################

    def _centerLinks(self):
        links = [
            ["decks", ("Decks"), ("Shortcut key: %s") % "D"],
        ]
        return self._linkHTML(links)

    def _linkHTML(self, links):
        buf = ""
        for ln, name, title in links:
            buf += '''
            <a class=hitem tabindex="-1" aria-label="%s" title="%s" href=# onclick="return pycmd('%s')">%s</a>''' % (
                name, title, ln, name)
        return buf

    # Link handling
    ######################################################################

    def _linkHandler(self, link):
        if link in self.link_handlers:
            self.link_handlers[link]()
        return False

    def _deckLinkHandler(self):
        print("Made it here")
        # self.mw.moveToState("deckBrowser")

    # HTML and CSS
    ######################################################################

    _body = """
<center id=outer>
<table id=header width=100%%>
<tr>
<td class=tdcenter align=center>%s</td>
</tr></table>
</center>
"""
