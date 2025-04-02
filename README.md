# Distributed Web Scraper

A distributed web scraper with Dockerized services for URL management and HTML parsing, designed for scalable and efficient data extraction.

## Features
- **Modular architecture**: Separate services for URL management and HTML parsing.
- **Dockerized**: Uses Docker and `docker-compose` for easy deployment.
- **Scalability**: Designed to handle large-scale scraping tasks efficiently.

## Installation

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

### Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper
   ```
2. Build and start the services:
   ```sh
   docker-compose up --build
   ```
3. The scraper services should now be running.

## Usage

- **Adding a new task**:
  ```sh
  python new_task.py <url>
  ```
  This will add a URL to the queue for scraping.

- **Monitoring logs**:
  ```sh
  docker-compose logs -f
  ```

## License
This project is licensed under the Apache-2.0 License.

