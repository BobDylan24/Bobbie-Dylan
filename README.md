# Bobbie-Dylan

Bobbie Dylan is a multi-purpose public discord bot written in python using the nextcord library.

## Installation

We do not recomend you self host the bot. And recommend you use the one we host!

First download [python](https://python.org)

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the librarys we are going to need to run the bot.

```bash
pip install nextcord python-dateutil buttons motor requests 
```

## How to run

Once you have installed all the required librarys for the bot. You need to run the bot using python.

But first we need to create a config.py file and enter the following values:

```python
token = "Your discord bot token"
mongo = "Your mongoDB url"
```

Now that we have done this we need to run it with the following command below:

```bash
python bot.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)