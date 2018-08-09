from functools import partial

from dance.helper import load_yaml_file
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from dance.service import IService


class WatchHandler(FileSystemEventHandler):
    def __init__(self, router):
        self.router = router

    def on_modified(self, event):
        self.router.events = load_yaml_file('config/iotnn/config.yaml')
        self.router.logger.info(self.router.events)


class Router(IService):
    def __init__(self):
        IService.__init__(self, 'router')
        self.dance = None
        self.events = load_yaml_file('config/iotnn/config.yaml')
        self.observer = Observer()
        self.observer.schedule(WatchHandler(self), 'config/iotnn', recursive=True)

    def stop(self):
        self.observer.stop()

    def get_topics(self, event):
        m = self.events.get(event)
        if m is None:
            return []
        return m

    def start(self, dance):
        self.dance = dance
        self.observer.start()
        # def watch_topics(event, topics):
        #     self.events[event] = topics
        #
        # def watch_events(events):
        #     for event in events:
        #         m = self.events.get(event)
        #         if m is None:
        #             m = {}
        #             self.events[event] = m
        #             self.dance.sync.watch(
        #                 '/iotnn/{0}/{1}/{2}'.format(self.dance.matrix, self.dance.name, event),
        #                 partial(watch_topics, event)
        #             )
        # self.dance.sync.watch('/iotnn/{0}/{1}'.format(self.dance.matrix, self.dance.name), watch_events)

    def config(self, conf):
        pass
