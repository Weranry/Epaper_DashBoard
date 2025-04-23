from flask import jsonify
from lib.date.date_calculator import DateCalculator

class DateInfoAPI:
    def __init__(self):
        self.calculator = DateCalculator()

    def get_date_info(self):
        return jsonify({
            'solar': self.calculator.get_solar_date(),
            'lunar': self.calculator.get_lunar_date(),
            'ganzhi': self.calculator.get_ganzhi_date(),
            'season': self.calculator.get_season_info(),
            'festival': self.calculator.get_festival_info()
        }) 