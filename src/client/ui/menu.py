"""Menu system for game UI.

This module handles the main menu, pause menu, and other UI screens.
"""

import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIDropDownMenu
from pygame_gui.windows import UIMessageWindow

from shared.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    UI_FONT,
    UI_FONT_SIZE,
    GameState,
    PlayerRole
)
from shared.logger import get_logger

logger = get_logger(__name__)

class MenuManager:
    """Manages game menus and UI screens."""
    
    def __init__(self, ui_manager: pygame_gui.UIManager):
        """Initialize the menu manager."""
        self.ui_manager = ui_manager
        self.current_state = GameState.MENU
        self.elements = {
            GameState.MENU: [],
            GameState.PLAYING: [],
            GameState.PAUSED: []
        }
        
        # Create UI elements for each state
        self._create_main_menu()
        self._create_pause_menu()
        self._create_game_hud()
        
        # Initially hide all elements except menu
        self.show_state(GameState.MENU)
    
    def _create_main_menu(self) -> None:
        """Create main menu UI elements."""
        center_x = WINDOW_WIDTH // 2
        
        # Title
        title = UILabel(
            relative_rect=pygame.Rect((center_x - 200, 50), (400, 50)),
            text="Varygen: Lords of Resolution",
            manager=self.ui_manager,
            object_id="#title_label"
        )
        
        # Role selection
        role_label = UILabel(
            relative_rect=pygame.Rect((center_x - 100, 150), (200, 30)),
            text="Select Your Role:",
            manager=self.ui_manager
        )
        
        role_dropdown = UIDropDownMenu(
            options_list=[role.value for role in PlayerRole],
            starting_option=PlayerRole.MEDIATOR_RUPOK.value,
            relative_rect=pygame.Rect((center_x - 100, 190), (200, 30)),
            manager=self.ui_manager
        )
        
        # Buttons
        start_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 250), (200, 50)),
            text="Start Game",
            manager=self.ui_manager
        )
        
        settings_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 320), (200, 50)),
            text="Settings",
            manager=self.ui_manager
        )
        
        quit_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 390), (200, 50)),
            text="Quit Game",
            manager=self.ui_manager
        )
        
        self.elements[GameState.MENU] = [
            title,
            role_label,
            role_dropdown,
            start_button,
            settings_button,
            quit_button
        ]
    
    def _create_pause_menu(self) -> None:
        """Create pause menu UI elements."""
        center_x = WINDOW_WIDTH // 2
        
        # Buttons
        resume_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 200), (200, 50)),
            text="Resume Game",
            manager=self.ui_manager
        )
        
        settings_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 270), (200, 50)),
            text="Settings",
            manager=self.ui_manager
        )
        
        quit_button = UIButton(
            relative_rect=pygame.Rect((center_x - 100, 340), (200, 50)),
            text="Quit to Menu",
            manager=self.ui_manager
        )
        
        self.elements[GameState.PAUSED] = [
            resume_button,
            settings_button,
            quit_button
        ]
    
    def _create_game_hud(self) -> None:
        """Create in-game HUD elements."""
        # Player info
        role_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            text="Role: ",
            manager=self.ui_manager
        )
        
        money_label = UILabel(
            relative_rect=pygame.Rect((10, 50), (200, 30)),
            text="Money: $0",
            manager=self.ui_manager
        )
        
        # Room info
        room_label = UILabel(
            relative_rect=pygame.Rect((WINDOW_WIDTH - 210, 10), (200, 30)),
            text="Location: ",
            manager=self.ui_manager
        )
        
        self.elements[GameState.PLAYING] = [
            role_label,
            money_label,
            room_label
        ]
    
    def show_state(self, state: GameState) -> None:
        """Show UI elements for the given state."""
        logger.debug(f"Showing UI state: {state}")
        
        # Hide all elements
        for elements in self.elements.values():
            for element in elements:
                element.hide()
        
        # Show elements for new state
        if state in self.elements:
            for element in self.elements[state]:
                element.show()
        
        self.current_state = state
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle UI events."""
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            button_text = event.ui_element.text
            logger.debug(f"Button pressed: {button_text}")
            
            if button_text == "Start Game":
                self.show_state(GameState.PLAYING)
            elif button_text == "Resume Game":
                self.show_state(GameState.PLAYING)
            elif button_text == "Quit Game":
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif button_text == "Quit to Menu":
                self.show_state(GameState.MENU)
    
    def update(self, delta_time: float) -> None:
        """Update UI elements."""
        pass  # UI manager updates are handled in Game class 