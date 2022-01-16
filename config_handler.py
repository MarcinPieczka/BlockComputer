import configparser
from datetime import time, datetime, timedelta, date
from dateutil import parser
from typing import Optional


class Options:
    def __init__(self, block_until, time_block_start, time_block_end):
        self.block_until: Optional[datetime] = block_until
        self.time_block_start: Optional[datetime] = time_block_start
        self.time_block_end: Optional[datetime] = time_block_end


class Config:
    def __init__(self):
        self.possible_options = ["block_until", "time_block_start", "time_block_end"]
        self.conf_file = "config.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.conf_file)
        if "config" not in self.config:
            self.config["config"] = {
                "block_until": "",
                "time_block_start": "",
                "time_block_end": "",
            }

    def save_from_args(self, parser_args):
        if parser_args.schedule_between:
            self.write("time_block_start", parser_args.schedule_between[0].strftime("%H:%M"))
            self.write("time_block_end", parser_args.schedule_between[1].strftime("%H:%M"))
        if parser_args.days:
            date_until = datetime.combine(date.today(), time(4)) + timedelta(days=parser_args.days)
            config.write("block_until", date_until.isoformat())

    def write(self, key, value):
        if key not in self.possible_options:
            raise Exception
        self.config["config"][key] = value
        with open(self.conf_file, "w") as f:
            self.config.write(f)

    @property
    def options(self):
        block_until = self.config["config"]["block_until"] or None
        if block_until:
            block_until = parser.parse(block_until)

        time_block_start = self.config["config"]["time_block_start"] or None
        if time_block_start:
            time_block_start = parser.parse(time_block_start)

        time_block_end = self.config["config"]["time_block_end"] or None
        if time_block_end:
            time_block_end = parser.parse(time_block_end)

        if time_block_end and time_block_start and time_block_end < time_block_start:
            time_block_end += timedelta(days=1)

        return Options(
            block_until=block_until,
            time_block_start=time_block_start,
            time_block_end=time_block_end
        )


config = Config()
