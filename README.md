# Project-F
By: andysit1, swatkinson, [luca], kevinscix

**--- Project Structure ---**

src/
    components/
        attack.py        - Handles Player Attacks
        camera.py        - Handles Pygame Camera
        player.py        - Handles Player Class (Movement)
        enemy.py         - Handles Enemy Class (Movement, Health)

    modules/
        state_machine.py - Handles the states of the game (idk how it works lmfao it was copy/pasted)

    state/
        gameState.py     - Handles everything happening on the game screen itself
        menuState.py     - (doesnt exist) Handles everything happening on the menu screen

    main.py              - Initializes pygame and game window, starts game loop

