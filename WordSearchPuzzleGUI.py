import base64
import io
import json
import sys
import uuid
import webbrowser

import PySimpleGUI as sg
import win32clipboard
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtWidgets import QApplication

import WordSearchPuzzleGen as SWP

# Setup variables
global layout, image
sg.theme('Dark')
seed = str(uuid.uuid4()).replace('-', '')
default_font = 'Dosis 12 bold'
category_name_font = 'Dosis 11 bold'
github_view_data = """iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAD
                   sMAAA7DAcdvqGQAAAV4SURBVGhDzZnNbhxFEMfH65z8tR+OjUVix7n4YIOUPAHYES8RLnkLMEKIF/CVSOHC1S/hTeQLEgpEDv
                   YFoQQQKGDi3bUdLsRr+l9dNVvT0zPTvd6Y/DY1XVXT3VXV0zM73iQjYvno6KhzHgH6Y5wdfnHGuB0KJMTqhRkzsDoUNW5jaNC
                   SGtgeCTwl5mxYTxxRq8CBLoXYKxR0Rer1+q3LLAIgHuKyeXG2t7fbmPT/AvE5leGJfRK9KfgJV0rhPsTgZrM51I33Juh0Ot1W
                   q9VkM4f3HsHlfJuKAMgnaptNTEzQjf22UvQAyG0tdGY1x/zCNauYUYvXF5PH331r7RHw+RdfJg8efM1Wkvz14nfW8vgezRlHW
                   RFgTgpxOCwJWgUWR4JSMuaALKrmdIvRBr6xS58OcwvvsgYwNPSrxddXQmv/wHf44g/W/Zg6cON3raVu9qoiCMSUuFg2sVM/J+
                   L65UK7vtwcOLBegZtv1LvWIN75QCdh+7xPjozPCOrL1jI4ZzXxmQ/PHQsVYgYHjpXwwLQ0TNkp2meTo5Zty0DPpm70wHR03lF
                   XJI0tAhwfze34cgJ8fpEhQCFBf9zMzi+YGLKqiFf8kfO+XnTOFOt+yK8+iBcI5V8zryI/kFmFzYsEgUgHyi8iV5waR9KxjuSu
                   ZCCS/5iZoHLY7Nw7rBWhH69aD6G8/8vDP1krBt8pQfcIwogAbVuhdSbRxzAZjBUBWg9gOfxmp0tvgnKbijoHwflcH4jTz2aq7
                   YEvMz6AO3c+uhe0tVpX51m7fJ79/BP+QmXLT7vdfhhUSHPWFOJu5dhbQcA4TckceJt68v3jZGlpkT3FBG4tE43qVeLaGbFJaD
                   vVMU5L2sdIZozdYiFFgLgvxGB4n6dovYTMmDjCnlomgAiCpUmyLWT6Obbrlzanc6vPVYF7JKgQ/eovU1MgtKI7QYuSEL8+n9G
                   5jWFra+tR0M3eaF01R3RDQbrVFPkEOVc0h79v9+hv1osxC30zqBBQb85Sm6ZhlKKRbooafY5Sp4N/rl7nJWvl0Dc7fmZhOwiJ
                   V1Z+yanMOeiYJ2wp/Uj+WI9lc1Gewaii3myxZkBwXs0c3nNwFGWsz1m91zmyZgXYVqZ5TuFCtxeoNwbFFNWiUwJ68nzK2Rb0u
                   mFFAGwranGIKQSgGPvMKsOmN2Y+tmdYiONu9U8HGimEHr9iaL66fz+Zqft/ocSKUUA3N9ipmAP+yU1APhbg2Jhv2CJAqviuyn
                   S9wSt6npz0qp8Jtr/NTbeCtn/79ZfKl8EqdCHpF6Lx5ZbfJm/rQ5IhyGroVgSIPoIiMvnqb3bvkh+jGI7+yaeb1lmEbxsZoWV
                   zfCMgk6++8oRvi03N2NVD5x+fPk1u3FgiWzPNfWQw+kKnq2+mJJ19APrJcc8akegtJeTetVZWVm6zmnKKgCYDlLj23vvJ1HQ9
                   2d3dpXN7e3tkI0FaAhbRz/t4D8v6SDfNMPjyA7nKwM7OTnt9ff1DNolr15eSXsANH8PpyTFrYeAtd2NjY53NDN5CgO9/rKamZ
                   1grBitdOKlDTCFD/Y8VwCD3PQyBIZ9tbpptYl/dIR/fvZvq5pDq1tT2QGKoKiIIbDMTuJKJyaloCQHxOZVSgnbB6urqrf39/d
                   JfJCcnp+xsstg0sznI6tODBpfImjj16vSUDT9ra2u3Dw4OnrBZCoULBSvEag6zwqyF88+r4kJ8j9gyCu8RH5jcULBXpUa3dYG
                   /cD0Qo4kgbAYTVQjTRSDAtkXnhgtH+aJlyfhZV/CUmHOoZ/wwhaRwbHCz3+93aefpXFnsrUJa6kN/jLPD46+Ay4Un8LA8Pj5+
                   r1arfTB+5Ur6pXr2+vXDfj95dHb27zfGfG69oyJJ/gNAqt4egK2qkgAAAABJRU5ErkJggg=="""

