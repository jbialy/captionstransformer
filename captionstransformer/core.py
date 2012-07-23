from datetime import datetime, timedelta

class Reader(object):
    def __init__(self, fileobject):
        self.fileobject = fileobject
        self.captions = []
        self.rawcontent = None

    def read(self):
        self.rawcontent = self.fileobject.read()
        return self.captions

    def add_caption(self, caption):
        self.captions.append(caption)

    def __repr__(self):
        return u"%s" % [caption.text for caption in self.captions]

    def close(self):
        self.fileobject.close()


class Writer(object):
    DOCUMENT_TPL = "%s"
    CAPTION_TPL = "MUST BE IMPLEMENTED: %(start)s , %(end)s, %(text)s"

    def __init__(self, fobject, captions=None):
        self.fileobject = fobject
        self.captions = []
        if captions is not None:
            self.captions = captions

    def add_caption(self, caption):
        self.captions.append(caption)

    def set_captions(self, captions):
        self.captions = captions

    def write(self, captions=None):
        if captions is not None:
            self.captions = captions
        value = self.captions_to_text()
        self.fileobject.write(value)

    def close(self):
        self.fileobject.close()

    def captions_to_text(self):
        text = self.DOCUMENT_TPL
        buffer = u""
        for caption in self.captions:
            time_info = self.format_time(caption)
            buffer+= self.CAPTION_TPL % {'start': time_info['start'],
                                    'end': time_info['end'],
                                    'text': caption.text}
        return text % buffer

    def format_time(self, caption):
        return {'start': start.strftime('%H:%M:%S.%f')[:-3],
                'end': end.strftime('%H:%M:%S.%f')[:-3]}


class Caption(object):
    def __init__(self):
        self._duration = None
        self._start = None
        self._end = None
        self._text = u""
        self.encoding = "utf-8"

    def update(self):
        if self._end is None and\
           self._start is not None and\
           self._duration is not None:
            self._end = self.start + self.duration
        if self._duration is None and\
           self._start is not None and\
           self._end is not None:
            self._duration = self._end - self._start

    def get_duration(self):
        return self._duration

    def set_duration(self, value):
        if type(value) != timedelta:
            raise ValueError('duration must be a timedelta: %s' % value)
        self._duration = value
        self.update()

    duration = property(get_duration, set_duration)

    def get_start(self):
        return self._start

    def set_start(self, value):
        if type(value) != datetime:
            raise ValueError('start must be a datetime instance: %s' % type(value))
        self._start = value
        self.update()

    start = property(get_start, set_start)

    def get_end(self):
        return self._end

    def set_end(self, value):
        if type(value) != datetime:
            raise ValueError('start must be a datetime instance: %s' % type(value))
        self._end = value
        self.update()

    end = property(get_end, set_end)

    def get_text(self):
        return self._text

    def set_text(self, value):
        if type(value) == str:
            value = str.decode(self.encoding)
        elif type(value) != unicode:
            raise ValueError("text must be either encoded string or unicode")
        self._text = value

    text = property(get_text, set_text)

    def __repr__(self):
        return self.text


def get_date(hour=0, minute=0, second=0, millisecond=0, microsecond=0):
    """return a reference date to 1901-01-01 to work with time"""
    dt = None
    if second > 59:
        dt = timedelta(seconds=second)
        second = 0
    if millisecond:
        microsecond += millisecond * 1000
    date = datetime(year=1900, month=1, day=1, hour=hour, minute=minute,
                    second=second, microsecond=microsecond)
    if dt:
        date += dt
    return date
