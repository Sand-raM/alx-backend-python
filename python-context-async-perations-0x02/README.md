# Python Context and Async Operations

## Project Overview
This project explores advanced Python concepts related to **context managers** and **asynchronous programming**. It includes hands-on implementations and examples demonstrating the effective use of:

- Custom context managers with the `contextlib` module.
- Managing resources efficiently using `with` statements.
- Asynchronous programming patterns with `asyncio`.
- Combining context management with async operations for scalable and maintainable code.

## Key Features

### 1. Context Managers
- Implementation of custom context managers using:
  - Class-based approach with `__enter__` and `__exit__` methods.
  - Function-based approach with `@contextlib.contextmanager`.
- Resource cleanup and exception handling.

### 2. Asynchronous Programming
- Use of `async` and `await` keywords to manage asynchronous workflows.
- Examples of `asyncio` tasks for concurrent operations.
- Combining `async` functions with context managers.

### 3. Integration
- Demonstrates integration of context management and async programming to:
  - Handle resources in asynchronous tasks.
  - Avoid resource leaks in concurrent workflows.

## Directory Structure
```plaintext
.
├── async_examples
│   ├── file_reader.py       # Asynchronous file reading example
│   ├── task_scheduler.py    # Task scheduling with asyncio
├── context_managers
│   ├── db_connection.py     # Context manager for database connections
│   ├── resource_handler.py  # General resource handler
├── tests
│   ├── test_context.py      # Unit tests for context managers
│   ├── test_async.py        # Unit tests for async operations
└── README.md                # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sand-raM/python-context-async-operations-0x02.git
   cd python-context-async-operations-0x02
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the examples:
   ```bash
   python async_examples/file_reader.py
   python context_managers/db_connection.py
   ```

## Tests
Run the unit tests to verify the implementations:
```bash
pytest tests/
```

## Usage
- Explore the provided examples to understand how to implement and use context managers and async operations.
- Adapt the code to integrate these concepts into your own projects.

## Author
Sandra MURAZA

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

