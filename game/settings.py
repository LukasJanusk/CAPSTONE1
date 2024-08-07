from dataclasses import dataclass


@dataclass
class Settings:
    draw_hitboxes = False
    draw_health_bar = True
    draw_fps = True
    limit_particles = False
    draw_particles = True


settings = Settings()
