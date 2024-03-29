Maybe the true Christmas was the bugs we found along the way?

![alt text](https://github.com/alexeygorskiy/AdventOfCode/blob/main/anim_export/animation.gif)

# Useful Things to Remember
- When using RegEx, don't forget to escape special characters  
- Sets are useful for finding intersections/overlaps as well as subsets  
- Python [start : end : stop] list notation  
- Memoization: cache results of expensive operations  
- Use primitive solutions to test advanced solutions  
- Code snippets for efficient copy-pasting  
- A number can be stored compactly if you modulo it by the least common multiple (lcm) of all the division operators that will be performed on it  
- For path finding it does not matter if you travel from start to goal or from goal to start   
- not None in Python evaluates to True  
- Print statements slow down execution by a lot  
- python -m cProfile -o program.prof main.py  
- snakeviz program.prof  
- Function caching is especially effective with recursive functions  
- In state space searches good heurestics are key to speeding up the search  
- BFS usually requires more memory than DFS  

# AoC Specific
- Read instructions VERY carefully and double check the code against the instructions VERY carefully. Don't try to simplify prematurely: if it asks to convert it to a list, then do that. Optimization can come later  
- Beware of indices (start on 0 vs 1)  
- Raise exceptions in all else cases just in case you forgot to handle it  
