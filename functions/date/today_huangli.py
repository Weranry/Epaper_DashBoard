from datetime import datetime
from lunar_python import Lunar
import pytz

class todayhuangli:
    def __init__(self, timezone='Asia/Shanghai'):
        self.timezone = pytz.timezone(timezone)
        self.current_time = datetime.now(self.timezone)
        self.lunar = Lunar.fromDate(self.current_time)
    def get_jishen(self) -> dict:
        return {
            "喜神": self.lunar.getDayPositionXiDesc(),
            "福神": self.lunar.getDayPositionFuDesc(),
            "财神": self.lunar.getDayPositionCaiDesc(),
            "阳贵神": self.lunar.getDayPositionYangGuiDesc(),
            "阴贵神": self.lunar.getDayPositionYinGuiDesc()

        }

    def get_taishen(self) -> str:
        return self.lunar.getDayPositionTai()

    def get_taisui(self) -> str:
        return self.lunar.getDayPositionTaiSuiDesc(1)

    def get_pengzubaiji(self) -> str:
        gan = self.lunar.getPengZuGan()
        zhi = self.lunar.getPengZuZhi()
        return f"{gan}，{zhi}"

    def get_ershibaxingxiu(self) -> str:
        xiu = self.lunar.getXiu()
        animal = self.lunar.getAnimal()
        luck = self.lunar.getXiuLuck()
        return f"{xiu}{animal}{luck}"
    
    def get_chongsha(self) -> str:
        return self.lunar.getDayChongDesc()


