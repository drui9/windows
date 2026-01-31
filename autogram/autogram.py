from threading import Event
from autogram.base import Bot
from abc import abstractmethod

# --
class Autogram(Bot):
    def __init__(self, config):
        self.initialized = Event()
        return super().__init__(self.initialized, config)

    # -- prepare wrapper
    @abstractmethod
    def run(self):
        if self.initialized.is_set():
            self.data("offset", 0)
            if (bot := self.getMe()).status_code != 200:
                raise RuntimeError(bot.json())
            # --
            info = bot.json()["result"]
            for name, value in info.items():
                setattr(self, name, value)
            return self.initialized.set()
        else:
            raise RuntimeError("Init not set!")

    @property
    def stop(self):
        return not self.initialized.is_set()

