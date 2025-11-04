"""
Inventory Management System

This module provides basic functions for managing an inventory,
including adding, removing, saving, and loading items. It uses JSON
for persistence and Python's logging for error reporting.
"""

import json
import logging
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# Global inventory dictionary
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item and quantity to the inventory."""
    if logs is None:
        logs = []

    # Type validation
    if not isinstance(item, str):
        logging.error(
            "Invalid item type: %s (expected string)",
            type(item).__name__,
        )
        return

    if not isinstance(qty, (int, float)):
        logging.error(
            "Invalid quantity type for %s: %s",
            item,
            type(qty).__name__,
        )
        return

    if not item:
        logging.warning("Item name cannot be empty.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """Remove an item or reduce its quantity safely."""
    if not isinstance(qty, (int, float)):
        logging.error(
            "Invalid quantity type for %s: %s",
            item,
            type(qty).__name__,
        )
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Attempted to remove non-existent item: %s", item)
    except TypeError:
        logging.error("Invalid quantity type for %s: %s", item, qty)


def get_qty(item):
    """Return the quantity of the specified item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logging.warning(
            "File %s not found, starting with empty inventory.",
            file,
        )
        return {}
    except json.JSONDecodeError:
        logging.error(
            "Error decoding JSON in %s, starting with empty inventory.",
            file,
        )
        return {}


def save_data(data, file="inventory.json"):
    """Save current inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def print_data():
    """Print all items in the inventory."""
    print("Items Report")
    for i, qty in stock_data.items():
        print(f"{i} -> {qty}")


def check_low_items(threshold=5):
    """Return items with stock below a given threshold."""
    return [i for i, qty in stock_data.items() if qty < threshold]


def main():
    """Main driver function."""
    global stock_data
    stock_data = load_data()

    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid types — now logged, not crashed

    remove_item("apple", 3)
    remove_item("orange", 1)

    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())

    save_data(stock_data)
    print_data()
    print("Inventory operations completed successfully.")


if __name__ == "__main__":
    main()
