from montecarlo.montecarlo import Die, Game, Analyzer
import numpy as np
import pandas as pd
import unittest

class DieTestSuite(unittest.TestCase):

    def test_01_init(self):
        # Check if die object is of Die type and create dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        self.assertIs(type(die), Die)
        self.assertIs(type(die._df_faces_weights), pd.DataFrame)

    def test_02_change_side_weight(self):
        # Check if after weights change private 
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die.change_side_weight(1, 100)
        self.assertEqual(die._df_faces_weights[0][1], 100)

    def test_03_roll_the_die(self):
        # Check if rolled return is a list
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        rolled = die.roll_the_die(5)
        self.assertIs(type(rolled), list)

    def test_04_current_state(self):
        # Check if state return is a pd.DataFrame
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        state = die.current_state()
        self.assertIs(type(state), pd.DataFrame)


class GameTestSuite(unittest.TestCase):
    
    def test_05_init(self):
        # Check if game object is of Game type
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        self.assertIs(type(die_list), list)
        self.assertIs(type(game), Game)

    def test_06_play(self):
        # Check if play operates on and saves dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        self.assertIs(type(game._df_play), pd.DataFrame)
        self.assertEqual(len(game._df_play.index), 5)

    def test_07_show_play_results(self):
        # Check if show play returns dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        show_play = game.show_play_results()
        self.assertIs(type(show_play), pd.DataFrame)


class AnalyzerTestSuite(unittest.TestCase):

    def test_08_init(self):
        # Check if analyzer object is of Analyzer type
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        analyzer = Analyzer(game)
        self.assertIs(type(game), Game)
        self.assertIs(type(analyzer), Analyzer)

    def test_09_jackpot(self):
        # Check if jackpot returns type integer
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        analyzer = Analyzer(game)
        jack_num = analyzer.jackpot()
        self.assertIs(type(jack_num), int)

    def test_10_face_count_per_roll(self):
        # Check if face counts returns dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        analyzer = Analyzer(game)
        face_count = analyzer.face_count_per_roll()
        self.assertIs(type(face_count), pd.DataFrame)

    def test_11_combo_count(self):
        # Check if combo counts returns dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        analyzer = Analyzer(game)
        combine_count = analyzer.combo_count()
        self.assertIs(type(combine_count), pd.DataFrame)

    def test_12_permutation_count(self):
        # Check if combo counts returns dataframe
        die_face = np.array([1,2,3,4,5,6])
        die = Die(die_face)
        die_list = [die, die, die]
        game = Game(die_list)
        game.play(5)
        analyzer = Analyzer(game)
        permute_count = analyzer.permutation_count()
        self.assertIs(type(permute_count), pd.DataFrame)


if __name__ == '__main__':
    unittest.main(verbosity=3)