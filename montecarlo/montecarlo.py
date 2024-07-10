import numpy as np
import pandas as pd


class Die():
    '''
    The Die Class.
    '''
    def __init__(self, faces):
        '''
        Input: Die's faces 
        -> np.array with string or numeric type
        -> array must have distinct values
        ....................................................
        Output: None
        Created: initalized weights and face-weight dataframe
        -> weights are all set to 1
        -> pandas dataframe with faces and weights
        '''
        # Check for faces type (must be NumPy array)
        try:
            assert isinstance(faces, np.ndarray)
        except:
            raise TypeError("Faces must be a NumPy array.")
        
        # Check for data type within faces array (must be string or numeric)
        try:
            for val in faces:
                assert (type(val) == np.str_) | (type(val) == np.int_) | (type(val) == np.float_)
        except:
            print('Faces must be data type strings or numbers.')
        
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
        
        # Check the input face is in the die faces array
        try:
            assert face_value in self.faces
        except: 
            raise IndexError('This face is not present in the die array.')
        
        # Check if the input weight is a numeric type
        try:
            assert isinstance(new_weight, (int, float))
            new_weight = float(new_weight)
        except:
            raise TypeError('Input weight must be a numeric type (or castable to one).')
        
        # Identify cell to reassign weight and assign with input
        self._df_faces_weights.loc[face_value, 0] = new_weight


    def roll_the_die(self, num_roll = 1):
        # Check if the input weight is a integer type
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
        '''Return a copy of die dataframe with faces and weights'''
        return self._df_faces_weights.copy()



class Game():
    '''
    The Game Class.
    '''
    def __init__(self, die_list):
        self.die_list = die_list

    def play(self, times_rolled):
        '''
        Save result of play in private dataframe.
        .........................................
        Input: Number of times the dice should be rolled (int)
        Output: Play dataframe (private)
            -> index: roll number
            -> columns: die number (list index as header)
            -> cells: face rolled in each instance
        '''
        roller = []
        for die in self.die_list:
            roller.append(die.roll_the_die(times_rolled))
        self._df_play = pd.DataFrame(roller).T
        
    def show_play_results(self, frame_form = 'wide'):
        if frame_form == 'wide':
            return self._df_play.copy()
        elif frame_form == 'narrow':
            # MultiIndex with roll number and die number, respectively
            return self._df_play.stack().copy()
        else:
            raise ValueError('Parameter frame_form must be set to "narrow" or "wide".')


class Analyzer():
    '''
    The Analyzer Class.
    '''
    def __init__(self, game):
        if not isinstance(game, Game):
            raise ValueError('Analyzer class only accepts Game objects.')
        self.game = game

    def jackpot(self):
        '''
        Computes number of times a game results in a jackpot.
        Input: None
        Output: Number of jackpots in a game (int)
        '''
        jackpot_count = 0
        for index, row in self.game._df_play.iterrows():
            if len(row.unique()) == 1:
                jackpot_count += 1
        return jackpot_count

    def face_count_per_roll(self):
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


    def combo_count(self):
        pal = []
        for indexer, row in self.game._df_play.iterrows():
            pal.append(sorted(row.to_list()))
        return pd.DataFrame(pal).value_counts()
        
       
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
        #closer = closer.replace(0, np.nan, inplace=True)
        closer = closer.replace('0', '')
        print(big_string_lister)
        return closer.value_counts() for row in closer
        '''


    def permutation_count(self):
        '''
        More description here.
        .......................
        Input: None
        Output: pd.DataFrame
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
    