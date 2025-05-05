def handleBtn(buttons,mousePos):
    for label, rect in buttons:
        if rect.collidepoint(mousePos):
            return label
    return None