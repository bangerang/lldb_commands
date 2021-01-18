# lldb_commands

## Installation
### [lowmad](https://github.com/bangerang/lowmad)
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
(lldb) find_label Welcome to the jungle! -s
<UIScrollView: 0x7ffed2895600; baseClass = UIScrollView; frame = (0 0; 428 926); clipsToBounds = YES; gestureRecognizers = <NSArray: 0x6000026896b0>; layer = <CALayer: 0x6000029e8d80>; contentOffset: {0, 0}; contentSize: {0, 532.66666666666674}; adjustedContentInset: {0, 0, 83, 0}>
   | <UILabel: 0x7ffed2494e70; frame = (50 214; 328 36); text = 'Welcome to the jungle!'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600000ae6ad0>>
```
#### vc
Prints out description of UIViewController responsible for view
```
(lldb) vc 0x7fe69a110e50
<Project.MyViewController: 0x7fe6b8d23300>
```
#### color
Change background color of given view.
```
(lldb) color 0x7ffed2895600 [UIColor greenColor]
```
#### c
If the given command yields an address, the address is copied to clipboard.
```
(lldb) c find_label Hel
Did copy address to clipboard.
<UILabel: 0x7fefb7a0cd20; frame = (56 377; 302 72); text = 'Hello!'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600000ee3250>>
```
#### mirror
Uses Swifts mirror API to reflect a struct or class.
```
(lldb) mirror self.myClass
MyProject.MyClass

name: foo, value: bar, type: String
name: number, value: 8, type: Int
```
#### set_lang
Alias for settings set target.language, force language setting for target.
```
(lldb) set_lang swift
```
#### nudge
Nudge a view by modifying it's center. I'm not the author of this script, it comes from this [WWDC video](https://developer.apple.com/videos/play/wwdc2018/412/)
```
(lldb) nudge 1 1 self.textLabel
```


