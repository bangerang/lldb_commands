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
#### diff
Performs a diff using git difftool. Accepts any expression that yields a result.
```
(lldb) diff model // Set lhs
(lldb) diff sameModelLater // Set rhs and performs diff
```
Also supports passing two arguments right away.
```
(lldb) diff frame variable self.dog == frame variable self.cat
```
diff also has support for locking the lhs.
```
(lldb) diff -l model
(lldb) diff sameModelLater // model == sameModelLater
(lldb) diff sameModelEvenLater // model == sameModelEvenLater
```
#### logger
Write expressions or a string message to a log. Log is saved to ~/Library/Logs/ which makes is available in the Console app.
```
(lldb) logger po self.view.frame
```
Description argument can be added for categorisation.
```
(lldb) logger -d "Layout" po self.view.frame
```
Can also log a regular string message, if this argument is passed the expression is ignored.
```
(lldb) logger -s "Hello world!"
```
#### rviews
Prints out the recursive description of a view expression.
```
(lldb) rviews self.view
    <UIView: 0x7fd2eae09c40; frame = (0 0; 428 926); autoresize = W+H; layer = <CALayer: 0x600001f1ef40>>
        | <UILabel: 0x7fd2daf094a0; frame = (195.667 453; 37 20.3333); text = 'error'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600003c1c0a0>>
```
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
#### pipe
Transform output by piping commands together.  
Example uses `find_label` and `vc` command to print out description of `UIViewController` responsible for the `UILabel` with text `Welcome to the jungle!`
```
(lldb) pipe find_label Welcome to the jungle! -a | vc
<Project.MyViewController: 0x7fe6b8d23300>
```
### vcl
Convenience script for the pipe example above. Prints out description of `UIViewController` responsible for the `UILabel` with text `Welcome to the jungle!`
```
(lldb) vcl Welcome to the jungle!
<Project.MyViewController: 0x7fe6b8d23300>
```
#### c
If the given command yields an address, the address is copied to clipboard.
```
(lldb) c find_label Hel
Did copy address to clipboard.
<UILabel: 0x7fefb7a0cd20; frame = (56 377; 302 72); text = 'Hello!'; userInteractionEnabled = NO; layer = <_UILabelLayer: 0x600000ee3250>>
```
#### color
Change background color of given view.
```
(lldb) color 0x7ffed2895600 [UIColor greenColor]
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


