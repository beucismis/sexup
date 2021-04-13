import os

# import re
import qrcode

# import hashlib
import logging
from pyx import *

# import subprocess
from tempfile import mkstemp
from datetime import datetime


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


class Pill:
    def __init__(self, asc_file):
        self.ASC_FILE = asc_file

        self.pageno = 0
        self.pageid = 0
        self.code_blocks = []

        self._init_pdf()

        with open(asc_file) as file:
            self.ASCDATA = file.read()

    def _init_pdf(self):
        unit.set(defaultunit="cm")
        self.pdf = document.document()

    def _generate_barcode(self, chunkdata):
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

    def _finish_page(self, pdf, canvas, pageno):
        canvas.text(10, 0.6, "Page {}".format(pageno + 1))
        pdf.append(document.page(canvas, paperformat=PF_OBJ, fittosize=0, centered=0))

    def generate_backup(self):
        chunkdata = "^1 "
        c = canvas.canvas()

        for char in list(self.ASCDATA):
            if len(chunkdata) + 1 > QRCODE_MAX_BYTE:
                self.code_blocks.append(self._generate_barcode(chunkdata))
                chunkdata = "^" + str(len(self.code_blocks) + 1) + " "
            chunkdata += char

        self.code_blocks.append(self._generate_barcode(chunkdata))

        for bc in range(len(self.code_blocks)):
            if self.pageid >= QRCODE_PER_PAGE:
                self._finish_page(self.pdf, c, self.pageno)
                c = canvas.canvas()
                self.pageno += 1
                self.pageid = 0

            c.text(
                QRCODE_X_POS[self.pageid] + TEXT_X_OFFSET,
                QRCODE_Y_POS[self.pageid] + TEXT_Y_OFFSET,
                "{} ({}/{})".format(
                    text.escapestring(self.ASC_FILE), bc + 1, len(self.code_blocks)
                ),
            )

            c.insert(
                bitmap.bitmap(
                    QRCODE_X_POS[self.pageid],
                    QRCODE_Y_POS[self.pageid],
                    self.code_blocks[bc],
                    height=QRCODE_HEIGHT,
                )
            )

            self.pageid += 1

        self._finish_page(self.pdf, c, self.pageno)

        fd, temp_barcode_path = mkstemp(".pdf", "qr_", ".")
        self.pdf.writetofile(temp_barcode_path)
        os.rename(temp_barcode_path.split(os.sep)[-1], self.ASC_FILE + ".pdf")
