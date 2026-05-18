# Data Food Consortium taxonomies

This repository contains the semantic taxonomies to be used with the [DFC ontology](https://github.com/datafoodconsortium/ontology):
   - facets: the certifications, natural origins, nutrition and health claims and territorial origins.
   - measures: the dimensions and units.
   - productTypes: the different kinds of product like vegetables, drink, bakery...
   - vocabulary: specific vocabulary utilises within the DFC Standard, for example: Order Statuses

These taxonomies are using the SKOS format and are available as RDF and JSON-LD.

To load these taxonomies into your application, you can use the DFC connector. If you want to load them from the network, you could use the files contained in the Github releases (assets).

This is an example of the `Apples` product type in JSON-LD:
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

To request a change in these taxonomies please open an issue, or register on our [VOCbench instance](https://vocbench.dfc-standard.org/vocbench3/#/Home) and submit changes there.

We will discuss together about how we can integrate your needs as best as possible.

Then, a member of the DFC ontology team will edit the taxonomies files to reflect the changes and commit them to the repo. He/She __must also update the CHANGELOG.md file__ and __release a new version__. The Github release __must contain all the RDF and JSON files as assets__.

Thank you!

