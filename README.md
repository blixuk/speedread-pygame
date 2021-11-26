# speedread (pygame)

This is a speed reader tool written in pyhton using PyGame

- word per minute can be set (defualt if 250). This changes when delay and punctuation delay are enabled.
- there is a few different pointers to choose from that enable better focus.
- focus finds the index character of a word and highlights it in red for better focus.
- delay will change the amount of time a word is show based on its length.
- punctuation delay will delay a word based on the punctuation used.

```
usage: __main__.py [-h] [-f FILE] [-w WPM] [-p POINTER] [-F] [-d] [-P] [-H]
                   [-W] [-t]
                   {} ...

SpeedRead

positional arguments:
  {}

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  file to read
  -w WPM, --wpm WPM     words per minute
  -p POINTER, --pointer POINTER
                        set pointer (pipe, carrot, dot, bar, full, none)
  -F, --focus           use focus on word, highlighting center character
  -d, --delay           use word delay based on word length
  -P, --punctuation     use punctuation delay
  -H, --height          set display height
  -W, --width           set display width
  -t, --font            set font size

```
