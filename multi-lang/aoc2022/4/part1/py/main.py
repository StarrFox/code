from dataclasses import dataclass

@dataclass
class SectionRange:
    start: int
    end: int

    @classmethod
    def from_text(cls, text) -> "SectionRange":
        # I spent like 40 minutes trying to figure out that start and end where still strings
        start, end = map(int, text.split("-"))
        return cls(start, end)

    def within(self, other: "SectionRange") -> bool:
        if self == other:
            return True 

        return other.start <= self.start <= other.end and other.start <= self.end <= other.end
    
    def __eq__(self, other) -> bool:
        return self.start == other.start and self.end == other.end


with open("input") as input_:
    lines = input_.read().splitlines()

within_sum = 0

for line in lines:
    elf1, elf2 = map(SectionRange.from_text, line.split(","))

    if elf1.within(elf2) or elf2.within(elf1):
        within_sum += 1

print(within_sum)
