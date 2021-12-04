import random
import textwrap
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

multiplier = 2
global_font = r'assets\fonts\VarelaRound-Regular.ttf'


def create_grid(cells_in_row=10, cell_size=10, line_color=(0, 0, 0), background_color=(255, 255, 255), line_width=10,
                high_res=False):
    """
    Creates a grid as an image according to some parameters.

    :param cells_in_row: The number of cells/squares in a row/column in the grid
    :type cells_in_row: int
    :param cell_size: The size of each cell in the grid
    :type cell_size: int
    :param line_color: The line color of the separator lines of the grid
    :type line_color: Tuple(int, int, int) | str
    :param background_color: The background color of the grid
    :type background_color: Tuple(int, int, int) | str
    :param line_width: The line width of the separators of the grid
    :type line_width: int
    :param high_res: True if the resolution multiplier is bigger than 2
    :type high_res: bool
    :returns: (The grid as a PIL image, A coord set of all the coordinates of the cells in the grid)
    :rtype: Tuple(PIL.Image, Dict{List[Tuple(int, int)]})
    """

    # Lowers the resolutions of the grid because it can be resized and it wont change the look
    ml = multiplier // 2

    # Setup variables
    cell_size = cell_size * ml
    line_width = int(line_width)
    coords = {}
    coord_set = {}
    counter = 0

    # Creating a new image to draw on
    dim = cell_size * cells_in_row * ml
    img = Image.new('RGB', (dim, dim), color=background_color)

    width, height = img.size

    # Initializes the ImageDraw.Draw for the img so I can draw on it
    img_draw = ImageDraw.Draw(img)

    # Looping and drawing lines horizontally for the grid
    for i in range(cells_in_row):
        shape = [(0, i * cell_size * ml), (width, i * cell_size * ml)]
        img_draw.line(shape, fill=line_color, width=line_width * int(ml / 2))

    # Looping and drawing lines vertically for the grid
    for i in range(cells_in_row):
        shape = [(i * cell_size * ml, 0), (i * cell_size * ml, height)]
        img_draw.line(shape, fill=line_color, width=line_width * int(ml / 2))

    # Drawing the left lines on the outline of the grid
    img_draw.line([(0, height - 1), (width, height - 1)], fill=line_color, width=line_width * int(ml / 2))
    img_draw.line([(width - 1, 0), (width - 1, height)], fill=line_color, width=line_width * int(ml / 2))

    # Getting positions of each cell and adding to a 3d array && dict
    if high_res:
        ml = multiplier + 2
    else:
        ml = multiplier + 1
    for y in range(0, cells_in_row):
        y = (y * cell_size * ml + int((cell_size / 2 * ml))) + ml ** 2 + int(cell_size // 2)
        counter += 1
        for x in range(0, cells_in_row):
            x = (x * cell_size * ml + int((cell_size / 2 * ml)))
            coord_set[(x, y)] = None
        coords[counter] = coord_set
        coord_set = {}

    return img, coords


def check(coords, start_coord: tuple, word: str, words, allow_diagonal):
    """
    Checks if a word can be placed on the grid in a certain spot.

    :param coords: A 3d array && dict of all the coords on the grid
    :type coords: Dict{List[Tuple(int, int)]}
    :param start_coord: A random coordinate on the grid that the check will start from
    :type start_coord: Tuple(int, int)
    :param word: The word to check if possible and where possible to place the chars of the word
    :type word: str
    :param words: The list of all words that was given to the program
    :type words: List[str, ...]
    :param allow_diagonal:
    :type allow_diagonal: bool
    :returns: If the function found valid spots for the word to be placed in it will return the coords
     if not it will return None
    :rtype: List[Tuple(int, int), ...] | None
    """

    def check_right():

        """
        Checks if the word can be placed to the right of the start_coord.

        :returns: The valid coords List[Tuple(int, int)] if it has a valid place to be placed at and return None if it
        cannot be placed
        :rtype: List[Tuple(int, int)] | None
        """

        # Setup variables
        coord_set = []
        cc = 0
        good_coords = []

        # Gets the coord_set that contains the start coord
        for i in coords:
            if start_coord in list(coords[i].keys()):
                coord_set = coords[i]

        for c, i in enumerate(coord_set):

            # Checks if the loop has passed the start coord (so it wont give coords to the left of the start coord)
            # so it can start checking
            if c >= list(coord_set.keys()).index(start_coord):

                # Checks if the char in the currently processed cell is None (empty)
                # or is the same as the char in that cell
                if coord_set[list(coord_set.keys())[c]] is None or \
                        coord_set[list(coord_set.keys())[c]] == list(word)[cc]:

                    cc += 1
                    # Appends the position if it has passed all the checks
                    good_coords.append(list(coord_set.keys())[c])

                    # Checks if we got the right number of positions (number of chars in the word) if there's the right
                    # number it will break out of the loop so I wont get a coord list that is longer than the word
                    if len(good_coords) == len(word):
                        break
                else:
                    break

        # If we have enough positions it will return them if not it will return None which means the word cannot be
        # placed there (from the start_coord to the right)
        if len(good_coords) == len(word):
            return good_coords
        else:
            return None

    def check_down():

        """
        Checks if the word can be placed down of the start_coord.

        :returns: The valid coords List[Tuple(int, int)] if it has a valid place to be placed at and return None if it
        cannot be placed
        :rtype: List[Tuple(int, int)] | None
        """

        # Setup variables
        index = 0
        coord_set = 0
        cc = 0
        good_coords = []

        # Gets the index of the start_coord in the coord_set and sets
        # a variable that contains the coord_set of the start_coord
        for i in coords:
            if start_coord in coords[i]:
                index = list(coords[i]).index(start_coord)
                coord_set = i
                break

        for counter, ind in enumerate(coords):

            # Checks if the index of the currently processed cell is bigger than
            # the index of the coord_set of the start_coord
            if ind >= coord_set:

                # Checks if the currently processed cell's char is or None (empty) or the same char
                # of the currently processed char of the word (so the words will combine)
                if coords[ind][list(coords[ind].keys())[index]] is None or \
                        coords[ind][list(coords[ind].keys())[index]] == list(word)[cc]:

                    cc += 1

                    # Appends the position if it has passed all the checks
                    good_coords.append(list(coords[ind].keys())[index])

                    # Checks if we got the right number of positions (number of chars in the word) if there's the right
                    # number it will break out of the loop so I wont get a coord list that is longer than the word
                    if len(good_coords) == len(word):
                        break
                else:
                    break

        # If we have enough positions it will return them if not it will return None which means the word cannot be
        # placed there (from the start_coord down)
        if len(good_coords) == len(word):
            return good_coords
        else:
            return None

    def check_diagonal_ltr():

        """
        Checks if the word can be placed diagonally from the left to the right and down.

        :returns: The valid coords List[Tuple(int, int)] if it has a valid place to be placed at and return None if it
        cannot be placed
        :rtype: List[Tuple(int, int)] | None
        """

        # Setup variables
        index = 0
        start_coord_set = 0
        good_coords = []
        cc = 0

        # Gets the index of the start_coord in the coord_set
        for c in coords:
            if start_coord in coords[c]:
                start_coord_set = c
                index = list(coords[c].keys()).index(start_coord) - 1

        for counter, coord_set in enumerate(coords):

            # Checks if the index of the set is lower than the currently processed set which means the next
            # char is below the char before it
            if counter >= start_coord_set:

                # Checks if the currently processed cell's char is or None (empty) or the same char
                # of the currently processed char of the word (so the words will combine)
                if coords[counter][list(coords[counter].keys())[index]] is None or \
                        coords[counter][list(coords[counter].keys())[index]] == list(word)[cc]:

                    index += 1

                    # Checks if the word can continue going forwards by checking if the index is bigger than the
                    # length of a coord set
                    if index > len(coords[coord_set]) - 1:
                        return None

                    # Checks if the currently processed cell's char is or None (empty) or the same char
                    # of the currently processed char of the word (so the words will combine)
                    if coords[counter][list(coords[counter].keys())[index]] is None or \
                            coords[counter][list(coords[counter].keys())[index]] == list(word)[cc]:
                        pass
                    else:
                        break

                    cc += 1

                    # Appends the position if it has passed all the checks
                    good_coords.append(list(coords[counter].keys())[index])

                    # Checks if we got the right number of positions (number of chars in the word) if there's the right
                    # number it will break out of the loop so I wont get a coord list that is longer than the word
                    if len(good_coords) == len(word):
                        return good_coords
                    continue
                else:
                    break

        # If we have enough positions it will return them if not it will return None which means the word cannot be
        # placed there (from the start_coord down diagonally)
        if len(good_coords) == len(word):
            return good_coords
        else:
            return None

    # A list of all of the functions
    options = [check_down, check_right]

    # If diagonals are allowed it will append the diagonal function to the list
    if allow_diagonal:
        options.append(check_diagonal_ltr)

    # Gets a random function from the list and stores the value in a variable
    res = random.choice(options)

    # If diagonals are allowed and the current processed word is the first in the word list it will make it diagonal
    # so theres a determined diagonal
    if allow_diagonal and word == words[0]:
        res = check_diagonal_ltr

    return res()


def get_font_characters(font_path):

    """
    Gets all chars in a font.
    source: https://stackoverflow.com/a/19438403

    :param font_path: A path for a specific font
    :type font_path: str
    :returns: A list of all characters in a specific font
    :rtype: List[str, ...]
    """

    # Gets all chars in a font - source: https://stackoverflow.com/a/19438403
    with TTFont(font_path) as font_file:
        characters = list(chr(y[0]) for x in font_file["cmap"].tables for y in x.cmap.items())

    return characters


def populate_list(lst, target_num, randomize=False, hard_randomizer=False):

    """
    Adds elements to the list from the list until the length of the list reaches the target_number.

    :param lst: The list that we want to make bigger (have a specific amount of elements)
    :type: lst: list
    :param target_num: The number of elements we want the list to reach
    :type: target_num: int
    :param randomize: If True shuffle the list if not dont
    :type: randomize: bool
    :param hard_randomizer: If True choose even random elements from the list to append to the list
    :type: hard_randomizer: bool
    :raises IndexError: "Number of elements in the list are bigger than the target number"
    :returns: A list that has this specific amount of elements
    :rtype: list
    """

    # If randomize is true it will shuffle the list
    if randomize:
        random.shuffle(lst)

    # Gets the number of elements left (the number of elements we want - the number of elements in the list)
    elements_left = target_num - len(lst)

    # If theres more elements to the list than the target_num it will return an error
    if elements_left < 0:
        raise IndexError("Number of elements in the list are bigger than the target number")

    # If the target num and the number of elements in the list are the same it will check if randomize is True if it
    # is it will shuffle the list and return the list as it is
    if elements_left == 0:
        if randomize:
            random.shuffle(lst)
        return lst

    # Appends a random elements from the list to the list if hard_randomizer is True if not it would just go by order
    for i in range(elements_left):
        lst.append(lst[i if not hard_randomizer else random.randint(0, len(lst) - 1)])

    # Shuffles the list a "couple" times
    for i in range(50):
        if randomize:
            random.shuffle(lst)
    return lst


def draw_chars(words, available_chars='abcdefghijklmnopqrstuvwxyz', allow_diagonal=True, cells_in_row=15,
               square_size=10, grid_separator_color=(0, 0, 0), grid_background_color=(255, 255, 255),
               grid_separator_width=10, grid_text_color=(0, 0, 255), grid_text_size=50, random_char_color=None,
               add_randomized_chars=True, random_seed=None, high_res=False):
    """
    Draws all the chars (random and the words the user has decided) to an image.

    :param words: A list of words that need to be drawn to the grid
    :type words: List[str, ...]
    :param available_chars: A string of all available characters that'll be written in
     the free cells (without chars in there)
    :type available_chars: str
    :param allow_diagonal: A boolean that decides if there will be diagonals when the word list is being drawn
    :type allow_diagonal: bool
    :param cells_in_row: The number of cells in a row/column in the grid
    :type cells_in_row: int
    :param square_size: The square/cell size in the grid
    :type square_size: int
    :param grid_separator_color: The color of the separator lines in the grid
    :type grid_separator_color: Tuple(int, int, int) | str
    :param grid_background_color: The color of the background of the grid
    :type grid_background_color: Tuple(int, int, int) | str
    :param grid_separator_width: The grid separator line width
    :type grid_separator_width: int
    :param grid_text_color: The grid's text color
    :type grid_text_color: Tuple(int, int, int) | str
    :param grid_text_size: The grid's text size
    :type grid_text_size: int
    :param random_char_color: The color of the random characters
    :type random_char_color: Tuple(int, int, int) | str
    :param add_randomized_chars: Decides if randomized chars will be drawn
    :type add_randomized_chars: bool
    :param random_seed: A random seed that can be inputted
    :type random_seed: str | int
    :param high_res: If high_res is bigger than 2 it will be True if not it will be False
    :type high_res: bool
    :returns: A grid with the words and randomized chars (if add_randomized_chars is True) as an image
    :rtype: PIL.Image
    """

    global multiplier
    random.seed(random_seed)
    if random_char_color is None:
        random_char_color = grid_text_color

    # Calls the create_grid function and stores the output in vars
    img, coords = create_grid(cells_in_row=cells_in_row, cell_size=square_size, line_color=grid_separator_color,
                              background_color=grid_background_color, line_width=grid_separator_width,
                              high_res=high_res)

    # Resizes the image to be multiplied by 3 and it would look the same because the grid is made out of straight lines
    img = img.resize((img.size[0] * 3, img.size[0] * 3), Image.NEAREST)

    if type(words) == str:
        words = words.split(',')

    # Initializes the ImageDraw.Draw for the img so I can draw on it
    img_draw = ImageDraw.Draw(img)

    for word in words:

        # If the word's first char is in hebrew it would reverse the word
        if list(word)[0] in 'אבגדהוזחטיכלמנסעפצקרשת':
            word = list(word)
            word.reverse()

        # Gets a random coord out of a random set
        c = list(coords.values())
        t = random.sample(c, 1)[0]
        start_coord = random.sample(list(t), 1)[0]

        # Checks if the word can be placed with the start coord as the start coord set above
        word_coords = check(coords, start_coord, word, words, allow_diagonal)

        # If the first try didn't work it will loop until it will find valid coords for the word
        while word_coords is None:
            c = list(coords.values())
            t = random.sample(c, 1)[0]
            start_coord = random.sample(list(t), 1)[0]
            word_coords = check(coords, start_coord, word, words, allow_diagonal)

        # Writes the chars with the chars the check function returned
        for counter, c in enumerate(word_coords):
            font = ImageFont.truetype(global_font, int(grid_text_size * 2))
            img_draw.text((c[0], c[1] - multiplier * (2 if high_res else 4) + (97 if high_res else 2)),
                          list(word)[counter].upper(), fill=grid_text_color, font=font,
                          anchor='mb')

            # Sets all the coords the check function
            # returned as occupied (sets it as the char that was drawn in that coord)
            for i in coords:
                if c in list(coords[i].keys()):
                    coords[i][c] = list(word)[counter]

    # If the user has inputted a random seed it will set the seed to that if not it will set it to a random one
    if random_seed is not None:
        random.seed(random_seed)

    if add_randomized_chars:
        free_coords = []
        available_chars = list(available_chars)

        # Appends to a list all the coords that have None in them (that are empty)
        for i in coords:
            for c, x in enumerate(coords[i]):
                if coords[i][x] is None:
                    free_coords.append(list(coords[i].keys())[c])

        font = ImageFont.truetype(global_font, int(grid_text_size * 2))

        # Calls the populate_list function and stores the returned value in a var
        if len(available_chars) <= len(free_coords):
            available_chars = populate_list(available_chars, len(free_coords), True, False)
        else:
            random.shuffle(available_chars)

        # Draws random chars all over the free coords (that have no chars on them)
        for c, coord in enumerate(free_coords):
            img_draw.text((coord[0], coord[1] - multiplier * (2 if high_res else 4) + (97 if high_res else 2)),
                          available_chars[c].upper(), fill=random_char_color,
                          font=font, anchor='mb')

    return img


def fit_text(text, text_size, text_color, max_horizontal_chars, box_outline_color, box_background_color,
             box_outline_width, font_file, word_bank_outline, high_res):

    """
    :param text: The text that needs to be fir inside the bounding box (words separated by ,)
    :type text: str
    :param text_size: The size of the text
    :type text_size: int
    :param text_color: The color of the text
    :type text_color: Tuple(int, int, int) | str
    :param max_horizontal_chars: The number of the max horizontal chars allowed in one line
    :type max_horizontal_chars: int
    :param box_outline_color: The color of the outline of the bounding box
    :type box_outline_color: Tuple(int, int, int) | str
    :param box_background_color: The color of the background of the bounding box
    :type box_background_color: Tuple(int, int, int) | str
    :param box_outline_width: The thickness of the outline of the bounding box
    :type box_outline_width: int
    :param font_file: The file of the font of the text
    :type font_file: str
    :param word_bank_outline: Whether there will be an outline or not
    :type word_bank_outline: bool
    :param high_res: If high_res is bigger than 2 it will be True if not it will be False
    :type high_res: bool
    :return: The image
    :rtype: PIL.Image
    """

    text_size *= multiplier // 2
    text_size -= int(text_size//3)

    # Replaces every ',' to '-' because the wrapper library will associate '-' as a separator and sorts by length and
    # removes all spaces
    text = text.replace(' ', '')
    text = text.split(',')

    # Checks if theres a hebrew letter in the word if there is it will reverse it
    for c, i in enumerate(text):
        if list(i)[0] in 'אבגדהוזחטיכלמנסעפצקרשת':
            i = list(i)
            i.reverse()
            text[c] = (''.join(i))

    text.sort(key=len, reverse=True)
    text = ','.join(text).upper()
    text = text.replace(',', '-')

    # Changes the text size to fit the box if the longest word cannot fit in one line
    font = ImageFont.truetype(font_file, text_size)
    longest_word = sorted(text.split('-'), key=len)[-1]
    if longest_word[0] == ' ':
        longest_word = longest_word[1:]
    longest_word_size = font.getsize(longest_word)[0]
    while longest_word_size >= 1100:
        longest_word = sorted(text.split('-'), key=len)[-1]
        if longest_word[0] == ' ':
            longest_word = longest_word[1:]
        longest_word_size = font.getsize(longest_word)[0]
        text_size -= 1
        font = ImageFont.truetype(font_file, text_size)

    # Initializes the text wrapper
    wrapper = textwrap.TextWrapper()
    wrapper.max_lines = 3
    wrapper.placeholder = '...'
    wrapper.break_long_words = False
    wrapper.width = max_horizontal_chars-10

    # Wrap the text
    text = wrapper.fill(text=text)

    # Create a new image according to the size of the text
    img = Image.new('RGBA', (font.getsize_multiline((max_horizontal_chars-10)*'A')[0]+20,
                             (font.getsize_multiline(text)[1]+20+(60 if high_res else 20) +
                              box_outline_width+(text.count('\n')*10))), (0, 0, 0, 0))

    # Initializes the ImageDraw.Draw for the img so I can draw on it
    draw = ImageDraw.Draw(im=img)

    # If word_bank_outline is true it will draw a bunch or rectangles according to box_outline_width
    if word_bank_outline:
        w, h = img.size
        for i in range(0, box_outline_width):
            shape = [(0 + i, 0 + i), (w - i, h - i)]
            draw.rectangle(shape, box_background_color, box_outline_color)

    # Replaces every '-' back to ','
    text = text.replace('-', ', ').upper()

    # Checks if the first char is ' ' if it is it will be cut out
    if text[0] == ' ':
        text = text[1:]

    # Draws the text onto the bounding box
    draw.multiline_text(xy=(10 + (20 if high_res else 0), 0), text=text, font=font, fill=text_color, spacing=20)

    return img


def create_search_word_puzzle(words, random_chars='abcdefghijklmnopqrstuvwxyz', allow_diagonal=True,
                              cells_in_row='auto', square_size=10, grid_separator_color='black',
                              grid_background_color='white', grid_separator_width=10, grid_text_color='black',
                              grid_text_size=50, random_char_color=None, add_randomized_chars=True, page_color='white',
                              page_title='Search word puzzle Game', title_color='black', word_bank_outline=True,
                              word_bank_outline_color='black', word_bank_outline_width=10, word_bank_fill_color='white',
                              words_in_word_bank_color='black', random_seed=None, subtitle='Circle the words',
                              subtitle_color='gray', title_size=120, subtitle_size=80, words_in_word_bank_size=100,
                              res_multiplier=2):

    """
    The function that connects all the other functions and makes it to one image.

    :param words: A list of words that need to be drawn to the grid
    :type words: List[str, ...]
    :param random_chars: A string of all available characters that'll be written in
     the free cells (without chars in there)
    :type random_chars: str
    :param allow_diagonal: A boolean that decides if there will be diagonals when the word list is being drawn
    :type allow_diagonal: bool
    :param cells_in_row: The number of cells in a row/column in the grid
    :type cells_in_row: int
    :param square_size: The square/cell size in the grid
    :type square_size: int
    :param grid_separator_color: The color of the separator lines in the grid
    :type grid_separator_color: Tuple(int, int, int) | str
    :param grid_background_color: The color of the background of the grid
    :type grid_background_color: Tuple(int, int, int) | str
    :param grid_separator_width: The grid separator line width
    :type grid_separator_width: int
    :param grid_text_color: The grid's text color
    :type grid_text_color: Tuple(int, int, int) | str
    :param grid_text_size: The grid's text size
    :type grid_text_size: int
    :param random_char_color: The color of the random characters
    :type random_char_color: Tuple(int, int, int) | str
    :param add_randomized_chars: Decides if randomized chars will be drawn
    :type add_randomized_chars: bool
    :param random_seed: A random seed that can be inputted
    :type random_seed: str | int
    :param subtitle: A text that will be shown on the page
    :type subtitle: str
    :param subtitle_color: The subtitle's color
    :type subtitle_color: Tuple(int, int, int) | str
    :param title_size: The title's size
    :type title_size: int
    :param subtitle_size: The subtitle's size
    :type subtitle_size: int
    :param words_in_word_bank_size: The words' size in the word bank
    :type words_in_word_bank_size: int
    :param res_multiplier: The resolutions multiplier
    :type res_multiplier: int
    :param page_color: The page's color
    :type page_color: Tuple(int, int, int) | str
    :param page_title: The page's title
    :type page_title: str
    :param title_color: The page title's color
    :type title_color: Tuple(int, int, int) | str
    :param word_bank_outline: Decides if there will be an outline for the word bank
    :type word_bank_outline: bool
    :param word_bank_outline_color: The word bank outline's color
    :type word_bank_outline_color: Tuple(int, int, int) | str
    :param word_bank_outline_width: The world bank's outline thickness
    :type word_bank_outline_width: int
    :param word_bank_fill_color: The word bank's fill color
    :type word_bank_fill_color: Tuple(int, int, int) | str
    :param words_in_word_bank_color: The word bank's word color
    :type words_in_word_bank_color: Tuple(int, int, int) | str
    :raises AttributeError
    :returns: The page
    :rtype: PIL.Image
    """

    # Setup variables
    global multiplier
    multiplier = res_multiplier

    if res_multiplier == 2:
        grid_text_size = 13
    elif res_multiplier == 4:
        grid_text_size = 213

    if res_multiplier == 2:
        word_bank_outline_width = 100-1
    elif res_multiplier == 4:
        word_bank_outline_width = 100-1

    if res_multiplier == 2:
        grid_separator_width = 100-1
    elif res_multiplier == 4:
        grid_separator_width = 100-40

    square_size = square_size * multiplier // (20 // multiplier)
    grid_separator_width = grid_separator_width // multiplier
    word_bank_outline_width = 100//word_bank_outline_width * multiplier
    title_size = title_size * multiplier
    subtitle_size = int(subtitle_size * multiplier // 1.7)
    words_in_word_bank_size = words_in_word_bank_size

    long = []

    # If the cells in row is 'auto' it will set it to the longest word's length + 2
    if cells_in_row == 'auto':
        cells_in_row = len(max(words, key=len)) + 2

    # Appends all the words that their length is bigger than the cells_in_row
    for word in words:
        if len(word) > cells_in_row:
            long.append(word)

    # Raises an error if there are words longer
    if len(long) > 0:
        raise AttributeError(f"The maximum characters of a word can be {cells_in_row} you have invalid words: {long}")

    random.seed(random_seed)

    font = ImageFont.truetype(global_font, title_size)

    # Calls the function draw_chars and stores it's returned value into a var
    img = draw_chars(words=words, available_chars=random_chars, allow_diagonal=allow_diagonal,
                     cells_in_row=cells_in_row, square_size=square_size, grid_separator_color=grid_separator_color,
                     grid_background_color=grid_background_color, grid_separator_width=grid_separator_width,
                     grid_text_color=grid_text_color,
                     grid_text_size=grid_text_size, random_char_color=random_char_color,
                     add_randomized_chars=add_randomized_chars, random_seed=random_seed,
                     high_res=res_multiplier > 2)

    # Creates the page image
    page = Image.new('RGB', (2480 * multiplier // 2, 3508 * multiplier // 2), color=page_color)

    # Initializes the ImageDraw.Draw for the page so I can draw on it
    page_draw = ImageDraw.Draw(page)

    # Checks if the page starts with a letter in the hebrew language if it does it will reverse it
    if len(page_title) != 0 and list(page_title)[0] in 'אבגדהוזחטיכלמנסעפצקרשת':
        page_title = list(page_title)
        page_title.reverse()
        page_title = ''.join(page_title)

    # Draws the title on the page
    page_draw.text((page.size[0] // 2, page.size[1] // 18), page_title, fill=title_color, font=font, anchor='mb',
                   align='center')
    font = ImageFont.truetype(global_font, subtitle_size)

    # Draws the subtitle on the page
    page_draw.multiline_text((page.size[0] / 15, page.size[1] // 15), subtitle, fill=subtitle_color, font=font,
                             align='left')

    # Calls the function fit_text and then stores it's returned values into a var
    word_bank = fit_text(text=', '.join(words), text_size=words_in_word_bank_size, text_color=words_in_word_bank_color,
                         max_horizontal_chars=35, box_outline_color=word_bank_outline_color,
                         box_background_color=word_bank_fill_color, box_outline_width=word_bank_outline_width,
                         font_file=global_font, word_bank_outline=word_bank_outline, high_res=res_multiplier > 2)
    font = ImageFont.truetype(global_font, 75 * multiplier // 2)

    # If the mode is high res it will resize it with a better mode (high quality)
    if res_multiplier == 2:
        img = img.resize((2000 * multiplier // 2, 2000 * multiplier // 2), resample=Image.MEDIANCUT)
    else:
        img = img.resize((2000 * multiplier // 2, 2000 * multiplier // 2), resample=Image.LANCZOS)

    # Draws text on the page according to the allow_diagonal
    page_draw.text(((page.size[0] - img.size[0]) // 2, page.size[1] // 6),
                   'Including diagonals' if allow_diagonal else 'Not including diagonals', fill='gray',
                   font=font)

    # If the mode is high res it will resize it with a better mode (high quality)
    if res_multiplier == 2:
        word_bank = word_bank.resize((int(word_bank.size[0]*2 - word_bank.size[0]//4), int(word_bank.size[1]*2 -
                                      word_bank.size[1]//4)), resample=Image.MEDIANCUT)
    else:
        word_bank = word_bank.resize((word_bank.size[0]*2 - word_bank.size[0]//4, word_bank.size[1]*2 -
                                      word_bank.size[1]//4), resample=Image.LANCZOS)

    # Pastes the word bank on the page
    page.paste(word_bank, ((page.size[0] - word_bank.size[0]) // 2, page.size[1] // 5 + img.size[1] +
                           (multiplier * 10)))

    # Draws the credit on the page
    page_draw.text((multiplier * 10, page.size[1] - page.size[1] // 33), 'Made By KingOfTNT10', fill='gray', font=font)

    # Pastes the img on the page
    page.paste(img, ((page.size[0] - img.size[0]) // 2, page.size[1] // 5))

    return page
