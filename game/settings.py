from dataclasses import dataclass


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


settings = Settings()
