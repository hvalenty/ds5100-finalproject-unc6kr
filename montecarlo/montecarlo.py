import numpy as np
import pandas as pd


class Die():
    '''
    The Die Class creates a die object. A die has N faces (sides)
    and W weights. A die can be rolled to select a face, where each
    face of a die is a unique symbol (alphabetic or numeric). These 
    faces have weights associated with them (default 1.0) and can 
    be changed following the creation of a die object. The one behavior
    of a die is that it can be rolled one or more times.

    Methods
    -------
    __init__()
    change_side_weight()
    roll_the_die()
    current_state()
    '''
    def __init__(self, faces):
        '''
        Initalize the Die class.
        __init__(self, faces)

        Parameters
        ----------
        faces : np.array
            Array can contain string or numeric (int, float)
            types, and must have distinct (unique) values.

        Changes
        -------
        weights: np.array
            Array is initalized to all ones, but can
            be changed with method following initalization.
        
        _df_faces_weights: np.DataFrame
            Private attribute dataframe to save die faces and weights.
        Returns
        -------
        None
        '''
        # Check for faces type (must be NumPy array)
        try:
            assert isinstance(faces, np.ndarray)
        except:
            raise TypeError("Faces must be a NumPy array.")
        
        # Check for data type within faces array (must be string or numeric)
        try:
            for val in faces:
                assert (type(val) == np.str_) | (type(val) == np.int_) | (type(val) == np.float_)\
                                           | (type(val) == int) | (type(val) == float) | (type(val) == str)
        except:
            raise TypeError('Faces must be data type strings or numbers.')
        
        # Check if faces array has distinct values (must be all unique)
        try:
            assert len(set(faces)) == len(faces)
        except:
            raise ValueError('The faces array must have distinct values.')
        
        # Initalize with input faces array 
        self.faces = faces

        # Initalize weights with array of ones
        weights = np.ones(len(faces))
        self.weights = weights

        # Save faces and weights arrays in a private dataframe
        self._df_faces_weights = pd.DataFrame(self.weights, self.faces)
        

    def change_side_weight(self, face_value, new_weight):
        '''
        Change the weight of a single face (side) of a die.
        change_side_weight(self, face_value, new_weight)

        Parameters
        ----------
        face_value: str or numeric (int, float)
            Face value must be present in list of die's faces,
            if not, a IndexError is raised.
        new_weight: numeric (int, float)
            If the input can be cast as numeric that action
            is done, otherwise TypeError is raised.
        
        Changes
        -------
        weights: np.array
            Corresponding die face_value's weight in vector is
            changed to user new_weight input. 

        Returns
        -------
        None
        '''
        # Check the input face is in the die faces array
        try:
            assert face_value in self.faces
        except: 
            raise IndexError('This face is not present in the die array.')
        
        # Check if the input weight is a numeric type
        try:
            #assert (type(new_weight) == np.bool_) | (type(new_weight) == np.int_) | (type(new_weight) == np.float_)
            assert isinstance(new_weight, (int, float))
            new_weight = float(new_weight)
        except:
            raise TypeError('Input weight must be a numeric type (or castable to one).')
        
        # Identify cell to reassign weight and assign with input
        self._df_faces_weights.loc[face_value, 0] = new_weight


    def roll_the_die(self, num_roll = 1):
        '''
        Roll the die object one or more times.
        roll_the_die(self, num_roll = 1)

        Parameters
        ----------
        num_roll: int, default 1
            Define number of die rolls, essentially
            sampling with replacement.

        Returns
        -------
        List of roll outcomes, but not stored internally.
        '''
        # Check if the input roll count is an integer type
        try:
            assert isinstance(num_roll, int)
        except:
            raise TypeError('Input roll must be an integer type.')
        
        # Roll the die using sampling with replacement
        rolled = self._df_faces_weights.sample(n = num_roll, 
                                        replace = True,
                                        weights = self.weights)
        return rolled.index.to_list()
        

    def current_state(self):
        '''Return a copy of die dataframe with faces and weights
        current_state(self)
        
        Returns
        -------
        np.DataFrame(faces, weights)
            Current state of the die.
        '''
        return self._df_faces_weights.copy()



