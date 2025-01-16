"""Tilemap module.

This module handles the office environment's tile-based map system.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import pygame

from shared.constants import (
    TILE_SIZE,
    MAP_WIDTH,
    MAP_HEIGHT,
    COLOR_WHITE,
    COLOR_BLACK,
    COLOR_GRAY
)
from shared.logger import get_logger

logger = get_logger(__name__)

class TileType(Enum):
    """Types of tiles in the office environment."""
    FLOOR = auto()
    WALL = auto()
    DOOR = auto()
    DESK = auto()
    CHAIR = auto()
    PLANT = auto()
    WINDOW = auto()
    CABINET = auto()
    MEETING_TABLE = auto()
    WATER_COOLER = auto()

@dataclass
class Room:
    """Room in the office environment."""
    name: str
    x: int
    y: int
    width: int
    height: int
    room_type: str

class Tile:
    """Single tile in the map."""
    
    def __init__(self, type: TileType, position: Tuple[int, int]):
        """Initialize a tile.
        
        Args:
            type: Type of tile
            position: Grid position (x, y)
        """
        self.type = type
        self.position = position
        self.sprite: Optional[pygame.Surface] = None
        self.is_collidable = type in {TileType.WALL, TileType.DESK, TileType.MEETING_TABLE, TileType.CABINET}
        
        # Create default colored rectangle
        self.sprite = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self._set_default_color()
    
    def _set_default_color(self) -> None:
        """Set the default color based on tile type."""
        if self.type == TileType.FLOOR:
            self.sprite.fill((240, 240, 240))  # Light gray
        elif self.type == TileType.WALL:
            self.sprite.fill((100, 100, 100))  # Dark gray
        elif self.type == TileType.DOOR:
            self.sprite.fill((150, 75, 0))  # Brown
        elif self.type == TileType.DESK:
            self.sprite.fill((160, 110, 60))  # Light brown
        elif self.type == TileType.CHAIR:
            self.sprite.fill((80, 80, 80))  # Dark gray
        elif self.type == TileType.PLANT:
            self.sprite.fill((0, 150, 0))  # Green
        elif self.type == TileType.WINDOW:
            self.sprite.fill((200, 230, 255))  # Light blue
        elif self.type == TileType.CABINET:
            self.sprite.fill((120, 80, 40))  # Dark brown
        elif self.type == TileType.MEETING_TABLE:
            self.sprite.fill((180, 130, 80))  # Medium brown
        elif self.type == TileType.WATER_COOLER:
            self.sprite.fill((0, 150, 200))  # Blue
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the tile.
        
        Args:
            screen: Surface to draw on
            camera_offset: Camera offset (x, y)
        """
        if self.sprite:
            x = self.position[0] * TILE_SIZE - camera_offset[0]
            y = self.position[1] * TILE_SIZE - camera_offset[1]
            screen.blit(self.sprite, (x, y))

