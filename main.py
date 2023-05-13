import copy


def getMRV(grid, domains):
    """
    Get the index of the cell with the minimum remaining values (MRV)
    """
    mrvList = []
    mrvIndex = (-1, -1)
    blankMin = float('inf')
    for i in range(5):
        row = []
        for j in range(5):
            if grid[i][j] == "-":
                # count the number of empty cells around the current cell
                blanks = 0
                if i < 4 and grid[i + 1][j] == "-":
                    blanks += 1
                if j < 4 and grid[i][j + 1] == "-":
                    blanks += 1
                if i > 0 and grid[i - 1][j] == "-":
                    blanks += 1
                if j > 0 and grid[i][j - 1] == "-":
                    blanks += 1
                # if the current cell has fewer remaining values than the previous minimum, update the MRV
                if blanks < blankMin:
                    blankMin = blanks
                    mrvIndex = (i, j)
                row.append(blanks)
                if blankMin == float('inf'):
                    blankMin = 100
        mrvList.append(row)
    return mrvIndex, blankMin


def findDomain(alphabets, constraintsMatrix, grid):
    """
    Find the domain of each cell based on the current state of the grid and the constraints
    """
    domains = {}
    for i in range(5):
        for j in range(5):
            domain = getDomain(i, j, grid, constraintsMatrix, alphabets)
            domains[(i, j)] = domain
    return domains, alphabets


def getDomain(i, j, grid, constraintsMatrix, alphabetsRemaining):
    """
    Find the domain of the cell at index (i, j) based on the current state of the grid and the constraints
    """
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y']
    domain = []
    neighbours = []
    adjacentAlphabet = False
    constraintDomain = []
    for constraints in constraintsMatrix[i][j]:
        if grid[constraints[0]][constraints[1]] != "-":
            adjacentAlphabet = True
            neighbours.append(grid[constraints[0]][constraints[1]])

    if adjacentAlphabet:
        for neighbour in neighbours:
            index = alphabets.index(neighbour)
            if index < 24 and (alphabets[index + 1] in alphabetsRemaining):
                domain.append(alphabets[index + 1])
            if index > 0 and (alphabets[index - 1] in alphabetsRemaining):
                domain.append(alphabets[index - 1])
    else:
        domain.append(alphabetsRemaining)
    return domain


def getLCV(i, j, grid, constraintMatrix, domains, alphabetsRemaining):
    """
    For the selected cell by MRV, LCV finds the order of the domain of the cell
    which will give the least constraint to neighbouring cells
    """
    gridCopy = copy.deepcopy(grid)
    domain = domains[(i, j)]
    value = []
    if grid[i][j] == "-" and len(domain) >= 1:
        for d in domain:
            gridCopy[i][j] = d
            tempValue = []
            for constraint in constraintMatrix[i][j]:
                newDomain = getDomain(constraint[0], constraint[1], gridCopy, constraintMatrix,
                                      alphabetsRemaining)
                tempValue.append(len(newDomain))
            value.append((d, min(tempValue)))
        value.sort(key=lambda k: k[1], reverse=True)
        return [t[0] for t in value]
    return False


def backtrack(grid, constraintMatrix, domains, alphabetsRemaining):
    # find the cell with the minimum remaining values
    index, min_values = getMRV(grid, domains)
    # if there are no empty cells, we're done
    if min_values == float('inf'):
        return True
    # try each possible value for the cell with the minimum remaining values, in LCV order
    possible_values = getLCV(index[0], index[1], grid, constraintMatrix, domains, alphabetsRemaining)
    if not possible_values:
        return False
    for value in possible_values:
        # For each possible value, the grid is updated, the alphabetsRemaining list is updated by removing the
        # selected value, and the domains are updated by calling the findDomain() function.
        grid[index[0]][index[1]] = value
        alphabetsRemainingCopy = copy.deepcopy(alphabetsRemaining)
        alphabetsRemainingCopy.remove(value)
        # update domains of all cells
        domains, alphabetsRemainingCopy = findDomain(alphabetsRemainingCopy, constraintMatrix, grid)
        # try to fill out the rest of the grid
        if backtrack(grid, constraintMatrix, domains, alphabetsRemainingCopy):
            return grid
        # if we couldn't fill out the rest of the grid, backtrack
        grid[index[0]][index[1]] = '-'
    return False


def main():
    # initialize grid and Alphabets
    grid = [['-', '-', '-', '-', 'Y'],
            ['R', 'A', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', 'E', '-', '-', '-'],
            ['-', '-', '-', '-', 'K']]

    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y']
    # find adjacency constraints for each cell
    constraintsList = []
    for i in range(5):
        for j in range(5):
            if grid[i][j] != "-":
                alphabets.remove(grid[i][j])
            constraints = []
            if i < 4:
                constraints.append([i + 1, j])
            if j < 4:
                constraints.append([i, j + 1])
            if i > 0:
                constraints.append([i - 1, j])
            if j > 0:
                constraints.append([i, j - 1])
            constraintsList.append(constraints)
    # Store these constraints as 5x5 matrix for ease of use
    constraintsMatrix = []
    for i in range(0, len(constraintsList), 5):
        constraintsMatrix.append(constraintsList[i:i + 5])
    domains, alphabets = findDomain(alphabets, constraintsMatrix, grid)
    # Start search
    result = backtrack(grid, constraintsMatrix, domains, alphabets)
    if result:
        for row in result:
            print(row)
    else:
        print("No solution found")


if __name__ == '__main__':
    main()
