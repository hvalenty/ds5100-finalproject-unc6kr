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
        pass

    

class Analyzer():
    '''
    The Analyzer Class.
    '''
    def __init__():
        pass


if __name__ == '__main__':
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
    