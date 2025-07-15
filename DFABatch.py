#!/usr/bin/python
import sys
import pandas as pd
from tabulate import tabulate
from Node import *
from Parser import *

def test_string_on_dfa(test_string, nodes, final_states, alphabet):
    """
    Test a single string against the DFA
    Returns True if accepted, False if rejected
    """
    # We always begin at state 0
    current_node = 0
    
    # Process each character in the string
    for letter in test_string:
        # Check if letter is in alphabet
        if letter not in alphabet:
            return False
        
        # Find transition for current state and letter
        transition_found = False
        for node in nodes:
            if node.mValue == current_node and node.mLetter == letter:
                current_node = node.mGoto
                transition_found = True
                break
        
        # If no transition found, reject
        if not transition_found:
            return False
    
    # Check if we end in a final state
    return current_node in final_states

def parse_dfa_file(filename):
    """
    Parse DFA definition file and return nodes, final states, and alphabet
    """
    try:
        file = open(filename)
    except:
        print(f"Error: Could not open file '{filename}'")
        return None, None, None
    
    # Parse file using existing Parser class
    file_parser = Parser(file)
    file_parser.parse()
    
    nodes = file_parser.getNodes()
    final_states = file_parser.getFinalStates()
    alphabet = file_parser.getAlphabet()
    
    return nodes, final_states, alphabet

def count_states(nodes):
    """
    Count the number of unique states in the DFA
    """
    states = set()
    for node in nodes:
        states.add(node.mValue)
        states.add(node.mGoto)
    return len(states)

def main(dfa_file, positive_test_file, negative_test_file):
    """
    Main function to run batch DFA testing
    """
    # Parse DFA definition
    nodes, final_states, alphabet = parse_dfa_file(dfa_file)
    if nodes is None:
        print("Failed to parse DFA file!")
        return
    
    # Count the number of states
    num_states = count_states(nodes)
    
    print("DFA loaded successfully.")
    print(f"Number of states: {num_states}")
    print(f"Final states: {final_states}")
    print(f"Alphabet: {alphabet}")
    
    # Process positive tests
    try:
        with open(positive_test_file, 'r') as pos_file:
            positive_tests = [line.rstrip('\n\r') for line in pos_file if line.strip()]
    except:
        print(f"Error: Could not open positive test file '{positive_test_file}'")
        return
    
    p_strings_for_show = {"String": [], "Is Accepted": []}
    for test in positive_tests:
        # Convert epsilon symbol to empty string for testing
        test_string = "" if test == "ε" else test
        is_accepted = test_string_on_dfa(test_string, nodes, final_states, alphabet)
        p_strings_for_show["String"].append(test)
        p_strings_for_show["Is Accepted"].append(is_accepted)
    
    p_strings_df = pd.DataFrame(p_strings_for_show)
    print(f"\nPositive Tests:\n{tabulate(p_strings_df, headers='keys', tablefmt='fancy_grid')}")
    
    # Process negative tests
    try:
        with open(negative_test_file, 'r') as neg_file:
            negative_tests = [line.rstrip('\n\r') for line in neg_file if line.strip()]
    except:
        print(f"Error: Could not open negative test file '{negative_test_file}'")
        return
    
    n_strings_for_show = {"String": [], "Is Rejected": []}
    for test in negative_tests:
        # Convert epsilon symbol to empty string for testing
        test_string = "" if test == "ε" else test
        is_accepted = test_string_on_dfa(test_string, nodes, final_states, alphabet)
        n_strings_for_show["String"].append(test)
        n_strings_for_show["Is Rejected"].append(not is_accepted)
    
    n_strings_df = pd.DataFrame(n_strings_for_show)
    print(f"\nNegative Tests:\n{tabulate(n_strings_df, headers='keys', tablefmt='fancy_grid')}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: DFABatch.py <dfa_file> <positive_test_file> <negative_test_file>")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
