import importlib.resources as resources


class AudioEngine:
    def __init__(self, app, sound_enabled: bool = True):
        self.app = app
        self.sound_enabled = sound_enabled

    def play_sound(self, filename: str):
        if not self.sound_enabled:
            return

        def _play():
            try:
                from playsound3 import playsound
                resource = resources.files("vim_masterpiece.assets").joinpath(filename)
                with resources.as_file(resource) as sound_path:
                    playsound(str(sound_path), block=True)
            except Exception:
                pass

        self.app.run_worker(_play, thread=True, exclusive=False)

    def clack(self):
        self.play_sound("clack.mp3")

    def tick(self):
        self.play_sound("tick.mp3")
