# Bankers-Algorithm

Bankers Algo Assignment by AbdulRahman Moustafa 19104424

## Introduction
This is a Python implementation of the Banker's algorithm, which is a deadlock avoidance algorithm used in operating systems. The algorithm is used to check if it is safe to allocate resources to a process. This implementation uses PyQt5 for the graphical user interface.

## How to Use
1. Clone the repository to a local directory.
2. Install the required packages by running the command `pip install -r requirements.txt` from the root of the cloned repository.
3. Run the program: `python main.py`
4. Enter the values for the input fields:
   - **Total Resources**: the total number of resources available in the system.
   - **Available Resources**: the number of resources that are currently available in the system.
   - **Current Allocation**: the amount of resources currently allocated to each process.
   - **Maximum Need**: the maximum amount of resources that each process can request.
   - **Process ID**: the ID of the process requesting resources.
   - **Request Resources**: the amount of resources the process is requesting.
5. Click on the "Check Request" button to check if the request is safe.
6. The result will be displayed in a message box. If the request was granted, then the safe sequence will be displayed.

## Inputs
The input fields for the algorithm are described below:

**Total Resources**:
This field specifies the total number of resources available in the system. It should be entered as a space-separated list of integers, where each integer represents the total number of resources of a certain type.

Example: `10 10 10`

**Available Resources**:
This field specifies the number of resources that are currently available in the system. It should be entered as a space-separated list of integers, where each integer represents the number of available resources of a certain type.

Example: `5 5 5`

**Current Allocation**:
This field specifies the amount of resources currently allocated to each process. It should be entered as a matrix, where each row represents a process and each column represents a resource type. Each element of the matrix is an integer representing the amount of a certain resource allocated to a certain process.

Example:
```
0 1 0
2 0 0
3 0 2
```

**Maximum Need**:
This field specifies the maximum amount of resources that each process can request. It should be entered as a matrix, where each row represents a process and each column represents a resource type. Each element of the matrix is an integer representing the maximum amount of a certain resource that a certain process can request.

Example:
```
7 5 3
3 2 2
9 0 2
```

**Process ID**:
This field specifies the ID of the process that is requesting resources. It should be entered as an integer.

Example: `2`

**Request Resources**:
This field specifies the amount of resources the process is requesting. It should be entered as a space-separated list of integers, where each integer represents the number of resources of a certain type that the process is requesting.

Example: `1 2 0`

## Outputs
The output will be displayed in a message box and will indicate whether the request was granted or denied. If the request was granted, then the safe sequence will be displayed.

- If the request is granted, the message box will display:  
  **Request Granted. Safe sequence is: [list of process IDs].**

- If the request is denied due to exceeding the maximum need, the message box will display:  
  **Request Denied. Request exceeds maximum need.**

- If the request is denied due to insufficient available resources, the message box will display:
Request Denied. Request exceeds available resources.

If the request is denied because it would lead to an unsafe state, the message box will display:
Request Denied. Request would lead to an unsafe state.
Implementation Details
The BankersAlgorithm class contains the implementation of the Banker's algorithm. The is_safe method checks if there is a safe sequence of processes that can complete execution.

The request_resources method takes as input the ID of the process requesting resources and the number of resources being requested. It checks if the request can be granted without leading to a deadlock or violating the maximum need constraint. If the request can be granted, it updates the state accordingly and returns True along with the safe sequence. Otherwise, it returns False along with an error message.

The App class contains the implementation of the graphical user interface using PyQt5. The initUI method sets up the layout of the input fields and buttons. The check_request method reads the input values and calls the request_resources method of the BankersAlgorithm class. The result is displayed in a message box.

Feel free to modify the input values and observe the output to test different scenarios.
