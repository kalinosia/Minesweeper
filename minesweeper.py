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

        if len(self.cells)==self.count:
            return self.cells

        return False
        #for cell in self.cells:
        #    mark_mine(cell)
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count==0:
            return self.cells

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count-=1
            self.cells.remove(cell)
            #if not know_mine():
            #    know_safes()


        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.count-=1
            self.cells.remove(cell)
            #if not know_safe():
            #    know_safe()

        #raise NotImplementedError


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
        self.moves_made.add(cell) #1
        self.safes.add(cell) #2

        #ADD EVERY NEIGHBOR OUR CELL - CARFULL IF NEAR BOARD
        neighbors=set()
        #(i,j) i = (height) j (width)
        if cell[1] > 0: neighbors.add((cell[0], cell[1]-1)) #left side
        if cell[0] > 0: neighbors.add((cell[0]-1, cell[1]))  # up side
        if cell[1] < self.width-1: neighbors.add((cell[0], cell[1]+1)) # right side
        if cell[0] < self.height-1: neighbors.add((cell[0] + 1, cell[1])) # down side
        if cell[0] > 0 and cell[1] > 0: neighbors.add((cell[0] -1, cell[1]-1)) #left up corner
        if cell[0] > 0 and cell[1] < self.width-1: neighbors.add((cell[0] -1, cell[1]+1))  # right up corner
        if cell[0] < self.height-1 and cell[1] < self.width-1: neighbors.add((cell[0] +1, cell[1]+1)) # right down corner
        if cell[0] < self.height-1 and cell[1] > 0: neighbors.add((cell[0] +1, cell[1]-1)) # left down corner
        # NOW CHECK IF SOMETHING IS TO REMOVE - MABEY VISITED OR IT'S SAFE OR IT'S MINE
        to_remove=set()
        for every_cell in neighbors:
            if every_cell in self.mines: # if neighbor is mine, count is less..
                to_remove.add(every_cell)
                count-=1
            elif every_cell in self.safes:
                to_remove.add(every_cell)
            elif every_cell in self.moves_made:
                to_remove.add(every_cell)
        # NOW REMOVE THIS CELLS
        while len(to_remove)>0:
            neighbors.remove(to_remove.pop())

        # IF THERE IS CELLS EXACTLY HOW MUCH COUNT, EVERY CELL IS MINE
        if len(neighbors)==count:
            for neighbor in neighbors:
                self.mines.add(neighbor)
        # IF COUNT==0 THEN THERE IS NO MORE MINE IN THIS CELLS
        if count==0:
            for neighbor in neighbors:
                self.safes.add(neighbor)
        
        # ADD TO KNOWLEDGE WHAT WE KNOW #############################
        self.knowledge.append((neighbors,count)) #3?????????

        '''
        if sentence.known_mines():
            for one_cell in sentence.known_mines():
                self.mark_mine(one_cell)
        if sentence.known_safes():
            for one_cell in sentence.known_safes():
                self.mark_safe(one_cell)
        '''
        for sentence in self.knowledge:
            if neighbors.intersection(sentence[0]):
                # add something to knowledge??

                if count>sentence[1]:   #len(neighbors)>len(sentence[0]): probably wrong
                    if len(set(neighbors)-set(sentence[0]))==count-sentence[1]: # so there is mine(s)
                        for cell in set(neighbors)-set(sentence[0]):
                            self.mines.add(cell)
                    elif count-sentence[1]==0:
                        for cell in set(neighbors)-set(sentence[0]):
                            self.safes.add(cell)
                elif sentence[1]>=count:   #len(neighbors)>len(sentence[0]): probably wrong
                    if len(set(sentence[0])-set(neighbors))==count-sentence[1]: # so there is mine(s)
                        #add something to knowledge??
                        for cell in set(sentence[0])-set(neighbors):
                            self.mines.add(cell)
                    elif sentence[1]-count==0:
                        for cell in set(neighbors)-set(sentence[0]):
                            self.safes.add(cell)

        ########################CHECK THIS ^ UPP

            #sentence.know_safe()
            #sentence.know_mines()


        #raise NotImplementedError

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


        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # height width (i,j) cell
        while True:
            i=random.randint(0,self.height-1)
            j=random.randint(0,self.width-1)
            if (i,j) not in self.moves_made and (i,j) not in self.mines:
                return (i,j)

        #raise NotImplementedError
