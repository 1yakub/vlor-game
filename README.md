# Varygen: Lords of Resolution (V:LoR)

A multiplayer business simulation and social deduction game where players navigate corporate politics, resolve conflicts, and manage hidden agendas within the prestigious Varygen Corporation.

## Features

- 🎮 Real-time multiplayer gameplay
- 💼 Business simulation mechanics
- 🤝 Conflict resolution system
- 🕵️ Hidden role mechanics (Mafia system)
- 💰 Dynamic economy system
- 🏢 Virtual office environment

## Tech Stack

- Python 3.8+
- Pygame (Game engine)
- FastAPI (Server)
- Socket.IO (Real-time communication)
- SQLAlchemy (Database ORM)
- Pytest (Testing)

## Development Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd vlor-game
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python src/server/app.py
```

5. In a new terminal, run the client:
```bash
python src/client/game.py
```

## Project Structure

```
vlor/
├── src/
│   ├── client/         # Client-side game code
│   │   ├── ui/         # User interface components
│   │   ├── game.py     # Main game loop
│   │   └── player.py   # Player entity
│   ├── server/         # Server-side code
│   │   ├── game_logic/ # Game mechanics
│   │   ├── networking/ # Socket.IO handling
│   │   └── database/   # Data models
│   └── shared/         # Shared utilities
├── assets/             # Game resources
│   ├── sprites/        # Character sprites
│   ├── maps/          # Level layouts
│   └── sounds/        # Audio files
├── tests/             # Test suites
├── docs/              # Documentation
└── requirements.txt   # Dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Game design inspired by social deduction games
- Built with Python and Pygame
- Developed using Cursor IDE
