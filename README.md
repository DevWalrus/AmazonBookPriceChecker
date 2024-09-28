# Amazon Book Price Checker

## Requests

| Type    | Link                                                                           |
|---------|--------------------------------------------------------------------------------|
| SOAP    | [ISBNService](http://webservices.daehosting.com/services/ISBNService.wso?WSDL) |
| REST    | [Google Books API](https://www.googleapis.com/books/v1/volumes)                |
| GraphQL | [Canopy API (Amazon)](https://graphql.canopyapi.co/)                           |

## Getting Started

Follow the instructions below to set up the development environment.

### Prerequisites

- Python 3.7 or later
- `pip` (Python package manager)

### Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/DevWalrus/AmazonBookPriceChecker.git
    cd AmazonBookPriceChecker
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On MacOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install the required packages**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application**
    ```bash
    flask run
    ```
