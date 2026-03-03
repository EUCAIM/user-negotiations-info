from dataclasses import dataclass

# @dataclass
# class Negotiation:
#     id: str
#     creationDate: str
#     modifiedDate: str
#     resources: list = field(default_factory=list)
    
#     def set_resources(self, elements:list):
#         self.resources.extend(elements)

@dataclass
class Resource:
    id: str
    name: str
    sourceId: str
    negotiationId: str

@dataclass
class ErrorResponse():

    title: str
    status: int
    detail: str