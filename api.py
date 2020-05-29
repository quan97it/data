# -*- coding: utf-8 -*-
from flask import Flask, request
import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module
app = Flask(__name__)

#@app.route('/')
def process(input_string):
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    bigram_path = pkg_resources.resource_filename("symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
        print("Dictionary file not found")
        return
    if not sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2):
        print("Bigram dictionary file not found")
        return

    max_edit_distance_lookup = 2
    suggestion_verbosity = Verbosity.CLOSEST
    suggestions = sym_spell.lookup(input_string, suggestion_verbosity, max_edit_distance_lookup)
    return list(map(lambda sug: (sug.term, sug.distance, sug.count), suggestions))
   
import json

@app.route("/", methods=["GET"])
def query():
    input_string = request.args.get("input")
    print(input_string)
    output = process(input_string)
    return json.dumps(output)

if __name__ == "__main__":
    app.run("0.0.0.0", 6009)
