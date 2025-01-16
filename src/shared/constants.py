"""Game constants and enumerations.

This module defines constant values and enumerations used throughout the game.
"""

from enum import Enum, auto
from pygame.math import Vector2


# Window settings
TILE_SIZE = 32
WINDOW_WIDTH = 30 * TILE_SIZE  # 960 pixels
WINDOW_HEIGHT = 20 * TILE_SIZE  # 640 pixels
WINDOW_TITLE = "Varygen: Lords of Resolution"

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)

# Player settings
PLAYER_SIZE = 24
PLAYER_SPEED = 200  # pixels per second
PLAYER_COLLISION_RADIUS = 16

# Game States
class GameState(Enum):
    """Possible game states."""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

# Player Roles
class PlayerRole(Enum):
    """Available player roles."""
    MEDIATOR_RUPOK = "Rupok"
    MEDIATOR_SHORON = "Shoron"
    BUSINESSMAN = "Businessman"
    MAFIA = "Mafia"

# Business Types
class BusinessType(Enum):
    """Types of businesses players can operate."""
    RETAIL = "Retail"
    TECHNOLOGY = "Technology"
    MANUFACTURING = "Manufacturing"
    SERVICES = "Services"
    FINANCE = "Finance"

# Conflict Types
class ConflictType(Enum):
    """Types of conflicts that can occur."""
    BUSINESS_DISPUTE = "Business Dispute"
    CONTRACT_VIOLATION = "Contract Violation"
    RESOURCE_COMPETITION = "Resource Competition"
    TERRITORY_DISPUTE = "Territory Dispute"

# Resolution Methods
class ResolutionMethod(Enum):
    """Methods for resolving conflicts."""
    MEDIATION = "Mediation"
    ARBITRATION = "Arbitration"
    NEGOTIATION = "Negotiation"

# Event Types
class EventType(Enum):
    """Game event types."""
    PLAYER_MOVE = "player_move"
    PLAYER_COLLISION = "player_collision"
    BUSINESS_TRANSACTION = "business_transaction"
    CONFLICT_START = "conflict_start"
    CONFLICT_RESOLVE = "conflict_resolve"
    MAFIA_ACTION = "mafia_action"

# Network Events
class NetworkEvent(Enum):
    """Network communication events."""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    STATE_UPDATE = "state_update"
    PLAYER_UPDATE = "player_update"
    CHAT_MESSAGE = "chat_message"
    ERROR = "error"

# Asset Paths
ASSET_PATH = "assets"
SPRITE_PATH = f"{ASSET_PATH}/sprites"
SOUND_PATH = f"{ASSET_PATH}/sounds"
MAP_PATH = f"{ASSET_PATH}/maps"

# UI Constants
UI_FONT = "Arial"
UI_FONT_SIZE = 16
UI_PADDING = 10
UI_MARGIN = 5

# Game Balance
STARTING_MONEY = 1000
MEDIATION_FEE_MIN = 100
MEDIATION_FEE_MAX = 500
MAFIA_COLLECTION_FEE = 200
MAX_INVENTORY_SLOTS = 20

# Time Constants
TICK_RATE = 60
NETWORK_UPDATE_RATE = 20
ANIMATION_FRAME_RATE = 8

# Map Constants
TILE_SIZE = 32
MAP_WIDTH = 40  # tiles
MAP_HEIGHT = 30  # tiles 