from openpyxl import load_workbook


class GlassPlate:
    def __init__(self, num, expected_dip, dipping_time, clean):
        self.num = num
        self.expected_dip = expected_dip
        self.dipping_time = dipping_time
        self.clean = clean
        self.number_of_dip = 0


SAMPLE_NUMBER = 0
DIPPING_NUMBER = 1
CLEAN = 2
DIPPING_TIME = 3


def read_dipping_parameter(file_name, sheet_name):
    glass_sample = []

    # read data from excel table
    wb = load_workbook(filename=file_name)
    wb.active = wb[sheet_name]
    data = wb.active['B1:K4']

    # Store the data
    for n in range(10):
        if data[DIPPING_NUMBER][n].value == 0 or data[DIPPING_NUMBER][n].value is None:
            continue
        else:
            glass_sample.append(
                GlassPlate(data[SAMPLE_NUMBER][n].value, data[DIPPING_NUMBER][n].value, data[DIPPING_TIME][n].value,
                           data[CLEAN][n].value))

    return glass_sample
