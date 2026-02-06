from url_builder import url_builder


def test_url_builder() -> None:
    _url_builder: url_builder.UrlBuilder = url_builder.UrlBuilder()

    # Assert default parameters
    assert _url_builder._get_year() == 2009
    assert _url_builder._get_month() == 2
    assert _url_builder._get_number() == 1
    assert (
        _url_builder.get_url()
        == "https://www.der-postillon.com/2009/02/newstickernewstickernewsti.html"
    )

    # Assert set parameters
    _url_builder._set_all_params(
        year=2023,
        month=5,
        number=5000,
    )
    assert _url_builder._get_year() == 2023
    assert _url_builder._get_month() == 5
    assert _url_builder._get_number() == 5000
    assert (
        _url_builder.get_url()
        == "https://www.der-postillon.com/2023/05/newsticker-5000.html"
    )

    # Assert some special URLs
    _url_builder._set_number(60)
    assert (
        _url_builder.get_url()
        == "https://www.der-postillon.com/2010/04/newsticker-60_05.html"
    )
    _url_builder._set_number(71)
    assert _url_builder.get_url() is None
