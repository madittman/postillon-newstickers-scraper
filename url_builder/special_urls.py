"""
Some URLs don't follow the rules, so they are kept in a dictionary.
A None entry means there was no newsticker with that number.
"""
from typing import Union


SPECIAL_URLS: dict[int, Union[str, None]] = {
    1: "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html",
    39: "https://www.der-postillon.com/2009/12/weihnachts-newsticker-39.html",
    45: "https://www.der-postillon.com/2010/01/berufsrisiko-newsticker-45.html",
    54: "https://www.der-postillon.com/2010/03/newsticker-54_08.html",
    56: "https://www.der-postillon.com/2010/03/newsticker-56_18.html",
    60: "https://www.der-postillon.com/2010/04/newsticker-60_05.html",
    71: None,
    100: "https://www.der-postillon.com/2010/09/newsticker-100-das-jubilaum.html",
    500: "https://www.der-postillon.com/2013/09/newsticker-500-xxl-edition-106.html",
    546: "https://www.der-postillon.com/2013/12/newsticker-546_23.html",
    696: "https://www.der-postillon.com/2014/12/newsticker-696-christmas-edition.html",
    991: "https://www.der-postillon.com/2016/12/newsticker-991-weihnachtsspezialausgabe.html",
    992: "https://www.der-postillon.com/2016/12/newsticker-992-weihnachtsspezialausgabe.html",
    1141: "https://www.der-postillon.com/2017/12/newsticker-1141-weihnachtsspezialausgabe.html",
    1290: "https://www.der-postillon.com/2018/12/newsticker-1290_28.html",
    1742: "https://www.der-postillon.com/2021/12/newsticker-1742-weihnachtsausgabe.html",
    1796: None,  # Somehow newsticker 1796 has number 1795 in URL and newsticker 1795 doesn't exist
    1869: "https://www.der-postillon.com/2022/10/newsticker-1869-halloween-spezialausgabe.html",
    2039: "https://www.der-postillon.com/2023/12/newsticker-2039-weihnachtsausgabe.html",
    2339: "https://www.der-postillon.com/2025/12/newsticker-2339-weihnachtsspezialausgabe.html",
}