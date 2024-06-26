<p align="center">
  <img src="./logo.png" alt="Threes Logo" height=300 />
  <h1 align="center">Threes</h1>
</p>

Threes is a novelty programming language that operates as a stack-based reduced instruction set language.

## Syntax

All source code written in Threes are written using only the following characters: 0, 1, 2, and 3.

Example: the following code prints "Hello, World!" to the console

```
321201    33 Load !
3211210   33 Load d
3211230   33 Load l
3211302   33 Load r
3211233   33 Load o
3211313   33 Load w
321200    33 Load space
321230    33 Load comma
3211233   33 Load o
3211230   33 Load l
3211230   33 Load l
3211211   33 Load e
3211020   33 Load H
32131     33 Set loop counter
23        33 Swap
30        33 Print
1111      33 Decrement loop counter
22        33 Duplicate loop counter
21133     33 Jump to print
```

## Commands

### Addition

#### Stack - `00`

Takes the top two values on the stack and pushes their sum to the stack.

#### Immediate - `10`

Takes the top value from the stack and pushes back the result of adding the provided [immediate](#immediates).

### Subtraction

#### Stack - `01`

Takes the top two values on the stack and pushes their difference (top minus second from the second-from-the-top) to the
stack.

#### Immediate - `11`

Takes the top value from the stack and pushes back the result of subtracting the provided [immediate](#immediates).

### Multiplication

#### Stack - `02`

Takes the top two values on the stack and pushes their product to the stack.

#### Immediate - `12`

Takes the top value from the stack and pushes back the result of multiplying by the provided [immediate](#immediates).

### Division

#### Stack - `03`

Takes the top two values on the stack and pushes their quotient (top minus divided by the second-from-the-top) to the
stack.

#### Immediate - `13`

Takes the top value from the stack and pushes back the result of dividing by the provided [immediate](#immediates).

### Print

#### Print - `20`

Pops the top value from the stack and prints it as a number

#### PrintCharacter - `30`

Pops the top value from the stack and prints it as a character.

### Jump

#### JumpIf - `21`

Jumps to the provided [line number](#immediates) if the stack contains a value, and it is non-zero

#### JumpIfNot - `31`

Jumps to the provided [line number](#immediates) if the stack is empty or the top value is a zero.

### Duplicate

#### Duplicate - `22`

Duplicates the top value in the stack

### Swap

#### Swap - `23`

Swaps the top values in the stack. Optionally takes a provided [line count](#immediates), which informs the command how
many lines to swap (default two).

### Load Value

#### Immediate - `32`

Loads the provided [immediate value](#immediates) to the top of the stack

### Comments

#### Comment - `33`

Anything following this command is treated as a comment and is ignored by the interpreter (yes, even normal words 😱)

## Immediates

Immediates, or integer literals, are encoded as a positive base 4 value with a numeric prefix indicating sign where
positive values start with odd prefixes while negative values start with even prefixes. The same rules apply for
characters. If a character were to be encoded as an immediate, then the ascii value would be converted to base 4 and
then prefixed with an odd number (e.g., 'A' becomes 11000).

Examples:

| Decimal Number | Base 4 | Immediate Encoding |
| :------------- | :----- | :----------------- |
| 1              | 1      | 11                 |
| -1             | -1     | 21                 |
| -1             | -1     | 21                 |
| 16             | 100    | 3100               |
