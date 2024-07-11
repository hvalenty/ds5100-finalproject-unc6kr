# ds5100-finalproject-unc6kr
Final project as culmination of summer DS5100 class.

## Metadata
* Author: Hannah Valenty
* Project Name: Monte Carlo Simulator

## Synopsis
Thr Monte Carlo Simulator allows users to create dice, play a game, and analyze a game. The three classes include methods that suppport these functions and provide information on the class objects created. 

To import this module and necessary packages:
```python
from montecarlo import Die, Game, Analyzer
import numpy as np
import pandas as pd
```
Once the module is imported, die objects can be created. Dies must be formed using a NumPy array of faces.
```python
face_list = np.array(1,2,3,4,5,6)
die = Die(face_list)
```
One Die method is to view the current state of the die. That can be accomplished using the current_state function.
```python
die.current_state()
```
Now that a die has been made it can be used to play a game. A game object is created using a list of one or more dice.
```python
die_list = [die, die, die]
game = Game(die_list)
```
One Game method is the play function. This rolls the die within a game for a number of rolls specified by the user.
```python
game.play(5)
```
To analyze a game it is necessary to use the Analyzer class. This class accepts a game and has methods to provide statistical information on the game played.
```python
analyzer = Analyzer(game)
```
A method to use for an analyzer object is the face_count_per_roll functon. This returns a dataframe with the results of rolls performed.
```python
analyzer.face_count_per_roll()
```
More methods are available within the three classes, and are described further in the API Documentation.

## API Description
This module contains three classes:
* Die
* Game 
* Analyzer

### Die Class

    The Die Class creates a die object. A die has N faces (sides)
    and W weights. A die can be rolled to select a face, where each
    face of a die is a unique symbol (alphabetic or numeric). These 
    faces have weights associated with them (default 1.0) and can 
    be changed following the creation of a die object. The one behavior
    of a die is that it can be rolled one or more times.

* \__init__(self, faces)    

        Initalize the Die class.

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
        
        Returns
        -------
        None

* change_side_weight(self, face_value, new_weight)

        Change the weight of a single face (side) of a die.

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

* roll_the_die(self, num_roll = 1)

        Roll the die object one or more times.

        Parameters
        ----------
        num_roll: int, default 1
            Define number of die rolls, essentially
            sampling with replacement.

        Returns
        -------
        List of roll outcomes, but not stored internally.

* current_state(self)

        Return a dataframe with faces and weights
        
        Returns
        -------
        np.DataFrame(faces, weights)
            Current state of the die.

### Game Class
    The Game Class makes a game object. Each game is initalized
    with a Python list which contains one or more die. These dice
    must be similar dice (same number of sides and associated faces),
    but each may have their own weights. Game objects have a behavior to 
    play a game (roll all dice set number of times), and they only keep
    the results of their most recent play.

* \__init__(self, die_list)

        Initalize the Game class.

        Parameters
        ----------
        die_list: list
            List should contain die objects, all with
            the same faces.

        Returns
        -------
        None

* play(self, times_rolled)

        Play a game by choosing number of dice rolls

        Parameters
        ----------
        times_rolled: int
            Specify the number of times the dice should be rolled.

        Returns
        -------
        None

* show_play_results(self, frame_form = 'wide)

        Show user the results of most recent play.

        Parameters
        ----------
        frame_form: 'wide' or 'narrow', default 'wide'
            Format returned dataframe, returns ValueError
            if neither option is chosen.
        
        Returns
        -------
        pd.DataFrame()
            Dataframe in wide or narrow format.
            Index: roll number
            Columns: die number (list index as header)
            Cells: face rolled in each instance

### Analyzer Class

    The Analyzer Class creates an analyzer object which takes the
    results of a single game and computes various descriptive
    statistical properties.

* \__init__(self, game)

        Initalize the Analyzer class.

        Parameters
        ----------
        game: Game
            Game object as input, throws a ValueError if the
            passed value is not a game.

        Returns
        -------
        None

* jackpot(self)

        Computes number of times a game results in a jackpot.

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of jackpots in a game.

* face_count_per_roll(self)

        Computes number of times a given face is rolled in
        each event.

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

* combo_count(self)

        Compute distinct combinations (order-independent) of faces
        rolled, along with their counts.

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Order-independent combinations which may contain repetitions.
            MultiIndex: distinct combinations 
            Column: associated counts

* permutation_count(self)

        Compute distinct permutations (order-dependent) of faces
        rolled, along with their counts.

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Order-dependent permutations which may contain repetitions.
            MultiIndex: distinct permutations 
            Column: associated counts