class Game():
    '''
    The Game Class makes a game object. Each game is initalized
    with a Python list which contains one or more die. These dice
    must be similar dice (same number of sides and associated faces),
    but each may have their own weights. Game objects have a behavior to 
    play a game (roll all dice set number of times), and they only keep
    the results of their most recent play.

    Methods
    -------
    __init__()
    play()
    show_play_results()
    '''
    def __init__(self, die_list):
        '''
        Initalize the Game class.
        __init__(self, die_list)

        Parameters
        ----------
        die_list: list
            List should contain die objects, all with
            the same faces.

        Returns
        -------
        None
        '''
        self.die_list = die_list

    def play(self, times_rolled):
        '''
        Play a game by choosing number of dice rolls
        play(self, times_rolled)

        Parameters
        ----------
        times_rolled: int
            Specify the number of times the dice should be rolled.

        Changes
        -------
        _df_play: pd.DataFrame
            Private attribute dataframe in wide format.
            Index: roll number
            Columns: die number (list index as header)
            Cells: face rolled in each instance

        Returns
        -------
        None
        '''
        # Check if the roll amount is an integer type
        try:
            assert isinstance(times_rolled, int)
        except:
            raise TypeError('Input roll must be an integer type.')
        roller = []
        for die in self.die_list:
            roller.append(die.roll_the_die(times_rolled))
        self._df_play = pd.DataFrame(roller).T
        
    def show_play_results(self, frame_form = 'wide'):
        '''
        Show user the results of most recent play.
        show_play_results(self, frame_form = 'wide)

        Parameters
        ----------
        frame_form: 'wide' or 'narrow', default 'wide'
            Format returned dataframe, returns ValueError
            if neither option is chosen.
        
        Returns
        -------
        pd.DataFrame()
            Private attribute dataframe in wide or narrow format.
            Index: roll number
            Columns: die number (list index as header)
            Cells: face rolled in each instance
        '''
        if frame_form == 'wide':
            return self._df_play.copy()
        elif frame_form == 'narrow':
            # MultiIndex with roll number and die number, respectively
            return self._df_play.stack().copy()
        else:
            raise ValueError('Parameter frame_form must be set to "narrow" or "wide".')


