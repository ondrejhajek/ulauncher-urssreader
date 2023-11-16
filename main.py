from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import feedparser
import utils


class RssReaderExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        for i in range(1, 5):
            title = extension.preferences['rss' + str(i) + '_title']
            url = extension.preferences['rss' + str(i) + '_url']
            if title.strip() and url.strip() and utils.is_valid_url(url):
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=title,
                                                 description=url,
                                                 on_enter=ExtensionCustomAction(
                                                     {'rss_link': url},
                                                     keep_app_open=True)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        feed = feedparser.parse(event.get_data()['rss_link'])
        items = []
        i = 0
        for entry in feed.entries:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=utils.sanitize(entry.title, 50),
                                             description=utils.sanitize(entry.description, 70),
                                             on_enter=OpenUrlAction(entry.link)))
            i += 1
            if i == 10:
                break

        return RenderResultListAction(items)


if __name__ == '__main__':
    RssReaderExtension().run()
