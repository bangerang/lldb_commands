# lldb_commands

## Installation
### [lowmad](https://www.google.com)
```
lowmad install git@github.com:bangerang/lldb_commands.git
```
### Manual
Add the scripts manually to **~/.lldbinit**
```
command script import /path/to/script
```
## LLDB Scripts
#### instruction
Returns the first occurence of given opcode.
```
(lldb) instruction jne
    0x101d88520 <+160>: jne    0x101d8852c               ; <+172> at ViewController.swift:141:9
```
You can also change the opcode on the fly.
```
(lldb) instruction jne -o 74
```
#### find_label
Prints out description of UILabel with given text.
```
(lldb) find_label Welcome to the jungle!
<UILabel: 0x7ffed2494e70; frame = (50 214; 328 36); text = 'Welcome to the jungle!'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600000ae6ad0>>
```
Print out superview as well.
```
(lldb) find_label Welcome to the jungle!
<UIScrollView: 0x7ffed2895600; baseClass = UIScrollView; frame = (0 0; 428 926); clipsToBounds = YES; gestureRecognizers = <NSArray: 0x6000026896b0>; layer = <CALayer: 0x6000029e8d80>; contentOffset: {0, 0}; contentSize: {0, 532.66666666666674}; adjustedContentInset: {0, 0, 83, 0}>
   | <UILabel: 0x7ffed2494e70; frame = (50 214; 328 36); text = 'Welcome to the jungle!'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600000ae6ad0>>
```
#### color
Change background color of given view.
```
(lldb) color 0x7ffed2895600 [UIColor greenColor]




