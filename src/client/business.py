"""Business module.

This module handles business entities and their interactions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from uuid import uuid4
import time

from shared.constants import (
    BusinessType,
    ConflictType,
    ResolutionMethod,
    STARTING_MONEY
)
from shared.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Resource:
    """Resource class representing business inventory items."""
    name: str
    quantity: int
    value: float

@dataclass
class Contract:
    """Contract class representing business agreements."""
    seller: 'Business'
    buyer: 'Business'
    resource: str
    quantity: int
    price: float
    id: str = field(default_factory=lambda: str(uuid4()))
    is_fulfilled: bool = False
    created_at: float = field(default_factory=time.time)

@dataclass
class Conflict:
    """Conflict class representing business disputes."""
    type: ConflictType
    description: str
    parties: List['Business']
    id: str = field(default_factory=lambda: str(uuid4()))
    resolution_method: Optional[ResolutionMethod] = None
    mediator: Optional[str] = None
    is_resolved: bool = False
    created_at: float = field(default_factory=time.time)
    resolved_at: Optional[float] = None
    
    def resolve(self) -> None:
        """Mark the conflict as resolved."""
        self.is_resolved = True
        self.resolved_at = time.time()
        logger.info(f"Conflict {self.id} resolved via {self.resolution_method.value}")

class Business:
    """Business class representing game entities."""
    
    def __init__(self, name: str, type: BusinessType, owner: str):
        """Initialize a business.
        
        Args:
            name: Business name
            type: Business type
            owner: Owner name
        """
        self.name = name
        self.type = type
        self.owner = owner
        self.money = STARTING_MONEY
        
        # Resources and contracts
        self.resources: Dict[str, Resource] = {}
        self.contracts: List[Contract] = []
        self.conflicts: List[Conflict] = []
        
        logger.info(f"Created business: {self.name} ({self.type.value})")
    
    def add_resource(self, name: str, quantity: int, value: float) -> None:
        """Add a resource to inventory.
        
        Args:
            name: Resource name
            quantity: Resource quantity
            value: Resource value per unit
        """
        if name in self.resources:
            self.resources[name].quantity += quantity
            self.resources[name].value = value
        else:
            self.resources[name] = Resource(name, quantity, value)
        logger.debug(f"{self.name} added {quantity} {name} @ ${value}/unit")
    
    def remove_resource(self, name: str, quantity: int) -> bool:
        """Remove a resource from inventory.
        
        Args:
            name: Resource name
            quantity: Resource quantity
        
        Returns:
            True if resource was removed, False if insufficient quantity
        """
        if name not in self.resources:
            return False
        
        if self.resources[name].quantity < quantity:
            return False
        
        self.resources[name].quantity -= quantity
        if self.resources[name].quantity == 0:
            del self.resources[name]
        
        logger.debug(f"{self.name} removed {quantity} {name}")
        return True
    
    def add_money(self, amount: float) -> None:
        """Add money to the business.
        
        Args:
            amount: Amount to add
        """
        self.money += amount
        logger.debug(f"{self.name} added ${amount:,.2f}")
    
    def remove_money(self, amount: float) -> bool:
        """Remove money from the business.
        
        Args:
            amount: Amount to remove
        
        Returns:
            True if money was removed, False if insufficient funds
        """
        if self.money < amount:
            return False
        
        self.money -= amount
        logger.debug(f"{self.name} removed ${amount:,.2f}")
        return True

class BusinessManager:
    """Manages all businesses in the game."""
    
    def __init__(self):
        """Initialize the business manager."""
        self.businesses: Dict[str, Business] = {}
        self.contracts: List[Contract] = []
        self.conflicts: List[Conflict] = []
    
    def create_business(
        self,
        name: str,
        type: BusinessType,
        owner: str
    ) -> Business:
        """Create a new business.
        
        Args:
            name: Business name
            type: Business type
            owner: Owner name
        
        Returns:
            The created business
        """
        business = Business(name, type, owner)
        self.businesses[name] = business
        return business
    
    def create_contract(
        self,
        seller: Business,
        buyer: Business,
        resource: str,
        quantity: int,
        price: float
    ) -> Optional[Contract]:
        """Create a contract between businesses.
        
        Args:
            seller: Selling business
            buyer: Buying business
            resource: Resource name
            quantity: Resource quantity
            price: Total price
        
        Returns:
            Created contract or None if invalid
        """
        # Validate contract
        if resource not in seller.resources:
            logger.warning(f"Contract failed: {seller.name} does not have {resource}")
            return None
        
        if seller.resources[resource].quantity < quantity:
            logger.warning(f"Contract failed: {seller.name} has insufficient {resource}")
            return None
        
        if not buyer.remove_money(price):
            logger.warning(f"Contract failed: {buyer.name} has insufficient funds")
            return None
        
        # Create and register contract
        contract = Contract(
            seller=seller,
            buyer=buyer,
            resource=resource,
            quantity=quantity,
            price=price
        )
        
        seller.contracts.append(contract)
        buyer.contracts.append(contract)
        self.contracts.append(contract)
        
        # Transfer resources and money
        seller.remove_resource(resource, quantity)
        seller.add_money(price)
        buyer.add_resource(resource, quantity, price / quantity)
        
        contract.is_fulfilled = True
        logger.info(f"Created contract: {contract}")
        return contract
    
    def create_conflict(
        self,
        type: ConflictType,
        description: str,
        parties: List[Business]
    ) -> Conflict:
        """Create a conflict between businesses.
        
        Args:
            type: Conflict type
            description: Conflict description
            parties: Involved businesses
        
        Returns:
            Created conflict
        """
        conflict = Conflict(
            type=type,
            description=description,
            parties=parties
        )
        
        for party in parties:
            party.conflicts.append(conflict)
        self.conflicts.append(conflict)
        
        logger.info(f"Created conflict: {type.value} between {[p.name for p in parties]}")
        return conflict
    
    def update(self, delta_time: float) -> None:
        """Update all businesses.
        
        Args:
            delta_time: Time elapsed since last update
        """
        # Update contracts and conflicts
        for contract in self.contracts:
            if not contract.is_fulfilled:
                # Check if contract conditions are met
                pass
        
        for conflict in self.conflicts:
            if not conflict.is_resolved:
                # Update conflict state
                pass