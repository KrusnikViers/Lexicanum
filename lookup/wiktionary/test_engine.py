from lookup.wiktionary.interface import WiktionaryInterface

lookup_interface = WiktionaryInterface(None, None)
parrots = lookup_interface.lookup_by_answer('Parrot')
papageien = lookup_interface.lookup_by_answer('Papagei')

# print(engine.lookup(LookupRequest.from_answer('Parrot')))
# print(engine.lookup(LookupRequest.from_answer('goul')))
# print(engine.lookup(LookupRequest.from_answer('god')))
# print(engine.lookup(LookupRequest.from_answer('leave')))
# print(engine.lookup(LookupRequest.from_answer('fast')))

# print(engine.lookup(LookupRequest.from_answer('Parent')))
# print(engine.lookup(LookupRequest.from_question('Buch')))
# print(engine.lookup(LookupRequest.from_question('Milch')))
# print(engine.lookup(LookupRequest.from_question('Papagei')))
# print(engine.lookup(LookupRequest.from_question('Nachlappern')))
# print(engine.lookup(LookupRequest.from_question('Gott')))
# print(engine.lookup(LookupRequest.from_question('leben')))
