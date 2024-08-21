from dataclasses import dataclass
import json
import os


@dataclass
class Settings:
    _draw_hitboxes = False
    _draw_health_bar = False
    _draw_fps = False
    _limit_particles = False
    _render_particles = False

    @property
    def draw_hitboxes(self):
        return self._draw_hitboxes

    @draw_hitboxes.setter
    def draw_hitboxes(self, value):
        if value is True and self._draw_hitboxes is True:
            self._draw_hitboxes = False
        else:
            self._draw_hitboxes = True

    @property
    def draw_health_bar(self):
        return self._draw_health_bar

    @draw_health_bar.setter
    def draw_health_bar(self, value):
        if value is True and self._draw_health_bar is True:
            self._draw_health_bar = False
        else:
            self._draw_health_bar = True

    @property
    def draw_fps(self):
        return self._draw_fps

    @draw_fps.setter
    def draw_fps(self, value):
        if value is True and self._draw_fps is True:
            self._draw_fps = False
        else:
            self._draw_fps = True

    @property
    def render_particles(self):
        return self._render_particles

    @render_particles.setter
    def render_particles(self, value):
        if value is True and self._render_particles is True:
            self._render_particles = False
        else:
            self._render_particles = True

    def save(self) -> bool:
        """Saves User data to json file"""
        data = self.to_dict()
        try:
            with open(os.path.join(".", "user", "settings.json"), mode="w") as file:
                json.dump(data, file, indent=4)
                print("Settings saved")
                return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False

    def load(self) -> bool:
        """Loads User data from json file"""
        file_path = os.path.join(".", "user", "settings.json")
        if not os.path.isfile(file_path):
            self.save()
        else:
            try:
                path = os.path.join(".", "user", "settings.json")
                with open(path, mode="r") as file:
                    data = json.load(file)
                    settings_data = data.get("settings", [])
                    self._draw_hitboxes = settings_data[0].get("draw_hitboxes", self._draw_hitboxes)
                    self._draw_health_bar = settings_data[1].get("draw_health_bar", self._draw_health_bar)
                    self._draw_fps = settings_data[2].get("draw_fps", self._draw_fps)
                    self._limit_particles = settings_data[3].get("limit_particles", self._limit_particles)
                    self._render_particles = settings_data[4].get("render_particles", self._render_particles)
                    print("Settings loaded")
                    return True
            except Exception as e:
                print(f"Failed to load settings: {e}")
                return False

    def to_dict(self) -> dict:
        """Converts User object to dictionary"""
        return {
            "settings": [
                {"draw_hitboxes": self._draw_hitboxes},
                {"draw_health_bar": self._draw_health_bar},
                {"draw_fps": self._draw_fps},
                {"limit_particles": self._limit_particles},
                {"render_particles": self._render_particles}
            ]
        }


settings = Settings()
