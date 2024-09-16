from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelection, QItemSelectionRange, QItemSelectionModel

def select_all_cells_in_row(table_widget, row):
        """Select all cells in a given row."""
        if row < 0 or row >= table_widget.rowCount():
            return

        # Create a range that spans all columns in the given row
        selection_range = QItemSelectionRange(
            table_widget.model().index(row, 0),
            table_widget.model().index(row, table_widget.columnCount() - 1)
        )

        # Get the selection model
        selection_model = table_widget.selectionModel()

        # Select the range
        selection_model.select(selection_range, QItemSelectionModel.Select)