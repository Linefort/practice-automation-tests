# окна на страницах modals и ads сделаны одним плагином Popup Maker,
# поэтому их XPath собираются здесь, а страницы указывают только текст окна


def popup_xpath(text):
    return ("//div[(@role='dialog' or contains(@class, 'pum-container'))]"
            f"[.//*[contains(normalize-space(), '{text}')]]")


TITLE = "//*[contains(@class, 'pum-title') or contains(@class, 'popmake-title')]"
CONTENT = "//*[contains(@class, 'pum-content') or contains(@class, 'popmake-content')]"
CLOSE = "//*[contains(@class, 'pum-close') or contains(@class, 'popmake-close')]"
