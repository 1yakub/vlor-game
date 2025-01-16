"""Mediation UI module.

This module handles the conflict resolution interface.
"""

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIPanel,
    UILabel,
    UIButton,
    UITextBox,
    UIDropDownMenu,
    UITextEntryLine
)

from shared.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MEDIATION_FEE_MIN,
    MEDIATION_FEE_MAX,
    ResolutionMethod
)
from shared.logger import get_logger
from client.business import Business, Conflict

logger = get_logger(__name__)

class MediationPanel:
    """Panel for handling business conflicts."""
    
    def __init__(self, ui_manager: pygame_gui.UIManager):
        """Initialize the mediation panel.
        
        Args:
            ui_manager: The game's UI manager
        """
        self.ui_manager = ui_manager
        self.visible = False
        self.current_conflict = None
        
        # Create main panel
        panel_width = 600
        panel_height = 500
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2
        
        self.panel = UIPanel(
            relative_rect=pygame.Rect(
                (panel_x, panel_y),
                (panel_width, panel_height)
            ),
            manager=ui_manager
        )
        
        # Title
        self.title = UILabel(
            relative_rect=pygame.Rect((10, 10), (580, 30)),
            text="Conflict Resolution",
            manager=ui_manager,
            container=self.panel
        )
        
        # Conflict info
        self.conflict_info = UITextBox(
            html_text="",
            relative_rect=pygame.Rect((10, 50), (580, 100)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Parties section
        party_label = UILabel(
            relative_rect=pygame.Rect((10, 160), (280, 30)),
            text="Involved Parties",
            manager=ui_manager,
            container=self.panel
        )
        
        self.parties_info = UITextBox(
            html_text="",
            relative_rect=pygame.Rect((10, 200), (280, 120)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Resolution section
        resolution_label = UILabel(
            relative_rect=pygame.Rect((310, 160), (280, 30)),
            text="Resolution Method",
            manager=ui_manager,
            container=self.panel
        )
        
        self.resolution_dropdown = UIDropDownMenu(
            options_list=[method.value for method in ResolutionMethod],
            starting_option=ResolutionMethod.MEDIATION.value,
            relative_rect=pygame.Rect((310, 200), (280, 30)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Fee section
        fee_label = UILabel(
            relative_rect=pygame.Rect((310, 240), (280, 30)),
            text=f"Mediation Fee (${MEDIATION_FEE_MIN:,.2f} - ${MEDIATION_FEE_MAX:,.2f})",
            manager=ui_manager,
            container=self.panel
        )
        
        self.fee_entry = UITextEntryLine(
            relative_rect=pygame.Rect((310, 280), (280, 30)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Notes section
        notes_label = UILabel(
            relative_rect=pygame.Rect((10, 330), (580, 30)),
            text="Resolution Notes",
            manager=ui_manager,
            container=self.panel
        )
        
        self.notes_entry = UITextEntryLine(
            relative_rect=pygame.Rect((10, 370), (580, 30)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Status section
        self.status_label = UILabel(
            relative_rect=pygame.Rect((10, 410), (580, 30)),
            text="",
            manager=ui_manager,
            container=self.panel
        )
        
        # Buttons
        self.resolve_button = UIButton(
            relative_rect=pygame.Rect((10, 450), (280, 40)),
            text="Resolve Conflict",
            manager=ui_manager,
            container=self.panel
        )
        
        self.cancel_button = UIButton(
            relative_rect=pygame.Rect((310, 450), (280, 40)),
            text="Cancel",
            manager=ui_manager,
            container=self.panel
        )
        
        # Hide panel initially
        self.hide()
    
    def show(self, conflict: Conflict) -> None:
        """Show the mediation panel.
        
        Args:
            conflict: Conflict to resolve
        """
        self.current_conflict = conflict
        
        # Update conflict info
        self.conflict_info.html_text = (
            f"<b>Type:</b> {conflict.type.value}<br>"
            f"<b>Description:</b> {conflict.description}"
        )
        self.conflict_info.rebuild()
        
        # Update parties info
        parties_text = "<br>".join(
            f"<b>{party.name}</b> ({party.type.value})"
            for party in conflict.parties
        )
        self.parties_info.html_text = parties_text
        self.parties_info.rebuild()
        
        # Reset inputs
        self.resolution_dropdown.selected_option = ResolutionMethod.MEDIATION.value
        self.fee_entry.set_text(str(MEDIATION_FEE_MIN))
        self.notes_entry.set_text("")
        self.status_label.set_text("")
        
        # Show panel
        self.panel.show()
        self.visible = True
        logger.debug(f"Showing mediation panel for conflict {conflict.id}")
    
    def hide(self) -> None:
        """Hide the mediation panel."""
        self.panel.hide()
        self.visible = False
        self.current_conflict = None
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle UI events.
        
        Args:
            event: The event to handle
        """
        if not self.visible:
            return
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.cancel_button:
                self.hide()
            elif event.ui_element == self.resolve_button:
                self._resolve_conflict()
        
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.resolution_dropdown:
                self._update_fee_visibility()
    
    def _update_fee_visibility(self) -> None:
        """Update fee input visibility based on resolution method."""
        is_mediation = self.resolution_dropdown.selected_option == ResolutionMethod.MEDIATION.value
        self.fee_entry.visible = is_mediation
    
    def _resolve_conflict(self) -> None:
        """Resolve the current conflict."""
        if not self.current_conflict:
            return
        
        try:
            # Get resolution details
            resolution_method = ResolutionMethod(self.resolution_dropdown.selected_option)
            notes = self.notes_entry.get_text()
            
            # Validate fee if mediation
            if resolution_method == ResolutionMethod.MEDIATION:
                fee = float(self.fee_entry.get_text())
                if not MEDIATION_FEE_MIN <= fee <= MEDIATION_FEE_MAX:
                    self.status_label.set_text(f"Invalid fee: must be between ${MEDIATION_FEE_MIN:,.2f} and ${MEDIATION_FEE_MAX:,.2f}")
                    return
            
            # Get game instance
            from client.game import Game  # Avoid circular import
            game = Game.instance
            
            # Update conflict
            self.current_conflict.resolution_method = resolution_method
            self.current_conflict.mediator = game.player.name
            self.current_conflict.resolve()
            
            # Add mediation fee to player if applicable
            if resolution_method == ResolutionMethod.MEDIATION:
                game.player.add_money(fee)
            
            logger.info(f"Resolved conflict {self.current_conflict.id} via {resolution_method.value}")
            self.hide()
            
        except ValueError as e:
            self.status_label.set_text(f"Error: {e}")
        except Exception as e:
            logger.exception("Error resolving conflict")
            self.status_label.set_text("An error occurred") 