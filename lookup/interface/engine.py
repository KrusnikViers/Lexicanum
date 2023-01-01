from core.util import StatusOr
from lookup.interface.request import LookupRequest
from lookup.interface.response import LookupResponse


class LookupEngine:
    def lookup(self, request: LookupRequest) -> StatusOr[LookupResponse]:
        raise NotImplementedError