class TileMap:
    """Map of tiles representing the office environment."""
    
    def __init__(self, width: int = MAP_WIDTH, height: int = MAP_HEIGHT):
        """Initialize the tilemap.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles: List[List[Optional[Tile]]] = [[None] * height for _ in range(width)]
        self.rooms: List[Room] = []
        
        logger.info(f"Created tilemap: {width}x{height} tiles")
    
    def set_tile(self, x: int, y: int, type: TileType) -> None:
        """Set a tile at the given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            type: Tile type
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[x][y] = Tile(type, (x, y))
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get the tile at the given position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        
        Returns:
            Tile at position or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return None
    
    def add_room(self, name: str, x: int, y: int, width: int, height: int, room_type: str) -> None:
        """Add a room definition.
        
        Args:
            name: Room name
            x: Room left position
            y: Room top position
            width: Room width in tiles
            height: Room height in tiles
            room_type: Type of room
        """
        room = Room(name, x, y, width, height, room_type)
        self.rooms.append(room)
        logger.debug(f"Added room: {name} ({room_type})")
    
    def get_room_at(self, position: pygame.Vector2) -> Optional[Room]:
        """Get the room at the given world position.
        
        Args:
            position: World position
        
        Returns:
            Room at position or None if not in a room
        """
        tile_x = int(position.x / TILE_SIZE)
        tile_y = int(position.y / TILE_SIZE)
        
        for room in self.rooms:
            if (room.x <= tile_x < room.x + room.width and 
                room.y <= tile_y < room.y + room.height):
                return room
        return None
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """Check if a rectangle collides with any collidable tiles.
        
        Args:
            rect: Rectangle to check
        
        Returns:
            True if collision detected
        """
        # Convert rect to tile coordinates
        start_x = max(0, int(rect.left / TILE_SIZE))
        end_x = min(self.width - 1, int(rect.right / TILE_SIZE))
        start_y = max(0, int(rect.top / TILE_SIZE))
        end_y = min(self.height - 1, int(rect.bottom / TILE_SIZE))
        
        # Check each tile in the rect's area
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                tile = self.tiles[x][y]
                if tile and tile.is_collidable:
                    tile_rect = pygame.Rect(
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    if rect.colliderect(tile_rect):
                        return True
        return False
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the tilemap.
        
        Args:
            screen: Surface to draw on
            camera_offset: Camera offset (x, y)
        """
        # Only draw tiles that are visible on screen
        start_x = max(0, int(camera_offset[0] / TILE_SIZE))
        end_x = min(self.width, int((camera_offset[0] + screen.get_width()) / TILE_SIZE) + 1)
        start_y = max(0, int(camera_offset[1] / TILE_SIZE))
        end_y = min(self.height, int((camera_offset[1] + screen.get_height()) / TILE_SIZE) + 1)
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                if tile:
                    tile.draw(screen, camera_offset)

def create_test_map() -> TileMap:
    """Create a test office map.
    
    Returns:
        Created tilemap
    """
    tilemap = TileMap()
    
    # Fill with floor tiles
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            tilemap.set_tile(x, y, TileType.FLOOR)
    
    # Add outer walls
    for x in range(MAP_WIDTH):
        tilemap.set_tile(x, 0, TileType.WALL)
        tilemap.set_tile(x, MAP_HEIGHT - 1, TileType.WALL)
    for y in range(MAP_HEIGHT):
        tilemap.set_tile(0, y, TileType.WALL)
        tilemap.set_tile(MAP_WIDTH - 1, y, TileType.WALL)
    
    # Add reception area
    tilemap.add_room("Reception", 2, 2, 8, 6, "reception")
    for x in range(2, 10):
        tilemap.set_tile(x, 2, TileType.WALL)
        tilemap.set_tile(x, 7, TileType.WALL)
    for y in range(2, 8):
        tilemap.set_tile(2, y, TileType.WALL)
        tilemap.set_tile(9, y, TileType.WALL)
    tilemap.set_tile(5, 2, TileType.DOOR)
    tilemap.set_tile(4, 4, TileType.DESK)
    tilemap.set_tile(4, 5, TileType.CHAIR)
    
    # Add meeting room
    tilemap.add_room("Meeting Room", 12, 2, 10, 8, "meeting")
    for x in range(12, 22):
        tilemap.set_tile(x, 2, TileType.WALL)
        tilemap.set_tile(x, 9, TileType.WALL)
    for y in range(2, 10):
        tilemap.set_tile(12, y, TileType.WALL)
        tilemap.set_tile(21, y, TileType.WALL)
    tilemap.set_tile(12, 5, TileType.DOOR)
    for x in range(14, 20, 2):
        tilemap.set_tile(x, 4, TileType.MEETING_TABLE)
        tilemap.set_tile(x, 7, TileType.CHAIR)
    
    # Add offices
    for i in range(3):
        x = 2 + i * 8
        tilemap.add_room(f"Office {i+1}", x, 12, 6, 6, "office")
        for dx in range(6):
            tilemap.set_tile(x + dx, 12, TileType.WALL)
            tilemap.set_tile(x + dx, 17, TileType.WALL)
        for dy in range(6):
            tilemap.set_tile(x, 12 + dy, TileType.WALL)
            tilemap.set_tile(x + 5, 12 + dy, TileType.WALL)
        tilemap.set_tile(x + 2, 12, TileType.DOOR)
        tilemap.set_tile(x + 2, 14, TileType.DESK)
        tilemap.set_tile(x + 2, 15, TileType.CHAIR)
        tilemap.set_tile(x + 4, 14, TileType.CABINET)
    
    # Add break room
    tilemap.add_room("Break Room", 28, 12, 8, 8, "break")
    for x in range(28, 36):
        tilemap.set_tile(x, 12, TileType.WALL)
        tilemap.set_tile(x, 19, TileType.WALL)
    for y in range(12, 20):
        tilemap.set_tile(28, y, TileType.WALL)
        tilemap.set_tile(35, y, TileType.WALL)
    tilemap.set_tile(28, 15, TileType.DOOR)
    tilemap.set_tile(30, 14, TileType.DESK)
    tilemap.set_tile(33, 14, TileType.WATER_COOLER)
    for x in range(30, 34, 2):
        tilemap.set_tile(x, 17, TileType.CHAIR)
    
    # Add some decoration
    for x in range(2, MAP_WIDTH - 2, 6):
        tilemap.set_tile(x, 9, TileType.PLANT)
    for y in range(2, MAP_HEIGHT - 2, 6):
        tilemap.set_tile(25, y, TileType.WINDOW)
    
    logger.info("Created test office map")
    return tilemap 