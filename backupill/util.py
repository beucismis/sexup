import os

# import re
import qrcode

# import hashlib
import logging
from pyx import *

# import subprocess
from tempfile import mkstemp
from datetime import datetime


__all__ = ["generate_backup"]

TEXT_X_OFFSET = 0.6
TEXT_Y_OFFSET = 8.2
PLAINTEXT_MAXLINECHARS = 73

QRCODE_HEIGHT = 8
QRCODE_PER_PAGE = 6
QRCODE_MAX_BYTE = 140
QRCODE_X_POS = [1.5, 11, 1.5, 11, 1.5, 11]
QRCODE_Y_POS = [18.7, 18.7, 10, 10, 1.2, 1.2]

PF_STR = "A4"
PF_OBJ = document.paperformat.A4

# suppressing all the warnings
for name in logging.Logger.manager.loggerDict.keys():
    logging.getLogger(name).setLevel(logging.CRITICAL)


def _generate_barcode(chunkdata):
    qr = qrcode.QRCode(
        version=1,
        border=4,
        box_size=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )
    qr.add_data(chunkdata)
    qr.make(fit=True)

    im = qr.make_image(fill_color="black", back_color="white")

    return im


def _finish_page(pdf, canvas, pageno):
    canvas.text(10, 0.6, "Page {}".format(pageno + 1))
    pdf.append(document.page(canvas, paperformat=PF_OBJ, fittosize=0, centered=0))


def generate_backup(asc_file: str):
    """Generates PDF backup file.

    Parameters:
        asc_file (str): ASC (.asc) file path.
    """

    pageno = 0
    pageid = 0
    code_blocks = []
    chunkdata = "^1 "
    c = canvas.canvas()

    with open(asc_file) as file:
        ASCDATA = file.read()

    unit.set(defaultunit="cm")
    pdf = document.document()

    for char in list(ASCDATA):
        if len(chunkdata) + 1 > QRCODE_MAX_BYTE:
            code_blocks.append(_generate_barcode(chunkdata))
            chunkdata = "^" + str(len(code_blocks) + 1) + " "
        chunkdata += char

    code_blocks.append(_generate_barcode(chunkdata))

    for bc in range(len(code_blocks)):
        if pageid >= QRCODE_PER_PAGE:
            _finish_page(pdf, c, pageno)
            c = canvas.canvas()
            pageno += 1
            pageid = 0

        c.text(
            QRCODE_X_POS[pageid] + TEXT_X_OFFSET,
            QRCODE_Y_POS[pageid] + TEXT_Y_OFFSET,
            "{} ({}/{})".format(
                text.escapestring(asc_file.split(os.sep)[-1]), bc + 1, len(code_blocks)
            ),
        )

        c.insert(
            bitmap.bitmap(
                QRCODE_X_POS[pageid],
                QRCODE_Y_POS[pageid],
                code_blocks[bc],
                height=QRCODE_HEIGHT,
            )
        )

        pageid += 1

    _finish_page(pdf, c, pageno)

    fd, temp_barcode_path = mkstemp(".pdf", "qr_", ".")
    pdf.writetofile(temp_barcode_path)
    os.rename(temp_barcode_path.split(os.sep)[-1], asc_file + ".pdf")
