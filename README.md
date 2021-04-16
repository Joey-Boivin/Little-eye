# Little eye

This is a simple low dependency multithreading application to track items listed on [Newegg](https://www.newegg.ca/). This was made for self-educational purposes

![Image](Screenshot.png "Little eye gui")
## Dependencies

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

## Installation

1. Fork and clone the repository
2. Install the dependencies as stated above
3. The data-example.json file exists to give the reader an idea of how the data is structured. It is not necessary.

## First use

To track your first item, retrieve the url extention that follows https://www.newegg.ca/

Move into the App directory and enter in the command line:

> python main.py N --add your-url-extension

To open the help menu:

> python main.py -h

## License

This software is licensed under the [MIT Liscence](https://github.com/Joey-Boivin/newegg-tracker/blob/main/LICENSE)