class Analyzer():
    '''
    The Analyzer Class creates an analyzer object which takes the
    results of a single game and computes various descriptive
    statistical properties.

    Methods
    -------
    __init__()
    jackpot()
    face_count_per_roll()
    combo_count()
    permutation_count()
    '''
    def __init__(self, game):
        '''
        Initalize the Analyzer class.
        __init__(self, game)

        Parameters
        ----------
        game: Game
            Game object as input, throws a ValueError if the
            passed value is not a game.

        Returns
        -------
        None
        '''
        if not isinstance(game, Game):
            raise ValueError('Analyzer class only accepts Game objects.')
        self.game = game

    def jackpot(self):
        '''
        Computes number of times a game results in a jackpot.
        jackpot(self)

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of jackpots in a game.
        '''
        jackpot_count = 0
        for index, row in self.game._df_play.iterrows():
            if len(row.unique()) == 1:
                jackpot_count += 1
        return jackpot_count

    def face_count_per_roll(self):
        '''
        Computes number of times a given face is rolled in
        each event.
        face_count_per_roll(self)

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Results of rolls in wide dataframe form.
            Index: roll number
            Columns: face values
            Cells: count values
        '''
        # Empty dict and list for face counts
        results = {}
        big_list_csv = []
        # Iterate over rows in game results
        for indexer, row in self.game._df_play.iterrows():
            # face_comp is Die faces list to match with
            # roll_comp which is roll results list
            face_comp = self.game.die_list[0].faces
            roll_comp = row.to_list()
            # Below loop counts matches between face_comp and roll_comp
            for i in face_comp:
                results[i] = roll_comp.count(i)
                # appends in comma separated list form
                big_list_csv.append(results[i]) 
        # Convert list to string and clean it up
        big_string = str(big_list_csv).replace('[', '').replace(']','').split(', ')
        # Chunk long data string into proper form for pandas dataframe
        big_string_lister = [big_string[x:x + len(self.game.die_list[0].faces)]\
                for x in range(0, len(big_string), len(self.game.die_list[0].faces))]
        # Make the final output dataframe
        closer = pd.DataFrame(big_string_lister, columns=self.game.die_list[0].faces)
        return closer

        '''
        #df_shell = pd.DataFrame(columns = self.game.die_list[0].faces)
        # Empty dict and list for face counts
        results = {}
        big_list_csv = []
        # Iterate over rows in game results
        for indexer, row in self.game._df_play.iterrows():
            # face_comp is Die faces list to match with
            # roll_comp which is roll results list
            face_comp = self.game.die_list[0].faces
            roll_comp = row.to_list()
            # Below loop counts matches between face_comp and roll_comp
            for i in face_comp:
                results[i] = roll_comp.count(i)
                # appends in comma separated list form
                big_list_csv.append(results[i]) 
        #for indexer, row in self.game._df_play.iterrows():
            #list_shell = row.value_counts().to_frame()
            #df_shell.index = range(indexer)
        # Convert list to string and clean it up
        big_string = str(big_list_csv).replace('[', '').replace(']','').split(', ')
        # Chunk long data string into proper form for pandas dataframe
        big_string_lister = [big_string[x:x + len(self.game.die_list[0].faces)]\
                for x in range(0, len(big_string), len(self.game.die_list[0].faces))]
        #fine_df = pd.DataFrame([str(big_list_csv).split(',') for big_list_csv in len(big_list_csv)])
        #fin_df = pd.DataFrame([sub.split(',') for sub in big_list_csv], columns=self.game.die_list[0].faces)
        # Make the final output dataframe
        closer = pd.DataFrame(big_string_lister, columns=self.game.die_list[0].faces)
        #print(big_list_csv)
        return closer
        '''


    def combo_count(self):
        '''
        Compute distinct combinations (order-independent) of faces
        rolled, along with their counts.
        combo_count(self)

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Order-independent combinations which may contain repetitions.
            MultiIndex: distinct combinations 
            Column: associated counts
        '''
        pal = []
        # Iterate through rows of game play dataframe
        for indexer, row in self.game._df_play.iterrows():
            # Sort each row to "standardize" the order of face appearance
            # thus making combinations order IN-dependent
            pal.append(sorted(row.to_list()))
        return pd.DataFrame(pal).value_counts().to_frame()
        
       
    def permutation_count(self):
        '''
        Compute distinct permutations (order-dependent) of faces
        rolled, along with their counts.
        permutation_count(self)

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Order-dependent permutations which may contain repetitions.
            MultiIndex: distinct permutations 
            Column: associated counts
        '''
        return self.game._df_play.value_counts().to_frame()

        '''
        roll_dict = pd.DataFrame()
        count = 0
        for index, row in self.game._df_play.iterrows():
            roll_dict = pd.concat([roll_dict, row.value_counts().to_frame()])
            roll_dict['indexer'] = index
            print(index)
        print(row.value_counts().to_frame())
        print(roll_dict)
        '''

        #roll_dict = {}
        #for index, row in self.game._df_play.iterrows():
         #   roll_dict['indexer'] = index


if __name__ == '__main__':
    '''
    d1_faces = np.array([1,2,3,4,5,6])
    die1 = Die(d1_faces)
    d2_faces = np.array(['j','o','s','e','p','h'])
    die2 = Die(d2_faces)
    print(type('j'))
    die2.change_side_weight('o',3)
    print(die2._df_faces_weights)
    print(die2.weights)
    die2.change_side_weight('e',3)
    print(die2._df_faces_weights)
    print(die2.current_state())
    print(die2.roll_the_die(10))
    '''
    d1_face = np.array([1,2,3,4,5,6])
    die1 = Die(d1_face)
    die2 = Die(d1_face)
    die3 = Die(d1_face)
    die3.change_side_weight(3, 10)
    die3.change_side_weight(4, 10)
    die_lister = [die1, die2, die3]
    game1 = Game(die_lister)
    game1.play(8)
    print(game1.show_play_results(frame_form='wide'))
    any1 = Analyzer(game1)
    print(any1.jackpot())
    print(any1.face_count_per_roll())
    print(any1.combo_count())
    print(any1.permutation_count())
    print(die1._df_faces_weights)
    

 