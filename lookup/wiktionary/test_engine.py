from lookup.interface import LookupRequest
from lookup.wiktionary.engine import WiktionaryLookupEngine

engine = WiktionaryLookupEngine()
engine.lookup(LookupRequest.from_answer('Parrot'))