def get_scaling():
    """
    Gets scaling data.
    Source: https://github.com/PySimpleGUI/PySimpleGUI/issues/4998#issuecomment-985360403
    :return: The scaling data
    :rtype: float
    """

    root = sg.tk.Tk()
    scaling = root.winfo_fpixels('1i') / 72
    root.destroy()
    return scaling


def to_clipboard(target_img):
    """
    Puts a PIL image into the clipboard.
    Source: https://stackoverflow.com/a/7052068/16469230
    :param target_img: A PIL image to send to the clipboard
    :type target_img: PIL.Image
    :returns: None
    :rtype: None
    """

    def send_to_clipboard(clip_type, image_data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, image_data)
        win32clipboard.CloseClipboard()

    output = io.BytesIO()
    target_img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)


def pil2pixmap(im):
    """
    Converts a PIL image to a PyQt5 Pixmap.
    Source: https://stackoverflow.com/a/48705903/16592435
    :param im: A pil image to convert to a pixmap
    :type im: PIL.Image
    :returns: A pixmap
    :rtype: PyQt5.QtGui.QPixmap
    """

    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(
        data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    qim = qim.scaled(int(2480 * 2), int(3508 * 2),
                     Qt.KeepAspectRatio, Qt.SmoothTransformation)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap


def save_configuration(variables_info):
    """
    Saves all the settings for the generator as a file that can be loaded later.
    :param variables_info: All variable values and names
    :type variables_info: List[Tuple(*, str)]
    :returns: None
    :rtype: None
    """

    # Pops up a message that requests the user to save as a file, then store the file into a var
    save_filename = sg.popup_get_file("Save as", file_types=(("CONFIG", '.swpconfig'), ("CONFIG", '.swpconfig')),
                                      save_as=True, no_window=True)
    if save_filename:

        # Stores all variable names and values inside a dict
        conf = {}
        for i in variables_info:
            variable_name = i[1]
            value = i[0]
            conf[variable_name] = value

        conf = str(conf)

        # Corrects all python vars to string
        conf = conf.replace("'", '"')
        conf = conf.replace("True", '"True"')
        conf = conf.replace("False", '"False"')
        conf = conf.replace("None", '"None"')

        # Encodes the dictionary with base64
        message_bytes = conf.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        # Creates a file in the selected directory
        with open(save_filename, 'w') as f:
            f.write(base64_message)

        sg.popup(f'Settings Configuration file saved as {save_filename}')


def load_configuration(window):
    """
    Loads a .swpconfig file and load the settings.
    :param window: The window so it can update the loaded values
    :type window: PySimpleGui.Window
    :return: None
    :rtype: None
    """

    # Popups a message that requests the user to select a file to load the settings off of
    save_filename = sg.popup_get_file(
        "Load configuration file", file_types=(("CONFIG", '.swpconfig'), ("CONFIG", '.swpconfig')), no_window=True
    )

    # A dict that associates all the var keys with the keys of the window
    key_dict = {
        "allow_diagonals": '-1TOGGLE-',
        "add_random_chars": '-2TOGGLE-',
        "add_word_bank_outline": '-3TOGGLE-',
        "grid_line_color": '-1COLOR_COMBO-',
        "grid_background_color": '-2COLOR_COMBO-',
        "grid_text_color": '-3COLOR_COMBO-',
        "grid_random_chars_color": '-4COLOR_COMBO-',
        "page_background_color": '-5COLOR_COMBO-',
        "page_title_color": '-6COLOR_COMBO-',
        "page_subtitle_color": '-7COLOR_COMBO-',
        "word_bank_outline_color": '-8COLOR_COMBO-',
        "word_bank_background_color": '-9COLOR_COMBO-',
        "word_bank_word_color": '-10COLOR_COMBO-',
        "words": '-INPUT1STR-',
        "available_random_chars": '-INPUT2STR-',
        "page_title": '-INPUT3STR-',
        "page_subtitle": '-INPUT4STR-',
        "grid_cell_size": '-INPUT1NUM-',
        "grid_cells_in_row": '-INPUT2NUM-',
        "grid_line_width": '-INPUT3NUM-',
        "grid_text_size": '-INPUT4NUM-',
        "word_bank_outline_width": '-INPUT5NUM-',
        "word_bank_word_size": '-INPUT6NUM-',
        "page_title_size": '-INPUT7NUM-',
        "page_subtitle_size": '-INPUT8NUM-',
        "random_seed": "-OTHER1-"
    }

    if save_filename:

        # Opens the selected file and stores it's content into a var
        data = open(save_filename).read().replace('\n', '')

        # Decodes the data with base64
        decoded_data = base64.b64decode(data + '==').decode()

        try:

            # Converts the decoded string to a  python dict
            data = json.loads(decoded_data)

            # Updates all the window elements according to the loaded data
            for counter, key in enumerate(data):
                w_key = key_dict[key]
                window[w_key].update(data[key].replace(
                    'None', '') if type(data[key]) == str else data[key])

        except json.JSONDecodeError as ex:
            sg.popup(
                f'Error while opening the config ({save_filename}) \nError:\n {ex}')


def reset_to_default(window):
    """
    Reset all element values to default.
    :param window: The window so it can update the loaded values
    :type window: PySimpleGui.Window
    :return: None
    :rtype: None
    """

    # Toggles
    window['-1TOGGLE-'].update(True)

    window['-2TOGGLE-'].update(True)
    window['-3TOGGLE-'].update(True)

    # Colors
    window['-1COLOR_COMBO-'].update('Black')
    window['-2COLOR_COMBO-'].update('White')
    window['-3COLOR_COMBO-'].update('Black')
    window['-4COLOR_COMBO-'].update('Black')
    window['-5COLOR_COMBO-'].update('White')
    window['-6COLOR_COMBO-'].update('Black')
    window['-7COLOR_COMBO-'].update('Gray')
    window['-8COLOR_COMBO-'].update('Black')
    window['-9COLOR_COMBO-'].update('White')
    window['-10COLOR_COMBO-'].update('Black')

    # Strings
    window['-INPUT1STR-'].update('Bagel, Three, House')
    window['-INPUT2STR-'].update('abcdefghijklmnopqrstuvwxyz')
    window['-INPUT3STR-'].update('Search word puzzle')
    window['-INPUT4STR-'].update('Circle the correct words')

    # Numbers
    window['-INPUT1NUM-'].update('100')
    window['-INPUT2NUM-'].update('auto')
    window['-INPUT3NUM-'].update('100')
    window['-INPUT4NUM-'].update('100')
    window['-INPUT5NUM-'].update('100')
    window['-INPUT6NUM-'].update('100')
    window['-INPUT7NUM-'].update('100')
    window['-INPUT8NUM-'].update('100')

    # Other
    window['-OTHER1-'].update('')


def print_image(target_image):
    """
    This function handles the print preview and the print itself.
    Source: https://github.com/PyQt5/PyQt/issues/145#issuecomment-975009897
    :param target_image: A pil image to print preview and print
    :type target_image: PIL.Image
    :return: None
    :rtype: None
    """

    def draw_image(printer_obj):
        painter = QPainter()
        painter.begin(printer_obj)
        painter.setPen(Qt.red)
        painter.drawPixmap(0, 0, pil2pixmap(target_image.resize(
            (int(2480 * 2), int(3508 * 2)), Image.LANCZOS)))
        painter.end()
        dlg.close()
        app.exit()

    app = QApplication(sys.argv)
    printer = QPrinter(QPrinter.HighResolution)
    printer.setResolution(600)
    printer.setCreator('KingOfTNT10 : IlaiK')
    dlg = QPrintPreviewDialog(printer)
    dlg.paintRequested.connect(draw_image)
    dlg.exec_()
    app.exec_()
    dlg.close()
    app.exit()


def save_file(img):
    """
    Saves a PIL image to a file.
    :param img: A PIL image to save to a file
    :type img: PIL.Image
    :return: None
    :rtype: None
    """

    # Pops up a message that requests the user to save the image as a file
    save_filename = sg.popup_get_file(
        "Save as", file_types=(("PNG", '.png'), ("JPG", ".jpg")), save_as=True, no_window=True
    )
    if save_filename:
        # Save the image
        img.save(save_filename)

        sg.popup(f"Saved: {save_filename}")


def image_to_bios(target_image, size: tuple):
    """
    Saves a PIL image to bios after it gets resized and keeps it's ratio
    and returns it's value as a base64 encoded data.
    :param target_image: A PIL image to get as a base64 encoded data
    :type target_image: PIL.Image
    :param size: The wanted size of the image
    :type size: Tuple(int, int)
    :return: The image as a base64 encoded data
    :rtype: str
    """

    target_image.thumbnail(size)
    bio = io.BytesIO()
    target_image.save(bio, format="PNG")
    value = bio.getvalue()
    bio.close()
    return value


def setup_layout():
    """
    Set's up the layout of the window
    :return: None
    :rtype: None
    """

    global layout

    toggle_tab = [
        [sg.Checkbox("Diagonals", default=True, key='-1TOGGLE-', pad=(20, 0), font=default_font, enable_events=True,
                     background_color=sg.theme_background_color())],
        [sg.Checkbox("Add randomized characters", default=True, key='-2TOGGLE-', pad=(20, 0), font=default_font,
                     enable_events=True, background_color=sg.theme_background_color())],
        [sg.Checkbox("Add word bank outline", default=True, key='-3TOGGLE-', pad=(20, 0), font=default_font,
                     enable_events=True, background_color=sg.theme_background_color())],

    ]

    color_tab = [
        [sg.Text("Grid - line color:", pad=(20, 0), font=default_font, background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-1COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Grid - background color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-2COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Grid - text color:", pad=(20, 0), font=default_font, background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-3COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Grid - randomized characters color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-4COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Page - background color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-5COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Page - title color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-6COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Page - subtitle color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-7COLOR_COMBO-', default_value="Gray", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Word bank - outline color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-8COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Word bank - background color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-9COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],
        [sg.Text("Word bank - word color:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
                  key='-10COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
                  background_color=sg.theme_background_color())],

    ]

    string_tab = [
        [sg.Text("Words (seperated by ','):", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="Bagel, Three, House", font=default_font,
                              size=(25, 1), key='-INPUT1STR-', enable_events=True,
                              background_color=sg.theme_background_color())]])],
        [sg.Text("Available random characters:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="abcdefghijklmnopqrstuvwxyz", font=default_font,
                              size=(25, 1), key='-INPUT2STR-', enable_events=True,
                              background_color=sg.theme_background_color())]])],
        [sg.Text("Page title:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Input(default_text="Search Word Puzzle", font=default_font,
                  size=(25, 1), key='-INPUT3STR-', enable_events=True, background_color=sg.theme_background_color())],
        [sg.Text("Page subtitle:", pad=(20, 0), font=default_font,
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Multiline(default_text="Circle the correct words", key='-INPUT4STR-', font=default_font,
                                  autoscroll=True, size=(30, 1), background_color=sg.theme_background_color(),
                                  enable_events=True)]])],

    ]

    number_tab = [
        [sg.Text("Grid - cell size:", font=default_font, pad=(20, 0), background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT1NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Grid - cells in a row ('auto' to automatically set size):", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="auto", font=default_font, size=(4, 1), key='-INPUT2NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Grid - line thickness:", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT3NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Grid - text size:", font=default_font, pad=(20, 0), background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT4NUM-',
                              background_color=sg.theme_background_color(), enable_events=True)]])],
        [sg.Text("Word bank - outline thickness:", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT5NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Word bank - word size:", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT6NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Page - title size:", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT7NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],
        [sg.Text("Page - subtitle size:", font=default_font, pad=(20, 0),
                 background_color=sg.theme_background_color()),
         sg.Column([[sg.Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT8NUM-',
                              enable_events=True, background_color=sg.theme_background_color())]])],

    ]

    other_tab = [
        [sg.Text("Random seed (leave empty for randomness):", font=default_font, pad=(20, 0),#7af820
                 background_color=sg.theme_background_color()), sg.Input(default_text="", font=default_font,
                                                                         size=(3, 1), key='-OTHER1-',
                                                                         enable_events=True,
                                                                         background_color=sg.theme_background_color())],
        [sg.Checkbox('Enhanced resolution (worse performance)', key='switch', enable_events=True,
                     tooltip='This option is recommended only for viewing the end result', pad=(20, 0))],
        [sg.Button('Randomize', font=default_font,
                   key='RANDOMIZE', pad=(20, 10))],

    ]

    tabgroup_layout = [[
        sg.Tab('Toggles', toggle_tab),
        sg.Tab('Colors', color_tab),
        sg.Tab('Strings', string_tab),
        sg.Tab('Numbers', number_tab),
        sg.Tab('Other', other_tab),
    ]]

    options_tab_group = [[
        sg.TabGroup(tabgroup_layout, enable_events=True,
                    key='-TAB_GROUP-', expand_x=False, expand_y=True),
        sg.Image(key='-CWIMAGE-', right_click_menu=['&Right', ['Copy', 'Save as...', 'Print']])],
        [sg.Button("Reset to default", key='-RESET-', button_color=sg.theme_background_color(),
                   mouseover_colors=sg.theme_background_color()),
         sg.Button(image_data=github_view_data, size=50, mouseover_colors=sg.theme_background_color(),
                   button_color=sg.theme_background_color(), border_width=0, key='-VIEW_GITHUB-')
         ]
    ]

    start_window = [
        [sg.Button('Create Page', key='-CREATE_PAGE-')]
    ]

    menu_def = [['&!File', ['&!Save', '&!Open...']]]

    layout = [
        [sg.Menu(menu_def, visible=True, key='MENU')],
        [sg.Column(options_tab_group, visible=False, key='OPTIONS'),
         sg.Column(start_window, key='START')]
    ]


