from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product, Category

@registry.register_document
class ProductDocument(Document):

    category = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    class Index:
        # Name of the Elasticsearch index
        name = 'products'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 2,
                    'number_of_replicas': 1}

    class Django:
        model = Product # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'description',
            'slug',
        ]

