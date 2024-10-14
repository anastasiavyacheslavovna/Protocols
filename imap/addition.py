import base64
import quopri
import re
from unittest.mock import DEFAULT


class ExceptionImap(Exception):
    def __init__(self, msg: str):
        self.msg = msg


def decode_data(data: str):
    reg = r"=\?([^?]+)\?(\w)\?([^?]*)\?="
    matches = re.finditer(reg, data, re.MULTILINE)
    for match in matches:
        encode_to = match.group(1).lower()
        decode_from = match.group(2).lower()
        ans = match.group(3)
        if decode_from == 'b':
            ans = base64.b64decode(ans.encode()).decode(encode_to)
        if decode_from == 'q':
            ans = quopri.decodestring(ans.encode()).decode(encode_to)
        data = data.replace(match.group(), ans)
    return data


def get_head(ans: str):
    from_re = r'(From):((\s.+\n)+)'
    to_re = r'(To):((\s.+\n)+)'
    date_re = r'(Date):(.+)'
    subject_re = r'(Subject):((\s.+\n)+)'
    res = [from_re, to_re, subject_re, date_re]
    result = {}

    for r in res:
        matches = re.finditer(r, ans, re.MULTILINE)
        for match in matches:
            val = match.group(2).replace('\r\n ', '').replace('?= =?', '?==?').strip()
            decode_val = decode_data(val)
            if len(decode_val) > 0:
                result[match.group(1)] = decode_val
    reg = r"\(\"[^\"]+\" \"[^\"]+\" \(\"name\" \"[^\"]+\"\)[^(]+ (\d+) [^(]+\(\"attachment\" \(\"filename\" \"([^\"]+)\"\)\)"
    matches = re.finditer(reg, ans, re.MULTILINE)
    for match in matches:
        attachment = decode_data(match.group(2)), match.group(1)
    if len(attachment) > 0:
        result['attachments'] = attachment
    return result


def print_head(head: dict[str, str]):
    if "From" in head:
        print(f'From: {head['From']}')
    if "To" in head:
        print(f'To: {head['To']}')
    if "Date" in head:
        print(f'Date: {head["Date"]}')
    if "Subject" in head:
        print(f'Subject: {head["Subject"]}')
    if "Attachments" in head:
        print("Attachments: ")
        for name, size in head['Attachments']:
            print(f'- {name} ({int(size) / 1.33 // 1024} kBytes)')
