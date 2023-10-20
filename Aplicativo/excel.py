import xlwings as xw

class Excel_sheet():
    def __init__(self, book, sheet):
        self.wb = xw.Book(book)
        self.hoja
