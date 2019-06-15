from random import randint
import copy


class Cube3():
    """This class stores and manipulates a 3x3x3 cube"""

    def __init__(self):
        """initialize the cube as solved state"""
        self.cube = []
        for i in range(0, 6):
            temp = [[i, i, i] for j in range(3)]
            self.cube.append(temp)
        self.unsolvable = False

    def input_scramble(self, algorithm):
        """use a scramble algorithm on a solved cube to scramble it"""
        self.algo(algorithm)
        print(algorithm)
        print("scramble complete")

    def input_raw(self, cube_list):
        """input the raw list of cube data, in the form of 6x3x3 list"""
        self.cube = copy.deepcopy(cube_list)
        print("finished updating the cube")

    def print_cube(self):
        """
        print the cube's expansion view
        formated like this:
           B
           U
         L F R
           D
        further explaination on how the cube is represented by
        the list can be found in input_output_conventions.txt
        """
        for side in range(4, 6):
            for i in range(3):
                print("        ", end="")
                for j in range(3):
                    print(self.cube[side][i][j], end=' ')
                print("")
            print("")
        for i in range(3):
            for side in [3, 1, 2]:
                for j in range(3):
                    print(self.cube[side][i][j], end=' ')
                print("  ", end="")
            print("")
        print("")
        for i in range(3):
            print("        ", end="")
            for j in range(3):
                print(self.cube[0][i][j], end=' ')
            print("")

    def scramble(self):
        """randomly scramble the cube, and returns the scramble algorithm"""
        algorithm = ""
        last_move = 0
        for i in range(20):
            move = randint(1, 12)
            while round((move-1)/2) == round((last_move-1)/2):
                move = randint(1, 12)
            if move == 1:
                self.R(1)
                algorithm = algorithm + "R "
            if move == 2:
                self.R_(1)
                algorithm = algorithm + "R_ "
            if move == 3:
                self.L(1)
                algorithm = algorithm + "L "
            if move == 4:
                self.L_(1)
                algorithm = algorithm + "L_ "
            if move == 5:
                self.U(1)
                algorithm = algorithm + "U "
            if move == 6:
                self.U_(1)
                algorithm = algorithm + "U_ "
            if move == 7:
                self.D(1)
                algorithm = algorithm + "D "
            if move == 8:
                self.D_(1)
                algorithm = algorithm + "D_ "
            if move == 9:
                self.F(1)
                algorithm = algorithm + "F "
            if move == 10:
                self.F_(1)
                algorithm = algorithm + "F_ "
            if move == 11:
                self.B(1)
                algorithm = algorithm + "B "
            if move == 12:
                self.B_(1)
                algorithm = algorithm + "B_ "
            last_move = move
        return algorithm.rstrip()

# the following four functions checks if each step of cfop is done.

    def cross_done(self):
        if self.cube[0][0][1] != 0:
            return False
        if self.cube[0][1][0] != 0:
            return False
        if self.cube[0][1][2] != 0:
            return False
        if self.cube[0][2][1] != 0:
            return False
        if self.cube[1][2][1] != self.cube[1][1][1]:
            return False
        if self.cube[2][2][1] != self.cube[2][1][1]:
            return False
        if self.cube[3][2][1] != self.cube[3][1][1]:
            return False
        if self.cube[4][2][1] != self.cube[4][1][1]:
            return False
        return True

    def f2l_done(self):
        for i in range(3):
            for j in range(3):
                if self.cube[0][i][j] != 0:
                    return False
        for k in range(1, 5):
            for i in range(1, 3):
                for j in range(3):
                    if self.cube[k][i][j] != self.cube[k][1][1]:
                        return False
        return True

    def oll_done(self):
        if self.f2l_done() == False:
            return False
        for i in range(3):
            for j in range(3):
                if self.cube[5][i][j] != 5:
                    return False
        return True

    def cfop_done(self):
        if self.oll_done() == False:
            return False
        for k in range(1, 5):
            for i in range(3):
                if self.cube[k][0][i] != self.cube[k][1][1]:
                    return False
        return True

