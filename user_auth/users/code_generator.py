import random

class CodeGenerator:
    def create_code(self):
        return ''.join(str(random.randint(0, 9)) for _ in range(6))

# Instantiate the class
generator = CodeGenerator()
print(generator.create_code())
