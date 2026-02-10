import json
from pathlib import Path

import pytest

from urls_to_json_dumper.urls_to_json_dumper import UrlsToJsonDumper

URLS: dict[int, str|None] = {
    1: "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html",
    2: "https://www.der-postillon.com/2009/02/newsticker-2.html",
    71: None,
    500: "https://www.der-postillon.com/2013/09/newsticker-500-xxl-edition-106.html",
    1652: "https://www.der-postillon.com/2021/05/newsticker-1652.html",
    2358: "https://www.der-postillon.com/2026/02/newsticker-2358.html",
}

@pytest.fixture
def urls_to_json_dumper() -> UrlsToJsonDumper:
    return UrlsToJsonDumper(urls=URLS)

def test_remove_none_values(urls_to_json_dumper: UrlsToJsonDumper) -> None:
    urls_to_json_dumper._remove_none_values()
    expected_urls: dict[int, str | None] = URLS.copy()
    del expected_urls[71]  # Remove None entry
    assert urls_to_json_dumper.urls == expected_urls

def test_dump_urls(urls_to_json_dumper: UrlsToJsonDumper) -> None:
    filename: str = "test_urls.json"
    urls_to_json_dumper.dump_urls(filename=filename)
    file_path: Path = Path(filename)
    assert file_path.is_file()

    with open(filename, "r", encoding="utf-8") as json_file:
        loaded_urls: dict[str, str] = json.load(json_file)
        expected_urls: dict[int, str | None] = URLS.copy()
        del expected_urls[71]  # Remove None entry

        # The loaded JSON file only contains strings
        expected_urls: dict[str, str] = {str(k): v for k, v in expected_urls.items()}

        assert loaded_urls == expected_urls

    # Delete the created JSON file
    file_path.unlink(missing_ok=True)