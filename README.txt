Chess Agent: Minimax with Alpha-Beta Pruning & Scout
Omeed Fallahi and Paul Miller-Schmidt
-----------------------------------------------------------------------------------------------------
Summary of Project

For our final project, we created a chess agent that plays the game using two main algorithms:
the minimax algorithm with alpha-beta pruning and scout (principal variation search). 

The game itself is modeled using the python-chess library, which provides a lot of functionality 
such as determining possible (legal) moves, simulating a board, making moves on the board, keeping
track of piece position, and more. This library was very helpful in allowing us to keep our main focus
on implementing the algorithms for the agent.

For the algorithms, we implemented the minimax algorithm with alpha-beta pruning and scout, which both 
search to a depth of 4. For both of these agents, the depth increases as it gets closer to end game positions,
as the branching factor shrinks. While both of these algorithms rely primarily on minimax, the scout agent is able 
to make moves much faster than the minimax agent by 1) ordering moves prior to search using a simple material 
heuristic and 2) never examining a node that can be pruned using alpha-beta. We also created two additional 
basic agents (random and greedy) which we used to test our alpha-beta and scout agents against as well.
-----------------------------------------------------------------------------------------------------
Running and Testing the Program

First, it is necessary to install a couple packages that our program relies on. To do this, run the following 
command from the project directory which installs the packages listed in the requirements.txt file.

    pip install -r requirements.txt

Next, you can run the program using the following command:

    python3 main.py --P1 {player1_agent} --P2 {player2_agent} --games {int} [--viz]

For example, to have the scout agent play against the greedy against for a total of 5 games, enter the command:
    
    python3 main.py --P1 scout --P2 greedy --games 5

The choices for player agents are: minimax, scout, greedy, and random.

The optional --viz parameter launches a visualization of the board and shows moves as they are being made. This
is nice to use if you would like to watch the agents play against each other, observing the moves they make. An
example of a visualized game would use the following command:

    python3 main.py --P1 scout --P2 greedy --games 5 --viz

It is important to note that, in all cases, P1 is the maximizing player and controls the white pieces while P2
is the minimizing player and controls the black pieces.
-----------------------------------------------------------------------------------------------------
Results and Evaluation

Here are some results from running the program against itself using various combinations of matchups, 
such as minimax v. random, minimax v. greedy, scout v. random, scout v. greedy, and scout v. minimax
across hundreds of games.

    Minimax v. Random, 250 games (python3 main.py --P1 minimax --P2 random --games 250)
    Player 1 wins: 250
    Player 2 wins: 0
    Draws / stalemates: 0
    Completed in 2471.94 seconds
    -> Player 1 (minimax) has a win rate of 100%

    Minimax v. Greedy, 250 games (python3 main.py --P1 minimax --P2 greedy --games 250)
    Player 1 wins: 250
    Player 2 wins: 0
    Draws / stalemates: 0
    Completed in 2918.05 seconds
    -> Player 1 (minimax) has a win rate of 100%

    Scout v. Random, 250 games (python3 main.py --P1 scout --P2 random --games 250)
    Player 1 wins: 249
    Player 2 wins: 0
    Draws / stalemates: 1
    Completed in 617.31 seconds
    -> Player 1 (scout) has a win rate of 99.6%

    Scout v. Greedy, 250 games (python3 main.py --P1 scout --P2 greedy --games 250)
    Player 1 wins: 248
    Player 2 wins: 0
    Draws / stalemates: 2
    Completed in 1542.87 seconds
    -> Player 1 (scout) has a win rate of 99.2%

    Scout v. Minimax, 10 games (python3 main.py --P1 scout --P2 minimax --games 10)
    Player 1 wins: 6
    Player 2 wins: 2
    Draws / stalemates: 2
    Completed in 962.95 seconds
    -> Player 1 (scout) has a 60% win rate

    Scout v. Minimax, 20 games (python3 main.py --P1 scout --P2 minimax --games 20)
    Player 1 wins: 11
    Player 2 wins: 8
    Draws / stalemates: 1
    Completed in 1638.62 seconds
    -> Player 1 (scout) has a 55% win rate

    Scout v. Minimax, 100 games (python3 main.py --P1 scout --P2 minimax --games 100)
    Player 1 wins: 41
    Player 2 wins: 44
    Draws / stalemates: 15
    Completed in 11966.73 seconds
    -> Player 1 (scout) has a 41% win rate

The results and evaluation were encouraging in that it highlighted the advantage that scout
has over minimax with alpha-beta pruning with regard to time efficiency. While both minimax
and scout have nearly the same win rate against the random and greedy agents, scout is able
to complete the games much faster than minimax. This was expected, so it was nice to see it
reflected in our results.

When scout and minimax play against each other, they hover around having even win rates over
a large number of games. This makes sense because they employ the same heuristic function,
rely on the minimax algorithm to decide on moves to take, and search the game tree to the
same depth (4, plus equal increases based on remaining pieces on the board). 

Overall, we are satisfied with the results of the agents and had a fun time implementing them!
