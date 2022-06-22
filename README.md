![](https://img.shields.io/badge/python-3.10-orange)
# Cuchufletos Bot
The cuchufletos

## Install

## How to use
For a new telegram-command just add a new method in Cuchubot class from cuchubot.bots. See [cuchubot/bots.py](cuchubot/bots.py)
The method needs to start with `tf_{method}` and use the following signature:

```python
class Cuchubot():
    def __init__(self):
        ...
    def tf_examplemethod(self, update, context,
                         debug=False,
                         ):
        ...
        do_something(update, context)
        ...
```

Then, in telegram, the command will simply be:
```bash
/examplemethod
```


Just see the already implemented methods.
Also, use the references from:
https://python-telegram-bot.readthedocs.io/en/latest/telegram.html


Database for this repo: https://drive.google.com/drive/folders/1ghe9R6tAkdx5MKR-z9q5oAzgGjh1Gbp5?usp=sharing



## References:
- https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq