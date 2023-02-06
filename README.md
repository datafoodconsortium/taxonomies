# Data Food Consortium vocabularies

This repository contains the semantic vocabularies to be used with the [DFC ontology](https://github.com/datafoodconsortium/ontology):
   - facets: the certifications, natural origins, nutrition and health claims and territorial origins.
   - measures: the dimensions and units.
   - productTypes: the different kinds of product like vegetables, drink, bakery...

These vocabularies are using the SKOS format and are available as RDF and JSON-LD.

These vocabularies should not be edited directly but loaded, edited and exported from our [VocBench instance](https://vocbench.datafoodconsortium.org/vocbench3/).

To load these vocabularies into your application, you can use the DFC connector.

This is an example of the `Apple` product type in JSON-LD:
```
{
    "@id" : "http://static.datafoodconsortium.org/data/productTypes.rdf#apples",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" : [ {
      "@id" : "http://www.w3.org/2004/02/skos/core#Concept"
    } ],
    "http://www.w3.org/2004/02/skos/core#broader" : [ {
      "@id" : "http://static.datafoodconsortium.org/data/productTypes.rdf#fruit"
    } ],
    "http://www.w3.org/2004/02/skos/core#inScheme" : [ {
      "@id" : "http://static.datafoodconsortium.org/data/productTypes.rdf"
    } ],
    "http://www.w3.org/2004/02/skos/core#prefLabel" : [ {
      "@language" : "en",
      "@value" : "apples"
    }, {
      "@language" : "fr",
      "@value" : "pomme"
    } ]
}
```

## Contributing

These vocabularies should be edited with our VocBench instance, a dedicated web application that you can find at: https://vocbench.datafoodconsortium.org/vocbench3/.

On ce you have created your account, ask and administrator to confirm your account so he/she gives you the appropriate access.

When new modifications are made, the RDF and JSON-LD files must be exported from VocBench. Before pushing to this repository, be sure to update the `CHANGELOG.md` file. Depending on the nature of the changes, a new GitHub release might be created.