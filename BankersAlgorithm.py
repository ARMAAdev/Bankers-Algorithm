import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QGridLayout, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableView, QTableWidget, QTableWidgetItem

class BankersAlgorithm:
    def __init__(self, total_resources, available_resources, current_allocation, maximum_need):
        self.total_resources = total_resources
        self.available_resources = available_resources
        self.current_allocation = current_allocation
        self.maximum_need = maximum_need
        self.num_processes = len(current_allocation)
        self.num_resources = len(total_resources)

    def is_safe(self):
        work = self.available_resources.copy()
        finish = [False]*self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            for p in range(self.num_processes):
                if not finish[p] and all(self.maximum_need[p][r] - self.current_allocation[p][r] <= work[r] for r in range(self.num_resources)):
                    work = [work[r] + self.current_allocation[p][r] for r in range(self.num_resources)]
                    finish[p] = True
                    safe_sequence.append(p)
                    break
            else:
                return False, []
        return True, safe_sequence

    def request_resources(self, process_id, request):
        if any(request[r] > self.maximum_need[process_id][r] - self.current_allocation[process_id][r] for r in range(self.num_resources)):
            return False, "Request exceeds maximum need"

        if any(request[r] > self.available_resources[r] for r in range(self.num_resources)):
            return False, "Request exceeds available resources"

        self.available_resources = [self.available_resources[r] - request[r] for r in range(self.num_resources)]
        self.current_allocation[process_id] = [self.current_allocation[process_id][r] + request[r] for r in range(self.num_resources)]
        self.maximum_need[process_id] = [self.maximum_need[process_id][r] - request[r] for r in range(self.num_resources)]

        safe, safe_sequence = self.is_safe()

        if not safe:
            self.available_resources = [self.available_resources[r] + request[r] for r in range(self.num_resources)]
            self.current_allocation[process_id] = [self.current_allocation[process_id][r] - request[r] for r in range(self.num_resources)]
            self.maximum_need[process_id] = [self.maximum_need[process_id][r] + request[r] for r in range(self.num_resources)]
            return False, "Request would lead to an unsafe state"

        return True, safe_sequence

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.resize(800, 600)  # Resize the window

    def initUI(self):
        self.layout = QGridLayout()

        # Add labels
        self.label_total_resources = QLabel("Total Resources")
        self.label_available_resources = QLabel("Available Resources")
        self.label_current_allocation = QLabel("Current Allocation")
        self.label_maximum_need = QLabel("Maximum Need")
        self.label_process_id = QLabel("Process ID")
        self.label_request_resources = QLabel("Request Resources")

        self.input_total_resources = QTableWidget(1, 4)
        self.input_total_resources.setFixedHeight(60)
        self.input_total_resources.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.input_available_resources = QTableWidget(1, 4)
        self.input_available_resources.setFixedHeight(60)
        self.input_available_resources.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.input_current_allocation = QTableWidget(5, 4)
        self.input_current_allocation.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.input_maximum_need = QTableWidget(5, 4)
        self.input_maximum_need.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.input_process_id = QLineEdit()
        self.input_process_id.setFixedWidth(200)

        self.input_request_resources = QTableWidget(1, 4)
        self.input_request_resources.setFixedHeight(60)
        self.input_request_resources.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.check_request_button = QPushButton("Check Request")
        self.check_request_button.clicked.connect(self.check_request)

        self.layout.addWidget(self.label_total_resources, 0, 0)
        self.layout.addWidget(self.input_total_resources, 0, 1)
        self.layout.addWidget(self.label_available_resources, 1, 0)
        self.layout.addWidget(self.input_available_resources, 1, 1)
        self.layout.addWidget(self.label_current_allocation, 2, 0)
        self.layout.addWidget(self.input_current_allocation, 2, 1)
        self.layout.addWidget(self.label_maximum_need, 3, 0)
        self.layout.addWidget(self.input_maximum_need, 3, 1)
        self.layout.addWidget(self.label_process_id, 4, 0)
        self.layout.addWidget(self.input_process_id, 4, 1)
        self.layout.addWidget(self.label_request_resources, 5, 0)
        self.layout.addWidget(self.input_request_resources, 5, 1)
        self.layout.addWidget(self.check_request_button, 6, 0, 1, 2)

        self.setLayout(self.layout)

    def table_to_matrix(self, table):
        return [[int(table.item(row, col).text()) if table.item(row, col) else 0 for col in range(table.columnCount())] for row in range(table.rowCount())]

    def table_to_vector(self, table):
        return [int(table.item(0, col).text()) if table.item(0, col) else 0 for col in range(table.columnCount())]


    def check_request(self):
        total_resources = self.table_to_vector(self.input_total_resources)
        available_resources = self.table_to_vector(self.input_available_resources)
        current_allocation = self.table_to_matrix(self.input_current_allocation)
        maximum_need = self.table_to_matrix(self.input_maximum_need)
        process_id = int(self.input_process_id.text())
        request_resources = self.table_to_vector(self.input_request_resources)

        banker = BankersAlgorithm(total_resources, available_resources, current_allocation, maximum_need)
        result, safe_sequence = banker.request_resources(process_id, request_resources)

        if result:
            msg = f"Request Granted.\nSafe sequence is: {', '.join(map(str, safe_sequence))}.\n"
            msg += "Explanation:\n"

            for step in safe_sequence:
                msg += f"Process {step} can be allocated required resources when available resources are {banker.available_resources}.\n"
                banker.available_resources = [banker.available_resources[i] + banker.current_allocation[step][i] for i in range(banker.num_resources)]
                msg += f"Process {step} finishes, release its resources, available resources are {banker.available_resources}.\n"
        else:
            msg = "Request Denied.\n"
            msg += "Explanation:\n"
            msg += "The system does not have enough resources to satisfy the request, or the request would lead to an unsafe state."

        QMessageBox.information(self, "Result", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = App()
    ex.show()

    sys.exit(app.exec_())

