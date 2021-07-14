import itertools
import random
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """

        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return self.cells

        return False
        # for cell in self.cells:
        #    mark_mine(cell)
        # raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)
            # if not know_mine():
            #    know_safes()

        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)
            # if not know_safe():
            #    know_safe()

        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.moves_made.add(cell)  # 1
        self.safes.add(cell)  # 2

        # ADD EVERY NEIGHBOR OUR CELL - CARFULL IF NEAR BOARD
        neighbors = set()
        # (i,j) i = (height) j (width)
        # left side
        if cell[1] > 0:
            if (cell[0], cell[1] - 1) in self.mines:
                count -= 1
            elif ((cell[0], cell[1] - 1) not in self.mines) and ((cell[0], cell[1] - 1) not in self.safes):
                neighbors.add((cell[0], cell[1] - 1))
        # up side
        if cell[0] > 0:
            if (cell[0] - 1, cell[1]) in self.mines:
                count -= 1
            elif ((cell[0] - 1, cell[1]) not in self.mines) and ((cell[0] - 1, cell[1]) not in self.safes):
                neighbors.add((cell[0] - 1, cell[1]))

        if cell[1] < self.width - 1:
            if (cell[0], cell[1] + 1) in self.mines:
                count -= 1
            elif ((cell[0], cell[1] + 1) not in self.mines) and ((cell[0], cell[1] + 1) not in self.safes):
                neighbors.add((cell[0], cell[1] + 1))  # right side

        if cell[0] < self.height - 1:
            if (cell[0] + 1, cell[1]) in self.mines:
                count -= 1
            elif ((cell[0] + 1, cell[1]) not in self.mines) and ((cell[0] + 1, cell[1]) not in self.safes):
                neighbors.add((cell[0] + 1, cell[1]))  # down side

        if cell[0] > 0 and cell[1] > 0:
            if (cell[0] - 1, cell[1] - 1) in self.mines:
                count -= 1
            elif ((cell[0] - 1, cell[1] - 1) not in self.mines) and ((cell[0] - 1, cell[1] - 1) not in self.safes):
                neighbors.add((cell[0] - 1, cell[1] - 1))  # left up corner

        if cell[0] > 0 and cell[1] < self.width - 1:
            if (cell[0] - 1, cell[1] + 1) in self.mines:
                count -= 1
            elif ((cell[0] - 1, cell[1] + 1) not in self.mines) and ((cell[0] - 1, cell[1] + 1) not in self.safes):
                neighbors.add((cell[0] - 1, cell[1] + 1))  # right up corner

        if cell[0] < self.height - 1 and cell[1] < self.width - 1:
            if (cell[0] + 1, cell[1] + 1) in self.mines:
                count -= 1
            elif ((cell[0] + 1, cell[1] + 1) not in self.mines) and ((cell[0] + 1, cell[1] + 1) not in self.safes):
                neighbors.add((cell[0] + 1, cell[1] + 1))  # right down corner

        if cell[0] < self.height - 1 and cell[1] > 0:
            if (cell[0] + 1, cell[1] - 1) in self.mines:
                count -= 1
            elif ((cell[0] + 1, cell[1] - 1) not in self.mines) and ((cell[0] + 1, cell[1] - 1) not in self.safes):
                neighbors.add((cell[0] + 1, cell[1] - 1))  # left down corner
        # ---------------------------------------------------------------------------------------------------------
        #print("cell: " , cell) ###############################################################################
        #print("Neighbors: ", neighbors, " count: ", count)
        # IF COUNT==0 THEN THERE IS NO MORE MINE IN THIS CELLS
        if count == 0:
            for neighbor in neighbors:
                self.safes.add(neighbor)
                #print("Adding to safe: ", neighbor)
        # IF THERE IS CELLS EXACTLY HOW MUCH COUNT, EVERY CELL IS MINE
        elif len(neighbors) == count:
            for neighbor in neighbors:
                self.mines.add(neighbor)
        # ADD TO KNOWLEDGE WHAT WE KNOW #############################
        else:  # changeningorsometh
            self.knowledge.append([neighbors, count])  # 3   # KNOWLEDGE APPEND !!
        # -----------------------------------------------------------------------------------------------------------
        # check if in sentence in knowledge is cell, if sentence ==0 or len==count in sentences
        for sentence in self.knowledge:
            if cell in sentence[0]:
                sentence[0].remove(cell)  # we remove cell from our knowledge because cell is safe
            for one_cell in self.safes:
                if one_cell in sentence[0]:
                    sentence[0].remove(one_cell)
            for one_cell in self.mines:
                if one_cell in sentence[0]:
                    sentence[0].remove(one_cell)
                    sentence[1] -= 1
            # if len(sentence[0])==0 and sentence[1]==0:#remove sentence???
            if sentence[1] == 0:
                for one_cell in sentence[0]:
                    self.safes.add(one_cell)
            if len(sentence[0]) == sentence[1]:
                for one_cell in sentence[0]:
                    self.mines.add(one_cell)
        # -------------------------------------- DELETE SENTENCE FROM KNOWLEDGE (less memory)
        len_of_knowledge = len(self.knowledge)
        turn=0
        while turn<len_of_knowledge:
            sentence=self.knowledge[turn]
            if len(sentence[0]) == 0 or sentence[1] == 0 or len(sentence[0]) == sentence[1]:
                del self.knowledge[turn]
                len_of_knowledge -= 1
            else:
                turn += 1

        # ----------------------------------------------------------------------------------------------------------
        if len(self.knowledge)>=3:

            for i in self.knowledge:
                for j in self.knowledge:
                    if i == j: continue
                    if i[0].issubset(j[0]):
                        # add something to knowledge??
                        new_tuple = (j[0] - i[0], j[1] - i[1])
                        # self.knowledge.append(new_tuple[0], new_tuple[1]]}?) #???????????add or no?
                        if not len(new_tuple): continue

                        if len(new_tuple[0]) == new_tuple[1]:  # so there is mine(s)
                            for new_cell in new_tuple[0]:
                                self.mines.add(new_cell)
                        elif new_tuple[1] == 0:
                            for new_cell in new_tuple[0]:
                                self.safes.add(new_cell)
                        else:  # ??????????
                            self.knowledge.append([new_tuple])  # KNOWLEDGE APPEND !!


            '''
            column=0
            row=1
            while True:
                sentence_first=self.knowledge[column]
                sentence_second=self.knowledge[row]

                if sentence_first[0].issubset(sentence_second[0]):
                    # add something to knowledge??
                    new_tuple = (sentence_second[0] - sentence_first[0], sentence_second[1] - sentence_first[1])
                    # self.knowledge.append(new_tuple[0], new_tuple[1]]}?) #???????????add or no?
                    if not len(new_tuple): continue

                    if len(new_tuple[0]) == new_tuple[1]:  # so there is mine(s)
                        for new_cell in new_tuple[0]:
                            self.mines.add(new_cell)
                    elif new_tuple[1] == 0:
                        for new_cell in new_tuple[0]:
                            self.safes.add(new_cell)
                    else:  # ??????????
                        self.knowledge.append([new_tuple])  # KNOWLEDGE APPEND !!

                elif (sentence_second[0]).issubset(sentence_first[0]):
                    new_tuple = (sentence_first[0] - sentence_second[0], sentence_first[1] - sentence_second[1])
                    if not len(new_tuple): continue

                    if len(new_tuple[0]) == new_tuple[1]:
                        for new_cell in new_tuple[0]:
                            self.mines.add(new_cell)
                    elif new_tuple[1] == 0:
                        for new_cell in new_tuple[0]:
                            self.safes.add(new_cell)
                    else:
                        self.knowledge.append([new_tuple])   # KNOWLEDGE APPEND !!

                print(row, column)
                row+=1
                if row >= len(self.knowledge):
                    column+=1
                    row=column+1
                if column>=len(self.knowledge):
                    break
            '''
        ########################CHECK THIS ^ UPP

        # sentence.know_safe()
        # sentence.know_mines()
        #print("end processing")
        # raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # height width (i,j) cell
        moves=0
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made:
                    if (i,j) not in self.mines and (i,j) not in self.safes:
                        moves+=1

        if moves == 0: return None

        while True:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)

        # raise NotImplementedError
