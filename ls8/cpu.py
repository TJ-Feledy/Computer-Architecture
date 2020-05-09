"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""
        address = 0

        if len(program) != 2:   # check for second argument from command line
            print('need proper filename passed')
            sys.exit(1)

        filename = program[1]

        with open(filename) as f:
            for line in f:
                # print(line)
                if line == '\n':    # skip empty lines
                    continue
                if line[0] == '#':  # skip lines that are comments
                    continue
                
                comment_split = line.split('#')  # everything before (#) and everything after

                num = comment_split[0].strip()   # save everything before (#) to num variable

                self.ram[address] = int(num,2)   # convert binary to int, and save to memory
                # print(int(num,2))
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # break

            IR = self.ram_read(self.pc)    # Instruction Register
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            LDI = 130    # Load Instruction
            PRN = 71     # Print Instruction
            MUL = 162    # Multiply Instruction
            HLT = 1      # Halt
            
            if IR == HLT:
                running = False   # Stop the loop/end program
                self.pc += 1

            elif IR == LDI:
                self.reg[operand_a] = operand_b    # Save the value at given address
                self.pc += 3

            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif IR == PRN:
                value = self.reg[operand_a]
                print(value)   # Print from given address
                self.pc += 2


            else:
                # if command is not recognizable
                print(f"Unknown instruction {IR}")
                sys.exit(1)    # Terminate program with error
