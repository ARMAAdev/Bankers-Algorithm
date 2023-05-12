import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QGridLayout, QTextEdit
from PyQt5.QtGui import QFont


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Add all your input fields and buttons here
        self.layout = QGridLayout()

        self.label_total_resources = QLabel("Total Resources")
        self.input_total_resources = QLineEdit()

        self.label_available_resources = QLabel("Available Resources")
        self.input_available_resources = QLineEdit()

        self.label_current_allocation = QLabel("Current Allocation")
        self.input_current_allocation = QTextEdit()

        self.label_maximum_need = QLabel("Maximum Need")
        self.input_maximum_need = QTextEdit()

        self.label_process_id = QLabel("Process ID")
        self.input_process_id = QLineEdit()

        self.label_request_resources = QLabel("Request Resources")
        self.input_request_resources = QLineEdit()

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

    # ...

    def str_to_matrix(self, text):
        return [list(map(int, row.split())) for row in text.split('\n') if row]

    def str_to_vector(self, text):
        return list(map(int, text.split()))

    def check_request(self):
        # Read and process inputs
        total_resources = self.str_to_vector(self.input_total_resources.text())
        available_resources = self.str_to_vector(self.input_available_resources.text())
        current_allocation = self.str_to_matrix(self.input_current_allocation.toPlainText())
        maximum_need = self.str_to_matrix(self.input_maximum_need.toPlainText())
        process_id = int(self.input_process_id.text())
        request_resources = self.str_to_vector(self.input_request_resources.text())

        # Create a BankersAlgorithm instance
        banker = BankersAlgorithm(total_resources, available_resources, current_allocation, maximum_need)

        # Call the request_resources method and display the result
        result, safe_sequence = banker.request_resources(process_id, request_resources)

        if result:
            msg = f"Request Granted. Safe sequence is: {safe_sequence}."
        else:
            msg = "Request Denied."

        # Show the result in a message box
        QMessageBox.information(self, "Result", msg)


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
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            for p in range(self.num_processes):
                if not finish[p] and all(
                        self.maximum_need[p][r] - self.current_allocation[p][r] <= work[r] for r in range(self.num_resources)):
                    work = [work[r] + self.current_allocation[p][r] for r in range(self.num_resources)]
                    finish[p] = True
                    safe_sequence.append(p)
                    break
            else:
                return False, []
        return True, safe_sequence

    def request_resources(self, process_id, request):
        if any(request[r] > self.maximum_need[process_id][r] - self.current_allocation[process_id][r] for r in
               range(self.num_resources)):
            return False, "Request exceeds maximum need"

        if any(request[r] > self.available_resources[r] for r in range(self.num_resources)):
            return False, "Request exceeds available resources"

        self.available_resources = [self.available_resources[r] - request[r] for r in range(self.num_resources)]
        self.current_allocation[process_id] = [
            self.current_allocation[process_id][r] + request[r] for r in range(self.num_resources)]
        self.maximum_need[process_id] = [self.maximum_need[process_id][r] - request[r] for r in
                                          range(self.num_resources)]

        safe, safe_sequence = self.is_safe()

        if not safe:
            self.available_resources = [self.available_resources[r] + request[r] for r in range(self.num_resources)]
            self.current_allocation[process_id] = [
                self.current_allocation[process_id][r] - request[r] for r in range(self.num_resources)]
            self.maximum_need[process_id] = [self.maximum_need[process_id][r] + request[r] for r in
                                              range(self.num_resources)]
            return False, "Request would lead to an unsafe state"

        return True, safe_sequence


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = App()
    ex.show()

    sys.exit(app.exec_())

