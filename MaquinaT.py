class TuringMachine:
    def __init__(
        self,
        states,
        alphabet,
        tape_alphabet,
        transitions,
        start_state,
        accept_state,
        reject_state,
        blank_symbol,
    ):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.tape = []
        self.current_state = start_state
        self.head_position = 0

    def load_tape(self, input_string):
        self.tape = list(input_string) + [self.blank_symbol]
        self.current_state = self.start_state
        self.head_position = 0

    def step(self):
        symbol = self.tape[self.head_position]
        if (self.current_state, symbol) in self.transitions:
            new_state, new_symbol, direction = self.transitions[
                (self.current_state, symbol)
            ]
            self.tape[self.head_position] = new_symbol
            self.current_state = new_state
            self.head_position += 1 if direction == "R" else -1
            if self.head_position < 0:
                self.head_position = 0
            elif self.head_position >= len(self.tape):
                self.tape.append(self.blank_symbol)
        else:
            return False
        return True

    def run(self):
        configurations = []
        visited_confs = set()

        current_config = (self.current_state, "".join(self.tape), self.head_position)
        configurations.append(current_config)
        visited_confs.add(current_config)

        while (
            self.current_state != self.accept_state
            and self.current_state != self.reject_state
        ):
            if not self.step():
                break
            current_config = (
                self.current_state,
                "".join(self.tape),
                self.head_position,
            )
            configurations.append(current_config)

            if current_config in visited_confs:
                break

            visited_confs.add(current_config)

        configurations.append(
            (self.current_state, "".join(self.tape), self.head_position)
        )
        return configurations

    def save_configurations(self, filename, configurations):
        with open(filename, "w") as f:
            for config in configurations:
                f.write(
                    f"State: {config[0]}, Tape: {config[1]}, Head Position: {config[2]}\n"
                )
