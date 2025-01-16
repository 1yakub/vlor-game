"""Business UI module.

This module handles the display of business information and interactions.
"""

import pygame
import pygame_gui
from pygame_gui.elements import (
    UIPanel,
    UILabel,
    UIButton,
    UIScrollingContainer,
    UITextBox,
    UIDropDownMenu
)

from shared.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BusinessType,
    ConflictType,
    ResolutionMethod
)
from shared.logger import get_logger
from client.business import Business, Contract, Conflict

logger = get_logger(__name__)

class BusinessPanel:
    """Panel displaying business information and controls."""
    
    def __init__(self, ui_manager: pygame_gui.UIManager):
        """Initialize the business panel.
        
        Args:
            ui_manager: The game's UI manager
        """
        self.ui_manager = ui_manager
        self.visible = False
        self.current_business = None
        
        # Create main panel
        panel_width = 400
        panel_height = 600
        panel_x = WINDOW_WIDTH - panel_width - 20
        panel_y = 60
        
        self.panel = UIPanel(
            relative_rect=pygame.Rect(
                (panel_x, panel_y),
                (panel_width, panel_height)
            ),
            starting_layer_height=2,
            manager=ui_manager
        )
        
        # Business info section
        self.name_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (380, 30)),
            text="Business Name",
            manager=ui_manager,
            container=self.panel
        )
        
        self.type_label = UILabel(
            relative_rect=pygame.Rect((10, 50), (380, 30)),
            text="Type: ",
            manager=ui_manager,
            container=self.panel
        )
        
        self.money_label = UILabel(
            relative_rect=pygame.Rect((10, 90), (380, 30)),
            text="Money: $0",
            manager=ui_manager,
            container=self.panel
        )
        
        # Resources section
        resources_label = UILabel(
            relative_rect=pygame.Rect((10, 130), (380, 30)),
            text="Resources",
            manager=ui_manager,
            container=self.panel
        )
        
        self.resources_container = UIScrollingContainer(
            relative_rect=pygame.Rect((10, 170), (380, 120)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Contracts section
        contracts_label = UILabel(
            relative_rect=pygame.Rect((10, 300), (380, 30)),
            text="Active Contracts",
            manager=ui_manager,
            container=self.panel
        )
        
        self.contracts_container = UIScrollingContainer(
            relative_rect=pygame.Rect((10, 340), (380, 120)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Conflicts section
        conflicts_label = UILabel(
            relative_rect=pygame.Rect((10, 470), (380, 30)),
            text="Active Conflicts",
            manager=ui_manager,
            container=self.panel
        )
        
        self.conflicts_container = UIScrollingContainer(
            relative_rect=pygame.Rect((10, 510), (380, 80)),
            manager=ui_manager,
            container=self.panel
        )
        
        # Hide panel initially
        self.hide()
    
    def show(self, business: Business) -> None:
        """Show the panel with business information.
        
        Args:
            business: Business to display
        """
        self.current_business = business
        self.update_display()
        self.panel.show()
        self.visible = True
        logger.debug(f"Showing business panel for {business.name}")
    
    def hide(self) -> None:
        """Hide the business panel."""
        self.panel.hide()
        self.visible = False
        self.current_business = None
    
    def update_display(self) -> None:
        """Update all displayed information."""
        if not self.current_business:
            return
        
        # Update basic info
        self.name_label.set_text(self.current_business.name)
        self.type_label.set_text(f"Type: {self.current_business.type.value}")
        self.money_label.set_text(f"Money: ${self.current_business.money:,.2f}")
        
        # Update resources
        self._update_resources()
        self._update_contracts()
        self._update_conflicts()
    
    def _update_resources(self) -> None:
        """Update the resources display."""
        # Clear existing elements
        for element in self.resources_container.elements():
            element.kill()
        
        # Add resource entries
        y_offset = 0
        for resource in self.current_business.resources.values():
            # Resource name and quantity
            text = f"{resource.name}: {resource.quantity:,} @ ${resource.value:,.2f}/unit"
            label = UILabel(
                relative_rect=pygame.Rect((0, y_offset), (360, 30)),
                text=text,
                manager=self.ui_manager,
                container=self.resources_container
            )
            y_offset += 35
        
        # Update container height
        self.resources_container.set_scrollable_area_height(max(120, y_offset))
    
    def _update_contracts(self) -> None:
        """Update the contracts display."""
        # Clear existing elements
        for element in self.contracts_container.elements():
            element.kill()
        
        # Add contract entries
        y_offset = 0
        for contract in self.current_business.contracts:
            # Contract details
            if contract.seller == self.current_business:
                text = f"Selling {contract.quantity} {contract.resource} for ${contract.price:,.2f}"
            else:
                text = f"Buying {contract.quantity} {contract.resource} for ${contract.price:,.2f}"
            
            if contract.is_fulfilled:
                text += " (Fulfilled)"
            
            label = UILabel(
                relative_rect=pygame.Rect((0, y_offset), (360, 30)),
                text=text,
                manager=self.ui_manager,
                container=self.contracts_container
            )
            y_offset += 35
        
        # Update container height
        self.contracts_container.set_scrollable_area_height(max(120, y_offset))
    
    def _update_conflicts(self) -> None:
        """Update the conflicts display."""
        # Clear existing elements
        for element in self.conflicts_container.elements():
            element.kill()
        
        # Add conflict entries
        y_offset = 0
        for conflict in self.current_business.conflicts:
            if not conflict.is_resolved:
                # Conflict details
                text = f"{conflict.type.value}"
                if conflict.mediator:
                    text += f" - Mediator: {conflict.mediator}"
                
                label = UILabel(
                    relative_rect=pygame.Rect((0, y_offset), (360, 30)),
                    text=text,
                    manager=self.ui_manager,
                    container=self.conflicts_container
                )
                y_offset += 35
        
        # Update container height
        self.conflicts_container.set_scrollable_area_height(max(80, y_offset))
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle UI events.
        
        Args:
            event: The event to handle
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in self.panel.elements:
                logger.debug(f"Business panel button pressed: {event.ui_element.text}")
                # Handle button presses here 