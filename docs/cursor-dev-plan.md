# Varygen: Lords of Resolution (V:LoR)
## Cursor-Optimized Development Plan

### Development Environment Setup

```python
# requirements.txt
pygame==2.5.0
python-socketio==5.8.0
fastapi==0.100.0
sqlalchemy==2.0.0
pytest==7.4.0
black==23.3.0
python-dotenv==1.0.0
pydantic==2.0.0
```

### Project Structure
```
vlor/
├── src/
│   ├── client/
│   │   ├── game.py
│   │   ├── player.py
│   │   └── ui/
│   ├── server/
│   │   ├── app.py
│   │   └── game_state.py
│   └── shared/
│       └── constants.py
├── assets/
│   ├── sprites/
│   ├── maps/
│   └── sounds/
├── tests/
├── requirements.txt
└── README.md
```

### Development Phases

#### Phase 1: Core Game Engine (Week 1)
- Basic Pygame setup
- Player movement
- Sprite rendering
- Collision detection
- Camera system

#### Phase 2: Multiplayer (Week 2)
- FastAPI server setup
- Socket.IO integration
- Room management
- Player synchronization
- Chat system

#### Phase 3: Business Systems (Week 3)
- Business class implementation
- Resource management
- Trading system
- Inventory system
- Currency mechanics

#### Phase 4: Conflict Resolution (Week 4)
- Mediator system
- Conflict mechanics
- Resolution interface
- Payment tracking
- Reputation system

#### Phase 5: Mafia Mechanics (Week 5)
- Role assignment
- Hidden information
- Enforcement system
- Collection mechanics
- Pursuit system

#### Phase 6: Polish (Week 6)
- Sound effects
- Particle effects
- Tutorial system
- Achievements
- Testing

### Cursor AI Development Guidelines

1. **Code Generation**
   - Use AI for boilerplate code
   - Let AI suggest implementations
   - Review and modify AI suggestions
   - Test thoroughly

2. **Documentation**
   ```python
   class Player:
       """A player in the game world.
       
       Attributes:
           position (Vector2): Current position
           role (Role): Current role
           inventory (Inventory): Player's inventory
       """
       def __init__(self, player_id: str, name: str):
           self.id = player_id
           self.name = name
           self.position = pygame.math.Vector2(0, 0)
   ```

3. **Testing Strategy**
   ```python
   def test_player_movement():
       """Test player movement mechanics."""
       player = Player("test_id", "Test Player")
       initial_pos = player.position.copy()
       player.move(Direction.RIGHT)
       assert player.position.x > initial_pos.x
   ```

### Development Workflow

1. **Planning**
   - Review requirements
   - Break down tasks
   - Set daily goals

2. **Implementation**
   - Write tests first
   - Use Cursor AI for code generation
   - Regular commits
   - Document as you go

3. **Review**
   - Run tests
   - Code quality checks
   - Performance testing
   - Update documentation

### Using Cursor AI Effectively

1. **Code Generation**
   - Provide clear requirements
   - Review generated code
   - Test thoroughly
   - Document changes

2. **Problem Solving**
   - Describe issues clearly
   - Use AI for debugging
   - Validate solutions
   - Document fixes

3. **Documentation**
   - Generate docstrings
   - Update README
   - Create examples
   - Maintain dev log

### Daily Development Log Template

```markdown
# Development Log

## [Date]

### Completed Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Challenges
- Challenge 1: Solution
- Challenge 2: Solution

### Next Steps
- [ ] Next task 1
- [ ] Next task 2
```

### Getting Started

1. Clone repository and setup:
```bash
git clone [repository-url]
cd vlor
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run initial setup:
```bash
python src/setup.py
```

3. Start development server:
```bash
python src/server/app.py
```

4. Run client:
```bash
python src/client/game.py
``` 