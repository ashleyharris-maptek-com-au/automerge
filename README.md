# AutoMerge

Have you ever been swamped by trivial git merge conflicts; conflicts that, 
a slightly smarter computer should've been able to figure out for example:

```
<<<<<<< Someone else commited this:
This_is_a_simple_function(arg1, argument2, argument3, 4);
This_is_a_harder_function(
  arg1, argument2, argument3, 4,  argument5);
                          
||||||| You both started from this code:
This_is_a_simple_function(arg1, argument2, argument3, argument4);
This_is_a_harder_function(arg1, argument2, argument3, argument4, argument5);

======= You commited this
This_is_a_simple_function(argument1, argument2, argument3, argument4);
This_is_a_harder_function(argument1, argument2, argument3, argument4, argument5);
>>>>>>> 
```

(For clarity this is using gits diff3 merge display format - which shows the common anscestor)

- You mearly replaced "arg1" with "argument1".
- Someone else replaced "arg4" with "4"
- Someone else changed the whitespace by inserting a newline and 2 spaces after the (

Despite having computers that know how to find-and-replace, most developers on shared
projects know the pain of having to resolve this by hand.

AutoMerge can detect these trivial changes, and apply two or more developers edits concurrently
to the same chunk of code.

### Is this 100% safe? Or is there a chance this introduces bugs?

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

### But - merging always needs a human?

AutoMerge is an attempt to automate many of these painfully trivial merge conflicts,
freeing developers up for other tasks - but yes - not all merges can be solved without high
level understanding of the code - for some a human is still needed - but AutoMerge
can simplify very complex merges and solve the trivial stuff, usually turning a 200 line
nightmare of merge tokens into a few single line merge conflicts.
