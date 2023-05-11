import re
import sys
from typing import List


class ParseException(Exception):
    def __init__(self, message: str, line: int):
        super().__init__('Parse error: [Line %d] %s' % (line, message))


class RuntimeException(Exception):
    def __init__(self, message: str, line: int):
        super().__init__('Runtime error: [Line %d] %s' % (line, message))


class Command:
    def __init__(self, line: int):
        self.line = line

    def run(self, stack: List[int], ptr: int) -> int:
        return ptr + 1


class ImmediateCommand(Command):
    def __init__(self, line: int, immediate: int):
        super().__init__(line)
        self.immediate = immediate


class AddCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 2:
            raise RuntimeException(
                'Add command requires at least 2 values in the stack',
                self.line
            )
        stack.append(stack.pop() + stack.pop())
        return ptr + 1


class AddImmCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Add immediate command requires at least 1 value in the stack',
                self.line
            )
        stack.append(stack.pop() + self.immediate)
        return ptr + 1


class SubCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 2:
            raise RuntimeException(
                'Subtract command requires at least 2 values in the stack',
                self.line
            )
        stack.append(stack.pop() - stack.pop())
        return ptr + 1


class SubImmCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Subtract immediate command requires at least 1 value in the stack',
                self.line
            )
        stack.append(stack.pop() - self.immediate)
        return ptr + 1


class MultCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 2:
            raise RuntimeException(
                'Multiplication command requires at least 2 values in the stack',
                self.line
            )
        stack.append(stack.pop() * stack.pop())
        return ptr + 1


class MultImmCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Multiply immediate command requires at least 1 value in the stack',
                self.line
            )
        stack.append(stack.pop() * self.immediate)
        return ptr + 1


class DivCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 2:
            raise RuntimeException(
                'Divide command requires at least 2 values in the stack',
                self.line
            )
        dividend = stack.pop()
        divisor = stack.pop()
        if divisor == 0:
            raise RuntimeException('Divide By Zero Error', self.line)
        stack.append(dividend // divisor)
        return ptr + 1


class DivImmCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Divide immediate command requires at least 1 value in the stack',
                self.line
            )
        dividend = stack.pop()
        divisor = self.immediate
        if divisor == 0:
            raise RuntimeException('Divide By Zero Error', self.line)
        stack.append(dividend // divisor)
        return ptr + 1


class PrintCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Print command requires at least 1 value in the stack',
                self.line
            )
        print(stack.pop(), end="")
        return ptr + 1


class PrintCharacterCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Print character command requires at least 1 value in the stack',
                self.line
            )
        print(chr(stack.pop()), end="")
        return ptr + 1


class JumpIfCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        # Subtract one to account for conversion to 1-indexed line numbers
        return ptr + 1 if len(stack) == 0 or stack.pop() == 0 else (self.immediate - 1)


class JumpIfNotCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        # Subtract one to account for conversion to 1-indexed line numbers
        return (self.immediate - 1) if len(stack) == 0 or stack.pop() == 0 else ptr + 1


class LoadImmCommand(ImmediateCommand):
    def run(self, stack: List[int], ptr: int):
        stack.append(self.immediate)
        return ptr + 1


class DuplicateCommand(Command):
    def run(self, stack: List[int], ptr: int):
        if len(stack) < 1:
            raise RuntimeException(
                'Duplicate command requires at least 1 value in the stack',
                self.line
            )
        stack.append(stack[-1])
        return ptr + 1


class SwapCommand(ImmediateCommand):
    def __init__(self, line: int, immediate: int = 2):
        super(SwapCommand, self).__init__(line, immediate)

    def run(self, stack: List[int], ptr: int):
        temp = []
        for _ in range(self.immediate):
            temp.append(stack.pop())
        for x in temp:
            stack.append(x)
        return ptr + 1


def parse_arg(arg: str, line: int) -> int:
    if len(arg) == 0:
        raise ParseException('Empty argument', line)
    characters = [*arg]
    if characters[0] == '1' or characters[0] == '3':
        sign = 1
    elif characters[0] == '0' or characters[0] == '2':
        sign = -1
    else:
        raise ParseException('Invalid sign character "%s"' % characters[0], line)

    number = ''.join(characters[1:])
    try:
        return sign * int(number, 4)
    except ValueError:
        raise ParseException('Invalid numeral "%s"' % number, line)


def parse(source) -> List[Command]:
    lines = source.split('\n')
    commands = []
    for i, line in enumerate(lines):
        line_number = i + 1
        trimmed_line = re.sub(r'\s+', '', line)
        command, args = trimmed_line[:2], trimmed_line[2:]
        if command == '00':
            commands.append(AddCommand(line_number))
        elif command == '01':
            commands.append(SubCommand(line_number))
        elif command == '02':
            commands.append(MultCommand(line_number))
        elif command == '03':
            commands.append(DivCommand(line_number))
        elif command == '10':
            commands.append(AddImmCommand(line_number, parse_arg(args, line_number)))
        elif command == '11':
            commands.append(SubImmCommand(line_number, parse_arg(args, line_number)))
        elif command == '12':
            commands.append(MultImmCommand(line_number, parse_arg(args, line_number)))
        elif command == '13':
            commands.append(DivImmCommand(line_number, parse_arg(args, line_number)))
        elif command == '20':
            commands.append(PrintCommand(line_number))
        elif command == '21':
            commands.append(JumpIfCommand(line_number, parse_arg(args, line_number)))
        elif command == '22':
            commands.append(DuplicateCommand(line_number))
        elif command == '23':
            commands.append(SwapCommand(line_number, parse_arg(args, line_number) if len(args) > 0  else 2))
        elif command == '30':
            commands.append(PrintCharacterCommand(line_number))
        elif command == '31':
            commands.append(JumpIfNotCommand(line_number, parse_arg(args, line_number)))
        elif command == '32':
            commands.append(LoadImmCommand(line_number, parse_arg(args, line_number)))
        elif command == '33':
            # Comments
            pass
    return commands


def run(commands: List[Command]):
    stack = []
    ptr = 0
    while 0 <= ptr < len(commands):
        ptr = commands[ptr].run(stack, ptr)


def main():
    if len(sys.argv) < 2:
        print("Please include a source file\nExample: python %s example.3" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        run(parse(f.read()))


if __name__ == '__main__':
    main()
