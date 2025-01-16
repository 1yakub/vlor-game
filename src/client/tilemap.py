"""Tilemap module for handling the game world.

This module manages the office environment using a tile-based system.
It handles tile loading, rendering, and collision detection.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Tuple
import pygame
from pygame.math import Vector2

from shared.constants import TILE_SIZE, COLOR_WHITE, COLOR_BLACK, COLOR_GRAY

class TileType(Enum):
    """Types of tiles available in the game."""
    FLOOR = auto()
    WALL = auto()
    DOOR = auto()
    DESK = auto()
    CHAIR = auto()
    PLANT = auto()
    WINDOW = auto()
    EMPTY = auto()

class Tile:
    """A single tile in the game world.
    
    Attributes:
        type: The type of tile
        position: Position in the game world
        sprite: Visual representation of the tile
        collidable: Whether entities can collide with this tile
    """
    
    def __init__(
        self,
        tile_type: TileType,
        position: Vector2,
        sprite_path: Optional[str] = None,
        collidable: bool = False
    ):
        """Initialize the tile.
        
        Args:
            tile_type: Type of tile
            position: Position in world coordinates
            sprite_path: Path to tile sprite image
            collidable: Whether the tile has collision
        """
        self.type = tile_type
        self.position = position
        self.sprite = None
        self.collidable = collidable
        
        # Create rect for collision and rendering
        self.rect = pygame.Rect(
            position.x,
            position.y,
            TILE_SIZE,
            TILE_SIZE
        )
        
        # Load sprite if provided, otherwise use default colors
        if sprite_path:
            self._load_sprite(sprite_path)
    
    def _load_sprite(self, sprite_path: str) -> None:
        """Load the tile sprite from file.
        
        Args:
            sprite_path: Path to sprite image
        """
        try:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Could not load tile sprite: {e}")
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the tile to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        if self.sprite:
            screen.blit(self.sprite, self.rect)
        else:
            # Use default colors based on tile type
            color = self._get_default_color()
            pygame.draw.rect(screen, color, self.rect)
    
    def _get_default_color(self) -> Tuple[int, int, int]:
        """Get the default color for this tile type.
        
        Returns:
            RGB color tuple
        """
        colors = {
            TileType.FLOOR: COLOR_WHITE,
            TileType.WALL: COLOR_BLACK,
            TileType.DOOR: COLOR_GRAY,
            TileType.DESK: (139, 69, 19),  # Brown
            TileType.CHAIR: (169, 169, 169),  # Dark gray
            TileType.PLANT: (0, 100, 0),  # Dark green
            TileType.WINDOW: (135, 206, 235),  # Sky blue
            TileType.EMPTY: COLOR_WHITE
        }
        return colors.get(self.type, COLOR_WHITE)

class TileMap:
    """Manages the game world's tile-based environment.
    
    Attributes:
        width: Width of the map in tiles
        height: Height of the map in tiles
        tiles: 2D array of tiles
    """
    
    def __init__(self, width: int, height: int):
        """Initialize the tilemap.
        
        Args:
            width: Map width in tiles
            height: Map height in tiles
        """
        self.width = width
        self.height = height
        self.tiles: List[List[Optional[Tile]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]
        
        # Dictionary to store room definitions
        self.rooms: Dict[str, pygame.Rect] = {}
    
    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        """Set a tile at the specified position.
        
        Args:
            x: X coordinate in tiles
            y: Y coordinate in tiles
            tile: Tile to place
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get the tile at the specified position.
        
        Args:
            x: X coordinate in tiles
            y: Y coordinate in tiles
            
        Returns:
            Tile at position or None if out of bounds
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    
    def add_room(self, name: str, rect: pygame.Rect) -> None:
        """Define a room area in the map.
        
        Args:
            name: Unique room identifier
            rect: Rectangle defining room boundaries
        """
        self.rooms[name] = rect
    
    def get_room_at(self, position: Vector2) -> Optional[str]:
        """Get the room name at the specified position.
        
        Args:
            position: Position to check
            
        Returns:
            Room name or None if not in a room
        """
        for name, rect in self.rooms.items():
            if rect.collidepoint(position):
                return name
        return None
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """Check if a rectangle collides with any collidable tiles.
        
        Args:
            rect: Rectangle to check collision for
            
        Returns:
            True if collision detected, False otherwise
        """
        # Get tile coordinates that the rect could be colliding with
        start_x = max(0, int(rect.left // TILE_SIZE))
        end_x = min(self.width, int(rect.right // TILE_SIZE) + 1)
        start_y = max(0, int(rect.top // TILE_SIZE))
        end_y = min(self.height, int(rect.bottom // TILE_SIZE) + 1)
        
        # Check each potentially colliding tile
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                if tile and tile.collidable and tile.rect.colliderect(rect):
                    return True
        return False
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw all tiles to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                if tile:
                    tile.draw(screen)

def create_test_map() -> TileMap:
    """Create a test map for development.
    
    Returns:
        TileMap with a basic office layout
    """
    # Create a 20x15 tile map
    tilemap = TileMap(20, 15)
    
    # Add floor tiles
    for y in range(tilemap.height):
        for x in range(tilemap.width):
            tile = Tile(
                TileType.FLOOR,
                Vector2(x * TILE_SIZE, y * TILE_SIZE)
            )
            tilemap.set_tile(x, y, tile)
    
    # Add walls around the edges
    for x in range(tilemap.width):
        # Top wall
        tilemap.set_tile(x, 0, Tile(
            TileType.WALL,
            Vector2(x * TILE_SIZE, 0),
            collidable=True
        ))
        # Bottom wall
        tilemap.set_tile(x, tilemap.height - 1, Tile(
            TileType.WALL,
            Vector2(x * TILE_SIZE, (tilemap.height - 1) * TILE_SIZE),
            collidable=True
        ))
    
    for y in range(tilemap.height):
        # Left wall
        tilemap.set_tile(0, y, Tile(
            TileType.WALL,
            Vector2(0, y * TILE_SIZE),
            collidable=True
        ))
        # Right wall
        tilemap.set_tile(tilemap.width - 1, y, Tile(
            TileType.WALL,
            Vector2((tilemap.width - 1) * TILE_SIZE, y * TILE_SIZE),
            collidable=True
        ))
    
    # Add some office furniture
    # Desk
    tilemap.set_tile(5, 5, Tile(
        TileType.DESK,
        Vector2(5 * TILE_SIZE, 5 * TILE_SIZE),
        collidable=True
    ))
    # Chair
    tilemap.set_tile(5, 6, Tile(
        TileType.CHAIR,
        Vector2(5 * TILE_SIZE, 6 * TILE_SIZE)
    ))
    
    # Define some rooms
    tilemap.add_room("main_office", pygame.Rect(
        TILE_SIZE,
        TILE_SIZE,
        (tilemap.width - 2) * TILE_SIZE,
        (tilemap.height - 2) * TILE_SIZE
    ))
    
    return tilemap 