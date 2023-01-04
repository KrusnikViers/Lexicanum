from lookup.interface import LookupRequest
from lookup.wiktionary.engine import WiktionaryLookupEngine

engine = WiktionaryLookupEngine()
print(engine.lookup(LookupRequest.from_answer('Parrot')))
# print(engine.lookup(LookupRequest.from_answer('parrot')))
# print(engine.lookup(LookupRequest.from_answer('goul')))
# print(engine.lookup(LookupRequest.from_answer('god')))
# print(engine.lookup(LookupRequest.from_answer('live')))
