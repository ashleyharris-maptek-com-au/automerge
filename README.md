# AutoMerge

Have you ever been swamped by trivial git merge conflicts; conflicts that, 
a slightly smarter computer should've been able to figure out. For example:

Lets say you have this code:
```
This_is_a_simple_function(arg1, argument2, argument3, argument4);
This_is_a_harder_function(arg1, argument2, argument3, argument4, argument5);
```
And you take a copy of that code, and submit this new improved version:
```
This_is_a_simple_function(argument1, argument2, argument3, argument4);
This_is_a_harder_function(argument1, argument2, argument3, argument4, argument5);
```
Much better! No more 'arg' because abbreviations are bad (citation needed), however someone else helpfully submitted this while you were working:
```
This_is_a_simple_function(arg1, argument2, argument3, 4);
This_is_a_harder_function(
  arg1, argument2, argument3, 4,  argument5);
```
They've replaced "argument4" with "4", and put a newline in.

Computer says NO. Or more specifically, (if using the git diff3 merge display format), computer says this:
```
<<<<<<< Upstream
This_is_a_simple_function(arg1, argument2, argument3, 4);
This_is_a_harder_function(
  arg1, argument2, argument3, 4,  argument5);
||||||| Common anscestor
This_is_a_simple_function(arg1, argument2, argument3, argument4);
This_is_a_harder_function(arg1, argument2, argument3, argument4, argument5);
======= Local
This_is_a_simple_function(argument1, argument2, argument3, argument4);
This_is_a_harder_function(argument1, argument2, argument3, argument4, argument5);
>>>>>>> 
```

Despite having computers that know how to find-and-replace, most developers on shared
projects know the pain of having to resolve this by hand. It's pretty easy to mess this up and
overlook a token in the sea of text.

AutoMerge can detect these trivial changes, and apply two or more developers edits concurrently
to the same chunk of code.

### But - merging always needs a human?

AutoMerge is an attempt to automate many of these painfully trivial merge conflicts,
freeing developers up for other tasks - but yes - not all merges can be solved without high
level understanding of the code - for some a human is still needed - but AutoMerge
can simplify very complex merges and solve the trivial stuff. 

Ideally when AutoMerge gives up and asked for someone to help, they haven't been worn down 
by 5 hours of trivial merges by the time they need to make a trivial merge.

### What language does this target?

AutoMerge was designed against and got most of it's testing by the author on a C++ codebase, however it has seen some light testing on
Perl, Javascript, HTML, Python, GLSL, HLSL, OpenSCAD, CSS, some text assembly languages (notably SPIR-V), JSON, YAML, and XML.
It should work on any text based code.

Your experience will be significantly better if you have an autoformatter you can auto run after a merge, **clang-format is highly recommended.**

### Is this 100% safe? Or is there a chance this introduces bugs?

You can configure which rules you want to allow and which you don't depending on your needs are your risk appetite.

Merges that don't even conflict can introduce bugs - classic example is 2 people fix the same bug
in two completely different ways. Consider a "Missing iterator increment from a while loop" bug,
fixed by two devs at the same time; one who adds it to the start of the loop, and one who adds it
to the end. They wont merge conflict, but the git merge process will give you two iterator increments,
and now your software isn't processing loop elements, or crashing cause it overruns.

Such bugs are more likely to occur when its easier for two concurrent changes to interact with each
other. That's a risk of using AutoMerge. However that needs to weighed against human merge process
introducing bugs.

Before creating this project I had been using this code on a large production C++ codebase 
(15 MLOC - 30 devs) for several months, and found the number of bugs introduced by AutoMerge was 0.
The number of bugs I introduced trying to manually resolve merge conflicts before AutoMerge was
switchd on - that's a much higher number.


