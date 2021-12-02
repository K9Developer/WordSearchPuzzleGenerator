import base64
import io
import uuid

import win32clipboard
from PIL import Image as PIL_IMAGE
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinter
from PyQt5.QtWidgets import QApplication
from PySimpleGUI import *

import WordSearchPuzzleGen as SWP

# Setup variables
global column1, column2, column3, column4, layout1
seed = str(uuid.uuid4()).replace('-', '')
default_button_texture = r'assets/images/button.png'
button_switch_on = r'assets/images/SwitchOn.png'
button_switch_off = r'assets/images/SwitchOff.png'
default_font = 'Dosis 12 bold'
category_name_font = 'Dosis 11 bold'
theme('Dark')


# TODO: CHNAGE VAR NAMES


def to_clipboard(image):
    """
    Puts a PIL image into the clipboard.
    Source: https://stackoverflow.com/a/7052068/16469230

    :param image: A PIL image to send to the clipboard
    :type image: PIL.Image
    :returns: None
    :rtype: None
    """

    def send_to_clipboard(clip_type, image_data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, image_data)
        win32clipboard.CloseClipboard()

    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
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
        im = PIL_IMAGE.merge("RGB", (b, g, r))
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    qim = qim.scaled(int(2480 * 2), int(3508 * 2), Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
    save_filename = popup_get_file("Save as", file_types=(("CONFIG", '.swpconfig'), ("CONFIG", '.swpconfig')),
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

        popup(f'Settings Configuration file saved as {save_filename}')


def load_configuration(window):
    """
    Loads a .swpconfig file and load the settings.

    :param window: The window so it can update the loaded values
    :type window: PySimpleGui.Window
    :return: None
    :rtype: None
    """

    # Popups a message that requests the user to select a file to load the settings off of
    save_filename = popup_get_file(
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
        "random_seed": "-OTHER1-",
        "res": "-RES_SLIDER-"
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
                window[w_key].update(data[key].replace('None', '') if type(data[key]) == str else data[key])

        except json.JSONDecodeError as ex:
            popup(f'Error while opening the config ({save_filename}) \nError:\n {ex}')


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
    window['-RES_SLIDER-'].update(1)


def print_image(image):
    """
    This function handles the print preview and the print itself.
    Source: https://github.com/PyQt5/PyQt/issues/145#issuecomment-975009897

    :param image: A pil image to print preview and print
    :type image: PIL.Image
    :return: None
    :rtype: None
    """

    def draw_image(printer_obj):
        painter = QPainter()
        painter.begin(printer_obj)
        painter.setPen(Qt.red)
        painter.drawPixmap(0, 0, pil2pixmap(image.resize((int(2480 * 2), int(3508 * 2)), PIL_IMAGE.LANCZOS)))
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
    save_filename = popup_get_file(
        "Save as", file_types=(("PNG", '.png'), ("JPG", ".jpg")), save_as=True, no_window=True
    )
    if save_filename:
        # Save the image
        img.save(save_filename)

        popup(f"Saved: {save_filename}")


def image_to_bios(image, size: tuple):
    """
    Saves a PIL image to bios after it gets resized and keeps it's ratio
    and returns it's value as a base64 encoded data.

    :param image: A PIL image to get as a base64 encoded data
    :type image: PIL.Image
    :param size: The wanted size of the image
    :type size: Tuple(int, int)
    :return: The image as a base64 encoded data
    :rtype: str
    """

    image.thumbnail(size)
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    value = bio.getvalue()
    bio.close()
    return value


def setup_columns():
    """
    Set's up the columns of the layout of the window

    :return: None
    :rtype: None
    """

    global column1, column2, column3, column4

    column1 = [
        [Text("Toggles", text_color='dark gray', font=category_name_font, background_color='#404040', size=(0, 1)),
         HorizontalSeparator(pad=(20, 0))],
        [Checkbox("Diagonals", default=True, key='-1TOGGLE-', pad=(20, 0), font=default_font, enable_events=True,
                  background_color='#404040'),
         Checkbox("Add randomized characters", default=True, key='-2TOGGLE-', pad=(20, 0), font=default_font,
                  enable_events=True, background_color='#404040'),
         Checkbox("Add word bank outline", default=True, key='-3TOGGLE-', pad=(20, 0), font=default_font,
                  enable_events=True, background_color='#404040')],
        [Text("Colors", text_color='dark gray', font=category_name_font, size=(0, 1), background_color='#404040'),
         HorizontalSeparator(pad=(20, 0))],
        [Text("Grid - line color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-1COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Grid - background color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-2COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Grid - text color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-3COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Grid - randomized characters color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-4COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Page - background color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-5COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Page - title color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-6COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Page - subtitle color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-7COLOR_COMBO-', default_value="Gray", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Word bank - outline color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-8COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Word bank - background color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-9COLOR_COMBO-', default_value="White", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Word bank - word color:", pad=(20, 0), font=default_font, background_color='#404040'),
         Combo(['Red', 'Orange', 'Yellow', 'White', 'Black', 'Blue', 'Green', 'Purple', 'Pink', 'Gray'],
               key='-10COLOR_COMBO-', default_value="Black", font=default_font, enable_events=True,
               background_color='#404040')],
        [Text("Strings", text_color='dark gray', font=category_name_font, size=(0, 1), background_color='#404040'),
         HorizontalSeparator(color='gray')],
        [Text("Words (seperated by ','):", pad=(20, 0), font=default_font, background_color='#404040'), Column([[Input(
            default_text="Bagel, Three, House", font=default_font, size=(25, 1), key='-INPUT1STR-', enable_events=True,
            background_color='#404040')]])],
        [Text("Available random characters:", pad=(20, 0), font=default_font, background_color='#404040'),
         Column([[Input(default_text="abcdefghijklmnopqrstuvwxyz", font=default_font, size=(25, 1),
                        key='-INPUT2STR-', enable_events=True, background_color='#404040')]])],
        [Text("Page title:", pad=(20, 0), font=default_font, background_color='#404040'),
         Input(default_text="Words", font=default_font, size=(25, 1), key='-INPUT3STR-', enable_events=True,
               background_color='#404040')],
        [Text("Page subtitle:", pad=(20, 0), font=default_font, background_color='#404040'), Column([[Multiline(
            default_text="Circle the correct words", key='-INPUT4STR-', font=default_font, autoscroll=True,
            size=(30, 1), background_color='#404040', enable_events=True)]])],
        [Text("Numbers", text_color='dark gray', font=category_name_font, size=(0, 1), background_color='#404040'),
         HorizontalSeparator(color='gray')],
        [Text("Grid - cell size:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT1NUM-', enable_events=True,
            background_color='#404040')]])],
        [Text("Grid - cells in a row ('auto' to automatically set size):", font=default_font, pad=(20, 0),
              background_color='#404040'), Column([[Input(default_text="auto", font=default_font, size=(4, 1),
                                                          key='-INPUT2NUM-', enable_events=True,
                                                          background_color='#404040')]])],
        [Text("Grid - line thickness:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT3NUM-', enable_events=True,
            background_color='#404040')]])],
        [Text("Grid - text size:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT4NUM-', background_color='#404040',
            enable_events=True)]])],
        [Text("Word bank - outline thickness:", font=default_font, pad=(20, 0), background_color='#404040'),
         Column([[Input(default_text="100", font=default_font, size=(3, 1), key='-INPUT5NUM-', enable_events=True,
                        background_color='#404040')]])],
        [Text("Word bank - word size:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT6NUM-', enable_events=True,
            background_color='#404040')]])],
        [Text("Page - title size:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT7NUM-', enable_events=True,
            background_color='#404040')]])],
        [Text("Page - subtitle size:", font=default_font, pad=(20, 0), background_color='#404040'), Column([[Input(
            default_text="100", font=default_font, size=(3, 1), key='-INPUT8NUM-', enable_events=True,
            background_color='#404040')]])],
        [Text("Other", text_color='dark gray', font=category_name_font, size=(0, 1), background_color='#404040'),
         HorizontalSeparator(color='gray')],
        [Text("Random seed (leave empty for randomness):", font=default_font, pad=(20, 0), background_color='#404040'),
         Input(default_text="", font=default_font, size=(3, 1), key='-OTHER1-', enable_events=True,
               background_color='#404040')],
        [Button("Reset to default", key='-RESET-',
                image_data=image_to_bios(PIL_IMAGE.open(default_button_texture), (150, 40)),
                border_width=0, button_color='#404040', mouseover_colors='#404040')]]
    column2 = [[Text(size=(0, 60), background_color='#404040'), VerticalSeparator()]]
    column3 = [
        [Button('Randomize', image_filename=default_button_texture, font=default_font, key='RANDOMIZE')],
        [Text("Enhanced resolution (worse performance)  ", font=default_font, background_color='#404040',
              tooltip='This option is recommended only for viewing the end result'),
         Button(image_filename=button_switch_off, key='switch', border_width=0, button_color='#404040',
                mouseover_colors='#404040', enable_events=True,
                tooltip='This option is recommended only for viewing the end result')],
        [Image(key='-CWIMAGE-')],
        [Button('Exit', image_filename=default_button_texture, font=default_font, key='EXIT', border_width=0,
                button_color='#404040', mouseover_colors='#404040'),
         Button('Save Image', image_filename=default_button_texture, font=default_font, key='-SAVE_FILE-',
                border_width=0, button_color='#404040', mouseover_colors='#404040'),
         Button('Print', image_filename=default_button_texture, font=default_font, key='-PRINT-', border_width=0,
                button_color='#404040', mouseover_colors='#404040'),
         Button('Save Configuration', image_filename=default_button_texture, font=default_font, key='-SAVE_CONFIG-',
                border_width=0, button_color='#404040', mouseover_colors='#404040'),
         Button('Load Configuration', image_filename=default_button_texture, font=default_font, key='-LOAD_CONFIG-',
                border_width=0, button_color='#404040', mouseover_colors='#404040'),
         Button('Copy', image_filename=default_button_texture, font=default_font, key='-COPY_TO_CLIPBOARD-')]
    ]
    column4 = [[Button("Start creating the page", image_filename=default_button_texture, font=default_font,
                       key='-START-', border_width=0, button_color='#404040', mouseover_colors='#404040')]]


