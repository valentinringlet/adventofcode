from shared.helper import (
    print_intro_message,
    is_user_input_valid_challenge_id,
    get_selected_challenge,
    print_wrong_input_message,
)

# 1. Ask user what challenge to run
print_intro_message()
user_input = input()

# 2. Continue asking until the user picks a valid challenge id
while not is_user_input_valid_challenge_id(user_input):
    print_wrong_input_message()
    user_input = input()
print()

# 3. Run that challenge
selected_challenge = get_selected_challenge(user_input)
selected_challenge.solve()
