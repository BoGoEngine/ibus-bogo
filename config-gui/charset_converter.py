def convert(html, text, sourceCharset):
    html = html.encode('latin-1').decode(sourceCharset)
    text = text.encode('latin-1').decode(sourceCharset)

    if sourceCharset == "tcvn3":
        html = html.replace("&shy;", "ư")

    # TODO Process LibreOffice's font tags
    #
    # Most of the times, legacy text will be enclosed in
    # <font face=".VnTimes"> tags. Using jQuery, we should be able to extract
    # these tags, convert and remove them so that only Unicode text remains.

    return html, text