def setup_layout():
    """
    Set's up the layout for the window.

    :return: None
    :rtype: None
    """

    global layout1
    layout1 = [[Column(column4, element_justification='c',
                       background_color='#404040',
                       key='-COL4-'),
                pin(Column(column1, element_justification='c', vertical_scroll_only=True, scrollable=True,
                           background_color='#404040',
                           key='-COL1-', visible=False, size=(650, 1015))),
                pin(Column(column2, element_justification='c',
                           background_color='#404040',
                           key='-COL2-', visible=False)),
                pin(Column(column3, element_justification='c', vertical_scroll_only=True, scrollable=True,background_color='#404040',
                           key='-COL3-', visible=False, size=(1198, 808)))
                ]]


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
    window.move(x, y - 50)


def window_loop():
    """
    The main window loop with all the error handling and generator calls.

    :return: None
    """

    global seed

    # Set's up the window
    window = Window("Search word puzzle generator", layout1, finalize=True, resizable=True)
    print(window.current_size_accurate())
    window.grab_any_where_on()

    toggle = False

    # Window loop
    while True:
        event, values = window.read()

        # Detects if the window closed if it does it will exit the program
        if event == WINDOW_CLOSED or event == 'EXIT':
            window.close()
            exit(0)

        # If the randomize button was clicked it will randomize the seed
        if event == 'RANDOMIZE':
            seed = str(uuid.uuid4()).replace('-', '')

        # If the enhanced res toggle button was clicked it will switch the image and the variable and change the tooltip
        if event == 'switch':
            if toggle:
                toggle = False
                window['switch'].update(image_filename=button_switch_off)
                window['switch'].set_tooltip('Regular speed and resolution')
            else:
                toggle = True
                window['switch'].update(image_filename=button_switch_on)
                window['switch'].set_tooltip('Slower speed and better resolution')

        # If the START button was clicked it will setup the main page
        if event == '-START-':
            window['-START-'].update(visible=False)
            window['-COL4-'].update(visible=False)
            window['-COL1-'].update(visible=True)
            window['-INPUT5NUM-'].Widget.configure(highlightcolor='red')
            window['-COL2-'].update(visible=True)
            window['-COL3-'].update(visible=True)
            window.refresh()
            move_center(window)
            window.Maximize()

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
        random_seed = None if window['-OTHER1-'].get() == "" else window['-OTHER1-'].get()

        # Set's up the the error list variable
        checks = [False, False, False, False, False, False, False, False, False, False, False]

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
            window['-INPUT1STR-'].set_tooltip("You have reached the max word limit (15)")
            checks[0] = False

        # If the chars in the word list is bigger than 60 it will show an error
        elif len(''.join(words)) > 65:
            window['-INPUT1STR-'].ParentRowFrame.config(background='red')
            window['-INPUT1STR-'].set_tooltip("You have reached the max character limit (65)")
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
                window['-INPUT1STR-'].ParentRowFrame.config(background=theme_background_color())
                checks[0] = True

        else:
            window['-INPUT1STR-'].set_tooltip('All good :)')
            window['-INPUT1STR-'].ParentRowFrame.config(background=theme_background_color())
            checks[0] = True

        # If the number of new lines in the subtitle is bigger than 2 it will show an error
        if page_subtitle.count('\n') > 2:
            window['-INPUT4STR-'].set_tooltip('You have reached the maximum lines (3)')
            window['-INPUT4STR-'].ParentRowFrame.config(background='red')
            checks[-1] = False

        else:
            window['-INPUT4STR-'].set_tooltip('All good :)')
            window['-INPUT4STR-'].ParentRowFrame.config(background=theme_background_color())
            checks[-1] = True

        # If available_random_chars (the random chars it will put on the grid) is empty it will show an error
        if available_random_chars == "":
            window['-INPUT2STR-'].set_tooltip("This field cannot be empty!")
            window['-INPUT2STR-'].ParentRowFrame.config(background='red')
            checks[1] = False

        else:
            window['-INPUT2STR-'].set_tooltip('All good :)')
            checks[1] = True
            window['-INPUT2STR-'].ParentRowFrame.config(background=theme_background_color())

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
                window['-INPUT1NUM-'].set_tooltip("This field has to be lower than or equal to 100")
                window['-INPUT1NUM-'].ParentRowFrame.config(background='red')
                checks[2] = False

            else:
                window['-INPUT1NUM-'].set_tooltip('All good :)')
                window['-INPUT1NUM-'].ParentRowFrame.config(background=theme_background_color())
                checks[2] = True

        # If the cells in a row field is empty it will show an error
        if grid_cells_in_row == "":
            window['-INPUT2NUM-'].set_tooltip("This field cannot be empty!")
            window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
            checks[3] = False

        # If the cells in a row field is NOT auto and is not a digit it will show an error
        elif grid_cells_in_row != "auto" and not grid_cells_in_row.isdigit():
            window['-INPUT2NUM-'].set_tooltip("This field has to be a number or 'auto'")
            window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
            checks[3] = False

        else:

            # If the cells in a row field is NOT auto it will convert it to a number
            if grid_cells_in_row != "auto":
                grid_cells_in_row = int(grid_cells_in_row)

                # If the cells in a row are bigger than 100 it will show an error
                if grid_cells_in_row > 100:
                    window['-INPUT2NUM-'].set_tooltip("This field has to be lower than or equal to 100")
                    window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
                    checks[3] = False
                else:

                    # If the length of the longest word in the words is bigger
                    # than grid_cells_in_row it will show an error
                    if len(max(words, key=len)) >= grid_cells_in_row:
                        window['-INPUT2NUM-'].set_tooltip(
                            f"The length of {max(words, key=len)} is larger then or equal to the cells in a row, "
                            f"either change the word or\nchange the cells in a row to "
                            f"'auto' or to more than {len(max(words, key=len))}")
                        window['-INPUT2NUM-'].ParentRowFrame.config(background='red')
                        checks[0] = False

                    else:
                        window['-INPUT2NUM-'].set_tooltip('All good :)')
                        window['-INPUT2NUM-'].ParentRowFrame.config(background=theme_background_color())
                        checks[3] = True

            else:
                window['-INPUT2NUM-'].set_tooltip('All good :)')
                window['-INPUT2NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT3NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT3NUM-'].ParentRowFrame.config(background='red')
            checks[4] = False

        else:
            grid_line_width = int(grid_line_width)
            window['-INPUT3NUM-'].set_tooltip("All good :)")
            window['-INPUT3NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT4NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT4NUM-'].ParentRowFrame.config(background='red')
            checks[5] = False

        else:
            grid_text_size = int(grid_text_size)
            window['-INPUT4NUM-'].set_tooltip("All good :)")
            window['-INPUT4NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT5NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT5NUM-'].ParentRowFrame.config(background='red')
            checks[6] = False

        else:
            word_bank_outline_width = int(word_bank_outline_width)
            window['-INPUT5NUM-'].set_tooltip("All good :)")
            window['-INPUT5NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT6NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT6NUM-'].ParentRowFrame.config(background='red')
            checks[7] = False

        else:
            word_bank_word_size = int(word_bank_word_size)
            window['-INPUT6NUM-'].set_tooltip("All good :)")
            window['-INPUT6NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT7NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT7NUM-'].ParentRowFrame.config(background='red')
            checks[8] = False

        else:
            page_title_size = int(page_title_size)
            window['-INPUT7NUM-'].set_tooltip("All good :)")
            window['-INPUT7NUM-'].ParentRowFrame.config(background=theme_background_color())
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
            window['-INPUT8NUM-'].set_tooltip("This field has lower than or equal to 100")
            window['-INPUT8NUM-'].ParentRowFrame.config(background='red')
            checks[9] = False

        else:
            page_subtitle_size = int(page_subtitle_size)
            window['-INPUT8NUM-'].set_tooltip("All good :)")
            window['-INPUT8NUM-'].ParentRowFrame.config(background=theme_background_color())
            checks[9] = True

        # If all the checks have passed it will continue
        if all(checks):

            # Sets all the buttons to have their valid status
            window['-SAVE_FILE-'].set_tooltip("Save the puzzle to a image")
            window['-PRINT-'].set_tooltip("Print the image in your printer")
            window['-SAVE_CONFIG-'].set_tooltip("Save the settings in a file")
            window['-LOAD_CONFIG-'].set_tooltip("Load a settings file")
            window['-COPY_TO_CLIPBOARD-'].set_tooltip("Copy the image to your clipboard")
            window['-SAVE_FILE-'].update(disabled=False)
            window['-PRINT-'].update(disabled=False)
            window['-SAVE_CONFIG-'].update(disabled=False)
            window['-COPY_TO_CLIPBOARD-'].update(disabled=False)

            # Converts the string of words to a list
            tmp_words = []
            for i in words:
                if i != "":
                    tmp_words.append(i.replace(' ', ''))

            # Calls the search word puzzle generator with the settings the user has inputted
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
                window["-CWIMAGE-"].update(data=image_to_bios(image, (600, 600)))

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
                                    (add_random_chars, f'{add_random_chars=}'.split('=')[0]),
                                    (add_word_bank_outline, f'{add_word_bank_outline=}'.split('=')[0]),
                                    (grid_line_color, f'{grid_line_color=}'.split('=')[0]),
                                    (grid_background_color, f'{grid_background_color=}'.split('=')[0]),
                                    (grid_text_color, f'{grid_text_color=}'.split('=')[0]),
                                    (grid_random_chars_color, f'{grid_random_chars_color=}'.split('=')[0]),
                                    (page_background_color, f'{page_background_color=}'.split('=')[0]),
                                    (page_title_color, f'{page_title_color=}'.split('=')[0]),
                                    (page_subtitle_color, f'{page_subtitle_color=}'.split('=')[0]),
                                    (word_bank_outline_color, f'{word_bank_outline_color=}'.split('=')[0]),
                                    (word_bank_background_color, f'{word_bank_background_color=}'.split('=')[0]),
                                    (word_bank_word_color, f'{word_bank_word_color=}'.split('=')[0]),
                                    (words, f'{words=}'.split('=')[0]),
                                    (available_random_chars, f'{available_random_chars=}'.split('=')[0]),
                                    (page_title, f'{page_title=}'.split('=')[0]),
                                    (page_subtitle, f'{page_subtitle=}'.split('=')[0]),
                                    (grid_cell_size, f'{grid_cell_size=}'.split('=')[0]),
                                    (grid_cells_in_row, f'{grid_cells_in_row=}'.split('=')[0]),
                                    (grid_line_width, f'{grid_line_width=}'.split('=')[0]),
                                    (grid_text_size, f'{grid_text_size=}'.split('=')[0]),
                                    (word_bank_outline_width, f'{word_bank_outline_width=}'.split('=')[0]),
                                    (word_bank_word_size, f'{word_bank_word_size=}'.split('=')[0]),
                                    (page_title_size, f'{page_title_size=}'.split('=')[0]),
                                    (page_subtitle_size, f'{page_subtitle_size=}'.split('=')[0]),
                                    (random_seed, f'{random_seed=}'.split('=')[0])])

            # If the user has pressed the reset to default button it will call the reset_to_default function
            elif event == '-RESET-':
                reset_to_default(window)

            # If the user has pressed the load config button it will call the load_configuration function
            elif event == '-LOAD_CONFIG-':
                load_configuration(window)

        # If there was even one error it will disable the buttons and show a tooltip on the buttons
        else:
            window['-SAVE_FILE-'].update(disabled=True)
            window['-SAVE_FILE-'].set_tooltip("There are some errors in the settings... look for a red box")
            window['-PRINT-'].update(disabled=True)
            window['-PRINT-'].set_tooltip("There are some errors in the settings... look for a red box")
            window['-SAVE_CONFIG-'].update(disabled=True)
            window['-SAVE_CONFIG-'].set_tooltip("There are some errors in the settings... look for a red box")
            window['-COPY_TO_CLIPBOARD-'].update(disabled=True)
            window['-COPY_TO_CLIPBOARD-'].set_tooltip("There are some errors in the settings... look for a red box")


# If the file was ran directly it will run the program
if __name__ == '__main__':
    setup_columns()
    setup_layout()
    window_loop()
    window_loop()