#   the following 5 functions solves the cube using the (psudo) cfop method.
#   these functions will return a list of strings representing the algorithms
# they have used.
#   only full_cfop needs to be called most of the times.

    def cfop_cross(self):
        algorithm = ""
        edge_not_on_top = 4
        if self.cube[5][0][1] == 0:
            edge_not_on_top = edge_not_on_top - 1
        if self.cube[5][1][0] == 0:
            edge_not_on_top = edge_not_on_top - 1
        if self.cube[5][1][2] == 0:
            edge_not_on_top = edge_not_on_top - 1
        if self.cube[5][2][1] == 0:
            edge_not_on_top = edge_not_on_top - 1
        FRBL = [1, 2, 4, 3]
        while edge_not_on_top > 0:
            found = 0
            for i in range(4):
                if self.cube[FRBL[i]][1][2] == 0:
                    found = 1
                    if i == 1:
                        algorithm = algorithm + self.algo("y") + " "
                    elif i == 2:
                        algorithm = algorithm + self.algo("y y") + " "
                    elif i == 3:
                        algorithm = algorithm + self.algo("y_") + " "
                    if self.cube[5][1][2] == 0:
                        if self.cube[5][0][1] != 0:
                            algorithm = algorithm + self.algo("U") + " "
                        elif self.cube[5][2][1] != 0:
                            algorithm = algorithm + self.algo("U_") + " "
                        else:
                            algorithm = algorithm + self.algo("U U") + " "
                    algorithm = algorithm + self.algo("R") + " "
                    edge_not_on_top = edge_not_on_top - 1
                    break
            if found == 1:
                continue
            for i in range(4):
                if self.cube[FRBL[i]][1][0] == 0:
                    found = 1
                    if i == 1:
                        algorithm = algorithm + self.algo("y") + " "
                    elif i == 2:
                        algorithm = algorithm + self.algo("y y") + " "
                    elif i == 3:
                        algorithm = algorithm + self.algo("y_") + " "
                    if self.cube[5][1][0] == 0:
                        if self.cube[5][2][1] != 0:
                            algorithm = algorithm + self.algo("U") + " "
                        elif self.cube[5][0][1] != 0:
                            algorithm = algorithm + self.algo("U_") + " "
                        else:
                            algorithm = algorithm + self.algo("U U") + " "
                    algorithm = algorithm + self.algo("L_") + " "
                    edge_not_on_top = edge_not_on_top - 1
                    break
            if found == 1:
                continue
            for i in range(4):
                if self.cube[FRBL[i]][0][1] == 0:
                    found = 1
                    if i == 1:
                        algorithm = algorithm + self.algo("U") + " "
                    elif i == 2:
                        algorithm = algorithm + self.algo("U U") + " "
                    elif i == 3:
                        algorithm = algorithm + self.algo("U_") + " "
                    algorithm = algorithm + self.algo("F") + " "
                    if self.cube[5][1][2] == 0:
                        if self.cube[5][0][1] != 0:
                            algorithm = algorithm + self.algo("U") + " "
                        elif self.cube[5][2][1] != 0:
                            algorithm = algorithm + self.algo("U_") + " "
                        else:
                            algorithm = algorithm + self.algo("U U") + " "
                    algorithm = algorithm + self.algo("R") + " "
                    edge_not_on_top = edge_not_on_top - 1
                    break
            if found == 1:
                continue
            for i in range(4):
                if self.cube[FRBL[i]][2][1] == 0:
                    found = 1
                    if i == 1:
                        algorithm = algorithm + self.algo("D_") + " "
                    elif i == 2:
                        algorithm = algorithm + self.algo("D D") + " "
                    elif i == 3:
                        algorithm = algorithm + self.algo("D") + " "
                    if self.cube[5][2][1] == 0:
                        if self.cube[5][1][2] != 0:
                            algorithm = algorithm + self.algo("U") + " "
                        elif self.cube[5][1][0] != 0:
                            algorithm = algorithm + self.algo("U_") + " "
                        else:
                            algorithm = algorithm + self.algo("U U") + " "
                    algorithm = algorithm + self.algo("F_") + " "
                    if self.cube[5][1][2] == 0:
                        if self.cube[5][0][1] != 0:
                            algorithm = algorithm + self.algo("U") + " "
                        elif self.cube[5][2][1] != 0:
                            algorithm = algorithm + self.algo("U_") + " "
                        else:
                            algorithm = algorithm + self.algo("U U") + " "
                    algorithm = algorithm + self.algo("R") + " "
                    edge_not_on_top = edge_not_on_top - 1
                    break
            if found == 1:
                continue
            if self.cube[0][0][1] == 0:
                algorithm = algorithm + self.algo("D_") + " "
            elif self.cube[0][2][1] == 0:
                algorithm = algorithm + self.algo("D") + " "
            elif self.cube[0][1][0] == 0:
                algorithm = algorithm + self.algo("D D") + " "
            if self.cube[5][1][2] == 0:
                if self.cube[5][0][1] != 0:
                    algorithm = algorithm + self.algo("U") + " "
                elif self.cube[5][2][1] != 0:
                    algorithm = algorithm + self.algo("U_") + " "
                else:
                    algorithm = algorithm + self.algo("U U") + " "
            algorithm = algorithm + self.algo("R R") + " "
            edge_not_on_top = edge_not_on_top - 1
        for i in range(4):
            for j in range(4):
                if self.cube[5][2][1] == 0 and self.cube[1][0][1] == self.cube[1][1][1]:
                    break
                algorithm = algorithm + self.algo("U") + " "
            algorithm = algorithm + self.algo("F F y") + " "
        return algorithm

    def cfop_f2l(self):
        if self.cross_done() == False:
            return "DNF"
        algorithm = ""
        for i in range(4):
            algorithm = algorithm + self.f2l_one_out_of_four()
            algorithm = algorithm + self.algo("y") + " "
        return algorithm

    def cfop_oll(self):
        patterns = [
            [[0, 0, 0], [0, 0, 5], [0, 0, 5], [0, 0, 5]],
            [[5, 0, 0], [5, 0, 0], [5, 0, 0], [0, 0, 0]],
            [[5, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 5]],
            [[0, 0, 5], [0, 0, 0], [5, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [0, 0, 0], [5, 0, 5]],
            [[5, 0, 5], [0, 0, 0], [0, 0, 0], [5, 0, 5]],
            [[0, 0, 5], [0, 0, 0], [5, 0, 5], [5, 0, 0]],
            [[0, 5, 0], [0, 0, 0], [5, 0, 5], [0, 5, 0]],
            [[0, 0, 0], [0, 0, 0], [5, 5, 5], [0, 5, 0]],
            [[0, 0, 0], [5, 5, 5], [0, 0, 0], [0, 5, 0]],
            [[5, 5, 0], [0, 0, 0], [0, 0, 0], [0, 5, 5]],
            [[0, 5, 5], [0, 5, 0], [5, 0, 5], [5, 0, 0]],
            [[5, 5, 0], [5, 0, 5], [0, 5, 0], [0, 0, 5]],
            [[0, 5, 5], [0, 0, 0], [5, 0, 5], [5, 5, 0]],
            [[0, 5, 5], [0, 5, 0], [5, 5, 5], [5, 5, 0]],
            [[0, 5, 0], [0, 5, 5], [0, 5, 5], [0, 5, 5]],
            [[5, 5, 0], [5, 5, 0], [5, 5, 0], [0, 5, 0]],
            [[0, 5, 0], [5, 5, 5], [5, 5, 5], [0, 5, 0]],
            [[0, 0, 0], [0, 0, 5], [0, 5, 5], [0, 5, 5]],
            [[5, 5, 0], [5, 0, 0], [5, 5, 0], [0, 0, 0]],
            [[0, 5, 5], [0, 5, 5], [0, 0, 0], [0, 0, 5]],
            [[5, 0, 0], [5, 5, 0], [0, 0, 0], [5, 5, 0]],
            [[5, 5, 0], [0, 5, 5], [0, 0, 0], [0, 0, 0]],
            [[5, 0, 0], [0, 0, 5], [0, 5, 0], [0, 5, 0]],
            [[5, 0, 0], [5, 5, 5], [0, 0, 0], [0, 5, 5]],
            [[5, 5, 0], [5, 5, 5], [0, 0, 0], [0, 0, 5]],
            [[5, 0, 5], [0, 5, 0], [0, 0, 0], [5, 5, 5]],
            [[0, 5, 0], [5, 0, 5], [5, 5, 5], [0, 0, 0]],
            [[0, 5, 0], [0, 5, 0], [0, 5, 5], [5, 5, 0]],
            [[0, 5, 0], [0, 5, 0], [0, 5, 0], [5, 5, 5]],
            [[0, 5, 0], [5, 5, 0], [0, 5, 5], [0, 5, 0]],
            [[5, 5, 0], [0, 5, 0], [5, 0, 0], [5, 0, 0]],
            [[0, 0, 5], [0, 5, 0], [0, 0, 5], [0, 5, 5]],
            [[0, 5, 0], [0, 5, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 5, 0], [0, 0, 0], [0, 0, 0], [0, 5, 0]],
            [[0, 0, 0], [5, 5, 5], [0, 5, 0], [0, 0, 0]],
            [[0, 5, 0], [0, 0, 5], [5, 0, 0], [0, 5, 0]],
            [[0, 5, 0], [5, 5, 0], [0, 0, 0], [0, 0, 5]],
            [[5, 0, 0], [0, 5, 5], [0, 0, 0], [0, 5, 0]],
            [[5, 0, 0], [5, 0, 0], [5, 5, 0], [0, 5, 0]],
            [[0, 5, 5], [0, 5, 0], [0, 0, 5], [0, 0, 5]],
            [[5, 0, 0], [0, 0, 0], [0, 5, 0], [0, 5, 5]],
            [[5, 5, 0], [0, 0, 0], [0, 5, 0], [0, 0, 5]],
            [[0, 5, 0], [0, 0, 0], [0, 0, 5], [5, 5, 0]],
            [[0, 5, 0], [5, 0, 0], [0, 0, 0], [0, 5, 5]],
            [[0, 5, 0], [0, 5, 0], [0, 0, 0], [5, 0, 5]],
            [[5, 0, 5], [0, 5, 0], [0, 0, 0], [0, 5, 0]],
            [[0, 0, 0], [5, 0, 0], [0, 5, 5], [0, 5, 0]],
            [[0, 5, 0], [0, 0, 5], [5, 5, 0], [0, 0, 0]],
            [[5, 5, 0], [5, 0, 0], [5, 0, 0], [0, 5, 0]],
            [[0, 5, 5], [0, 0, 5], [0, 0, 5], [0, 5, 0]],
            [[5, 5, 0], [0, 0, 0], [5, 0, 0], [5, 5, 0]],
            [[0, 5, 5], [0, 0, 5], [0, 0, 0], [0, 5, 5]],
            [[5, 0, 0], [5, 5, 5], [0, 5, 0], [0, 0, 5]],
            [[0, 5, 0], [5, 0, 5], [5, 0, 5], [0, 5, 0]],
            [[5, 5, 5], [0, 0, 0], [0, 0, 0], [5, 5, 5]],
            [[0, 5, 0], [0, 5, 0], [0, 5, 0], [0, 5, 0]],
        ]
        algorithms = [
            "R_ U U R U R_ U R",
            "R U_ U_ R_ U_ R U_ R_",
            "L F R_ F_ L_ F R F_",
            "F_ L F R_ F_ L_ F R",
            "R R D_ R U_ U_ R_ D R U_ U_ R",
            "R U U R_ U_ R U R_ U_ R U_ R_",
            "R U_ U_ R_ R_ U_ R R U_ R_ R_ U U R",
            "F R U R_ U_ F_",
            "B U L U_ L_ B_",
            "B_ U_ R_ U R B",
            "R U R_ U_ R_ F R F_",
            "F R U R_ U_ R U R_ U_ F_",
            "F_ L_ U_ L U L_ U_ L U F",
            "B U L U_ L_ U L U_ L_ B_",
            "F R U R_ U_ F_ B U L U_ L_ B_",
            "B U L U_ L_ B_ U_ F R U R_ U_ F_",
            "B U L U_ L_ B_ U F R U R_ U_ F_",
            "R U_ U_ R_ R_ F R F_ U U R_ F R F_",
            "L_ B B R B R_ B L",
            "L F_ F_ R_ F_ R F_ L_",
            "L F R_ F R F F L_",
            "L_ B_ R B_ R_ B B L",
            "F R U_ R_ U_ R U R_ F_",
            "R U_ U_ R_ R_ F R F_ R U_ U_ R_",
            "R B_ R R F R R B R R F_ R",
            "R_ F R R B_ R R F_ R R B R_",
            "L_ B B R B R_ B_ R B R_ B L",
            "L F R_ F R F_ R_ F R F_ F_ L_",
            "R U R_ U R_ F R F_ U U R_ F R F_",
            "F R U R_ U F_ U U F_ L F L_",
            "R L_ B R B R_ B_ R_ L R_ F R F_",
            "R U R_ U_ R_ F R R U R_ U_ F_",
            "R U R_ U R_ F R F_ R U_ U_ R_",
            "L F R_ F_ L_ R U R U_ R_",
            "R U R_ U_ L R_ F R F_ L_",
            "R_ U_ R_ F R F_ U R",
            "R U R_ U_ B_ R_ F R F_ B",
            "R U R_ U R U_ R_ U_ R_ F R F_",
            "R_ U_ R U_ R_ U R U R B_ R_ B",
            "F R U R_ U_ F_ U F R U R_ U_ F_",
            "L F R_ F R_ D R D_ R F F L_",
            "R U B_ U_ R_ U R B R_",
            "R_ U_ F U R U_ R_ F_ R",
            "R_ F R U R_ U_ F_ U R",
            "L F_ L_ U_ L U F U_ L_",
            "R U R_ U R U U R_ F R U R_ U_ F_",
            "R_ U_ R U_ R_ U U R F R U R_ U_ F_",
            "L_ B B R B R_ B L R U U R_ U_ R U_ R_",
            "L F F R_ F_ R F_ L_ R_ U U R U R_ U R",
            "L F L_ R U R_ U_ L F_ L_",
            "R_ F_ R L_ U_ L U R_ F R",
            "R_ F R U R_ F_ R F U_ F_",
            "F U R U_ R_ R_ F_ R U R U_ R_",
            "R_ U_ R U_ R_ U F_ U F R",
            "L F L_ U R U_ R_ U R U_ R_ L F_ L_",
            "R_ F U R U_ R_ R_ F_ R R U R_ U_ R",
            "L_ R B R B R_ B_ L L R R F R F_ L_"
        ]
        algorithm = ""
        for i in range(len(patterns)):
            rr = self.oll_check_algorithm(patterns[i])
            if rr == -1:
                continue
            if rr == 1:
                algorithm += self.algo("y ")
            elif rr == 2:
                algorithm += self.algo("y y ")
            elif rr == 3:
                algorithm += self.algo("y_ ")
            algorithm += self.algo(algorithms[i])
            break
        return algorithm

    def cfop_pll(self):
        patterns = [
            [[0, 3, 0], [0, 1, 0], [0, 3, 0], [0, 0, 0]],
            [[0, 2, 0], [0, 2, 0], [0, 1, 0], [0, 0, 0]],
            [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[0, 3, 0], [0, 2, 0], [0, 2, 0], [0, 3, 0]],
            [[1, 0, 2], [2, 0, 2], [0, 0, 1], [2, 0, 0]],
            [[3, 0, 3], [3, 0, 1], [0, 0, 3], [1, 0, 0]],
            [[3, 0, 2], [2, 0, 3], [2, 0, 3], [3, 0, 2]],
            [[0, 0, 3], [3, 1, 2], [0, 1, 0], [2, 0, 0]],
            [[0, 3, 3], [3, 2, 2], [0, 0, 0], [2, 0, 0]],
            [[0, 0, 3], [3, 3, 2], [0, 0, 0], [2, 2, 0]],
            [[0, 0, 1], [1, 0, 0], [1, 2, 0], [0, 3, 1]],
            [[0, 1, 3], [3, 0, 2], [0, 0, 0], [2, 1, 0]],
            [[0, 0, 1], [1, 3, 0], [1, 0, 0], [0, 2, 1]],
            [[3, 0, 2], [2, 3, 0], [0, 0, 3], [0, 2, 0]],
            [[0, 3, 0], [0, 2, 3], [2, 0, 0], [3, 0, 2]],
            [[0, 0, 1], [1, 1, 0], [1, 1, 0], [0, 0, 1]],
            [[1, 0, 0], [0, 1, 1], [0, 1, 1], [1, 0, 0]],
            [[3, 2, 1], [1, 2, 0], [3, 1, 3], [0, 0, 3]],
            [[2, 1, 0], [0, 0, 1], [2, 3, 2], [1, 3, 2]],
            [[2, 0, 0], [0, 3, 1], [2, 1, 2], [1, 3, 2]],
            [[3, 2, 1], [1, 0, 0], [3, 2, 3], [0, 1, 3]]
        ]
        algorithms = [
            "R U_ R U R U R U_ R_ U_ R R",
            "R_ R_ U R U R_ U_ R_ U_ R_ U R_",
            "L L R R D L L R R U U L L R R D L L R R",
            "U R_ U_ R U_ R U R U_ R_ U R U R R U_ R_ U",
            "R R F F R_ B_ R F F R_ B R_",
            "R B_ R F F R_ B R F F R R",
            "R R U R_ U_ B U B_ U_ B U B_ U_ B U B_ R U_ R R",
            "R U R_ U_ R_ F R R U_ R_ U_ R U R_ F_",
            "R U R_ F_ R U R_ U_ R_ F R R U_ R_ U_",
            "R_ U U R U R_ U U L U_ R U L_",
            "F R U_ R_ U_ R U R_ F_ R U R_ U_ R_ F R F_",
            "R_ U_ F_ R U R_ U_ R_ F R R U_ R_ U_ R U R_ U R",
            "R_ U R_ U_ B_ R_ B B U_ B_ U B_ R B R",
            "R U_ U_ R_ U U R B_ R_ U_ R U R B R R U",
            "R_ U U R U_ U_ R_ F R U R_ U_ R_ F_ R R U_",
            "R_ U R U_ R_ F_ U_ F R U R_ U_ R U_ B U B_",
            "F_ R U R_ U_ R_ F R R F U_ R_ U_ R U F_ R_",
            "R R D_ F U_ F U F_ D R R B U_ B_",
            "R U R_ F F D_ L U_ L_ U L_ D F F",
            "R R D B_ U B_ U_ B D_ R R F_ U F",
            "R_ U_ R B B D L_ U L U_ L D_ B B"
        ]
        algorithm = ""
        for i in range(len(patterns)):
            rr = self.pll_check_algorithm(patterns[i])
            if rr == -1:
                continue
            if rr == 1:
                algorithm += self.algo("y ")
            if rr == 2:
                algorithm += self.algo("y y ")
            if rr == 3:
                algorithm += self.algo("y_ ")
            algorithm += self.algo(algorithms[i])
            algorithm += " "
            break
        if self.cube[1][0][1] != self.cube[1][1][1]:
            if self.cube[2][0][1] == self.cube[1][1][1]:
                algorithm += self.algo("U")
            elif self.cube[3][0][1] == self.cube[1][1][1]:
                algorithm += self.algo("U_")
            elif self.cube[4][0][1] == self.cube[1][1][1]:
                algorithm += self.algo("U U")
        return algorithm.rstrip()

    def full_cfop(self):
        full_algorithm = []
        if self.cross_done() == False:
            full_algorithm.append(self.cfop_cross())
        if self.f2l_done() == False:
            full_algorithm.append(self.cfop_f2l())
        if self.oll_done() == False:
            full_algorithm.append(self.cfop_oll())
        if self.cfop_done() == False:
            full_algorithm.append(self.cfop_pll())
        return full_algorithm

# some auxiliary functions for the cfop method
    def f2l_edge_pos(self):
        edges = [0, 0, 0, 0, 0, 0, 0, 0]
        a = [[5, 1, 0], [5, 0, 1], [5, 1, 2], [5, 2, 1],
             [1, 1, 0], [4, 1, 2], [4, 1, 0], [1, 1, 2]]
        b = [[3, 0, 1], [4, 0, 1], [2, 0, 1], [1, 0, 1],
             [3, 1, 2], [3, 1, 0], [2, 1, 2], [2, 1, 0]]
        for i in range(8):
            for j in range(1, 3):
                if self.cube[a[i][0]][a[i][1]][a[i][2]] == self.cube[j][1][1]:
                    edges[i] = edges[i] + 1
                if self.cube[b[i][0]][b[i][1]][b[i][2]] == self.cube[j][1][1]:
                    edges[i] = edges[i] + 1
        for i in range(8):
            if edges[i] == 2:
                return i + 1

    def f2l_corner_pos(self):
        corners = [0, 0, 0, 0, 0, 0, 0, 0]
        a = [[5, 2, 0], [5, 0, 0], [5, 0, 2], [5, 2, 2],
             [0, 2, 0], [0, 0, 0], [0, 0, 2], [0, 2, 2]]
        b = [[1, 0, 0], [3, 0, 0], [4, 0, 0], [2, 0, 0],
             [1, 2, 0], [3, 2, 0], [4, 2, 0], [2, 2, 0]]
        c = [[3, 0, 2], [4, 0, 2], [2, 0, 2], [1, 0, 2],
             [3, 2, 2], [4, 2, 2], [2, 2, 2], [1, 2, 2]]
        for i in range(8):
            for j in range(3):
                if self.cube[a[i][0]][a[i][1]][a[i][2]] == self.cube[j][1][1]:
                    corners[i] = corners[i] + 1
                if self.cube[b[i][0]][b[i][1]][b[i][2]] == self.cube[j][1][1]:
                    corners[i] = corners[i] + 1
                if self.cube[c[i][0]][c[i][1]][c[i][2]] == self.cube[j][1][1]:
                    corners[i] = corners[i] + 1
        for i in range(8):
            if corners[i] == 3:
                return i + 1

    def f2l_one_out_of_four(self):
        finished = 0
        edge = self.f2l_edge_pos()
        edge_algs = ["", "U_ F R_ F_ R", "U R_ F R F_", "R_ F R F_",
                     "F R_ F_ R", "L_ U_ L F R_ F_ R",
                     "L U_ L_ F R_ F_ R", "R_ U R F R_ F_ R", ""]
        algorithm = self.algo(edge_algs[edge]) + " "
        corner = self.f2l_corner_pos()
        corner_algs = ["", "", "U_", "U U", "U",
                       "L_ U_ L U", "L U_ L_ U_", "B U U B_"]
        if corner == 8:
            if self.cube[1][1][2] == self.cube[1][1][1] and self.cube[0][2][2] == 0:
                finished = 1
            else:
                algorithm = algorithm + self.algo("R U R_ F R_ F_ R U U") + " "
        else:
            algorithm = algorithm + self.algo(corner_algs[corner]) + " "
        if finished == 1:
            return algorithm
        if self.cube[1][1][2] == self.cube[1][1][1]:
            if self.cube[5][2][0] == self.cube[0][1][1]:
                algorithm = algorithm + \
                    self.algo("U_ R U R_ U_ R U R_ U_ R U R_ U_") + " "
            elif self.cube[5][2][0] == self.cube[2][1][1]:
                algorithm = algorithm + self.algo("F_ U F U_ F R_ F_ R") + " "
            else:
                algorithm = algorithm + \
                    self.algo("U U R U_ R_ U U R U_ R_") + " "
        else:
            if self.cube[5][2][0] == self.cube[0][1][1]:
                algorithm = algorithm + self.algo("U_ R U_ R_ U F_ U F") + " "
            elif self.cube[5][2][0] == self.cube[2][1][1]:
                algorithm = algorithm + self.algo("F_ U_ F U_ R U R_") + " "
            else:
                algorithm = algorithm + self.algo("U U R U R_ U F_ U_ F") + " "
        return algorithm.lstrip()

    def oll_check_algorithm(self, v):
        rotations = 0
        for i in range(4):
            correct = 1
            for j in range(1, 5):
                for k in range(3):
                    if (self.cube[j][0][k] == 5) != (v[j-1][k] == 5):
                        correct = 0
                        break
            if correct == 1:
                return rotations
            t = v[0]
            v[0] = v[2]
            v[2] = v[3]
            v[3] = v[1]
            v[1] = t
            rotations += 1
        return -1

    def pll_check_algorithm(self, v):
        turns = -1
        left_side = [0, 3, 1, 4, 2]
        temp = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(4):
            for j in range(4):
                for k in range(1, 5):
                    for l in range(3):
                        if self.cube[k][0][l] == self.cube[k][1][1]:
                            temp[k-1][l] = 0
                        elif self.cube[k][0][l] == self.cube[5-k][1][1]:
                            temp[k-1][l] = 1
                        elif self.cube[k][0][l] == self.cube[left_side[k]][1][1]:
                            temp[k-1][l] = 2
                        else:
                            temp[k-1][l] = 3
                flag = 1
                for k in range(4):
                    for l in range(3):
                        if v[k][l] != temp[k][l]:
                            flag = 0
                if flag == 1:
                    turns = i+j
                self.rotate_right()
            self.U(1)
        if turns == -1:
            return -1
        return turns % 4

# the following 15 functions (from R to rotate_around) are the
# basic movements that can be done on a cube.

    def R(self, times):
        times = times % 4
        for j in range(times):
            for i in range(3):
                t = self.cube[0][2-i][2]
                self.cube[0][2-i][2] = self.cube[4][2-i][0]
                self.cube[4][2-i][0] = self.cube[5][i][2]
                self.cube[5][i][2] = self.cube[1][i][2]
                self.cube[1][i][2] = t
            self.surface_clockwise(2)

    def R_(self, times):
        times = times % 4
        self.R(4-times)

    def L(self, times):
        self.rotate_around()
        self.R(1)
        self.rotate_around()

    def L_(self, times):
        self.rotate_around()
        self.R_(1)
        self.rotate_around()

    def U(self, times):
        times = times % 4
        for j in range(times):
            for i in range(3):
                t = self.cube[1][0][i]
                self.cube[1][0][i] = self.cube[2][0][i]
                self.cube[2][0][i] = self.cube[4][0][i]
                self.cube[4][0][i] = self.cube[3][0][i]
                self.cube[3][0][i] = t
            self.surface_clockwise(5)

    def U_(self, times):
        times = times % 4
        self.U(4-times)

    def D(self, times):
        times = times % 4
        self.D_(4-times)

    def D_(self, times):
        times = times % 4
        for j in range(times):
            for i in range(3):
                t = self.cube[1][2][i]
                self.cube[1][2][i] = self.cube[2][2][i]
                self.cube[2][2][i] = self.cube[4][2][i]
                self.cube[4][2][i] = self.cube[3][2][i]
                self.cube[3][2][i] = t
            self.surface_clockwise(0)

    def F(self, times):
        self.rotate_left()
        self.R(1)
        self.rotate_right()

    def F_(self, times):
        self.rotate_left()
        self.R_(1)
        self.rotate_right()

    def B(self, times):
        self.rotate_right()
        self.R(1)
        self.rotate_left()

    def B_(self, times):
        self.rotate_right()
        self.R_(1)
        self.rotate_left()

    def rotate_left(self):
        temp = self.cube[1]
        self.cube[1] = self.cube[3]
        self.cube[3] = self.cube[4]
        self.cube[4] = self.cube[2]
        self.cube[2] = temp
        self.surface_anticlockwise(5)
        self.surface_anticlockwise(0)

    def rotate_right(self):
        for i in range(0, 3):
            self.rotate_left()

    def rotate_around(self):
        self.rotate_left()
        self.rotate_left()

# the above 15 functions are the basic movements of the cube.

    def surface_clockwise(self, side):
        # auxiliary function
        t = self.cube[side][0][0]
        self.cube[side][0][0] = self.cube[side][2][0]
        self.cube[side][2][0] = self.cube[side][2][2]
        self.cube[side][2][2] = self.cube[side][0][2]
        self.cube[side][0][2] = t
        t = self.cube[side][0][1]
        self.cube[side][0][1] = self.cube[side][1][0]
        self.cube[side][1][0] = self.cube[side][2][1]
        self.cube[side][2][1] = self.cube[side][1][2]
        self.cube[side][1][2] = t

    def surface_anticlockwise(self, side):
        # auxiliary function
        for i in range(3):
            self.surface_clockwise(side)

    def algo(self, algorithm):
        """
        perform the designated algorithm to the cube
        and returning it as a string at the same time
        """
        steps = algorithm.split()
        for step in steps:
            if step == "R":
                self.R(1)
            if step == "R_":
                self.R_(1)
            if step == "L":
                self.L(1)
            if step == "L_":
                self.L_(1)
            if step == "U":
                self.U(1)
            if step == "U_":
                self.U_(1)
            if step == "D":
                self.D(1)
            if step == "D_":
                self.D_(1)
            if step == "F":
                self.F(1)
            if step == "F_":
                self.F_(1)
            if step == "B":
                self.B(1)
            if step == "B_":
                self.B_(1)
            if step == "y":
                self.rotate_right()
            if step == "y_":
                self.rotate_left()
            if step == "y2":
                self.rotate_around()
        return algorithm
