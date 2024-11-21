from dataclasses import dataclass, asdict, field, InitVar

@dataclass
class Negotiation:
    id: str
    creationDate: str
    modifiedDate: str
    resources: list = field(default_factory=list)
    
    def set_resources(self, elements:list):
        self.resources.extend(elements)

@dataclass
class Resource:
    id: str
    name: str
    sourceId: str

@dataclass
class ErrorResponse():

    title: str
    status: int
    detail: str