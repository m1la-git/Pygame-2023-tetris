# Tetris Game

This is a simple Tetris game implemented in Python using the Pygame library.

## Features

*   **Classic Tetris Gameplay:**  Experience the familiar and addictive gameplay of Tetris.
*   **Seven Tetromino Shapes:** Includes all the standard Tetris pieces (I, J, L, O, S, T, Z).
*   **Random Piece Generation:**  Pieces are generated randomly, providing a unique gameplay experience each time.
*   **Scoring System:** Earn points for clearing rows.
*   **High Score Tracking:**  The game keeps track of your best score.
*   **Level Progression:** The game speed increases gradually as you play.
*   **Next Shape Preview:**  See the upcoming piece to plan your moves.
*   **Sound Effects:** Includes background music and a sound effect for dropping pieces.
*   **Restart Button:** Easily restart the game when it's over.
*   **Simple Graphics:**  Clean and clear visual representation of the game board and pieces.

## How to Play

1. **Run the game:** Execute the Python script.
2. **Move pieces:** Use the left and right arrow keys to move the falling piece horizontally.
3. **Rotate pieces:** Use the up arrow key to rotate the falling piece.
4. **Drop pieces faster:** Use the down arrow key to make the piece fall faster.
5. **Clear rows:**  Fill a complete row with blocks to clear it and earn points.
6. **Game Over:** The game ends when pieces stack up to the top of the play area.
7. **Restart:** Click the "Restart" button to start a new game after a game over.

## Dependencies

Before running the game, make sure you have the following libraries installed:

*   **Pygame:** This library is used for the game's graphics, sound, and input handling.

    You can install Pygame using pip:

    ```bash
    pip install pygame
    ```

## How to Run the Game

1. **Save the code:** Save the provided Python code as a `.py` file (e.g., `tetris.py`).
2. **Ensure resources are present:** Make sure you have the `images` and `sounds` folders in the same directory as your Python script, containing the following files:
    *   `images/bg.jpeg`
    *   `images/restart.png`
    *   `sounds/bg.mp3`
    *   `sounds/drop.mp3`
    *   `fonts/arcade.ttf`
    *   `fonts/flower.ttf`
3. **Run the script:** Open a terminal or command prompt, navigate to the directory where you saved the file, and run the script using Python:

    ```bash
    python tetris.py
    ```

## Game Controls

*   **Left Arrow Key:** Move piece left
*   **Right Arrow Key:** Move piece right
*   **Up Arrow Key:** Rotate piece
*   **Down Arrow Key:** Drop piece faster

## Potential Issues

*   **Missing Resources:** The game relies on image and sound files in the `images` and `sounds` folders, as well as font files in the `fonts` folder. Ensure these are present in the correct locations.
*   **Performance:** On very old or low-powered systems, the game might experience slight performance issues, although it is generally lightweight.
*   **Screen Resolution:** The game window has a fixed size. It might not scale perfectly to all screen resolutions.

## Credits

This game was developed as a personal project. It utilizes the Pygame library, which is developed and maintained by the Pygame community.

## License

This project is open-source and available under the [MIT License](LICENSE.txt). (You may want to create a `LICENSE.txt` file if you choose to use a specific license).

Enjoy playing Tetris!