def move_center(window):
    """
    Moves the window to the center of the screen.
    :param window: The window that needs to be moved to the center
    :type window: PySimpleGui.Window
    :return: None
    :rtype: None
    """

    # Gets the center of the screen
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.current_size_accurate()
    x, y = (screen_width - win_width) // 2, (screen_height - win_height) // 2

    # Moves the window
    window.move(x, y)


def window_loop():
    """
    The main window loop with all the error handling and generator calls.
    :return: None
    """

    global seed, layout, image

    # Set's up the window

    window = sg.Window("Search word puzzle generator",
                       layout, finalize=True, resizable=True)
    window.grab_any_where_on()

    # window.Maximize()
    toggle = False

    # Window loop
    while True:
        event, values = window.read()

        if event == '-VIEW_GITHUB-':
            webbrowser.open('https://github.com/KingOfTNT10/WordSearchPuzzleGenerator')  # Go to example.com

        if event == 'Copy':
            event = '-COPY_TO_CLIPBOARD-'

        if event == 'Save as...':
            event = '-SAVE_FILE-'

        if event == 'Print':
            event = '-PRINT-'

        if event == 'Save':
            event = '-SAVE_CONFIG-'

        if event == 'Open...':
            event = '-LOAD_CONFIG-'

        if event == '-CREATE_PAGE-':
            window['OPTIONS'].update(visible=True)
            window['START'].update(visible=False)
            window['MENU'].update([['&File', ['&Save', '&Open...']]])
            window.move(0, 0)

        # Detects if the window closed if it does it will exit the program
        if event == sg.WINDOW_CLOSED or event == 'EXIT':
            window.close()
            exit(0)

        # If the randomize button was clicked it will randomize the seed
        if event == 'RANDOMIZE':
            seed = str(uuid.uuid4()).replace('-', '')

        # If the enhanced res toggle button was clicked it will switch the image and the variable and change the tooltip
        if event == 'switch':
            toggle = window['switch'].get()

        # If the user has pressed the load config button it will call the load_configuration function,
        # This function is before the image gen because it needs to update after the changes have been made
        if event == '-LOAD_CONFIG-':
            load_configuration(window)

        # -------- Store all window element values into variables --------#

        # Toggles
        allow_diagonals = window['-1TOGGLE-'].get()
        add_random_chars = window['-2TOGGLE-'].get()
        add_word_bank_outline = window['-3TOGGLE-'].get()

        # Colors
        grid_line_color = window['-1COLOR_COMBO-'].get()
        grid_background_color = window['-2COLOR_COMBO-'].get()
        grid_text_color = window['-3COLOR_COMBO-'].get()
        grid_random_chars_color = window['-4COLOR_COMBO-'].get()
        page_background_color = window['-5COLOR_COMBO-'].get()
        page_title_color = window['-6COLOR_COMBO-'].get()
        page_subtitle_color = window['-7COLOR_COMBO-'].get()
        word_bank_outline_color = window['-8COLOR_COMBO-'].get()
        word_bank_background_color = window['-9COLOR_COMBO-'].get()
        word_bank_word_color = window['-10COLOR_COMBO-'].get()

        # Strings
        words = window['-INPUT1STR-'].get()
        available_random_chars = window['-INPUT2STR-'].get()
        page_title = window['-INPUT3STR-'].get()
        page_subtitle = window['-INPUT4STR-'].get()

        # Numbers
        grid_cell_size = window['-INPUT1NUM-'].get()
        grid_cells_in_row = window['-INPUT2NUM-'].get()
        grid_line_width = window['-INPUT3NUM-'].get()
        grid_text_size = window['-INPUT4NUM-'].get()
        word_bank_outline_width = window['-INPUT5NUM-'].get()
        word_bank_word_size = window['-INPUT6NUM-'].get()
        page_title_size = window['-INPUT7NUM-'].get()
        page_subtitle_size = window['-INPUT8NUM-'].get()

        # Other
        random_seed = None if window['-OTHER1-'].get(
        ) == "" else window['-OTHER1-'].get()

        # Set's up the the error list variable
        checks = [False, False, False, False, False,
                  False, False, False, False, False, False]

        # Convert the words variable from a string to a list
        t_words = []
        for i in words.replace(' ', '').replace(',,', ',').split(','):
            if i != '':
                t_words.append(i)
        words = t_words

        # If the words list is empty it will show an error
        if not words:
            window['-INPUT1STR-'].set_tooltip("This field can't be empty")
            window['-INPUT1STR-'].ParentRowFrame.config(background='red')
            checks[0] = False

        # If the words list is bigger than 15 it will show an error
        elif len(words) > 15:
            window['-INPUT1STR-'].ParentRowFrame.config(background='red')
            window['-INPUT1STR-'].set_tooltip(
                "You have reached the max word limit (15)")
            checks[0] = False

        # If the chars in the word list is bigger than 60 it will show an error
        elif len(''.join(words)) > 65:
            window['-INPUT1STR-'].ParentRowFrame.config(background='red')
            window['-INPUT1STR-'].set_tooltip(
                "You have reached the max character limit (65)")
            checks[0] = False

        # If the number of words is lower than 3 it will show an error
        elif len(words) < 2:
            window['-INPUT1STR-'].set_tooltip("You need at least 3 words")
            window['-INPUT1STR-'].ParentRowFrame.config(background='red')
            checks[0] = False

        # Checks if the variable grid_cells_in_row is NOT auto
        # (which means the user has set the number of cells in a row for the grid)
        elif grid_cells_in_row != 'auto':

            # If the length of the longest word in the words is bigger than grid_cells_in_row it will show an error
            if len(max(words, key=len)) >= int(grid_cells_in_row):
                window['-INPUT1STR-'].set_tooltip(f"The length of {max(words, key=len)} is larger then "
                                                  f"or equal to the cells in a row, either change the "
                                                  f"word or\nchange the cells in a row to 'auto' or to "
                                                  f"more than {len(max(words, key=len))}")
                window['-INPUT1STR-'].ParentRowFrame.config(background='red')
                checks[0] = False

            else:
                window['-INPUT1STR-'].set_tooltip('All good :)')
                window['-INPUT1STR-'].ParentRowFrame.config(
                    background=sg.theme_background_color())
                checks[0] = True

        else:
            window['-INPUT1STR-'].set_tooltip('All good :)')
            window['-INPUT1STR-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[0] = True

        # If the number of new lines in the subtitle is bigger than 2 it will show an error
        if page_subtitle.count('\n') > 2:
            window['-INPUT4STR-'].set_tooltip(
                'You have reached the maximum lines (3)')
            window['-INPUT4STR-'].ParentRowFrame.config(background='red')
            checks[-1] = False

        else:
            window['-INPUT4STR-'].set_tooltip('All good :)')
            window['-INPUT4STR-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[-1] = True

        # If available_random_chars (the random chars it will put on the grid) is empty it will show an error
        if available_random_chars == "":
            window['-INPUT2STR-'].set_tooltip("This field cannot be empty!")
            window['-INPUT2STR-'].ParentRowFrame.config(background='red')
            checks[1] = False

        else:
            window['-INPUT2STR-'].set_tooltip('All good :)')
            checks[1] = True
            window['-INPUT2STR-'].ParentRowFrame.config(
                background=sg.theme_background_color())

        # If the cell size is empty it will show an error
        if grid_cell_size == "":
            window['-INPUT1NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT1NUM-'].ParentRowFrame.config(background='red')
            checks[2] = False

        # If the cell size is not a number it will show an error
        elif not grid_cell_size.isdigit():
            window['-INPUT1NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT1NUM-'].ParentRowFrame.config(background='red')
            checks[2] = False

        else:
            grid_cell_size = int(grid_cell_size)

            # If the cell size is bigger than 100 it will show an error
            if grid_cell_size > 100:
                window['-INPUT1NUM-'].set_tooltip(
                    "This field has to be lower than or equal to 100")
                window['-INPUT1NUM-'].ParentRowFrame.config(background='red')
                checks[2] = False

            else:
                window['-INPUT1NUM-'].set_tooltip('All good :)')
                window['-INPUT1NUM-'].ParentRowFrame.config(
                    background=sg.theme_background_color())
                checks[2] = True

        # If the cells in a row field is empty it will show an error
        if grid_cells_in_row == "":
            window['-INPUT2NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
            checks[3] = False

        # If the cells in a row field is NOT auto and is not a digit it will show an error
        elif grid_cells_in_row != "auto" and not grid_cells_in_row.isdigit():
            window['-INPUT2NUM-'].set_tooltip(
                "This field has to be a number or 'auto'")
            window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
            checks[3] = False

        else:

            # If the cells in a row field is NOT auto it will convert it to a number
            if grid_cells_in_row != "auto":
                grid_cells_in_row = int(grid_cells_in_row)

                # If the cells in a row are bigger than 100 it will show an error
                if grid_cells_in_row > 100:
                    window['-INPUT2NUM-'].set_tooltip(
                        "This field has to be lower than or equal to 100")
                    window['-INPUT2NUM-'].ParentRowFrame.config(
                        background='red')
                    checks[3] = False
                else:

                    # If the length of the longest word in the words is bigger
                    # than grid_cells_in_row it will show an error
                    if words and len(max(words, key=len)) >= grid_cells_in_row:
                        window['-INPUT2NUM-'].set_tooltip(
                            f"The length of {max(words, key=len)} is larger then or equal to the cells in a row, "
                            f"either change the word or\nchange the cells in a row to "
                            f"'auto' or to more than {len(max(words, key=len))}")
                        window['-INPUT2NUM-'].ParentRowFrame.config(
                            background='red')
                        checks[0] = False

                    else:
                        window['-INPUT2NUM-'].set_tooltip('All good :)')
                        window['-INPUT2NUM-'].ParentRowFrame.config(
                            background=sg.theme_background_color())
                        checks[3] = True

            else:
                window['-INPUT2NUM-'].set_tooltip('All good :)')
                window['-INPUT2NUM-'].ParentRowFrame.config(
                    background=sg.theme_background_color())
                checks[3] = True

        # If the line width of the grid is empty it will show an error
        if grid_line_width == "":
            window['-INPUT3NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT3NUM-'].ParentRowFrame.config(background='red')
            checks[4] = False

        # If the line width of the grid is NOT a digit it will show an error
        elif not grid_line_width.isdigit():
            window['-INPUT3NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT3NUM-'].ParentRowFrame.config(background='red')
            checks[4] = False

        # If line width of the grid is bigger than 100 is will show an error
        elif int(grid_line_width) > 100:
            window['-INPUT3NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT3NUM-'].ParentRowFrame.config(background='red')
            checks[4] = False

        else:
            grid_line_width = int(grid_line_width)
            window['-INPUT3NUM-'].set_tooltip("All good :)")
            window['-INPUT3NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[4] = True

        # If the text size of the grid is empty it will show an error
        if grid_text_size == "":
            window['-INPUT4NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT4NUM-'].ParentRowFrame.config(background='red')
            checks[5] = False

        # If the text size of the grid is NOT a number it will show an error
        elif not grid_text_size.isdigit():
            window['-INPUT4NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT4NUM-'].ParentRowFrame.config(background='red')
            checks[5] = False

        # If the text size of the grid is bigger than 100 it will show an error
        elif int(grid_text_size) > 100:
            window['-INPUT4NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT4NUM-'].ParentRowFrame.config(background='red')
            checks[5] = False

        else:
            grid_text_size = int(grid_text_size)
            window['-INPUT4NUM-'].set_tooltip("All good :)")
            window['-INPUT4NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[5] = True

        # If the word bank outline width is empty it will show an error
        if word_bank_outline_width == "":
            window['-INPUT5NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT5NUM-'].ParentRowFrame.config(background='red')
            checks[6] = False

        # If the word bank outline width is NOT a number it will show an error
        elif not word_bank_outline_width.isdigit():
            window['-INPUT5NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT5NUM-'].ParentRowFrame.config(background='red')
            checks[6] = False

        # If the word bank outline width is bigger than 100 it will show an error
        elif int(word_bank_outline_width) > 100:
            window['-INPUT5NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT5NUM-'].ParentRowFrame.config(background='red')
            checks[6] = False

        else:
            word_bank_outline_width = int(word_bank_outline_width)
            window['-INPUT5NUM-'].set_tooltip("All good :)")
            window['-INPUT5NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[6] = True

        # If the word bank's word size is empty it will show an error
        if word_bank_word_size == "":
            window['-INPUT6NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT6NUM-'].ParentRowFrame.config(background='red')
            checks[7] = False

        # If the word bank's word size is NOT a number it will show an error
        elif not word_bank_word_size.isdigit():
            window['-INPUT6NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT6NUM-'].ParentRowFrame.config(background='red')
            checks[7] = False

        # If the word bank's word size is bigger than 100 it will show an error
        elif int(word_bank_word_size) > 100:
            window['-INPUT6NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT6NUM-'].ParentRowFrame.config(background='red')
            checks[7] = False

        else:
            word_bank_word_size = int(word_bank_word_size)
            window['-INPUT6NUM-'].set_tooltip("All good :)")
            window['-INPUT6NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[7] = True

        # If the page title size is empty it will show an error
        if page_title_size == "":
            window['-INPUT7NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT7NUM-'].ParentRowFrame.config(background='red')
            checks[8] = False

        # If the page title size is NOT a number it will show an error
        elif not page_title_size.isdigit():
            window['-INPUT7NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT7NUM-'].ParentRowFrame.config(background='red')
            checks[8] = False

        # If the page title size is bigger than it will show an error
        elif int(page_title_size) > 100:
            window['-INPUT7NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT7NUM-'].ParentRowFrame.config(background='red')
            checks[8] = False

        else:
            page_title_size = int(page_title_size)
            window['-INPUT7NUM-'].set_tooltip("All good :)")
            window['-INPUT7NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[8] = True

        # If the page subtitle size is empty it will show an error
        if page_subtitle_size == "":
            window['-INPUT8NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT8NUM-'].ParentRowFrame.config(background='red')
            checks[9] = False

        # If the page subtitle size is NOT a number it will show an error
        elif not page_subtitle_size.isdigit():
            window['-INPUT8NUM-'].set_tooltip("This field has to be a number!")
            window['-INPUT8NUM-'].ParentRowFrame.config(background='red')
            checks[9] = False

        # If the page subtitle size is bigger than 100 it will show an error
        elif int(page_subtitle_size) > 100:
            window['-INPUT8NUM-'].set_tooltip(
                "This field has lower than or equal to 100")
            window['-INPUT8NUM-'].ParentRowFrame.config(background='red')
            checks[9] = False

        else:
            page_subtitle_size = int(page_subtitle_size)
            window['-INPUT8NUM-'].set_tooltip("All good :)")
            window['-INPUT8NUM-'].ParentRowFrame.config(
                background=sg.theme_background_color())
            checks[9] = True

        # If all the checks have passed it will continue
        if not all(checks) and event in ['-SAVE_FILE-', '-PRINT-', '-COPY_TO_CLIPBOARD-']:
            sg.popup_error(
                'There are some errors in the input! look for red boxes')

        if all(checks):
            # Converts the string of words to a list
            tmp_words = []
            for i in words:
                if i != "":
                    tmp_words.append(i.replace(' ', ''))

            # Calls the search word puzzle generator with the settings the user has inputted
            if event != '-TAB_GROUP-':
                image = SWP.create_search_word_puzzle(
                    words=tmp_words,
                    random_chars=available_random_chars,
                    allow_diagonal=allow_diagonals,
                    cells_in_row=grid_cells_in_row,
                    square_size=grid_cell_size,
                    grid_separator_color=grid_line_color,
                    grid_background_color=grid_background_color,
                    grid_separator_width=grid_line_width,
                    grid_text_color=grid_text_color,
                    grid_text_size=grid_text_size,
                    random_char_color=grid_random_chars_color,
                    add_randomized_chars=add_random_chars,
                    page_color=page_background_color,
                    page_title=page_title,
                    title_color=page_title_color,
                    word_bank_outline=add_word_bank_outline,
                    word_bank_outline_color=word_bank_outline_color,
                    word_bank_outline_width=word_bank_outline_width,
                    word_bank_fill_color=word_bank_background_color,
                    words_in_word_bank_color=word_bank_word_color,
                    random_seed=random_seed if random_seed is not None else seed,
                    subtitle=page_subtitle,
                    subtitle_color=page_subtitle_color,
                    title_size=page_title_size,
                    subtitle_size=page_subtitle_size,
                    words_in_word_bank_size=word_bank_word_size,

                    # This is the resolution multiplier and it will rise automatically if
                    # the user has printed/copied/saved the image
                    res_multiplier=4 if (
                        event in ['-SAVE_FILE-', '-PRINT-', '-COPY_TO_CLIPBOARD-'] or toggle) else 2
                )
                # If the user has not pressed on the save/print/copy image buttons it will show the image on the page
            if event not in ['-SAVE_FILE-', '-PRINT-', '-COPY_TO_CLIPBOARD-']:
                window["-CWIMAGE-"].update(
                    data=image_to_bios(image, (750, 750)))

            # If the user has pressed the save file button it will call the save_file function
            if event == '-SAVE_FILE-':
                save_file(image)

            # If the user has pressed the print button it will call the print_image function
            elif event == '-PRINT-':
                print_image(image)

            # If the user has pressed the copy button it will call the to_clipboard function
            elif event == '-COPY_TO_CLIPBOARD-':
                to_clipboard(image)

            # If the user has pressed the save config button it will call the save_configuration function
            elif event == '-SAVE_CONFIG-':
                save_configuration([(allow_diagonals, f'{allow_diagonals=}'.split('=')[0]),
                                    (add_random_chars,
                                     f'{add_random_chars=}'.split('=')[0]),
                                    (add_word_bank_outline,
                                     f'{add_word_bank_outline=}'.split('=')[0]),
                                    (grid_line_color,
                                     f'{grid_line_color=}'.split('=')[0]),
                                    (grid_background_color,
                                     f'{grid_background_color=}'.split('=')[0]),
                                    (grid_text_color,
                                     f'{grid_text_color=}'.split('=')[0]),
                                    (grid_random_chars_color,
                                     f'{grid_random_chars_color=}'.split('=')[0]),
                                    (page_background_color,
                                     f'{page_background_color=}'.split('=')[0]),
                                    (page_title_color,
                                     f'{page_title_color=}'.split('=')[0]),
                                    (page_subtitle_color,
                                     f'{page_subtitle_color=}'.split('=')[0]),
                                    (word_bank_outline_color,
                                     f'{word_bank_outline_color=}'.split('=')[0]),
                                    (word_bank_background_color,
                                     f'{word_bank_background_color=}'.split('=')[0]),
                                    (word_bank_word_color,
                                     f'{word_bank_word_color=}'.split('=')[0]),
                                    (', '.join(words), f'{words=}'.split('=')[0]),
                                    (available_random_chars,
                                     f'{available_random_chars=}'.split('=')[0]),
                                    (page_title,
                                     f'{page_title=}'.split('=')[0]),
                                    (page_subtitle,
                                     f'{page_subtitle=}'.split('=')[0]),
                                    (grid_cell_size,
                                     f'{grid_cell_size=}'.split('=')[0]),
                                    (grid_cells_in_row,
                                     f'{grid_cells_in_row=}'.split('=')[0]),
                                    (grid_line_width,
                                     f'{grid_line_width=}'.split('=')[0]),
                                    (grid_text_size,
                                     f'{grid_text_size=}'.split('=')[0]),
                                    (word_bank_outline_width,
                                     f'{word_bank_outline_width=}'.split('=')[0]),
                                    (word_bank_word_size,
                                     f'{word_bank_word_size=}'.split('=')[0]),
                                    (page_title_size,
                                     f'{page_title_size=}'.split('=')[0]),
                                    (page_subtitle_size,
                                     f'{page_subtitle_size=}'.split('=')[0]),
                                    (random_seed, f'{random_seed=}'.split('=')[0])])

            # If the user has pressed the reset to default button it will call the reset_to_default function
            elif event == '-RESET-':
                reset_to_default(window)

        # If there was even one error it will disable the buttons and show a tooltip on the buttons
        else:
            pass


# If the file was ran directly it will run the program
if __name__ == '__main__':
    setup_layout()
    window_loop()
