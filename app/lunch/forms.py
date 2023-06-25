from app.core.client import Form

from .models import Lunch


class RouletteSpunForm(Form):
    lunches: list[Lunch]
