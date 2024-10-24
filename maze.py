import random

def generate_maze(width=10, height=10):
    """
    Generates a random, solvable maze using a depth-first search algorithm.

    Args:
        width (int): Width of the maze.
        height (int): Height of the maze.

    Returns:
        list: A 2D list representing the generated maze, where 1 represents walls and 0 represents paths.
    """
    # Initialize the maze with walls (1)
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Start from the top-left corner (1, 1)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    # Stack for Depth-First Search (DFS)
    stack = [(start_x, start_y)]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Move by two cells to create passages

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)  # Randomize directions each time to create a different maze

        found = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if the new cell is within bounds and is a wall
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                # Make the path between cells
                maze[ny][nx] = 0
                maze[y + dy // 2][x + dx // 2] = 0  # Carve the connecting path
                stack.append((nx, ny))
                found = True
                break

        if not found:
            # No unvisited neighbors, backtrack
            stack.pop()

    # Ensure the start and goal positions are open and reachable
    goal_x, goal_y = height - 2, width - 2
    if maze[goal_y][goal_x] == 1:
        # 如果终点位置是墙，扩展搜索直到找到一个可走路径
        found_goal = False
        search_radius = 1
        while not found_goal:
            for dy in range(-search_radius, search_radius + 1):
                for dx in range(-search_radius, search_radius + 1):
                    ny, nx = goal_y + dy, goal_x + dx
                    if 0 <= ny < height and 0 <= nx < width and maze[ny][nx] == 0:
                        goal_y, goal_x = ny, nx
                        found_goal = True
                        break
            if found_goal:
                break
            search_radius += 1

    maze[goal_y][goal_x] = 0

    return maze, (goal_x, goal_y)

def save_maze_to_file(maze, filepath):
    """
    Saves the generated maze to a text file.

    Args:
        maze (list): The 2D list representing the maze.
        filepath (str): The file path where the maze should be saved.
    """
    with open(filepath, "w") as file:
        for row in maze:
            file.write(" ".join(str(cell) for cell in row) + "\n")

def load_maze_from_file(filepath):
    """
    Loads a maze from a text file.

    Args:
        filepath (str): The file path of the maze to load.

    Returns:
        list: A 2D list representing the loaded maze.
    """
    maze = []
    with open(filepath, "r") as file:
        for line in file:
            try:
                row = [int(char) for char in line.strip().split() if char.isdigit()]
                maze.append(row)
            except ValueError:
                print(f"Error reading line: {line}")
    return maze

def print_maze(maze):
    """
    Prints the maze to the console for debugging purposes.

    Args:
        maze (list): The 2D list representing the maze.
    """
    for row in maze:
        print("".join(str(cell) for cell in row))

if __name__ == "__main__":
    # Generate a random maze
    generated_maze = generate_maze(width=10, height=10)
    
    # Print the generated maze for debugging
    print("Generated Maze:")
    print_maze(generated_maze)

    # Save the maze to a file
    save_maze_to_file(generated_maze, "maps/random_level.txt")

    # Load the maze from the file
    loaded_maze = load_maze_from_file("maps/random_level.txt")
    
    # Print the loaded maze for verification
    print("\nLoaded Maze:")
    print_maze(loaded_maze)
